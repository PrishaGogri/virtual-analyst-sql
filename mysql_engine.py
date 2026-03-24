from sqlalchemy import create_engine
import pandas as pd


# -------------------------
# Connect to MySQL server only
# -------------------------
def connect_server(host, user, password):
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}")
    return engine


# -------------------------
# Get all databases
# -------------------------
def get_databases(engine):
    df = pd.read_sql("SHOW DATABASES", engine)
    return df.iloc[:, 0].tolist()


# -------------------------
# Connect to specific database
# -------------------------
def connect_database(host, user, password, database):
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}"
    )
    return engine


# -------------------------
# Run SQL
# -------------------------
def run_sql(engine, sql):
    return pd.read_sql(sql, engine)


# -------------------------
# Get schema
# -------------------------
def get_schema(engine):
    schema = {}

    tables = pd.read_sql("SHOW TABLES", engine)

    for table in tables.iloc[:, 0]:
        cols = pd.read_sql(f"DESCRIBE {table}", engine)
        schema[table] = cols["Field"].tolist()

    return schema