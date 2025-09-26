import os
import requests
from dotenv import load_dotenv

# Load MISTRAL_API_KEY from .env
load_dotenv()
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY not found in environment variables.")

# Columns in the patients table
PATIENTS_COLUMNS = [
    "Patient_ID", "First_Name", "Last_Name", "Age", "Gender", "Hair_Color", "Eye_Color",
    "Height_cm", "Weight_kg", "Nationality", "Blood_Type", "Primary_Disease",
    "Secondary_Condition", "Allergies", "Emergency_Contact", "Phone_Number", "Email"  
]

def nl_to_sql(nl_query: str) -> dict:
    """
    Convert natural language to SQL SELECT query using Mistral API.
    Handles multiple conditions, ranges, diseases, no-allergies, and blocks unsafe queries.
    """
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    columns_str = ", ".join(PATIENTS_COLUMNS)
    prompt_content = f"""
You are an expert SQL generator. ONLY output a single SQL SELECT query.
Do not output explanations or comments. Use only the column names in the 'patients' table listed below:

{columns_str}

Instructions:
1. If the query mentions a disease or medical condition, check both Primary_Disease and Secondary_Condition columns using OR.
2. If the query mentions "no allergies" or patients without allergies, generate SQL that catches:
   - NULL values
   - Empty strings
   - Common placeholders like 'None' or 'N/A'
3. If the query mentions multiple conditions (e.g., age range, height, weight, hair color, eye color, diseases, allergies), combine them correctly using AND/OR in SQL so all conditions are applied.
4. If the query mentions ranges (e.g., age 30-40, height 150-180), generate proper BETWEEN statements.
5. Ensure the query works directly in MySQL.
6. Only output SELECT queries.
7. Block any unsafe queries like DELETE, DROP, UPDATE, INSERT, CREATE, ALTER, TRUNCATE, REPLACE.

Convert the following natural language request into a SQL SELECT query:

"{nl_query}"
"""

    payload = {
        "model": "codestral-latest",
        "messages": [
            {"role": "system", "content": "You are an expert SQL generator. ONLY respond with SQL SELECT queries."},
            {"role": "user", "content": prompt_content}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        sql_text = data["choices"][0]["message"]["content"].strip()

        # Block unsafe queries
        blocked_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE", "REPLACE"]
        if not sql_text.upper().startswith("SELECT") or any(k in sql_text.upper() for k in blocked_keywords):
            return {
                "sql": "",
                "errors": ["Blocked: Non-SELECT or unsafe query"],
                "warnings": [],
                "has_conditions": False
            }

        return {
            "sql": sql_text,
            "errors": [],
            "warnings": [],
            "has_conditions": "where" in sql_text.lower()
        }

    except Exception as e:
        return {
            "sql": "",
            "errors": [str(e)],
            "warnings": [],
            "has_conditions": False
        }
