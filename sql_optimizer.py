def clean_markdown(sql):
    return (
        sql.replace("```sql", "")
           .replace("```", "")
           .strip()
    )


def optimize_sql(sql):
    sql = clean_markdown(sql)

    # future improvements:
    # remove unused joins
    # reorder clauses
    # validate syntax

    return sql