import streamlit as st
from nl_to_sql import nl_to_sql
from db import run_query

st.title("MedQuery - NL to SQL with Mistral and MySQL Execution")

nl_query = st.text_input(
    "Enter your natural language query:",
    placeholder="e.g., show me all patients with brown eyes"
)

if st.button("Generate and Execute"):
    if not nl_query.strip():
        st.warning("Please enter a query!")
    else:
        try:
            # Generate SQL from NL query
            result = nl_to_sql(nl_query)

            # If unsafe or blocked query
            if result["errors"]:
                st.error(f"Invalid query: {result['errors'][0]}")
            else:
                sql_query = result["sql"]
                st.success("SQL Query Generated Successfully:")
                st.code(sql_query)

                # Execute SQL query on MySQL
                df = run_query(sql_query)

                if isinstance(df, str):  # Error returned from DB
                    st.error(f"MySQL Error: {df}")
                elif df.empty:  # No results
                    st.info("No results found.")
                else:  # Show results
                    st.dataframe(df)

        except Exception as e:
            st.error(f"NL→SQL processing error: {e}")
