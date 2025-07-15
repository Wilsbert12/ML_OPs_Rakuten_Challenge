# pages/6_FastAPI_demo.py
import streamlit as st
import requests
import os
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer, get_public_ip

st.set_page_config(
    page_title="MAY25 BDS // FastAPI Demo",
    page_icon="containers/rakuten_st/images/logos/rakuten-favicon.ico",
    layout="wide",
)

st.progress(6 / 9)
st.title("FastAPI Demonstration")

PUBLIC_IP = get_public_ip()

# Get FastAPI URL from environment or default to localhost
FASTAPI_INT_URL = os.getenv('FASTAPI_URL', 'http://localhost:8000')
FASTAPI_PUBLIC_URL = f"http://{PUBLIC_IP}:8000"

st.markdown(f"""
This page demonstrates real-time interaction with the Rakuten Product Category API.
            
* Connected to: `{FASTAPI_INT_URL}`
* Public URL: `{FASTAPI_PUBLIC_URL}`
""")

st.subheader("Product Prediction")

# Input form
with st.form("prediction_form"):
    title = st.text_input(
        "**Product Title** (French)", 
        value="Piscine Intex Prism",
        help="Enter the product title (in French)"
    )
    
    description = st.text_input(
        "**Product Description** (French)", 
        value="Piscine avec liner renforcé de dernière génération structure renforcée en acier",
        help="Enter the product description (in French)"
    )
    
    submitted = st.button("Get Prediction", type="primary")

if submitted and (title or description):
    with st.spinner("Retrieving prediction..."):
        try:
            # Call FastAPI endpoint
            response = requests.post(
                f"{FASTAPI_INT_URL}/predict/",
                json={
                    "title": title,
                    "description": description
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                prediction = result["predictions"][0]
                
                # Display main prediction
                st.metric(
                    "Predicted Category",
                    prediction["category"],
                    f"{prediction['confidence']:.1%} confidence"
                )
                
                # Display top 3 predictions
                if len(prediction["top_3"]) > 1:
                    with st.expander("**Show** Top 3 Predictions", expanded=False):
                        for i, pred in enumerate(prediction["top_3"], 1):
                            st.write(f"{i}. **{pred['category']}** ({pred['confidence']:.1%})")

            else:
                st.error(f"Prediction failed: {response.status_code}")
                st.code(response.text)
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to FastAPI service. Is it running?")
        except requests.exceptions.Timeout:
            st.error("Request timed out. The service may be busy.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Interactive API explorer
st.subheader("API endpoints")

endpoint = st.selectbox(
    "Choose endpoint to test:",
    ["/health", "/models/", "/predict/"]
)

if st.button("Test Endpoint", type="primary"):
    try:
        if endpoint == "/health":
            response = requests.get(f"{FASTAPI_INT_URL}{endpoint}")
        elif endpoint == "/models/":
            response = requests.get(f"{FASTAPI_INT_URL}{endpoint}")
        elif endpoint == "/predict/":
            response = requests.post(
                f"{FASTAPI_INT_URL}{endpoint}",
                json={"title": "Test", "description": "test product"}
            )
    
        with st.expander(f"**Show** status code", expanded=False):
            st.code(f"Status: {response.status_code}")

        with st.expander("**Show** full response", expanded=False):
            st.json(response.json())
            
    except Exception as e:
        st.error(f"Request failed: {str(e)}")

# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/6_FastAPI_Demo.py")