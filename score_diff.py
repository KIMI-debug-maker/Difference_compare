import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import json


@st.cache_data
def fetch_data():
    # read scores
    with open("all_scores.json", "r") as file:
        da = json.load(file)
    a = np.array(da['a'])
    b = np.array(da['b'])
    c = np.array(da['c'])
    st.title("Overview")
    fig = go.Figure()
    fig.add_trace(go.Box(y=a, name="Times Count vs Cosine Similarity"))
    fig.add_trace(go.Box(y=b, name="Times Count vs TFIDF"))
    fig.add_trace(go.Box(y=c, name="Cosine Similarity vs TFIDF"))
    fig.update_layout(title="Comparison of Method Differences",
                      yaxis_title="Difference in Scores",
                      boxmode='group')
    st.plotly_chart(fig, use_container_width=True)
    # read dataframe
    res = {"simtf_bot": pd.read_csv('simtf_bot_diff.csv'),
           "simtf_top": pd.read_csv('simtf_top_diff.csv'),
           "tsim_bot": pd.read_csv('timesim_bot_diff.csv'),
           "tsim_top": pd.read_csv('timesim_top_diff.csv'),
           "ttf_bot": pd.read_csv('timetf_bot_diff.csv'),
           "ttf_top": pd.read_csv('timetf_top_diff.csv')}
    return res


with st.sidebar:
    option = st.selectbox(
        'Select the comparison of method',
        ('Times Count vs Cosine Similarity', 'Times Count vs TFIDF', 'Cosine Similarity vs TFIDF'))

data = fetch_data()
st.subheader("Most different result")
st.write("Toggle Top100 or lowest 100:")
if option == "Times Count vs Cosine Similarity":
    key = "tsim_"
    key1 = "Times"
    key2 = "Sim"
elif option == "Times Count vs TFIDF":
    key = "ttf_"
    key1 = "Times"
    key2 = "TFIDF"
else:
    key = "simtf_"
    key1 = "Sim"
    key2 = "TFIDF"
Top = st.checkbox('Top100')
if Top:
    key += "top"
else:
    key += "bot"

df = data[key]
values = st.number_input("Please choose any JD you are interested:", min_value=0, max_value=99, step=1)

col1, col2, col3 = st.columns(3)
col1.metric(label="**" + key1 + "**", value=round(df.loc[values, key1], 1))
col2.metric(label="**" + key2 + "**", value=round(df.loc[values, key2], 1))
col3.metric(label="**Difference**", value=round(df.loc[values, "difference"], 1))
st.write(df.loc[values, "JobText"])
