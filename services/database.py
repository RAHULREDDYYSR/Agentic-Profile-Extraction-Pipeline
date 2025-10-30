# services/database.py
import os
import json
import psycopg2
from psycopg2 import sql
from langchain.tools import tool

def create_db_connection():
    """Creates a connection to the PostgreSQL database."""
    try:
        return psycopg2.connect(os.getenv('POSTGRES_CONNECTION_STRING'))
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

@tool
def check_if_profile_exists(email: str) -> dict:
    """Checks if a profile with the given email already exists in the database."""
    if not email: return {"exists": False, "profile": None}
    conn = create_db_connection()
    if not conn: return {"exists": False, "profile": None}
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM prism_table WHERE email = %s", (email,))
            result = cur.fetchone()
            if result:
                profile = dict(zip([desc[0] for desc in cur.description], result))
                return {"exists": True, "profile": profile}
            return {"exists": False, "profile": None}
    finally:
        if conn: conn.close()

def insert_profile(profile_data: dict):
    """Inserts a new profile into the database."""
    conn = create_db_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            query = sql.SQL("""
                INSERT INTO prism_table (email, name, summary, top_area_of_expertise, phd_title, phd_from_college, latest_projects_and_publications)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """)
            cur.execute(query, (
                profile_data.get('email'), profile_data.get('name'), profile_data.get('summary'),
                json.dumps(profile_data.get('top_skills') or []), profile_data.get('phd_title'),
                profile_data.get('phd_from_college'), json.dumps(profile_data.get('latest_three_projects_and_publications') or [])
            ))
            conn.commit()
    finally:
        if conn: conn.close()

def get_all_professors():
    """Retrieves all professors from the database."""
    conn = create_db_connection()
    if not conn: return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT name, email FROM prism_table")
            return [{"name": row[0], "email": row[1]} for row in cur.fetchall()]
    finally:
        if conn: conn.close()