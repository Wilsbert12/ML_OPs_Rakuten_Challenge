# 3_Flowcharts.py
import streamlit as st
from streamlit_mermaid import st_mermaid
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer

st.set_page_config(
    page_title="MAY25 BDS // Flowcharts",
    page_icon="containers/rakuten_st/images/logos/rakuten-favicon.ico",
    layout="wide",
)

st.progress(3 / 9)
st.title("Flowcharts")

# Project Outline content
screenshot_tab, architecture_tab, retraining_tab = st.tabs(["Screenshot (WIP)", "Architecture Overview", "Retraining"]
)

with screenshot_tab:
    st.image("containers/rakuten_st/images/screenshots/flowchart.png", caption="Flowcharts for the MAY25 BDS project [PLACEHOLDER]", use_container_width=True)

with architecture_tab:
    with open("containers/rakuten_st/flowcharts/rakuten_mlops_architecture_overview.mermaid", "r") as file:
        architecture_fc = file.read() # _fc as in "_flowchart"
        st_mermaid(architecture_fc, height="auto", pan=True, zoom=True, show_controls=True)

with retraining_tab:
    with open("containers/rakuten_st/flowcharts/rakuten_mlops_retraining.mermaid", "r") as file:
        retraining_fc = file.read() # _fc as in "_flowchart"
        st_mermaid(retraining_fc, height="auto", pan=True, zoom=True, show_controls=True)

# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/3_Flowcharts.py")