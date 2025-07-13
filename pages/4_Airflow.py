# 3_Flowcharts.py
import streamlit as st
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer

st.set_page_config(
    page_title="MAY25 BDS // Airflow",
    page_icon="containers/rakuten_st/images/logos/rakuten-favicon.ico",
    layout="wide",
)

st.progress(4 / 9)
st.title("Airflow")

# Airflow content

# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/4_Airflow.py")