# streamlit_app.py
import streamlit as st

# Define pages with clear navigation structure

# INTRODUCTION PAGES
home_page = st.Page("pages/1_Homepage.py", title="1. Homepage")
team_presentation = st.Page("pages/2_Team_Presentation.py", title="2. Team Presentation")

# PROJECT PAGES
architecture = st.Page("pages/3_Architecture.py", title="3. Architecture")
retraining = st.Page("pages/4_Retraining.py", title="4. Retraining")
preprocessing = st.Page("pages/5_Preprocessing.py", title="5. Preprocessing")
airflow = st.Page("pages/6_Airflow.py", title="6. Airflow")
fastapi_demo = st.Page("pages/7_FastAPI_Demo.py", title="7. FastAPI Demo")
monitoring_and_operations = st.Page("pages/8_Monitoring_and_Operations.py", title="8. Monitoring and Operations")
business_metrics_and_insights = st.Page("pages/9_Business_Metrics_and_Insights.py", title="9. Business Metrics and Insights")
future_improvements = st.Page("pages/10_Future_Improvements.py", title="10. Future Improvements")
appendix = st.Page("pages/11_Appendix.py", title="Appendix")


# Create navigation with grouped pages
pg = st.navigation({
    "INTRODUCTION": [home_page, team_presentation],
    "FLOWCHARTS": [architecture, retraining, preprocessing],
    "PROJECT": [airflow, fastapi_demo, 
                  monitoring_and_operations, business_metrics_and_insights, future_improvements],
    "MISC": [appendix]
})

# Run the selected page
pg.run()