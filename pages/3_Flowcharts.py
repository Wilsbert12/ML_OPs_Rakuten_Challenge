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

st.markdown("""
### Goal: Efficiently balance model readiness and resource consumption
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Low Data Volume Phase")
    st.markdown("""
- **Objective**: Quickly reach a usable model.
- **Trigger**: Retrain frequently with each batch.
- **Success Criteria**: Stop retraining when **F1 > 0.7**.
- **Why**: Early stage to builds usability.
""")

with col2:
    st.subheader("High Data Volume Phase")
    st.markdown("""
- **Objective**: Conserve system resources.
- **Trigger**: Retrain only on **data volume increase beyond a threshold**.
- **Strategy**: Use monitoring to detect drift or degraded performance.
- **Why**: Avoid overfitting and unnecessary compute usage.
""")

st.subheader("Additional Guidelines")
st.markdown("""
- **Versioning & Reproducibility**  
  Track all runs using MLflow with full metadata and artifacts(artifacts will be implemented later).

- **Evaluation Consistency**  
  Always compare models on a fixed validation set.
""")

st.markdown("---")
st.subheader("Visual Results")

col_img1, col_img2 = st.columns(2)

with col_img1:
    st.image("images/screenshots/training_dag.png", caption="Airflow DAG Execution", use_container_width=True)

with col_img2:
    st.image("images/screenshots/training_result.png", caption="MLflow Run Results", use_container_width=True)
    
# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/3_Flowcharts.py")