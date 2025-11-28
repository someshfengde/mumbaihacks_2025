"""MindGuard - Mental Health Monitoring Dashboard

A Streamlit application for monitoring mental health through behavioral data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from api_client import APIClient, BehavioralData

# Page configuration
st.set_page_config(
    page_title="MindGuard - Mental Health Monitor",
    page_icon="🧠",
    layout="wide"
)

# Initialize API client
API_URL = st.sidebar.text_input("API URL", "http://localhost:8000")
client = APIClient(API_URL)

# Custom CSS
st.markdown("""
    <style>
    .risk-low { color: #00cc00; font-size: 24px; font-weight: bold; }
    .risk-medium { color: #ffcc00; font-size: 24px; font-weight: bold; }
    .risk-high { color: #ff0000; font-size: 24px; font-weight: bold; }
    .big-metric { font-size: 48px; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🧠 MindGuard - Mental Health Monitor")
st.markdown("---")

# Check API health
api_healthy = client.health_check()
if api_healthy:
    st.sidebar.success("✅ API Connected")
else:
    st.sidebar.error("❌ API Not Connected")
    st.warning("⚠️ Backend API is not available. Please ensure the FastAPI server is running.")

# Create tabs
tab1, tab2 = st.tabs(["📝 Input Data", "📊 Dashboard"])

# Tab 1: Input Form
with tab1:
    st.header("Enter Your Daily Data")
    st.markdown("Please provide your daily behavioral data to monitor your mental health.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sleep_hours = st.slider(
            "🛏️ Hours of Sleep",
            min_value=0.0,
            max_value=24.0,
            value=7.0,
            step=0.5,
            help="How many hours did you sleep last night?"
        )
        
        mood_score = st.slider(
            "😊 Mood Score",
            min_value=1,
            max_value=10,
            value=5,
            help="How are you feeling today? (1=Very Bad, 10=Excellent)"
        )
        
        messages_sent = st.number_input(
            "💬 Messages Sent",
            min_value=0,
            max_value=1000,
            value=10,
            help="How many messages did you send today?"
        )
    
    with col2:
        steps = st.number_input(
            "🚶 Steps Walked",
            min_value=0,
            max_value=50000,
            value=5000,
            help="How many steps did you walk today?"
        )
        
        app_usage = st.slider(
            "📱 Screen Time (hours)",
            min_value=0.0,
            max_value=24.0,
            value=3.0,
            step=0.5,
            help="How many hours did you spend on apps/screens?"
        )
    
    st.markdown("---")
    
    if st.button("📤 Submit Data", type="primary", use_container_width=True):
        if api_healthy:
            data = BehavioralData(
                sleep_hours=sleep_hours,
                mood_score=mood_score,
                messages_sent=messages_sent,
                steps=steps,
                app_usage_hours=app_usage
            )
            result = client.submit_data(data)
            if result:
                st.success("✅ Data submitted successfully!")
                
                # Get immediate prediction
                prediction = client.predict_risk(data)
                if prediction:
                    st.subheader("Immediate Risk Assessment")
                    
                    # Display risk score
                    risk_color = {
                        "low": "🟢",
                        "medium": "🟡",
                        "high": "🔴"
                    }
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Risk Score", f"{prediction.risk_score:.0%}")
                    with col2:
                        st.metric("Risk Level", f"{risk_color.get(prediction.risk_level, '⚪')} {prediction.risk_level.upper()}")
                    with col3:
                        st.info(f"💡 **Suggestion:** {prediction.intervention_suggestion}")
            else:
                st.error("❌ Failed to submit data. Please try again.")
        else:
            st.error("❌ Cannot submit data - API is not connected.")

# Tab 2: Dashboard
with tab2:
    st.header("📊 Mental Health Dashboard")
    
    if api_healthy:
        # Get latest data
        data_list = client.get_latest_data(7)
        
        if data_list:
            # Convert to DataFrame
            df = pd.DataFrame(data_list)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Get latest prediction
            latest_prediction = client.predict_risk()
            
            if latest_prediction:
                # Risk Display
                st.subheader("Current Risk Status")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Risk Score Gauge
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=latest_prediction.risk_score * 100,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Risk Score"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 30], 'color': "lightgreen"},
                                {'range': [30, 60], 'color': "yellow"},
                                {'range': [60, 100], 'color': "red"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': latest_prediction.risk_score * 100
                            }
                        }
                    ))
                    fig_gauge.update_layout(height=250)
                    st.plotly_chart(fig_gauge, use_container_width=True)
                
                with col2:
                    risk_emoji = {
                        "low": "🟢",
                        "medium": "🟡", 
                        "high": "🔴"
                    }
                    st.markdown(f"""
                    ### Risk Level
                    # {risk_emoji.get(latest_prediction.risk_level, '⚪')} {latest_prediction.risk_level.upper()}
                    """)
                
                with col3:
                    st.markdown("### 💡 Recommended Action")
                    st.info(latest_prediction.intervention_suggestion)
            
            st.markdown("---")
            
            # Trends
            st.subheader("📈 7-Day Trends")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Mood Trend
                fig_mood = px.line(
                    df, x='timestamp', y='mood_score',
                    title='Mood Score Trend',
                    labels={'mood_score': 'Mood (1-10)', 'timestamp': 'Date'}
                )
                fig_mood.update_traces(line_color='#FF6B6B', line_width=3)
                fig_mood.update_layout(yaxis_range=[0, 10])
                st.plotly_chart(fig_mood, use_container_width=True)
                
                # Sleep Trend
                fig_sleep = px.bar(
                    df, x='timestamp', y='sleep_hours',
                    title='Sleep Hours',
                    labels={'sleep_hours': 'Hours', 'timestamp': 'Date'}
                )
                fig_sleep.update_traces(marker_color='#4ECDC4')
                st.plotly_chart(fig_sleep, use_container_width=True)
            
            with col2:
                # Activity Trend
                fig_steps = px.area(
                    df, x='timestamp', y='steps',
                    title='Daily Steps',
                    labels={'steps': 'Steps', 'timestamp': 'Date'}
                )
                fig_steps.update_traces(fill='tozeroy', line_color='#45B7D1')
                st.plotly_chart(fig_steps, use_container_width=True)
                
                # Social Activity
                fig_social = px.bar(
                    df, x='timestamp', y='messages_sent',
                    title='Messages Sent (Social Activity)',
                    labels={'messages_sent': 'Messages', 'timestamp': 'Date'}
                )
                fig_social.update_traces(marker_color='#96CEB4')
                st.plotly_chart(fig_social, use_container_width=True)
            
            st.markdown("---")
            
            # Data Table
            st.subheader("📋 Recent Data Entries")
            display_df = df[['timestamp', 'sleep_hours', 'mood_score', 'messages_sent', 'steps', 'app_usage_hours']].copy()
            display_df.columns = ['Timestamp', 'Sleep (hrs)', 'Mood', 'Messages', 'Steps', 'Screen Time (hrs)']
            st.dataframe(display_df, use_container_width=True)
            
        else:
            st.info("📭 No data available yet. Please submit your first entry in the 'Input Data' tab.")
    else:
        st.warning("⚠️ Cannot load dashboard - API is not connected.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🧠 MindGuard MVP - Mental Health Monitoring System</p>
    <p>⚠️ This is a prototype for demonstration purposes only. 
    If you're experiencing mental health challenges, please reach out to a healthcare professional.</p>
</div>
""", unsafe_allow_html=True)
