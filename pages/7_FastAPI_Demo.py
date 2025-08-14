# pages/7_FastAPI_Demo.py
import streamlit as st
import requests
import os
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer, get_public_ip

# Demo mode - set to False when running locally with full backend
DEMO_MODE = True

st.set_page_config(
    page_title="MAY25 BMLOPS // FastAPI Demo",
    page_icon="containers/rakuten_st/images/logos/rakuten-favicon.ico",
    layout="wide",
)

st.progress(7 / 10)
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

# Demo mode notification
if DEMO_MODE:
    st.info("💡 **Demo Mode Active** - Live backend integration has been taken offline due to hosting costs. Full predictions available when running locally with complete MLOps infrastructure.")

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
    
    submitted = st.form_submit_button("Get Prediction", type="primary", use_container_width=True)

if submitted and (title or description):
    with st.spinner("Retrieving prediction..."):
        if DEMO_MODE:
            # Demo response based on the input
            if "piscine" in title.lower() or "piscine" in description.lower():
                demo_response = {
                    "predictions": [{
                        "category": "Pool & Water Sports > Swimming Pools",
                        "confidence": 0.89,
                        "top_3": [
                            {"category": "Pool & Water Sports > Swimming Pools", "confidence": 0.89},
                            {"category": "Garden & Outdoor > Pool Equipment", "confidence": 0.08},
                            {"category": "Sports Equipment > Water Sports", "confidence": 0.03}
                        ]
                    }],
                    "model_id": "rakuten_classifier",
                    "status": "success"
                }
            elif "nintendo" in title.lower() or "console" in description.lower():
                demo_response = {
                    "predictions": [{
                        "category": "Video Games & Consoles > Consoles",
                        "confidence": 0.94,
                        "top_3": [
                            {"category": "Video Games & Consoles > Consoles", "confidence": 0.94},
                            {"category": "Video Games & Consoles > Video Games", "confidence": 0.04},
                            {"category": "Electronics > Gaming Accessories", "confidence": 0.02}
                        ]
                    }],
                    "model_id": "rakuten_classifier",
                    "status": "success"
                }
            else:
                # Generic demo response
                demo_response = {
                    "predictions": [{
                        "category": "Electronics > Consumer Electronics",
                        "confidence": 0.76,
                        "top_3": [
                            {"category": "Electronics > Consumer Electronics", "confidence": 0.76},
                            {"category": "Home & Garden > Home Appliances", "confidence": 0.15},
                            {"category": "Sports & Leisure > Sports Equipment", "confidence": 0.09}
                        ]
                    }],
                    "model_id": "rakuten_classifier",
                    "status": "success"
                }
            
            # Display demo prediction
            with st.expander("**Show** Prediction", expanded=True):
                prediction = demo_response["predictions"][0]
                
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
            # Live API call
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
                    with st.expander("**Show** Prediction", expanded=False):
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
                    with st.expander("**Show** Error Message", expanded=False):
                        st.error(f"Prediction failed: {response.status_code}")
                        st.code(response.text)
                        
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI service. Is it running?")
            except requests.exceptions.Timeout:
                st.error("Request timed out. The service may be busy.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Add screenshots section
st.divider()
st.subheader("📸 API Documentation Interface")
st.info("💡 Live integration works when run locally. Screenshots shown below:")

# Add placeholder for FastAPI screenshot
try:
    st.image("containers/rakuten_st/images/screenshots/fastapi-swagger.png", 
             caption="FastAPI Interactive Documentation (Swagger UI)",
             use_column_width=True)
except:
    st.write("📷 *FastAPI Swagger UI screenshot would be displayed here*")

# Horizontal line as divider for better layout
st.divider()

# Interactive API explorer
st.subheader("API endpoints")

endpoint = st.selectbox(
    "Choose endpoint to test:",
    ["/health", "/models/", "/predict/"]
)

if st.button("Test Endpoint", type="primary", use_container_width=True):
    if DEMO_MODE:
        # Demo responses for different endpoints
        if endpoint == "/health":
            demo_response = {
                "status": "healthy",
                "training_active": False,
                "services": {
                    "api": "running",
                    "mlflow_tracking (internal)": "http://mlflow:5000",
                    "mlflow_tracking (public)": f"http://{PUBLIC_IP}:5001"
                }
            }
        elif endpoint == "/models/":
            demo_response = {
                "models": ["rakuten_classifier"],
                "message": "Model registry from MLflow tracking server"
            }
        elif endpoint == "/predict/":
            demo_response = {
                "predictions": [{
                    "category": "Electronics > Consumer Electronics",
                    "confidence": 0.85,
                    "top_3": [{"category": "Electronics > Consumer Electronics", "confidence": 0.85}]
                }],
                "model_id": "rakuten_classifier",
                "status": "success"
            }
        
        with st.expander(f"**Show** status code", expanded=False):
            st.code("Status: 200")

        with st.expander("**Show** full response", expanded=False):
            st.json(demo_response)
    
    else:
        # Live endpoint testing
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
add_pagination_and_footer("pages/7_FastAPI_Demo.py")