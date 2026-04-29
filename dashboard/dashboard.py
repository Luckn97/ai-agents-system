import streamlit as st
import pandas as pd

from config import GENERATED_FILE
from utils.logger import read_logs
from utils.memory_manager import load_history

st.set_page_config(page_title="Multi-Agent Dashboard", layout="wide")
st.title("Multi-Agent System Dashboard")

logs = read_logs()
history = load_history()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Iteration Counts")
    if history:
        df = pd.DataFrame(history)
        st.dataframe(df[["timestamp", "task", "iterations"]], use_container_width=True)
    else:
        st.info("No memory history yet.")

with col2:
    st.subheader("Latest Review Result")
    if history:
        st.json(history[-1].get("review", {}))
    else:
        st.info("No reviews yet.")

st.subheader("Generated Code")
try:
    with open(GENERATED_FILE, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
except FileNotFoundError:
    st.info("No generated code file yet.")

st.subheader("Memory History")
st.json(history)

st.subheader("Workflow Logs")
st.json(logs)
