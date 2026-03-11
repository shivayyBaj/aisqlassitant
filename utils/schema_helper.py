def get_schema(df):
    
    schema = []

    for col in df.columns:
        schema.append(col)

    return ", ".join(schema)