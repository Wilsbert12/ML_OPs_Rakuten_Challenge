# 4_Flowcharts.py
import streamlit as st
from streamlit_mermaid import st_mermaid
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer

st.set_page_config(
    page_title="MAY25 BDS // Flowcharts",
    page_icon="images/logos/rakuten-favicon.ico",
    layout="wide",
)

st.progress(4 / 7)
st.title("Flowcharts")


# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/4_Flowcharts.py")