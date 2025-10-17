from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import re
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
# THIS IS THE KEY IMPORT
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from sqlalchemy import create_engine

# --- Page Configuration ---
st.set_page_config(page_title="BankPulse Chatbot", layout="centered")
st.title("🏦 BankPulse Data Detective")
st.write("Ask a question about your Snowflake data in plain English.")

# --- Snowflake Connection ---
db = None
try:
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    database = os.getenv("SNOWFLAKE_DATABASE")
    schema = os.getenv("SNOWFLAKE_SCHEMA")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")

    snowflake_url = f"snowflake://{account}/{database}/{schema}?warehouse={warehouse}"
    engine = create_engine(snowflake_url, connect_args={'user': user, 'password': password})

    db = SQLDatabase(engine=engine)
    st.success("✅ Connected to Snowflake successfully!")

except Exception as e:
    st.error("❌ Could not connect to Snowflake. Please double-check your environment variables.")
    st.error(f"   Error details: {e}")
    st.stop()

# --- Functions to Clean and Correct the SQL ---
def clean_sql_query(query_string: str) -> str:
    """Removes markdown formatting from the AI's SQL output."""
    cleaned_query = query_string.replace("```sql", "").replace("```", "")
    return cleaned_query.strip().rstrip(';')

def force_uppercase_sql(query_string: str) -> str:
    """Programmatically forces all quoted identifiers to be uppercase."""
    return re.sub(r'"(.*?)"', lambda m: f'"{m.group(1).upper()}"', query_string)

# --- LangChain Setup ---
llm = ChatGoogleGenerativeAI(model="models/gemini-pro-latest", temperature=0, convert_system_message_to_human=True)

template = """
Based on the table schema below, write a SQL query that would answer the user's question.
Schema: {schema}
Question: {question}
SQL Query:
"""
prompt = ChatPromptTemplate.from_template(template)

# This chain generates, cleans, and corrects the SQL query.
# THIS IS THE DEFINITIVE FIX: We wrap our custom functions in RunnableLambda.
sql_generation_chain = (
    RunnablePassthrough.assign(schema=lambda _: db.get_table_info())
    | prompt
    | llm
    | StrOutputParser()
    | RunnableLambda(clean_sql_query)
    | RunnableLambda(force_uppercase_sql)
)

# This chain takes a SQL query and runs it to get the final result.
sql_execution_chain = RunnableLambda(db.run)


# --- User Interface ---
question = st.text_input("Your Question:", placeholder="e.g., What is the average loan amount for grade A?")

if question:
    with st.spinner("Thinking..."):
        try:
            # Step 1: Generate and correct the SQL. This will now work.
            generated_sql = sql_generation_chain.invoke({"question": question})

            # Step 2: Display the SQL.
            with st.expander("🔍 View Executed SQL"):
                st.code(generated_sql, language="sql", line_numbers=True)

            # Step 3: Run the SQL to get the answer.
            response = sql_execution_chain.invoke(generated_sql)

            # Step 4: Display the result.
            st.subheader("Answer:")
            st.write(response)

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.warning("The AI might generate invalid SQL. Try rephrasing your question more simply.")
