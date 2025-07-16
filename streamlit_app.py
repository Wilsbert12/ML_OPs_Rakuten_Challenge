# streamlit_app.py
import streamlit as st

# Define pages with clear navigation structure

# INTRODUCTION PAGES
home_page = st.Page("pages/1_Homepage.py", title="1. Homepage")
team_presentation = st.Page("pages/2_Team_Presentation.py", title="2. Team Presentation")

# PROJECT PAGES
architecture = st.Page("pages/3_Architecture.py", title="3. Architecture")
retraining = st.Page("pages/4_Retraining.py", title="4. Retraining")
airflow = st.Page("pages/5_Airflow.py", title="5. Airflow")
fastapi_demo = st.Page("pages/6_FastAPI_Demo.py", title="6. FastAPI Demo")
monitoring_and_operations = st.Page("pages/7_Monitoring_and_Operations.py", title="7. Monitoring and Operations")
business_metrics_and_insights = st.Page("pages/8_Business_Metrics_and_Insights.py", title="8. Business Metrics and Insights")
future_improvements = st.Page("pages/9_Future_Improvements.py", title="9. Future Improvements")
appendix = st.Page("pages/10_Appendix.py", title="10. Appendix")

# DEV PAGES
tmp = st.Page("pages/11_tmp.py", title="10. tmp")

# Create navigation with grouped pages
pg = st.navigation({
    "INTRODUCTION": [home_page, team_presentation],
    "FLOWCHARTS": [architecture, retraining],
    "PROJECT": [airflow, fastapi_demo, 
                  monitoring_and_operations, business_metrics_and_insights, future_improvements, appendix],
    "DEV": [tmp]
})

# Run the selected page
pg.run()