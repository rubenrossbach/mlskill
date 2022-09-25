import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Machine Learning Skill Test",
    page_icon="chart_with_upwards_trend",
    layout="centered")

@st.cache
def get_data():
    return pd.read_csv("data/results.csv")

df = get_data()

st.write("# Machine Learning Skill Test")

# Session state
if "index" not in st.session_state:
    st.session_state.index = 0
if "correct" not in st.session_state:
    st.session_state.correct = np.array([np.nan] * len(df))
if "retry" not in st.session_state:
    st.session_state.retry = False

def quiz(df):
    # Controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("")
        st.write("")
        if st.button("Back"):
            st.session_state.index -= 1
    with col2:
        jump = st.selectbox('Jump to question', df.index + 1)
    with col3:
        st.write("")
        st.write("")
        if st.button("Go"):
            st.session_state.index = jump - 1
    with col4:
        st.write("")
        st.write("")
        if st.button("Continue"):
            st.session_state.index += 1

    # Display question and answers
    st.write(df.iloc[st.session_state.index, 0])

    try:
        st.image(df.iloc[st.session_state.index, 6])
    except:
        pass

    ans = df.iloc[st.session_state.index, 1:5].dropna()
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

    # Check
    cols = st.columns(6)
    with cols[2]:
        if st.button("Check"):
            if sel == correct_choice:
                st.success("Correct!")
                if (st.session_state.correct[st.session_state.index] != 0) \
                    | (st.session_state.retry == True):
                    st.session_state.correct[st.session_state.index] = 1
            else:
                st.error("Try again!")
                st.session_state.correct[st.session_state.index] = 0

quiz(df)

# Display progress
num_wrong = (st.session_state.correct == 0).sum()
num_correct = (st.session_state.correct == 1).sum()
num_unanswered = len(df) - num_wrong - num_correct
prog = pd.DataFrame({
    "wrong": num_wrong,
    "correct": num_correct,
    "unanswered": num_unanswered
    }, index=[0])

st.write("### Progess")

prog = pd.DataFrame({
    "value": [num_correct, num_wrong, num_unanswered],
    "label": ["correct", "wrong", "unanswered"],
    "y": [1,1,1]
    }, index=[0,1,2])

fig = px.bar(prog, x="value", y="y", color='label', orientation='h',
             labels={"value": "", "y": ""},
             hover_name="value", hover_data={"y": False},
             height=180, color_discrete_map={
                 "wrong": "#FF6666",
                 "correct": "#00FF00",
                 "unanswered": "#C0C0C0"})\
                     .update_layout(legend={"orientation": "h",
                                            "title": "",
                                            "x": 0.25,
                                            "y": -0.33},
                                    xaxis={"range": (0, len(df)),
                                           "tickmode": "array",
                                           "tickvals": np.array([20,40,60,80,len(df)])},
                                    yaxis={"showticklabels": False},
                                    plot_bgcolor="white")

st.plotly_chart(fig)

# Save and load progress
# csv = pd.DataFrame(st.session_state.correct).to_csv(index=False)
# col1, col2 = st.columns(2)
# with col1:
#     st.download_button(
#         label="Save Progress",
#         data=csv,
#         file_name='ML_Quiz_Progress.csv',
#         mime='text/csv',
#     )
# with col2:
#     if st.button("Load Progress"):
#         uploaded_file = st.file_uploader("Load Progress", type="csv")
#         if uploaded_file is not None:
#             arr = np.genfromtxt(uploaded_file, delimiter=",")
#         #     st.session_state.new_correct = arr

# Re-try failed tests
if num_wrong > 0:
    col1, col2 = st.columns(2)
    with col1:
        retry_index = st.selectbox('Re-try questions', df[st.session_state.correct == 0].index + 1)
        st.session_state.index = retry_index - 1
    with col2:
        st.write("")
        st.write("")
        if st.button("Retry"):
            st.session_state.retry = True

# Signature
st.write("")
st.write("")
urlrLink = "[LinkedIn](https://www.linkedin.com/in/ruben-rossbach/)"
urlrGH = "[Github](https://github.com/rubenrossbach)"
st.write("Made by Ruben Rossbach")
st.write(f"{urlrLink} | {urlrGH}")

# load progress

# Turn on dark theme
