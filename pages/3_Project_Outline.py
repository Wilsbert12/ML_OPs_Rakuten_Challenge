# Project Outline - MLOps Pipeline for Rakuten Product Classification
import streamlit as st
import pandas as pd
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer

st.set_page_config(
    page_title="MAY25 BDS // Project Outline",
    page_icon="images/logos/rakuten-favicon.ico",
    layout="wide",
)

st.progress(3 / 7)
st.title("Project Outline")

# Project Outline content
project_tab1, project_tab2, project_tab3, project_tab4 = st.tabs(
    ["Overview", "MLOps Architecture", "Pipeline Components", "Results & Performance"]
)

with project_tab1:
    st.markdown(
        """
        
        This project demonstrates a **complete MLOps pipeline** for the Rakuten product classification challenge, focusing on deployment, versioning, and operational aspects rather than model accuracy optimization.

        **Primary Objective:** Build a production-ready machine learning infrastructure that can reliably process French product descriptions and classify them into appropriate categories while maintaining operational excellence.

        **Key Focus Areas:**
        * **Infrastructure as Code** with Docker containerization and automated deployment
        * **Workflow Orchestration** using Apache Airflow for reproducible ML pipelines  
        * **Experiment Tracking** with MLflow for model versioning and performance monitoring
        * **API Development** using FastAPI for real-time model serving capabilities
        * **Data Management** with PostgreSQL for structured data and MinIO for object storage
        * **Monitoring & Observability** through comprehensive logging and health checks

        **:material/folder_code: GitHub Repository:** [rakuten_project](https://github.com/Pockyee/rakuten_project)
        
        **Current Performance:** SVM achieves 73.4% F1 score on French text classification with 16,983 training samples across 27 product categories.
        """
    )

with project_tab2:
    st.markdown(
        """
        **:material/architecture: MLOps Infrastructure Overview**
        
        The project implements a comprehensive MLOps stack designed for scalability and operational reliability:

        **Container Orchestration**
        >> All components run in isolated Docker containers to ensure consistent execution across different environments. The ML pipeline uses a dedicated container with scikit-learn, NLTK, and XGBoost dependencies.

        **Workflow Management with Apache Airflow**
        >> Three main DAGs orchestrate the entire pipeline: data download, data preparation, and ML training. Each workflow includes proper error handling, retry logic, and dependency management.

        **Data Storage Strategy**
        >> PostgreSQL handles structured data including product descriptions and metadata, while MinIO provides S3-compatible object storage for images and large files. This separation optimizes query performance and storage costs.

        **Experiment Tracking & Model Registry**
        >> MLflow automatically logs model parameters, metrics, and artifacts. The system tracks hyperparameter configurations, training time, and resource usage across all experiments.

        **API Layer for Model Serving**
        >> FastAPI provides REST endpoints for model training triggers, prediction requests, and health monitoring. The API integrates with MLflow for dynamic model loading and version management.

        **Monitoring & Health Checks**
        >> Each service includes health check endpoints and comprehensive logging. The system monitors data quality, model drift, application metrics, and resource utilization.
        """
    )

with project_tab3:
    components_col1, components_col2 = st.columns(2)

    with components_col1:
        st.markdown("### Data Pipeline Components")
        st.markdown(
            """
        **Data Ingestion (`download_data_dag.py`)**
        - Automated download from Rakuten challenge platform
        - Handles authentication and session management
        - Downloads X_train.csv and Y_train.csv datasets

        **Data Preparation (`prepare_data_dag.py`)**
        - Batch processing with configurable chunk sizes (default: 2000 rows)
        - Database schema creation and data validation
        - Incremental loading to prevent memory overflow

        **Feature Engineering (`preprocessing.py`)**
        - French stopword removal using NLTK
        - TF-IDF vectorization with 1000 features
        - Multiple text preprocessing versions (raw, classical ML, BERT-ready)
        """
        )

    with components_col2:
        st.markdown("### ML Training & Serving")
        st.markdown(
            """
        **Model Training (`training.py`)**
        - GridSearchCV with 3-fold cross-validation
        - Multiple algorithms: Random Forest, Logistic Regression, SVM, XGBoost
        - Automated hyperparameter tuning and model selection

        **Model Registry & Versioning**
        - MLflow integration for experiment tracking
        - Automatic model artifact storage
        - Version-controlled model deployment pipeline

        **API Services (`main.py`)**
        - FastAPI endpoints for training and prediction
        - Health monitoring and status reporting
        - Integration with MLflow model registry
        """
        )

with project_tab4:
    st.markdown("### Model Performance Results")

    # Current ML Performance based on repository information
    models_results_data = {
        "Algorithm": [
            "Support Vector Machine",
            "Logistic Regression", 
            "Random Forest",
            "XGBoost"
        ],
        "Hyperparameters": [
            "C=1, kernel=linear",
            "C=1, penalty=l2", 
            "n_estimators=100, max_depth=20",
            "n_estimators=50, max_depth=3"
        ],
        "Cross-Validation F1": [
            0.716,
            "-",
            "-", 
            "-"
        ],
        "Test F1 Score": [
            0.734,
            "-",
            "-",
            "-"
        ],
        "Test Accuracy": [
            0.731,
            "-", 
            "-",
            "-"
        ]
    }

    # Infrastructure performance metrics
    infrastructure_metrics_data = {
        "Component": [
            "Data Preprocessing",
            "Model Training (GridSearchCV)",
            "API Response Time",
            "Database Query Performance",
            "Container Startup Time"
        ],
        "Performance": [
            "~2 minutes for 16,983 samples",
            "~15 minutes with 3-fold CV",
            "<200ms for predictions",
            "<100ms for metadata queries", 
            "<30 seconds for ML container"
        ],
        "Resource Usage": [
            "CPU: 2 cores, RAM: 4GB",
            "CPU: 4 cores, RAM: 8GB",
            "CPU: 1 core, RAM: 2GB",
            "CPU: 2 cores, RAM: 4GB",
            "Minimal overhead"
        ]
    }

    models_results_df = pd.DataFrame(models_results_data)
    infrastructure_df = pd.DataFrame(infrastructure_metrics_data)

    st.dataframe(models_results_df, use_container_width=True)

    st.markdown("### Infrastructure Performance Metrics")
    st.dataframe(infrastructure_df, use_container_width=True)

    st.markdown("### Key Technical Achievements")
    
    achievement_col1, achievement_col2 = st.columns(2)
    
    with achievement_col1:
        st.markdown(
            """
        **Operational Excellence**
        - Zero-downtime deployments with health checks
        - Automated retry logic and error handling
        - Comprehensive logging and monitoring
        - Scalable batch processing capabilities
        """
        )
    
    with achievement_col2:
        st.markdown(
            """
        **Development Workflow**
        - Containerized development environment
        - Version-controlled ML experiments  
        - Automated testing and validation
        - Infrastructure as Code approach
        """
        )

    st.markdown("### Technical Insights & Lessons Learned")
    st.markdown(
        """
        **MLOps Implementation Insights:**
        
        The project successfully demonstrates that operational excellence can be achieved without sacrificing model performance. The SVM model achieves competitive results (73.4% F1 score) while being deployed through a robust, scalable infrastructure.

        **Scalability Considerations:**
        The modular architecture allows for easy scaling of individual components. The batch processing approach ensures the system can handle datasets much larger than the current 16,983 samples without memory constraints.

        **Monitoring & Observability:**
        Each component includes comprehensive health checks and logging. The system tracks data quality metrics, model performance over time, and infrastructure resource utilization, providing full visibility into system behavior.

        **Future Enhancement Opportunities:**
        The current architecture provides a solid foundation for implementing advanced MLOps capabilities such as automated model retraining, A/B testing frameworks, and real-time data drift detection.
        """
    )

# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/3_Project_Outline.py")