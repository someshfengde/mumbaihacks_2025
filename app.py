"""MindGuard - Mental Health Monitoring Dashboard

A unified Streamlit application for monitoring mental health through behavioral data.
This is a standalone app that can be deployed directly to Streamlit Cloud.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple, Optional
import random

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class BehavioralData:
    """Data class for behavioral data entry."""
    sleep_hours: float
    mood_score: int
    messages_sent: int
    steps: int
    app_usage_hours: float
    timestamp: Optional[datetime] = None
    id: Optional[int] = None


# ============================================================================
# RISK CALCULATOR (Integrated from backend)
# ============================================================================

INTERVENTIONS = {
    "low": [
        "Keep up the good work! Stay connected with friends. 💪",
        "Great job maintaining your routine! 🌟",
        "Continue your healthy habits. You're doing amazing! ✨",
        "Your mental wellness looks great today! 🎉"
    ],
    "medium": [
        "Consider taking a short walk today. 🚶",
        "Try a 5-minute breathing exercise. 🧘",
        "Reach out to a friend or family member. 📱",
        "Take a break from screens for 30 minutes. 🌿",
        "Listen to some calming music. 🎵",
        "Write down 3 things you're grateful for. 📝"
    ],
    "high": [
        "Please talk to a trusted friend or family member today. 💙",
        "Consider contacting a counselor or mental health professional. 🏥",
        "Call a mental health helpline if you're feeling overwhelmed. 📞",
        "Reach out to someone you trust - you don't have to face this alone. 🤝",
        "Take a moment to practice self-compassion. You matter. ❤️"
    ]
}


def calculate_risk_score(data: BehavioralData) -> float:
    """Calculate risk score based on behavioral data."""
    risk = 0.0
    
    # Sleep factor
    if data.sleep_hours < 4:
        risk += 0.3
    elif data.sleep_hours < 6:
        risk += 0.15
    
    # Mood factor (most important)
    if data.mood_score <= 3:
        risk += 0.4
    elif data.mood_score <= 5:
        risk += 0.2
    
    # Social activity factor
    if data.messages_sent < 5:
        risk += 0.2
    elif data.messages_sent < 10:
        risk += 0.1
    
    # Screen time factor
    if data.app_usage_hours > 8:
        risk += 0.1
    elif data.app_usage_hours > 6:
        risk += 0.05
    
    # Movement factor
    if data.steps < 1000:
        risk += 0.1
    elif data.steps < 3000:
        risk += 0.05
    
    return min(max(risk, 0.0), 1.0)


def get_risk_level(risk_score: float) -> str:
    """Determine risk level from risk score."""
    if risk_score < 0.3:
        return "low"
    elif risk_score < 0.6:
        return "medium"
    else:
        return "high"


def get_intervention_suggestion(risk_level: str) -> str:
    """Get an intervention suggestion based on risk level."""
    suggestions = INTERVENTIONS.get(risk_level, INTERVENTIONS["medium"])
    return random.choice(suggestions)


def predict_risk(data: BehavioralData) -> Tuple[float, str, str]:
    """Main prediction function that combines all risk assessment."""
    risk_score = calculate_risk_score(data)
    risk_level = get_risk_level(risk_score)
    suggestion = get_intervention_suggestion(risk_level)
    return risk_score, risk_level, suggestion


# ============================================================================
# DATA STORAGE (Session State based)
# ============================================================================

def init_session_state():
    """Initialize session state for data storage."""
    if 'data_entries' not in st.session_state:
        st.session_state.data_entries = []
    if 'next_id' not in st.session_state:
        st.session_state.next_id = 1


def add_entry(data: BehavioralData) -> BehavioralData:
    """Add a new behavioral data entry."""
    data.id = st.session_state.next_id
    data.timestamp = datetime.now()
    st.session_state.data_entries.append(data)
    st.session_state.next_id += 1
    return data


def get_all_entries() -> List[BehavioralData]:
    """Get all behavioral data entries."""
    return st.session_state.data_entries


def get_latest_entries(n: int = 7) -> List[BehavioralData]:
    """Get the latest n entries."""
    return st.session_state.data_entries[-n:] if st.session_state.data_entries else []


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="MindGuard - Mental Health Monitor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* Risk level colors */
    .risk-low {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: bold;
        display: inline-block;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #F2994A 0%, #F2C94C 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: bold;
        display: inline-block;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: bold;
        display: inline-block;
    }
    
    /* Suggestion box */
    .suggestion-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .stat-label {
        color: #888;
        font-size: 0.9rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class="main-header">
    <h1>🧠 MindGuard</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">Your Personal Mental Health Companion</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 📊 Quick Stats")
    
    entries = get_all_entries()
    total_entries = len(entries)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Entries", total_entries)
    with col2:
        if entries:
            avg_mood = sum(e.mood_score for e in entries) / len(entries)
            st.metric("Avg Mood", f"{avg_mood:.1f}")
        else:
            st.metric("Avg Mood", "N/A")
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    MindGuard helps you track and understand your mental wellness through daily behavioral data.
    
    **Features:**
    - 📝 Log daily activities
    - 📈 Track trends over time
    - 🎯 Get personalized insights
    - 💡 Receive helpful suggestions
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚠️ Disclaimer")
    st.caption("""
    This is a prototype for demonstration purposes only. 
    If you're experiencing mental health challenges, please reach out to a healthcare professional.
    """)

# ============================================================================
# MAIN CONTENT - TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs(["📝 Log Entry", "📊 Dashboard", "📈 Analytics"])

# ============================================================================
# TAB 1: LOG ENTRY
# ============================================================================

with tab1:
    st.markdown("### How are you doing today?")
    st.markdown("Fill in your daily metrics to track your mental wellness journey.")
    
    with st.form("daily_entry_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 😴 Sleep & Mood")
            
            sleep_hours = st.slider(
                "Hours of Sleep",
                min_value=0.0,
                max_value=12.0,
                value=7.0,
                step=0.5,
                help="How many hours did you sleep last night?"
            )
            
            # Visual sleep indicator
            if sleep_hours < 5:
                st.warning("😟 That's not enough sleep. Try to get more rest!")
            elif sleep_hours < 7:
                st.info("😐 Could use a bit more sleep.")
            else:
                st.success("😊 Great sleep duration!")
            
            mood_score = st.slider(
                "Mood Score",
                min_value=1,
                max_value=10,
                value=5,
                help="How are you feeling today? (1=Very Bad, 10=Excellent)"
            )
            
            # Mood emoji feedback
            mood_emojis = {1: "😢", 2: "😞", 3: "😟", 4: "😕", 5: "😐", 
                         6: "🙂", 7: "😊", 8: "😄", 9: "😁", 10: "🤩"}
            st.markdown(f"**Current mood:** {mood_emojis.get(mood_score, '😐')} ({mood_score}/10)")
        
        with col2:
            st.markdown("#### 🏃 Activity & Social")
            
            steps = st.number_input(
                "Steps Walked",
                min_value=0,
                max_value=50000,
                value=5000,
                step=500,
                help="How many steps did you walk today?"
            )
            
            # Steps progress indicator
            step_goal = 10000
            progress = min(steps / step_goal, 1.0)
            st.progress(progress)
            st.caption(f"Progress to {step_goal:,} step goal: {progress*100:.0f}%")
            
            messages_sent = st.number_input(
                "Messages Sent",
                min_value=0,
                max_value=500,
                value=10,
                help="How many messages did you send today?"
            )
            
            app_usage = st.slider(
                "Screen Time (hours)",
                min_value=0.0,
                max_value=16.0,
                value=3.0,
                step=0.5,
                help="How many hours did you spend on screens?"
            )
            
            if app_usage > 8:
                st.warning("📱 High screen time! Consider taking breaks.")
        
        st.markdown("---")
        
        submitted = st.form_submit_button("📤 Submit Entry", use_container_width=True, type="primary")
        
        if submitted:
            data = BehavioralData(
                sleep_hours=sleep_hours,
                mood_score=mood_score,
                messages_sent=messages_sent,
                steps=steps,
                app_usage_hours=app_usage
            )
            
            entry = add_entry(data)
            risk_score, risk_level, suggestion = predict_risk(data)
            
            st.success("✅ Entry logged successfully!")
            
            # Show immediate feedback
            st.markdown("### 🎯 Your Assessment")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Animated gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=risk_score * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Risk Score", 'font': {'size': 20}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1},
                        'bar': {'color': "#667eea"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'steps': [
                            {'range': [0, 30], 'color': '#38ef7d'},
                            {'range': [30, 60], 'color': '#F2C94C'},
                            {'range': [60, 100], 'color': '#f45c43'}
                        ],
                    }
                ))
                fig.update_layout(height=250, margin=dict(t=50, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                risk_class = f"risk-{risk_level}"
                risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}
                st.markdown(f"""
                <div style="text-align: center; padding: 2rem;">
                    <p style="font-size: 1rem; color: #888;">Risk Level</p>
                    <div class="{risk_class}">
                        {risk_emoji.get(risk_level, '')} {risk_level.upper()}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="suggestion-box">
                    <h4>💡 Suggestion</h4>
                    <p style="font-size: 1.1rem;">{suggestion}</p>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: DASHBOARD
# ============================================================================

with tab2:
    entries = get_latest_entries(7)
    
    if not entries:
        st.info("📭 No data yet! Start by logging your first entry in the 'Log Entry' tab.")
        
        # Show demo data option
        if st.button("🎮 Load Demo Data"):
            demo_data = [
                BehavioralData(6, 6, 15, 4000, 4),
                BehavioralData(7, 7, 20, 6000, 3),
                BehavioralData(5, 4, 5, 2000, 6),
                BehavioralData(8, 8, 30, 8000, 2),
                BehavioralData(4, 3, 3, 1000, 8),
                BehavioralData(7, 6, 18, 5500, 4),
                BehavioralData(6.5, 5, 10, 4500, 5),
            ]
            for d in demo_data:
                add_entry(d)
            st.rerun()
    else:
        # Current Status Section
        latest_entry = entries[-1]
        risk_score, risk_level, suggestion = predict_risk(latest_entry)
        
        st.markdown("### 🎯 Current Status")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_score * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Risk Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#667eea"},
                    'steps': [
                        {'range': [0, 30], 'color': '#38ef7d'},
                        {'range': [30, 60], 'color': '#F2C94C'},
                        {'range': [60, 100], 'color': '#f45c43'}
                    ],
                }
            ))
            fig.update_layout(height=200, margin=dict(t=30, b=0, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}
            risk_colors = {"low": "#38ef7d", "medium": "#F2C94C", "high": "#f45c43"}
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem;">
                <p style="color: #888; margin-bottom: 0.5rem;">Risk Level</p>
                <div style="background: {risk_colors[risk_level]}; color: white; 
                            padding: 0.8rem 1.5rem; border-radius: 25px; 
                            font-size: 1.3rem; font-weight: bold; display: inline-block;">
                    {risk_emoji[risk_level]} {risk_level.upper()}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            mood_emojis = ["😢", "😞", "😟", "😕", "😐", "🙂", "😊", "😄", "😁", "🤩"]
            mood_idx = max(0, min(latest_entry.mood_score - 1, 9))  # Clamp to valid range
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem;">
                <p style="color: #888; margin-bottom: 0.5rem;">Today's Mood</p>
                <div style="font-size: 3rem;">{mood_emojis[mood_idx]}</div>
                <p style="font-weight: bold; color: #667eea;">{latest_entry.mood_score}/10</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem;">
                <p style="color: #888; margin-bottom: 0.5rem;">Sleep</p>
                <div style="font-size: 2rem;">😴</div>
                <p style="font-weight: bold; color: #667eea;">{latest_entry.sleep_hours}h</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Suggestion Box
        st.markdown(f"""
        <div class="suggestion-box">
            <h4>💡 Today's Recommendation</h4>
            <p style="font-size: 1.2rem; margin: 0;">{suggestion}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Trends Section
        st.markdown("### 📈 7-Day Trends")
        
        # Prepare data
        df = pd.DataFrame([{
            'timestamp': e.timestamp,
            'sleep_hours': e.sleep_hours,
            'mood_score': e.mood_score,
            'messages_sent': e.messages_sent,
            'steps': e.steps,
            'app_usage_hours': e.app_usage_hours
        } for e in entries])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Mood Trend
            fig_mood = go.Figure()
            fig_mood.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['mood_score'],
                mode='lines+markers',
                name='Mood',
                line=dict(color='#FF6B6B', width=3),
                marker=dict(size=10),
                fill='tozeroy',
                fillcolor='rgba(255, 107, 107, 0.2)'
            ))
            fig_mood.update_layout(
                title='😊 Mood Trend',
                yaxis_range=[0, 11],
                height=300,
                showlegend=False,
                margin=dict(t=50, b=30, l=30, r=30)
            )
            st.plotly_chart(fig_mood, use_container_width=True)
            
            # Sleep Trend
            fig_sleep = go.Figure()
            fig_sleep.add_trace(go.Bar(
                x=df['timestamp'],
                y=df['sleep_hours'],
                name='Sleep',
                marker_color='#4ECDC4'
            ))
            fig_sleep.add_hline(y=7, line_dash="dash", line_color="green", 
                              annotation_text="Recommended (7h)")
            fig_sleep.update_layout(
                title='😴 Sleep Hours',
                height=300,
                showlegend=False,
                margin=dict(t=50, b=30, l=30, r=30)
            )
            st.plotly_chart(fig_sleep, use_container_width=True)
        
        with col2:
            # Steps Trend
            fig_steps = go.Figure()
            fig_steps.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['steps'],
                mode='lines+markers',
                name='Steps',
                line=dict(color='#45B7D1', width=3),
                marker=dict(size=10),
                fill='tozeroy',
                fillcolor='rgba(69, 183, 209, 0.2)'
            ))
            fig_steps.add_hline(y=10000, line_dash="dash", line_color="green",
                              annotation_text="Goal (10k)")
            fig_steps.update_layout(
                title='🚶 Daily Steps',
                height=300,
                showlegend=False,
                margin=dict(t=50, b=30, l=30, r=30)
            )
            st.plotly_chart(fig_steps, use_container_width=True)
            
            # Screen Time
            fig_screen = go.Figure()
            fig_screen.add_trace(go.Bar(
                x=df['timestamp'],
                y=df['app_usage_hours'],
                name='Screen Time',
                marker_color='#96CEB4'
            ))
            fig_screen.add_hline(y=6, line_dash="dash", line_color="red",
                               annotation_text="Limit (6h)")
            fig_screen.update_layout(
                title='📱 Screen Time',
                height=300,
                showlegend=False,
                margin=dict(t=50, b=30, l=30, r=30)
            )
            st.plotly_chart(fig_screen, use_container_width=True)

# ============================================================================
# TAB 3: ANALYTICS
# ============================================================================

with tab3:
    entries = get_all_entries()
    
    if len(entries) < 2:
        st.info("📊 Need at least 2 entries to show analytics. Keep logging your data!")
    else:
        st.markdown("### 📊 Detailed Analytics")
        
        df = pd.DataFrame([{
            'timestamp': e.timestamp,
            'sleep_hours': e.sleep_hours,
            'mood_score': e.mood_score,
            'messages_sent': e.messages_sent,
            'steps': e.steps,
            'app_usage_hours': e.app_usage_hours,
            'risk_score': calculate_risk_score(e)
        } for e in entries])
        
        # Summary Statistics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        metrics = [
            ("Avg Sleep", f"{df['sleep_hours'].mean():.1f}h", "😴"),
            ("Avg Mood", f"{df['mood_score'].mean():.1f}", "😊"),
            ("Avg Steps", f"{df['steps'].mean():,.0f}", "🚶"),
            ("Avg Screen", f"{df['app_usage_hours'].mean():.1f}h", "📱"),
            ("Avg Risk", f"{df['risk_score'].mean()*100:.0f}%", "🎯")
        ]
        
        for col, (label, value, emoji) in zip([col1, col2, col3, col4, col5], metrics):
            with col:
                st.markdown(f"""
                <div class="stat-card">
                    <div style="font-size: 2rem;">{emoji}</div>
                    <div class="stat-value">{value}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Risk Score Over Time
        fig_risk = go.Figure()
        fig_risk.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['risk_score'] * 100,
            mode='lines+markers',
            name='Risk Score',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        fig_risk.add_hrect(y0=0, y1=30, fillcolor="rgba(56, 239, 125, 0.2)", 
                         line_width=0, annotation_text="Low Risk Zone")
        fig_risk.add_hrect(y0=30, y1=60, fillcolor="rgba(242, 201, 76, 0.2)", 
                         line_width=0)
        fig_risk.add_hrect(y0=60, y1=100, fillcolor="rgba(244, 92, 67, 0.2)", 
                         line_width=0)
        fig_risk.update_layout(
            title='🎯 Risk Score Trend',
            yaxis_title='Risk Score (%)',
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig_risk, use_container_width=True)
        
        # Correlation Analysis
        st.markdown("### 🔗 Factor Correlations")
        
        correlation_data = df[['sleep_hours', 'mood_score', 'messages_sent', 'steps', 'app_usage_hours', 'risk_score']].corr()
        
        fig_corr = px.imshow(
            correlation_data,
            labels=dict(color="Correlation"),
            x=['Sleep', 'Mood', 'Messages', 'Steps', 'Screen', 'Risk'],
            y=['Sleep', 'Mood', 'Messages', 'Steps', 'Screen', 'Risk'],
            color_continuous_scale='RdBu_r',
            aspect='auto'
        )
        fig_corr.update_layout(height=400)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Data Table
        st.markdown("### 📋 All Entries")
        
        display_df = df[['timestamp', 'sleep_hours', 'mood_score', 'messages_sent', 
                        'steps', 'app_usage_hours', 'risk_score']].copy()
        display_df.columns = ['Timestamp', 'Sleep (h)', 'Mood', 'Messages', 
                             'Steps', 'Screen (h)', 'Risk Score']
        display_df['Risk Score'] = display_df['Risk Score'].apply(lambda x: f"{x*100:.0f}%")
        
        st.dataframe(display_df.sort_values('Timestamp', ascending=False), 
                    use_container_width=True, hide_index=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 2rem;'>
    <p style="font-size: 1.2rem;">🧠 <strong>MindGuard</strong> - Your Mental Health Companion</p>
    <p>Built with ❤️ for MumbaiHacks 2025</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        ⚠️ This is a prototype for demonstration purposes only.<br>
        If you're experiencing mental health challenges, please reach out to a healthcare professional.
    </p>
</div>
""", unsafe_allow_html=True)
