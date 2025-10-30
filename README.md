

# Agentic Profile Extraction Pipeline

An advanced, self-contained web application that uses an agentic workflow to intelligently parse resumes and academic profiles. Built with a modern tech stack including LangGraph, Groq, and Streamlit, this tool extracts deep, structured information—including embedded hyperlinks—and stores it in a PostgreSQL database.

---

### Application Demo

Here is a quick overview of the application's user interface and workflow.

![Application Demo](assets/app-demo.png)

---

## ✨ Key Features

-   **Advanced Document Parsing**: Utilizes **PyMuPDF** to go beyond simple text extraction, accurately capturing embedded hyperlinks from PDFs for profiles like LinkedIn and GitHub. Also supports `.docx` and `.txt` formats.
-   **Comprehensive Data Extraction**: Employs LangChain with Pydantic schemas to reliably extract a rich, structured dataset from each resume:
    -   **Contact Info**: Name, Email, Phone, LinkedIn, GitHub, and Portfolio URLs.
    -   **Professional Summary**: A concise summary of the candidate's profile.
    -   **Skills**: A list of the top 5 most relevant skills.
    -   **Work Experience**: A detailed history of jobs, including titles, companies, dates, and responsibilities.
    -   **Education**: A complete list of degrees, institutions, and graduation dates.
-   **Agentic Workflow with LangGraph**: The entire process—from document validation and deep parsing to data extraction and duplicate checking—is managed by a robust LangGraph state machine.
-   **Rich Database Storage**: Stores profiles in a PostgreSQL database, using `JSONB` for flexible and queryable storage of work and education history.
-   **Interactive UI**: A clean, sidebar-navigated Streamlit interface allows users to upload documents, search profiles by email, and view all entries.

## ⚙️ Tech Stack

-   **Frontend**: [Streamlit](https://streamlit.io/)
-   **LLM Provider**: [Groq](https://groq.com/) (for high-speed Llama3 inference)
-   **Orchestration**: [LangGraph](https://langchain-ai.github.io/langgraph/)
-   **Core AI Framework**: [LangChain](https://www.langchain.com/)
-   **Document Parsing**: [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
-   **Database**: [PostgreSQL](https://www.postgresql.org/)
-   **Language & Packaging**: Python 3.9+, `uv`

---

## 🏗️ Architecture: The LangGraph Flow

The application's core is an agentic workflow that ensures a predictable, multi-step process for every document.

![LangGraph Flow Diagram](assets/langgraph-flow.png)

---

## 📂 Project Structure

The project is organized into a modular structure to separate concerns, making it easy to maintain and extend.

```plaintext
/agentic-profile-extraction-pipeline/
|-- .env
|-- requirements.txt
|-- app.py
|-- schemas.py
|
|-- services/
|   |-- database.py
|   |-- file_parser.py
|
|-- graph/
|   |-- chains.py
|   |-- graph.py
|   |-- nodes.py
|   |-- state.py
|
|-- ui_components/
|   |-- list_all.py
|   |-- search.py
|   |-- uploader.py
|
|-- assets/
|   |-- app-demo.gif
|   |-- langgraph-flow.png
```

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/agentic-profile-extraction-pipeline.git
cd agentic-profile-extraction-pipeline
```

### 2. Create Virtual Environment & Install Dependencies

This project uses `uv` for fast package management.

```bash
# Create and activate the virtual environment
uv init

source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


```

### 3. Set Up the PostgreSQL Database

Ensure you have a running PostgreSQL instance.

**A. Create the Database Table:**
Connect to your database and run the following SQL command. This schema is designed to hold all the newly extracted fields.

```sql
CREATE TABLE prism_table (
    id SERIAL PRIMARY KEY,
    email VARCHAR(50) UNIQUE,
    name VARCHAR(100),
    phone_number VARCHAR(50),
    linkedin_url VARCHAR(100),
    github_url VARCHAR(100),
    portfolio_url VARCHAR(100),
    summary TEXT,
    top_area_of_expertise JSONB,
    education JSONB,
    work_experience JSONB,
    phd_title TEXT,
    latest_projects_and_publications JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Configure Environment Variables

Create a file named `.env` in the project's root directory.

**⚠️ Important:** This file is the single source of truth for your API keys.

```plaintext
# .env file

# Get your free API key from https://console.groq.com/keys
GROQ_API_KEY="gsk_YourActualGroqApiKeyHere"

# Your PostgreSQL connection string
POSTGRES_CONNECTION_STRING="postgresql://your_user:your_password@your_host:your_port/your_database"
```

### 5. Run the Application

Once the setup is complete, run the Streamlit app:

```bash
uv run streamlit run app.py
```

The application will open in your default web browser.

---

## 💡 How to Use

1.  **Launch the App**: Run `streamlit run app.py`.
2.  **Ensure `.env` is Configured**: The app will display an error on startup if it cannot find the `GROQ_API_KEY`.
3.  **Navigate**: Use the sidebar to switch between the "Upload & Process," "Search Profiles," and "Show All Profiles" views.
4.  **Upload a Resume**: In the upload view, choose a `.pdf`, `.docx`, or `.txt` file. The status container will show the live progress, and the final extracted data will appear below.