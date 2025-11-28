# MindGuard MVP

🧠 **Mental Health Monitoring System** - AI-assisted behavioral monitoring and crisis prediction.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mindguard.streamlit.app)

## Overview

MindGuard is an MVP prototype that:
- **Monitors behavioral signals** (sleep, mood, social activity, movement, screen time)
- **Predicts mental health crisis risk** using rule-based analysis
- **Displays insights in a beautiful dashboard** with interactive trend charts
- **Suggests personalized interventions** based on risk level

## 🚀 Quick Start (Streamlit Cloud)

The app is designed to be deployed directly on **Streamlit Cloud**. Simply:

1. Fork this repository
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy `app.py`

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## ✨ Features

### 📝 Log Entry Tab
- Input daily behavioral data with instant feedback
- Visual indicators for sleep quality and mood
- Progress tracking for step goals
- Real-time risk assessment after each entry

### 📊 Dashboard Tab
- Beautiful risk score gauge with color coding
- Current mood and sleep status at a glance
- 7-day trend charts for all metrics
- Personalized recommendations

### 📈 Analytics Tab
- Summary statistics across all entries
- Risk score trend visualization
- Correlation heatmap between factors
- Complete data history table

## Risk Scoring

The risk score (0-1) is calculated based on:

| Factor | Condition | Risk Impact |
|--------|-----------|-------------|
| Sleep | < 4 hours | +0.30 |
| Sleep | < 6 hours | +0.15 |
| Mood | ≤ 3 | +0.40 |
| Mood | ≤ 5 | +0.20 |
| Social | < 5 messages | +0.20 |
| Social | < 10 messages | +0.10 |
| Screen | > 8 hours | +0.10 |
| Movement | < 1000 steps | +0.10 |

### Risk Levels

- 🟢 **Low** (< 0.3): Healthy patterns
- 🟡 **Medium** (0.3-0.6): Some concerns
- 🔴 **High** (≥ 0.6): Intervention recommended

## Project Structure

```
mindguard/
├── app.py              # Main Streamlit application (unified)
├── requirements.txt    # Python dependencies
├── README.md
├── backend/            # Legacy API (optional)
│   └── ...
└── frontend/           # Legacy frontend (optional)
    └── ...
```

## Screenshots

### Log Entry
![Log Entry](https://github.com/user-attachments/assets/input-screenshot)

### Dashboard
![Dashboard](https://github.com/user-attachments/assets/dashboard-screenshot)

## Disclaimer

⚠️ **This is a prototype for demonstration purposes only.** 

If you're experiencing mental health challenges, please reach out to a qualified healthcare professional or contact a mental health helpline in your area.

## License

MIT License

---

Built with ❤️ for **MumbaiHacks 2025**
