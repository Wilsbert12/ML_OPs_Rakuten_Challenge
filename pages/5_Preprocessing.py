# 5_Preprocessing.py
import streamlit as st
from streamlit_mermaid import st_mermaid
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer

st.set_page_config(
    page_title="MAY25 BDS // Preprocessing",
    page_icon="containers/rakuten_st/images/logos/rakuten-favicon.ico",
    layout="wide",
)

st.progress(5 / 12)
st.title("Preprocessing Pipeline")

# Load and display the preprocessing flowchart
with open("containers/rakuten_st/flowcharts/preprocessing_pipeline.mermaid", "r") as file:
    preprocessing_fc = file.read()  # *fc as in "*flowchart"
    st_mermaid(preprocessing_fc, height="auto", pan=True, zoom=True, show_controls=True)

# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/5_Preprocessing.py")
