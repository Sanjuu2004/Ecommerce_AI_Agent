# utils/visualizer.py
import plotly.express as px
import pandas as pd

def generate_chart(df: pd.DataFrame):
    if "date" in df.columns and "total_sales" in df.columns:
        fig = px.line(df, x="date", y="total_sales", title="Sales Over Time")
    elif "item_id" in df.columns and "total_units_ordered" in df.columns:
        fig = px.bar(df, x="item_id", y="total_units_ordered", title="Units Ordered by Item")
    else:
        fig = None
    return fig
