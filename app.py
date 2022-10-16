import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Machine Learning Skill Test",
    page_icon="chart_with_upwards_trend",
    layout="centered")

st.markdown("""
<style>
div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
    background-color: #3f5ca6;
}
</style>""", unsafe_allow_html=True)

st.write("# Machine Learning Skill Test")

# Get data
@st.cache
def get_data():
    return pd.read_csv("data/results.csv")

df = get_data()

# Session state
if "index" not in st.session_state:
    st.session_state.index = 0
if "correct" not in st.session_state:
    st.session_state.correct = np.array([np.nan] * len(df))
if "retry" not in st.session_state:
    st.session_state.retry = False
if "upload" not in st.session_state:
    st.session_state.upload = False
if "finished" not in st.session_state:
    st.session_state.finished = False

def quiz(df):
    # Controls
    col1, col2, col3, col4, col5 = st.columns([1,1.2,1,1,1])
    with col1:
        st.write("")
        st.write("")
        if st.button("Back"):
            if st.session_state.index != 0:
                st.session_state.index -= 1
            else:
                st.session_state.index = 95
    with col2:
        selection = st.radio("", ["All Questions", "Retry Questions"], index=0)
    with col3:
        if selection == "All Questions":
            st.session_state.retry = False
            jump = st.selectbox('Jump to question', df.index + 1)
        if selection == "Retry Questions":
            st.session_state.retry = True
            jump = st.selectbox('Jump to question', df[st.session_state.correct == 0].index + 1)
    with col4:
        st.write("")
        st.write("")
        if st.button("Go"):
            st.session_state.index = jump - 1
    with col5:
        st.write("")
        st.write("")
        if st.button("Continue"):
            if st.session_state.index != 95:
                st.session_state.index += 1
            else:
                st.session_state.index = 0
    if st.session_state.retry:
        st.info("Retry mode: repeat failed questions and correct mistakes")


    # Display question and answers
    st.write("")
    st.write(f"##### {df.iloc[st.session_state.index, 0]}")

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

st.write("#### Progess")

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
                 "correct": "#66ff66",
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

# Finish animation: show balloons only once upon finishing
if num_correct == len(df):
    st.success("##### Congratulations! You completed all questions!")
    if not st.session_state.finished:
        st.balloons()
        st.session_state.finished = True

# Save and load progress
if st.checkbox("Save/ Load Progress"):
    csv = pd.DataFrame(st.session_state.correct).to_csv(index=False)
    col1, col2 = st.columns(2)
    with col1:
        st.write("Save progress file")
        st.download_button(
            label="Download",
            data=csv,
            file_name='ML_Quiz_Progress.csv',
            mime='text/csv',
            )
    with col2:
        uploaded_file = st.file_uploader("Load progress file", type="csv")
        if (uploaded_file is not None) & (st.session_state.upload == False):
            try:
                arr = np.genfromtxt(uploaded_file, delimiter=",")[1:]
                if arr.shape == (len(df),):
                    st.session_state.correct[:] = arr[:]
                    st.session_state.upload = True
                    # session state: first unanswered question
                    for i in range(len(arr)):
                        if arr[i] not in [0,1]:
                            break
                    st.session_state.index = i
                else:
                    raise
            except:
                st.warning(f"Choose an array of shape ({len(df)},)")
            apply = st.button("Confirm loading progress")
        if uploaded_file is None:
            st.session_state.upload = False

# Signature
st.write("")
st.write("")
urlrLink = "[LinkedIn](https://www.linkedin.com/in/ruben-rossbach/)"
urlrGH = "[Github](https://github.com/rubenrossbach)"
st.write("Made by Ruben Rossbach")
st.write(f"{urlrLink} | {urlrGH}")
