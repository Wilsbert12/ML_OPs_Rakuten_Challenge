# streamlit_app.py
import streamlit as st

# Define pages with clear navigation structure
home_page = st.Page("pages/1_Home.py", title="1. Home")
team_presentation = st.Page("pages/2_Team_Presentation.py", title="2. Team presentation")
project_outline = st.Page("pages/3_Project_Outline.py", title="3. Project Outline")

# Create navigation with grouped pages
pg = st.navigation({
    "OVERVIEW": [home_page, team_presentation],
    "PROJECT": [project_outline]
})

# Run the selected page
pg.run()