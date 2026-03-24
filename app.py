import streamlit as st

from backend.mysql_engine import (
    connect_server,
    get_databases,
    connect_database,
    run_sql,
    get_schema
)

from backend.llm_sql import generate_sql
from backend.sql_optimizer import optimize_sql


st.title("🧠 Virtual Analyst — MySQL + English → SQL")


# =========================
# Connect server
# =========================

host = st.text_input("Host", "localhost")
user = st.text_input("User")
password = st.text_input("Password", type="password")

if st.button("Connect Server"):
    server = connect_server(host, user, password)
    st.session_state.server = server
    st.session_state.databases = get_databases(server)
    st.success("Connected")


# =========================
# Choose DB
# =========================

if "databases" in st.session_state:

    db_name = st.selectbox("Choose DB", st.session_state.databases)

    if st.button("Load Database"):
        engine = connect_database(host, user, password, db_name)
        st.session_state.engine = engine
        st.success(f"Connected to {db_name}")


# =========================
# Ask questions
# =========================

if "engine" in st.session_state:

    engine = st.session_state.engine
    schema = get_schema(engine)

    st.subheader("Schema")
    st.json(schema)

    question = st.text_area("Ask question in English")

    if st.button("Run Query"):

        sql = generate_sql(question, schema)
        sql = optimize_sql(sql)

        st.subheader("Generated SQL")
        st.code(sql)

        df = run_sql(engine, sql)

        st.dataframe(df)