import streamlit as st
import requests
import time
from streamlit_extras.let_it_rain import rain

st.set_page_config(page_title="🍅 Tomato Freshness Detector", page_icon="🍅", layout="centered")

# --- Styles ---
st.markdown("""
    <style>
    .card {
        background: #fff;
        border-radius: 20px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        padding: 2.5rem 2rem;
        margin: 2rem auto;
        max-width: 400px; http://41.86.177.218:5000
    }
    .result-fresh {
        color: #219150;
        font-size: 2.2rem;
        font-weight: bold;
        text-align: center;
    }
    .result-rotten {
        color: #d32f2f;
        font-size: 2.2rem;
        font-weight: bold;
        text-align: center;
    }
    .dashboard-card {
        background: #f7f7f7;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        padding: 1.2rem 1rem;
        margin-top: 1.5rem;
        text-align: center;
    }
    .subtitle {
        color: #666;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
# st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>🍅 Tomato Freshness Detector</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered tomato quality check</div>', unsafe_allow_html=True)

# --- Fetch Prediction from Backend ---
refresh_interval = st.slider("Refresh interval (seconds)", 2, 30, 5)
placeholder = st.empty()

response = requests.get("http://41.86.177.218:5000/predict")
print("Status code:", response.status_code)
print("Response text:", response.text)
while True:
    with placeholder.container():
        st.write(":hourglass: Fetching latest prediction from backend...")
        start_time = time.time()
        pred_class = None
        confidence = None
        elapsed = 0
        try:
            response = requests.get("http://41.86.177.218:5000/predict")
            result = response.json()
            detections = result.get("detections", [])
            if detections:
                pred_class = detections[0].get("class")
                confidence = detections[0].get("confidence")
                elapsed = time.time() - start_time
        except Exception as e:
            st.error(f"API error: {e}")

        if pred_class and confidence is not None and pred_class.lower() not in ["unknown", "none", ""]:
            # --- Prediction Display ---
            if pred_class.lower() == "fresh tomato":
                st.markdown('<div class="result-fresh">🥳 Fresh Tomato</div>', unsafe_allow_html=True)
                rain(
                    emoji="🍅",
                    font_size=32,
                    falling_speed=5,
                    animation_length="infinite"
                )
            elif pred_class.lower() == "rotten tomato":
                st.markdown('<div class="result-rotten">⚠️ Rotten Tomato</div>', unsafe_allow_html=True)
                st.warning("Rotten detected!", icon="⚠️")
            else:
                st.markdown(f'<div class="result-rotten">{pred_class}</div>', unsafe_allow_html=True)

            st.progress(confidence/100)
            st.markdown(f"<div style='text-align:center;font-size:1.2rem;'>Confidence: <b>{confidence:.2f}%</b></div>", unsafe_allow_html=True)

            # --- Dashboard Card ---
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.markdown(f"<b>Prediction:</b> {pred_class}", unsafe_allow_html=True)
            st.markdown(f"<b>Confidence:</b> {confidence:.2f}%", unsafe_allow_html=True)
            st.markdown(f"<b>Processing Time:</b> {elapsed:.2f} sec", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No prediction available.")
    time.sleep(refresh_interval)
st.markdown('</div>', unsafe_allow_html=True)