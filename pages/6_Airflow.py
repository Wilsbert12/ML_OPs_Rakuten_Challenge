# 6_Airflow.py
import streamlit as st
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer

st.set_page_config(
    page_title="MAY25 BMLOPS // Airflow",
    page_icon="containers/rakuten_st/images/logos/rakuten-favicon.ico",
    layout="wide",
)

st.progress(6 / 10)
st.title("Airflow")

# Airflow content

st.markdown("""
### Goal: Efficiently balance model readiness and resource consumption
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Low Data Volume Phase")
    st.markdown("""
- **Objective**: Quickly reach a usable model
- **Trigger**: Retrain frequently with each batch
- **Success Criteria**: Stop retraining when **F1 > 0.7**
- **Why**: Early stage to builds usability
""")

with col2:
    st.subheader("High Data Volume Phase")
    st.markdown("""
- **Objective**: Conserve system resources
- **Trigger**: Retrain only on **data volume increase beyond a threshold**
- **Strategy**: Use monitoring to detect drift or degraded performance
- **Why**: Avoid overfitting and unnecessary compute usage
""")

st.subheader("Additional Guidelines")
st.markdown("""
- **Versioning & Reproducibility**  
  Track all runs using MLflow with full metadata and artifacts _(artifacts will be implemented later)_

- **Evaluation Consistency**  
  Always compare models on a fixed validation set
""")

st.markdown("---")
st.subheader("Visual Results")

col_img1, col_img2 = st.columns(2)

with col_img1:
    st.image("containers/rakuten_st/images/screenshots/training_dag.png", use_container_width=True)
    st.image("containers/rakuten_st/images/screenshots/ml_pipeline_docker.png", caption="Airflow DAG Execution", use_container_width=True)

with col_img2:
    st.image("containers/rakuten_st/images/screenshots/training_result.png", caption="MLflow Run Results", use_container_width=True)
    

# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/6_Airflow.py")