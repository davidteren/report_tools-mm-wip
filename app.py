import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add the parent directory to the path to allow importing report_analyzer
sys.path.append(str(Path(__file__).parent))
import report_analyzer

# Set page configuration
st.set_page_config(
    page_title="Report Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# App title
st.title("Report Analyzer")
st.markdown("A new implementation of the report analyzer tool.")

# Main app content
st.write("This is a clean slate for our new implementation.")

