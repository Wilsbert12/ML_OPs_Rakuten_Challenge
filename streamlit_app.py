# streamlit_app.py
import streamlit as st

# Define pages with clear navigation structure
home_page = st.Page("pages/1_Home.py", title="1. Home")
team_presentation = st.Page("pages/2_Team_Presentation.py", title="2. Team Presentation")
key_focus_areas = st.Page("pages/3_Key_Focus_Areas.py", title="3. Key Focus Areas")
flowcharts = st.Page("pages/4_Flowcharts.py", title="4. Flowcharts (WIP)")
tmp = st.Page("pages/10_tmp.py", title="10. tmp")

# Create navigation with grouped pages
pg = st.navigation({
    "OVERVIEW": [home_page, team_presentation],
    "PROJECT": [key_focus_areas, flowcharts],
    "DEV": [tmp]
})

# Run the selected page
pg.run()