#pages/7_Monitoring_and_Operations.py
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer

st.set_page_config(
    page_title="MAY25 BDS // Monitoring and Operations",
    page_icon="containers/rakuten_st/images/logos/rakuten-favicon.ico",
    layout="wide",
)

st.progress(7 / 9)
st.title("Monitoring and Operations")

# Get service URLs from environment
PROMETHEUS_URL = os.getenv('PROMETHEUS_URL', 'http://localhost:9090')
GRAFANA_URL = os.getenv('GRAFANA_URL', 'http://localhost:3000')
FASTAPI_URL = os.getenv('FASTAPI_URL', 'http://localhost:8000')

st.markdown(f"""
### Live System Monitoring

Connected to:
- **Prometheus**: `{PROMETHEUS_URL}`
- **Grafana**: `{GRAFANA_URL}`
- **FastAPI**: `{FASTAPI_URL}`

Real-time metrics from our MLOps infrastructure.
""")

def query_prometheus(query, start=None, end=None, step=None):
    """Query Prometheus for metrics data"""
    try:
        if start and end and step:
            url = f"{PROMETHEUS_URL}/api/v1/query_range"
            params = {
                "query": query,
                "start": start.timestamp(),
                "end": end.timestamp(),
                "step": step
            }
        else:
            url = f"{PROMETHEUS_URL}/api/v1/query"
            params = {"query": query}
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()["data"]["result"]
    except Exception as e:
        st.error(f"Failed to query Prometheus: {e}")
        return []

# Create tabs for different monitoring areas
tab1, tab2, tab3, tab4 = st.tabs(["📊 Live Metrics", "🚀 API Performance", "🤖 Model Performance", "🖥️ System Health"])

with tab1:
    st.subheader("Real-time System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # API Health Check
    try:
        health_response = requests.get(f"{FASTAPI_URL}/health", timeout=3)
        api_status = "🟢 Healthy" if health_response.status_code == 200 else "🔴 Unhealthy"
    except:
        api_status = "🔴 Offline"
    
    with col1:
        st.metric("FastAPI Status", api_status)
    
    # Prometheus connectivity
    try:
        prom_response = requests.get(f"{PROMETHEUS_URL}/-/healthy", timeout=3)
        prom_status = "🟢 Connected" if prom_response.status_code == 200 else "🔴 Error"
    except:
        prom_status = "🔴 Offline"
    
    with col2:
        st.metric("Prometheus", prom_status)
    
    # Get total requests if available
    total_requests_data = query_prometheus('sum(increase(http_requests_total[1h]))')
    total_requests = float(total_requests_data[0]['value'][1]) if total_requests_data else 0
    
    with col3:
        st.metric("Total Requests (1h)", f"{total_requests:.0f}")
    
    # Get request rate
    rps_data = query_prometheus('sum(rate(http_requests_total[5m]))')
    rps = float(rps_data[0]['value'][1]) if rps_data else 0
    
    with col4:
        st.metric("Requests/sec (5m avg)", f"{rps:.2f}")

with tab2:
    st.subheader("🚀 FastAPI Performance Metrics")
    
    if st.button("🔄 Refresh API Metrics"):
        st.rerun()
    
    # Request count by endpoint
    requests_by_handler = query_prometheus('sum(rate(http_requests_total[5m])) by (handler)')
    
    if requests_by_handler:
        df = pd.DataFrame({
            "endpoint": [res['metric'].get('handler', 'unknown') for res in requests_by_handler],
            "requests_per_sec": [float(res['value'][1]) for res in requests_by_handler]
        })
        
        st.subheader("Request Rate by Endpoint")
        st.bar_chart(df.set_index("endpoint"))
    
    # Error rate
    error_rate_data = query_prometheus('sum(rate(http_requests_total{status=~"4..|5.."}[5m]))')
    error_rate = float(error_rate_data[0]['value'][1]) if error_rate_data else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Error Rate", f"{error_rate:.3f} errors/sec")
    
    # Average response time
    avg_duration_data = query_prometheus('rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])')
    avg_duration = float(avg_duration_data[0]['value'][1]) if avg_duration_data else 0
    
    with col2:
        st.metric("Avg Response Time", f"{avg_duration*1000:.1f}ms")

with tab3:
    st.subheader("🤖 Model Performance")
    
    # MLflow metrics (if available)
    accuracy_data = query_prometheus('mlflow_accuracy')
    if accuracy_data:
        accuracy = float(accuracy_data[0]['value'][1])
        st.metric("Current Model Accuracy", f"{accuracy:.1%}")
    
    f1_data = query_prometheus('mlflow_f1')
    if f1_data:
        f1_score = float(f1_data[0]['value'][1])
        st.metric("Current F1 Score", f"{f1_score:.1%}")
    
    # Model runs
    runs_data = query_prometheus('mlflow_experiment_run_total')
    if runs_data:
        total_runs = float(runs_data[0]['value'][1])
        st.metric("Total Model Runs", f"{total_runs:.0f}")
    
    # Time series chart for model performance
    end = datetime.now()
    start = end - timedelta(hours=24)
    step = 300  # 5 minutes
    
    accuracy_timeseries = query_prometheus('mlflow_accuracy', start=start, end=end, step=step)
    
    if accuracy_timeseries:
        times = []
        values = []
        for item in accuracy_timeseries:
            if "values" in item:
                for ts, val in item["values"]:
                    times.append(pd.to_datetime(float(ts), unit='s'))
                    values.append(float(val))
        
        if times and values:
            df_acc = pd.DataFrame({"Time": times, "Accuracy": values})
            st.subheader("Model Accuracy Trend (24h)")
            st.line_chart(df_acc.set_index("Time"))

with tab4:
    st.subheader("🖥️ System Health")
    
    # CPU usage
    cpu_data = query_prometheus('100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)')
    if cpu_data:
        cpu_usage = float(cpu_data[0]['value'][1])
        st.metric("CPU Usage", f"{cpu_usage:.1f}%")
    
    # Memory usage
    memory_data = query_prometheus('100 * (1 - ((node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes))')
    if memory_data:
        memory_usage = float(memory_data[0]['value'][1])
        st.metric("Memory Usage", f"{memory_usage:.1f}%")
    
    # Disk I/O
    disk_read_data = query_prometheus('rate(node_disk_read_bytes_total[5m])')
    if disk_read_data:
        disk_read = float(disk_read_data[0]['value'][1]) / 1024 / 1024  # Convert to MB/s
        st.metric("Disk Read Rate", f"{disk_read:.1f} MB/s")

# Grafana dashboard embed section
st.markdown("---")
st.subheader("📈 Grafana Dashboards")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔗 Open Grafana"):
        st.markdown(f"[Open Grafana Dashboard]({GRAFANA_URL})")

with col2:
    if st.button("🔗 Open Prometheus"):
        st.markdown(f"[Open Prometheus Targets]({PROMETHEUS_URL}/targets)")

# Auto-refresh option
if st.checkbox("🔄 Auto-refresh every 30 seconds"):
    st.empty()
    import time
    time.sleep(30)
    st.rerun()

# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/7_Monitoring_and_Operations.py")