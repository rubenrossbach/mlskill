import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Machine Learning Skill Test",
    page_icon="chart_with_upwards_trend",
    layout="centered")

@st.cache
def get_data():
    return pd.read_csv("data/results.csv")

df = get_data()

st.write("# Machine Learning Skill Test")

# index session state
if "index" not in st.session_state:
    st.session_state.index = 0

# Controls
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.write("")
    st.write("")
    if st.button("Back"):
            st.session_state.index -= 1
with col2:
    st.session_state.index = st.selectbox('Jump to question', df.index +1) - 1
with col4:
    st.write("")
    st.write("")
    if st.button("Continue"):
            st.session_state.index += 1

# Display first question and answers
st.write(df.iloc[st.session_state.index, 0])

ans = df.iloc[st.session_state.index, 1:5]
choice = st.radio("Choose one", ans, index=0)
correct_choice = df.iloc[st.session_state.index, 5]

sel = 0
if choice == ans[0]:
    sel = 1
elif choice == ans[1]:
    sel = 2
elif choice == ans[2]:
    sel = 3
elif choice == ans[3]:
    sel = 4

col1, col2, col3 = st.columns(3)
with col2:
    if st.button("Check"):
        if sel == correct_choice:
            st.write("Correct!")
        else:
            st.write("wrong")


# Made by Ruben Rossbach, GH LI
