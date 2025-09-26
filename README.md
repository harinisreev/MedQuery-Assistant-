MedQuery Assistant

Author: Harinisree Venkatesan 

Overview:

Interactive Python & Streamlit app to query patient health data stored in a MySQL database using natural language.

Features:

Store & manage patient records in MySQL (medquery).
Streamlit UI for dynamic query execution.
Supports age, gender, diseases, allergies, blood type, hair/eye color, nationality.
Handles complex age expressions and allergy conditions.

Tech Stack:
Python, MySQL, Streamlit, Pandas, Regex

Usage:
Set up MySQL database & import dataset.
Connect Python using mysql-connector and environment variables.
Run Streamlit app (streamlit run app.py).
Enter natural language queries and view results.

Project Structure
MedQuery Assistant/
├── app.py 
├── dc.py/  
├── nl_to_sql.py/  
├── requirements.txt/  
└── README.md

Conclusion

Enables intuitive, SQL-free exploration of patient data with accurate and flexible query handling.
