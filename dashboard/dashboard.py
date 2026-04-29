import streamlit as st

from utils.logger import read_logs

st.set_page_config(page_title="Multi-Agent Dashboard", layout="wide")
st.title("Multi-Agent System Dashboard")

st.subheader("Execution Logs")
logs = read_logs()

if not logs:
    st.info("No logs available yet. Run a Discord task first.")
else:
    st.write(f"Total log entries: {len(logs)}")
    for line in reversed(logs):
        st.code(line)
