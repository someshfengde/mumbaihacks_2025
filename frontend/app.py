"""
MindGuard - Aesthetic Minimal Streamlit App
Mental Health Monitoring Dashboard
"""

import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="MindGuard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for aesthetic minimal design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main title */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4ECDC4, #44A08D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        color: #a0a0a0;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    
    /* Card styles */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    /* Risk indicator */
    .risk-low { 
        color: #4ECDC4;
        text-shadow: 0 0 20px rgba(78, 205, 196, 0.5);
    }
    .risk-medium { 
        color: #FFE66D;
        text-shadow: 0 0 20px rgba(255, 230, 109, 0.5);
    }
    .risk-high { 
        color: #FF6B6B;
        text-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
    }
    
    /* Input fields */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #4ECDC4, #44A08D) !important;
    }
    
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(90deg, #4ECDC4, #44A08D) !important;
        color: #1a1a2e !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(78, 205, 196, 0.4) !important;
    }
    
    /* Suggestion box */
    .suggestion-box {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 1rem;
        border-left: 4px solid #4ECDC4;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(78, 205, 196, 0.5);
        border-radius: 4px;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease forwards;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Backend URL
API_URL = "http://localhost:8000"

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_risk' not in st.session_state:
    st.session_state.current_risk = None
if 'emotion_result' not in st.session_state:
    st.session_state.emotion_result = None
if 'journal_result' not in st.session_state:
    st.session_state.journal_result = None


def predict_risk(data):
    """Call the prediction API."""
    try:
        response = requests.post(f"{API_URL}/predict", json=data, timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        # Fallback: calculate locally if API is not available
        from backend.risk_calculator import calculate_risk_score
        (
            risk_score,
            risk_level,
            suggestion,
            color,
            drivers,
            actions,
        ) = calculate_risk_score(
            sleep_hours=data["sleep_hours"],
            mood_score=data["mood_score"],
            messages_sent=data["messages_sent"],
            steps=data["steps"],
            app_usage_hours=data["app_usage_hours"]
        )
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "suggestion": suggestion,
            "color": color,
            "drivers": drivers,
            "recommended_actions": actions,
        }
    return None


def analyze_journal(text: str):
    """Call the emotion analysis API or fall back to local heuristics."""
    payload = {"text": text}
    try:
        response = requests.post(f"{API_URL}/analyze-text", json=payload, timeout=8)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        from backend.ai_insights import analyze_emotions
        result = analyze_emotions(text)
        return result.to_dict()
    return None


def analyze_journal_entry(text: str):
    """Call backend emotion analysis or fall back locally."""
    payload = {"text": text}
    try:
        response = requests.post(f"{API_URL}/analyze-text", json=payload, timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        try:
            from backend.ai_insights import analyze_emotions
            return analyze_emotions(text).to_dict()
        except Exception:
            return None
    return None


def main():
    # Header
    st.markdown('<h1 class="main-title">🧠 MindGuard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your personal mental wellness companion</p>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Layout
    col1, col2 = st.columns([1, 1.5], gap="large")
    
    with col1:
        st.markdown("### 📊 Daily Check-in")
        st.markdown("*Track your wellbeing in just a few seconds*")
        
        # Input form with aesthetic styling
        sleep_hours = st.slider(
            "😴 Hours of Sleep",
            min_value=0.0,
            max_value=12.0,
            value=7.0,
            step=0.5,
            help="How many hours did you sleep last night?"
        )
        
        mood_score = st.slider(
            "😊 Mood Score",
            min_value=1,
            max_value=10,
            value=7,
            help="Rate your current mood from 1 (lowest) to 10 (highest)"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            messages_sent = st.number_input(
                "💬 Messages Sent",
                min_value=0,
                max_value=500,
                value=10,
                help="How many messages did you send today?"
            )
        
        with col_b:
            steps = st.number_input(
                "👟 Steps Taken",
                min_value=0,
                max_value=50000,
                value=5000,
                step=100,
                help="How many steps have you walked?"
            )
        
        app_usage_hours = st.slider(
            "📱 Screen Time (hours)",
            min_value=0.0,
            max_value=16.0,
            value=4.0,
            step=0.5,
            help="How many hours have you spent on your phone?"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✨ Analyze My Wellbeing"):
            data = {
                "sleep_hours": sleep_hours,
                "mood_score": mood_score,
                "messages_sent": messages_sent,
                "steps": steps,
                "app_usage_hours": app_usage_hours
            }
            
            result = predict_risk(data)
            
            if result:
                st.session_state.current_risk = result
                st.session_state.history.append({
                    **data,
                    "risk_score": result["risk_score"],
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                st.rerun()
    
    with col2:
        st.markdown("### 🌟 Your Wellness Dashboard")
        
        if st.session_state.current_risk:
            result = st.session_state.current_risk
            risk_class = f"risk-{result['risk_level']}"
            
            # Risk score display
            col_r1, col_r2, col_r3 = st.columns(3)
            
            with col_r1:
                st.markdown(f"""
                <div class="metric-card" style="text-align: center;">
                    <p style="color: #a0a0a0; margin-bottom: 0.5rem; font-size: 0.9rem;">Risk Score</p>
                    <h2 class="{risk_class}" style="font-size: 2.5rem; margin: 0;">{result['risk_score']:.0%}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col_r2:
                emoji = "🟢" if result['risk_level'] == 'low' else ("🟡" if result['risk_level'] == 'medium' else "🔴")
                st.markdown(f"""
                <div class="metric-card" style="text-align: center;">
                    <p style="color: #a0a0a0; margin-bottom: 0.5rem; font-size: 0.9rem;">Status</p>
                    <h2 style="font-size: 2rem; margin: 0;">{emoji} {result['risk_level'].capitalize()}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col_r3:
                st.markdown(f"""
                <div class="metric-card" style="text-align: center;">
                    <p style="color: #a0a0a0; margin-bottom: 0.5rem; font-size: 0.9rem;">Check-ins Today</p>
                    <h2 style="font-size: 2.5rem; margin: 0; color: #4ECDC4;">{len(st.session_state.history)}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Suggestion box
            st.markdown(f"""
            <div class="suggestion-box">
                <p style="color: #4ECDC4; font-weight: 600; margin-bottom: 0.5rem;">💡 Personalized Suggestion</p>
                <p style="color: white; font-size: 1.1rem; margin: 0;">{result['suggestion']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Risk drivers + actions
            drivers = result.get("drivers") or []
            actions = result.get("recommended_actions") or []
            st.markdown("#### 🔍 Risk Drivers & Micro-Actions")
            insight_col1, insight_col2 = st.columns(2)

            driver_list = "".join(f"<li>{driver}</li>" for driver in drivers[:4]) or "<li>No significant stressors detected.</li>"
            action_list = "".join(f"<li>{action}</li>" for action in actions[:4]) or "<li>Keep following your current routines.</li>"

            with insight_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <p style="color:#a0a0a0; font-size:0.85rem; margin-bottom:0.5rem;">Top Drivers</p>
                    <ul style="padding-left:1.2rem; color:#fff; margin:0;">
                        {driver_list}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with insight_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <p style="color:#a0a0a0; font-size:0.85rem; margin-bottom:0.5rem;">Micro-Actions</p>
                    <ul style="padding-left:1.2rem; color:#fff; margin:0;">
                        {action_list}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            # Trend chart
            if len(st.session_state.history) >= 2:
                st.markdown("#### 📈 Risk Trend")
                
                df = pd.DataFrame(st.session_state.history)
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['risk_score'],
                    mode='lines+markers',
                    line=dict(color='#4ECDC4', width=3),
                    marker=dict(size=10, color='#4ECDC4'),
                    fill='tozeroy',
                    fillcolor='rgba(78, 205, 196, 0.1)'
                ))
                
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis=dict(
                        showgrid=False,
                        zeroline=False,
                        title=""
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='rgba(255,255,255,0.1)',
                        zeroline=False,
                        range=[0, 1],
                        title=""
                    ),
                    margin=dict(l=0, r=0, t=20, b=0),
                    height=250
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Recent metrics
            st.markdown("#### 📋 Latest Metrics")
            
            metric_cols = st.columns(5)
            metrics = [
                ("😴", "Sleep", f"{sleep_hours}h"),
                ("😊", "Mood", f"{mood_score}/10"),
                ("💬", "Messages", str(messages_sent)),
                ("👟", "Steps", f"{steps:,}"),
                ("📱", "Screen", f"{app_usage_hours}h")
            ]
            
            for i, (emoji, label, value) in enumerate(metrics):
                with metric_cols[i]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 0.5rem;">
                        <p style="font-size: 1.5rem; margin: 0;">{emoji}</p>
                        <p style="color: #a0a0a0; font-size: 0.8rem; margin: 0;">{label}</p>
                        <p style="color: white; font-weight: 600; margin: 0;">{value}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        else:
            # Empty state
            st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem;">
                <p style="font-size: 4rem; margin-bottom: 1rem;">🌱</p>
                <h3 style="color: #a0a0a0; font-weight: 400;">Complete your first check-in</h3>
                <p style="color: #666;">Fill in your daily metrics and click "Analyze" to see your wellness insights</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("### 📝 Emotion Journal")
    st.markdown("Capture how you feel in your own words. We'll analyze the emotional tone and suggest next steps.")

    journal_text = st.text_area(
        "How are you feeling today?",
        placeholder="Write a few sentences about your day, your thoughts, or anything on your mind...",
        height=140,
    )

    journal_col1, journal_col2 = st.columns([1, 2])
    with journal_col1:
        if st.button("💬 Analyze Emotions", use_container_width=True, disabled=len(journal_text.strip()) < 10):
            analysis = analyze_journal(journal_text.strip())
            if analysis:
                st.session_state.emotion_result = analysis
                st.success("Emotion insights updated", icon="✨")

    if st.session_state.emotion_result:
        result = st.session_state.emotion_result
        with journal_col2:
            st.markdown("""
            <div class="metric-card" style="padding: 1rem 1.5rem;">
                <p style="color:#a0a0a0; font-size:0.85rem; margin:0;">Primary Emotion</p>
                <h3 style="margin:0; color:#fff;">{primary} ({confidence:.0%} confidence)</h3>
                <p style="color:#a0a0a0; font-size:0.85rem; margin-top:0.5rem;">Stress Level: <strong style="color:#FFE66D;">{stress}</strong></p>
                <p style="color:#ddd; margin-top:1rem;">{summary}</p>
                <p style="color:#4ECDC4; margin-top:1rem; font-weight:600;">👉 {recommendation}</p>
            </div>
            """.format(
                primary=result["primary_emotion"].title(),
                confidence=result["confidence"],
                stress=result["stress_level"].title(),
                summary=result["summary"],
                recommendation=result["recommendation"],
            ), unsafe_allow_html=True)

            if result.get("supporting_emotions"):
                chips = " ".join(
                    f"<span style='background:rgba(255,255,255,0.1); border-radius:999px; padding:0.2rem 0.8rem; margin-right:0.3rem; font-size:0.85rem;'>{emo.title()}</span>"
                    for emo in result["supporting_emotions"]
                )
                st.markdown(f"<div style='margin-top:0.5rem;'>Secondary cues: {chips}</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <p style="color: #666; font-size: 0.9rem;">
            Built with 💙 for MumbaiHacks 2025 | MindGuard v1.0
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
