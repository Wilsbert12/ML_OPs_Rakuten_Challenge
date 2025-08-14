# 4_Retraining.py
import streamlit as st
from streamlit_mermaid import st_mermaid
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer


st.set_page_config(
    page_title="MAY25 BMLOPS // Retraining",
    page_icon="containers/rakuten_st/images/logos/rakuten-favicon.ico",
    layout="wide",
)

st.progress(4 / 10)
st.title("Retraining")

with open("containers/rakuten_st/flowcharts/retraining.mermaid", "r") as file:
    retraining_fc = file.read() # _fc as in "_flowchart"
    st_mermaid(retraining_fc, height="auto", pan=True, zoom=True, show_controls=True)

# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/4_Retraining.py")