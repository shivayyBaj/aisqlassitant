

import plotly.express as px

def generate_chart(df):

    x = df.columns[0]
    y = df.columns[1]

    fig = px.bar(
        df,
        x=x,
        y=y,
        title=f"{y} by {x}"
    )

    return fig