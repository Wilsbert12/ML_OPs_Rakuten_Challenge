import streamlit as st
from streamlit_mermaid import st_mermaid

with open("containers/rakuten_st/flowcharts/rakuten_mlops_retraining.mermaid", "r") as file:
    retraining_fc = file.read() # _fc as in "_flowchart"
    st_mermaid(retraining_fc, height="auto", pan=True, zoom=True, show_controls=True)