

#  AI-Powered Resume Parser with LangGraph & Groq

This AI tool is a powerful, self-contained web application built with Streamlit that leverages the speed of Groq and the robustness of LangGraph to parse resumes, extract structured information, and store it in a database. The application provides a clean, interactive UI for uploading documents, searching for profiles, and viewing all entries.

---

### Application Demo

Here is a quick overview of the application's user interface and workflow.

![Prism AI Application Demo](assets/app-demo.png)


---

## ✨ Key Features

-   **Multi-Format File Upload**: Accepts resumes in `.pdf`, `.docx`, and `.txt` formats.
-   **Intelligent Document Validation**: An initial LLM call verifies if the uploaded document is actually a resume before proceeding.
-   **Structured Data Extraction**: Uses LangChain with structured output (Pydantic) to reliably extract key information:
    -   Full Name
    -   Email Address
    -   Professional Summary
    -   Top Skills
    -   PhD Title & University
    -   Recent Projects & Publications
-   **Database Integration**: Automatically checks for duplicate profiles based on email and stores new, unique profiles in a PostgreSQL database.
-   **Interactive UI**: A clean, sidebar-navigated Streamlit interface allows users to:
    -   Upload and process new resumes.
    -   Search for existing profiles by email.
    -   View a complete list of all stored profiles.
-   **Agentic Workflow with LangGraph**: The entire processing pipeline is managed by a LangGraph state machine, providing a clear, modular, and robust workflow.

## ⚙️ Tech Stack

-   **Frontend**: [Streamlit](https_streamlit.io/)
-   **LLM Provider**: [Groq](https://groq.com/) (for high-speed inference)
-   **Backend Orchestration**: [LangGraph](https://langchain-ai.github.io/langgraph/)
-   **Core AI Framework**: [LangChain](https://www.langchain.com/)
-   **Database**: [PostgreSQL](https://www.postgresql.org/)
-   **Language**: Python 3.9+

---

## 🏗️ Architecture: The LangGraph Flow

The core of the application is an agentic workflow defined by a state graph. This graph ensures a predictable and logical flow for every document that is processed.

![LangGraph Flow Diagram](assets/langgraph-flow.png)

---

## 📂 Project Structure

The project is organized into a modular structure to separate concerns, making it easy to maintain and extend.

```plaintext
/prism-ai-parser/
|-- .env
|-- requirements.txt
|-- app.py                 # Main Streamlit application file
|-- schemas.py             # Pydantic models for structured data
|
|-- services/
|   |-- database.py        # Database interaction functions
|   |-- file_parser.py     # Utility for parsing files
|
|-- graph/
|   |-- chains.py          # LLM chain definitions and initialization
|   |-- graph.py           # LangGraph workflow definition and compilation
|   |-- nodes.py           # Functions for each node in the graph
|   |-- state.py           # GraphState definition
|
|-- ui_components/
|   |-- list_all.py        # Streamlit component for listing profiles
|   |-- search.py          # Streamlit component for searching
|   |-- uploader.py        # Streamlit component for file uploading
|
|-- assets/                # (Create this folder for your images)
|   |-- app-demo.gif
|   |-- langgraph-flow.png```

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Clone the Repository



### 2. Create a Virtual Environment and Install Dependencies

It is highly recommended to use a virtual environment.

```bash
uv init
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
uv add -r requirements.txt
```

### 3. Set Up the PostgreSQL Database

Ensure you have a running PostgreSQL instance.

**A. Create the Database Table:**
Connect to your database and run the following SQL command to create the necessary table:

```sql
CREATE TABLE prism_table (
    id SERIAL PRIMARY KEY,
    email VARCHAR(60) UNIQUE,
    name VARCHAR(60),
    summary TEXT,
    top_area_of_expertise JSONB,
    phd_title TEXT,
    phd_from_college TEXT,
    latest_projects_and_publications JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Configure Environment Variables

Create a file named `.env` in the root of the project directory and add your credentials.

**⚠️ Important:** This file is the single source of truth for your API keys.

```plaintext
# .env file

# Get your free API key from https://console.groq.com/keys
GROQ_API_KEY="gsk_YourActualGroqApiKeyHere"

# Your PostgreSQL connection string
POSTGRES_CONNECTION_STRING="postgresql://your_user:your_password@your_host:your_port/your_database"```

### 5. Run the Application

Once the setup is complete, you can run the Streamlit application with a single command:

```bash
uv run streamlit run app.py
```

The application will open in your default web browser.

---

## 💡 How to Use

1.  **Launch the app**: Run the `streamlit run app.py` command.
2.  **Ensure `.env` is configured**: The app will show an error if it cannot find the `GROQ_API_KEY`.
3.  **Navigate**: Use the sidebar to switch between the "Upload & Process," "Search Profiles," and "Show All Profiles" views.
4.  **Upload**: In the upload view, choose a `.pdf`, `.docx`, or `.txt` file and watch the progress in the status container. The extracted data will appear below.