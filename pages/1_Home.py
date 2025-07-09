# pages/01_Home.py
import streamlit as st
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer


# Page configuration
st.set_page_config(
    page_title="MAY25 BMLOPS // Rakuten: Classification of eCommmerce products",
    page_icon="images/logos/rakuten-favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo display
st.logo(image="images/logos/rakuten-logo-red-wide.svg", size="large", icon_image="images/logos/rakuten-logo-red-square.svg")

st.progress(1 / 7)
st.title("MAY25 BMLOPS // Rakuten")

# Home page content
st.write("## eCommerce Products Classification Project")
st.markdown(
    """
    This Streamlit app is part of the final project for **_DataScientist_**'s training in **Machine Learning Operations** of the cohort **MAY25 BMLOPS**.
    
    Building upon a previous Rakuten product classification challenge, this project demonstrates a **MLOps pipeline** that automates the entire machine learning lifecycle from data ingestion to model deployment and monitoring.
    
    One solution could be an automation via **multimodal machine learning** combining text and image data.
    
    **Technical Implementation**
    * **Apache Airflow** orchestration for automated workflow management
    * **Docker** containerization for scalable and reproducible ML workloads
    * **MLflow** integration for experiment tracking and model registry
    * **PostgreSQL** for metadata storage and MinIO for artifact management
    * **Continuous** Integration/Continuous Deployment (CI/CD) pipelines
    * **Real-time monitoring** and performance tracking capabilities
    
    Use the sidebar or pagination to browse through the presentation of the project and the team, ...
    
    **:material/folder_code: GitHub Repository:** [rakuten_project](https://github.com/your-username/rakuten_project)
    
    """
)

# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/1_Home.py")
