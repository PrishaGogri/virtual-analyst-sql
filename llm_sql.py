from google import genai
import os
import json


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# ----------------------------
# Select tables
# ----------------------------
def select_tables_with_llm(tables, question):

    prompt = f"""
From the list below, select ONLY required tables.

Tables:
{tables}

Question:
{question}

Output JSON:
{{ "tables": ["table1"] }}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",   # ✅ works in new API
        contents=prompt
    )

    try:
        result = json.loads(response.text.strip())
        selected = result.get("tables", [])
        return [t for t in selected if t in tables] or tables
    except:
        return tables


# ----------------------------
# Generate SQL
# ----------------------------
def generate_sql(question, schema):

    tables = list(schema.keys())
    selected = select_tables_with_llm(tables, question)

    schema_prompt = ""

    for t in selected:
        schema_prompt += f"\nTable: {t}\n"
        for col in schema[t]:
            schema_prompt += f"  - {col}"

    final_prompt = f"""
You are an expert MySQL SQL generator.

Use ONLY these tables:
{schema_prompt}

Return ONLY SQL.
No explanation.

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=final_prompt
    )

    sql = response.text.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql
