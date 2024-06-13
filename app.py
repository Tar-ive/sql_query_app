import streamlit as st
import sqlite3
import mysql.connector
import pandas as pd
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os
import random

def upload_sqlite():
    st.header("Upload and Query SQLite Database")

    uploaded_file = st.file_uploader("Choose a SQL database file", type="db")
    
    if uploaded_file is not None:
        with open("uploaded_sqlite.db", "wb") as f:
            f.write(uploaded_file.getbuffer())

        conn = sqlite3.connect("uploaded_sqlite.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        table_name = st.selectbox("Select a table", [table[0] for table in tables])

        query = f"SELECT * FROM {table_name} LIMIT 10"
        df = pd.read_sql_query(query, conn)

        st.write("Top 10 rows of the table:")
        st.dataframe(df)

        conn.close()

        db = SQLDatabase.from_uri("sqlite:///uploaded_sqlite.db")
        llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
        write_query = create_sql_query_chain(llm, db)
        execute_query = QuerySQLDataBaseTool(db=db)
        chain = write_query | execute_query

        answer_prompt = PromptTemplate.from_template(
            """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

            Question: {question}
            SQL Query: {query}
            SQL Result: {result}
            Answer: """
        )

        answer = answer_prompt | llm | StrOutputParser()
        final_chain = (
            RunnablePassthrough.assign(query=write_query).assign(
                result=itemgetter("query") | execute_query
            )
            | answer
        )

        question = st.text_input("Enter your question about the data:")
        if question:
            response = final_chain.invoke({"question": question})
            st.write("Response from the model:")
            st.write(response)

def aws_rds():
    st.header("Connect and Query AWS RDS MySQL Database")

    rds_endpoint = st.text_input("Endpoint:")
    db_user = st.text_input("User:")
    db_password = st.text_input("Password:", type="password")
    db_name = st.text_input("Database Name:")

    if rds_endpoint and db_user and db_password and db_name:
        conn = mysql.connector.connect(
            host=rds_endpoint,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = conn.cursor()

        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        if tables:
            table_name = st.selectbox("Select a table", [table[0] for table in tables])

            query = f"SELECT * FROM {table_name} LIMIT 10"
            df = pd.read_sql_query(query, conn)

            st.write("Top 10 rows of the table:")
            st.dataframe(df)

            cursor.close()
            conn.close()

            db_uri = f"mysql+mysqlconnector://{db_user}:{db_password}@{rds_endpoint}/{db_name}"
            db = SQLDatabase.from_uri(db_uri)
            llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
            write_query = create_sql_query_chain(llm, db)
            execute_query = QuerySQLDataBaseTool(db=db)
            chain = write_query | execute_query

            answer_prompt = PromptTemplate.from_template(
                """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

                Question: {question}
                SQL Query: {query}
                SQL Result: {result}
                Answer: """
            )

            answer = answer_prompt | llm | StrOutputParser()
            final_chain = (
                RunnablePassthrough.assign(query=write_query).assign(
                    result=itemgetter("query") | execute_query
                )
                | answer
            )

            question = st.text_input("Enter your question about the data:")
            if question:
                response = final_chain.invoke({"question": question})
                st.write("Answer:")
                st.write(response)
        else:
            st.write("No tables found in the database.")

def data_encryption_page():
    st.header("Data Handling and Protection")

    st.write("""
    ### Steps Taken to Encrypt and Protect Data

    1. **Environment Variable for API Key**
        - The OpenAI API key is stored as an environment variable using `os.environ["OPENAI_API_KEY"] = openai_api_key`.
        - This method keeps the API key secure by not hardcoding it into the script.

    2. **Secure Inputs**
        - Sensitive inputs, such as the AWS RDS credentials and the OpenAI API key, are taken using `st.text_input` with `type="password"`.
        - This ensures that the input is masked and not displayed openly on the screen.

    3. **Database Connection**
        - Connections to the SQLite and AWS RDS databases are established securely:
          - SQLite: Connection is established locally with the uploaded file.
          - AWS RDS: The connection is made using credentials provided by the user, ensuring the connection string is not hardcoded.

    4. **Secure Query Execution**
        - SQL queries are generated and executed using the LangChain library, which abstracts the query generation process.
        - This minimizes the risk of SQL injection attacks by preventing direct user input in the query strings.

    ### Additional Security Measures

    - **Use HTTPS:** Ensuring the Streamlit app is served over HTTPS to encrypt data transmitted between the client and server.
    - **Regular Security Audits:** Regularly auditing our code and dependencies for security vulnerabilities.
    - **Environment Management:** Using virtual environments to manage dependencies and isolate the application environment.

    
    """)

def show_random_mysql_fact():
    mysql_facts = [
        "MySQL was created by a Swedish company, MySQL AB, founded by David Axmark, Allan Larsson, and Michael 'Monty' Widenius.",
        "MySQL was named after co-founder Michael Widenius's daughter, My, while 'SQL' stands for Structured Query Language.",
        "MySQL is used by many large-scale websites and applications, including Facebook, Twitter, YouTube, and Google.",
        "Oracle Corporation acquired MySQL AB in 2010 as part of its acquisition of Sun Microsystems.",
        "MySQL supports a wide range of operating systems, including Windows, Linux, macOS, and various Unix variants."
    ]
    fact = random.choice(mysql_facts)
    st.sidebar.info(f"💡 MySQL Fact: {fact}")

def main():
    st.set_page_config(page_title="SQL Query Application 🚀", page_icon=":bar_chart:", layout="wide")
    st.title("Interactive SQL Query Application 🚀")

    show_random_mysql_fact()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a page:", ["Upload SQL", "SQL Query with AWS RDS", "Data Handling and Protection"])

    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key

    if page == "Upload SQL":
        upload_sqlite()
    elif page == "SQL Query with AWS RDS":
        aws_rds()
    elif page == "Data Handling and Protection":
        data_encryption_page()

if __name__ == "__main__":
    main()
