import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime, timedelta
from containers.rakuten_st.streamlit_utils import add_pagination_and_footer, get_public_ip

# Configure page and set up Prometheus connection
st.set_page_config(
    page_title="MAY25 BMLOPS // Monitoring and Operations",
    page_icon="containers/rakuten_st/images/logos/rakuten-favicon.ico",
    layout="wide",
)

st.progress(8 / 10)
st.title("Monitoring and Operations")

PUBLIC_IP = get_public_ip()

# Use environment variable set in docker-compose for container mlflowking
PROMETHEUS_INT_URL = os.getenv('PROMETHEUS_URL', 'http://localhost:9090')
PROMETHEUS_PUBLIC_URL = f"http://{PUBLIC_IP}:9090"


def query_prometheus(query, start=None, end=None, step=None):
    """I query Prometheus for metrics data with optional time range"""
    endpoint = "query_range" if start and end and step else "query"
    url = f"{PROMETHEUS_INT_URL}/api/v1/{endpoint}"
    
    params = {"query": query}
    if start and end and step:
        params.update({
            "start": start.timestamp(),
            "end": end.timestamp(), 
            "step": step
        })
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()["data"]["result"]
    except requests.exceptions.ConnectionError:
        st.warning(f"Cannot connect to Prometheus at {PROMETHEUS_INT_URL}")
        return []
    except Exception as e:
        st.error(f"Prometheus query failed: {str(e)}")
        return []

def get_metric_value(data):
    """I extract the metric value from Prometheus response"""
    return float(data[0]['value'][1]) if data else 0

def parse_timeseries(result):
    """I convert Prometheus time series data to pandas DataFrame"""
    if not result:
        return pd.DataFrame()
    
    all_data = []
    for item in result:
        if "values" in item:
            for ts, val in item["values"]:
                all_data.append({
                    'timestamp': pd.to_datetime(float(ts), unit='s'),
                    'value': float(val)
                })
    
    return pd.DataFrame(all_data).set_index('timestamp') if all_data else pd.DataFrame()

# I show the most critical metrics first
st.subheader("System Health Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    f1_data = query_prometheus('mlflow_f1')
    f1_score = get_metric_value(f1_data)
    st.metric("Current F1 Score", f"{f1_score:.1%}")

with col2:
    accuracy_data = query_prometheus('mlflow_accuracy') 
    accuracy = get_metric_value(accuracy_data)
    st.metric("Model Accuracy", f"{accuracy:.1%}")

with col3:
    rps_data = query_prometheus('sum(rate(http_requests_total[1m]))')
    rps = get_metric_value(rps_data)
    st.metric("API Requests/sec", f"{rps:.2f}")

with col4:
    error_rate_data = query_prometheus('sum(rate(http_requests_total{status=~"4..|5.."}[1m]))')
    error_rate = get_metric_value(error_rate_data)
    st.metric("Error Rate/sec", f"{error_rate:.3f}")

st.divider()

# I display detailed performance metrics
st.subheader("Model Performance Trends")

# I set up time range for historical data
end_time = datetime.now()
start_time = end_time - timedelta(hours=24)
step_size = 300  # 5 minutes

col1, col2 = st.columns(2)

with col1:
    st.write("**F1 Score Over Time**")
    f1_history = query_prometheus('mlflow_f1', start=start_time, end=end_time, step=step_size)
    f1_df = parse_timeseries(f1_history)
    if not f1_df.empty:
        st.line_chart(f1_df['value'])
    else:
        st.info("No F1 score data available")

with col2:
    st.write("**Model Accuracy Over Time**")
    acc_history = query_prometheus('mlflow_accuracy', start=start_time, end=end_time, step=step_size)
    acc_df = parse_timeseries(acc_history)
    if not acc_df.empty:
        st.line_chart(acc_df['value'])
    else:
        st.info("No accuracy data available")

st.divider()

# I show system resource metrics
st.subheader("System Resources")

system_queries = {
    "CPU Usage": "100 - (avg(rate(node_cpu_seconds_total{mode='idle'}[5m])) * 100)",
    "Memory Usage": "100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))",
    "Disk Read Rate": "rate(node_disk_read_bytes_total[5m])",
    "mlflowk Receive": "rate(node_mlflowk_receive_bytes_total[5m])"
}

cols = st.columns(len(system_queries))
for i, (name, query) in enumerate(system_queries.items()):
    with cols[i]:
        data = query_prometheus(query)
        value = get_metric_value(data)
        unit = "%" if "Usage" in name else "bytes/s"
        st.metric(name, f"{value:.1f} {unit}")

# I provide connection status information
st.subheader("Connection Status")
st.info(f"Prometheus: {PROMETHEUS_INT_URL} | {PROMETHEUS_PUBLIC_URL}")

st.divider()

# I show API performance metrics
st.subheader("API Performance")

col1, col2, col3 = st.columns(3)

with col1:
    total_requests = query_prometheus('sum(increase(http_requests_total[1h]))')
    total = get_metric_value(total_requests)
    st.metric("Total Requests (1h)", f"{total:.0f}")

with col2:
    latency_data = query_prometheus('histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))')
    latency = get_metric_value(latency_data)
    st.metric("Latency P95 (sec)", f"{latency:.3f}")

with col3:
    in_progress = query_prometheus('sum(http_requests_in_progress_total)')
    active = get_metric_value(in_progress)
    st.metric("Active Requests", f"{active:.0f}")

# I display requests by endpoint
st.write("**Requests by Endpoint**")
handler_data = query_prometheus('sum(rate(http_requests_total[1m])) by (handler)')
if handler_data:
    handlers_df = pd.DataFrame([
        {
            'endpoint': item['metric'].get('handler', 'unknown'),
            'rate': float(item['value'][1])
        }
        for item in handler_data
    ]).sort_values('rate', ascending=False)
    
    st.bar_chart(handlers_df.set_index('endpoint')['rate'])
else:
    st.info("No endpoint data available")


# Pagination and footer
st.markdown("---")
add_pagination_and_footer("pages/8_Monitoring_and_Operations.py")