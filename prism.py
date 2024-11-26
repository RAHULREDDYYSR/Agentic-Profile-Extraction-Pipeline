import PyPDF2
import nltk
import google.generativeai as genai  
import streamlit as st
from io import BytesIO
import json
import psycopg2
from psycopg2 import sql
import re
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(layout="wide", page_title="Document Summarizer & Expertise Extractor")

# API Key Configuration for Generative AI
key = os.getenv('api_key')
genai.configure(api_key=key) 

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

# # Download required NLTK packages
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')


def create_db_connection():
    """Creates a connection to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(os.getenv('POSTGRES_CONNECTION_STRING'))
        return connection
    except psycopg2.Error as e:
        st.error(f"Error connecting to PostgreSQL Database: {e}")
        return None


def parse_pdf(pdf_file):
    """Parses the text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def preprocess_text(text):
    """Preprocesses the text by tokenizing, removing stopwords, and joining."""
    tokens = nltk.word_tokenize(text.lower())
    stop_words = set(nltk.corpus.stopwords.words('english'))
    filtered_words = [w for w in tokens if w not in stop_words]
    return " ".join(filtered_words)


def extract_json_from_markdown(text):
    """Extracts JSON data from the LLM response."""
    json_match = re.search(r'`json\n(.*?)\n`', text, re.DOTALL)
    return json_match.group(1) if json_match else text


def llm_process(text):
    """Processes the text using the LLM and returns the JSON response."""
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", generation_config=generation_config
    )
    chat_session = model.start_chat(history=[])
    prompt = (
        f"Analyze this text: {text}\n"
        f"Provide the following information in JSON format:\n"
        f"1. 'name': The full name of the person\n"
        f"2. 'email': The email address of the person\n"
        f"3. 'summary': A 3-sentence summary of the person's profile\n"
        f"4. 'top_skills': An array of the top 3 fields of expertise based on the profile\n"
        f"5. 'phd_title': phd name (null if not available)\n"
        f"6. 'phd_from_college': The name of the college/university where they pursued their PhD (null if not available)\n"
        f"7. 'latest_three_projects_and_publications': An array of the latest 3 projects and publications (null if not available)\n"
        f"Ensure that the JSON keys are exactly as specified: 'name', 'email', 'summary', 'top_skills', "
        f"'phd_title', 'phd_from_college', and 'latest_three_projects_and_publications'."
    )
    response = chat_session.send_message(prompt)
    return response.text.strip()


def insert_profile(connection, profile_data):
    """Inserts profile data into the database."""
    try:
        cursor = connection.cursor()
        query = sql.SQL("""
        INSERT INTO prism_table (
            email, name, summary, top_area_of_expertise, phd_title, phd_from_college, latest_projects_and_publications
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """)
        cursor.execute(query, (
            profile_data.get('email', ''),
            profile_data.get('name', ''),
            profile_data.get('summary', ''),
            json.dumps(profile_data.get('top_skills') or []),
            profile_data.get('phd_title', None),
            profile_data.get('phd_from_college', None),
            json.dumps(profile_data.get('latest_three_projects_and_publications') or [])
        ))
        connection.commit()
        st.success("Profile data inserted successfully!")
    except psycopg2.Error as e:
        st.error(f"Error inserting data into PostgreSQL Database: {e}")
    finally:
        if cursor:
            cursor.close()


def get_existing_profile(connection, email):
    """Retrieves an existing profile by email address."""
    try:
        cursor = connection.cursor()
        query = sql.SQL("""
            SELECT * FROM prism_table WHERE email = %s
        """)
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result:
            return dict(zip([desc[0] for desc in cursor.description], result))
        else:
            return None
    except psycopg2.Error as e:
        st.error(f"Error retrieving existing profile: {e}")
        return None


# **Header Section**
st.title("AI/MI | Professor Profile based Area of Expertise Analysis")
st.markdown("""
This tool allows you to extract and summarize information from documents, 
store the data in a database, and search for existing profiles by email or name.
""")

# **Main Layout: Two Columns**
upload_col, search_col = st.columns(2)

# **PDF Upload and Processing Section**
with upload_col:
    st.header("Upload Document for Analysis")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file:
        st.info("Processing the Document. Please wait...")
        with st.spinner("Extracting and summarizing data..."):
            connection = create_db_connection()
            if not connection:
                st.error("Unable to establish database connection.")
            else:
                text = preprocess_text(parse_pdf(uploaded_file))
                response = llm_process(text)
                json_content = extract_json_from_markdown(response)

                try:
                    profile_data = json.loads(json_content)
                    existing_profile = get_existing_profile(connection, profile_data['email'])

                    if existing_profile:
                        st.warning("Profile already exists in the database.")
                        st.json(existing_profile)
                    else:
                        insert_profile(connection, profile_data)
                        st.success("New profile inserted into the database!")
                        st.json(profile_data)

                    connection.close()
                except json.JSONDecodeError as e:
                    st.error(f"Error parsing JSON response: {e}")
                    st.code(json_content, language='json')

# **Search Section**
with search_col:
    st.header("Search Profiles")
    search_type = st.selectbox("Search By", options=["email", "name"], index=0)
    search_input = st.text_input(f"Enter {search_type.capitalize()}")

    if st.button("Search"):
        if search_input.strip():
            connection = create_db_connection()
            if connection:
                if search_type == "email":
                    profile = get_existing_profile(connection, search_input)
                elif search_type == "name":
                    profile = None
                    try:
                        cursor = connection.cursor()
                        query = sql.SQL("""
                            SELECT * FROM prism_table WHERE name ILIKE %s
                        """)
                        cursor.execute(query, (f"%{search_input}%",))
                        result = cursor.fetchone()
                        if result:
                            profile = dict(zip([desc[0] for desc in cursor.description], result))
                    except psycopg2.Error as e:
                        st.error(f"Error retrieving profile: {e}")

                if profile:
                    st.success("Profile found!")
                    st.json(profile)
                else:
                    st.warning(f"No profile found with {search_type}: {search_input}")
                connection.close()
        else:
            st.error("Please enter a valid search input.")

# **Footer Section**
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, and Generative AI.")
