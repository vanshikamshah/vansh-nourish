"""
Nourish — Autonomous Nutrition Platform
Streamlit Dashboard App
SP Jain GMBA · Blue Ocean Strategy Challenge · Dr. Umesh Kothari

Run with: streamlit run app.py
"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY   = "#0B1D3A"
TEAL   = "#00A896"
CORAL  = "#E8472A"
GOLD   = "#F7B731"
MINT   = "#D0F0EB"
LIGHT  = "#F0F9F7"
LIME   = "#52B788"
SKY    = "#3A86FF"
PURPLE = "#7B2D8B"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nourish — BOS Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .stApp { background: #F0F9F7; }
      h1, h2, h3 { color: #0B1D3A; font-family: Inter, Arial, sans-serif; }
      .metric-card { background: white; border-radius: 12px; padding: 16px;
                     border-left: 4px solid #00A896; margin: 8px 0; }
      .stTabs [data-baseweb="tab-list"] { background: #0B1D3A; border-radius: 8px; padding: 4px; }
      .stTabs [data-baseweb="tab"] { color: #D0F0EB !important; }
      .stTabs [aria-selected="true"] { background: #00A896 !important; border-radius: 6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    '<h1 style="text-align:center;color:#0B1D3A;font-size:2.4rem;">🌿 NOURISH</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="text-align:center;color:#00A896;font-size:1.1rem;">'
    'Autonomous Nutrition Platform &nbsp;·&nbsp; Blue Ocean Strategy Challenge &nbsp;·&nbsp; '
    'SP Jain GMBA &nbsp;·&nbsp; Dr. Umesh Kothari</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="text-align:center;font-style:italic;color:#888;font-size:0.95rem;">'
    '"Your Body. Your Food. No Decision."</p>',
    unsafe_allow_html=True,
)
st.divider()


# ── Sidebar controls ──────────────────────────────────────────────────────────
st.sidebar.image(
    "https://via.placeholder.com/200x60/0B1D3A/00A896?text=NOURISH",
    use_container_width=True,
)
st.sidebar.markdown("### ⚙️ Simulation Controls")
seed        = st.sidebar.slider("Random Seed", 0, 100, 42)
n_nodes     = st.sidebar.slider("Prep Nodes in City", 10, 25, 18)
user_month  = st.sidebar.slider("Subscription Month", 0, 24, 6)
sim_day     = st.sidebar.selectbox("Simulate Day", ["Workday", "Weekend", "High-Stress Day"], 0)
np.random.seed(seed)

st.sidebar.divider()
st.sidebar.markdown(
    "**Current biometric state:**  \n"
    "🩸 Glucose: **4.8 mmol/L** ↓  \n"
    "💧 Hydration: **62%** ↓  \n"
    "❤️ HRV: **68 ms** ↑  \n"
    "⚡ Energy: **54/100** ↓  \n\n"
    "🟡 **Meal trigger active** — ETA 18 min"
)


# ── Data simulation ───────────────────────────────────────────────────────────
def simulate_day(n=1440, mode="Workday"):
    t = np.linspace(0, 24, n)
    stress_boost = 1.5 if mode == "High-Stress Day" else (0.6 if mode == "Weekend" else 1.0)
    glucose = (
        4.8 + 0.4 * np.sin(2 * np.pi * t / 24 - 1)
        + 1.2 * np.exp(-((t - 8.5) / 0.4) ** 2)
        + 0.9 * np.exp(-((t - 13.0) / 0.4) ** 2)
        + 0.7 * np.exp(-((t - 19.5) / 0.4) ** 2)
        + 0.08 * np.random.randn(n)
    )
    hydration = (
        85 - 0.8 * t
        + 8 * np.exp(-((t - 9) / 0.3) ** 2)
        + 6 * np.exp(-((t - 14) / 0.3) ** 2)
        + 5 * np.exp(-((t - 20) / 0.3) ** 2)
        + 1.5 * np.random.randn(n)
    ).clip(40, 100)
    stress = (
        20 * stress_boost
        + 15 * np.exp(-((t - 11) / 2) ** 2) * stress_boost
        + 12 * np.exp(-((t - 16) / 1.5) ** 2) * stress_boost
        + 3 * np.random.randn(n)
    ).clip(5, 80)
    energy = (
        50 + 20 * np.sin(2 * np.pi * t / 24 - np.pi / 4)
        - 15 * np.exp(-((t - 14.5) / 1) ** 2)
        + 2 * np.random.randn(n)
    ).clip(0, 100)
    return t, glucose, hydration, stress, energy


t, glucose, hydration, stress, energy = simulate_day(mode=sim_day)
hours = t

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "⌚ Wearable UI",
    "📡 Biometrics",
    "🧠 Predictions",
    "🗺️ User Journey",
    "🏭 Kitchen Network",
    "📈 Flywheel",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — WEARABLE UI
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("⌚ Nourish Band — Live Biometric Watch Face (3D)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🩸 Blood Glucose", "4.8 mmol/L", delta="-0.3 (30 min)", delta_color="inverse")
    col2.metric("💧 Hydration", "62%", delta="-5% (1h)", delta_color="inverse")
    col3.metric("❤️ HRV Score", "68 ms", delta="+3")
    col4.metric("⚡ Energy Index", "54 / 100", delta="-8", delta_color="inverse")

    st.info("🍽️  **MEAL TRIGGER ACTIVE** — Blood glucose trending below 4.5 mmol/L. "
            "Nearest prep node dispatched. Estimated delivery: **18 minutes.** No action needed.")

    # 3D watch face
    theta = np.linspace(0, 2 * np.pi, 200)
    fig_w = go.Figure()

    # Outer rings
    for r, col, wid in [(1.05, NAVY, 22), (0.98, "#1A3A5C", 10)]:
        fig_w.add_trace(go.Scatter3d(
            x=r * np.cos(theta), y=r * np.sin(theta), z=np.zeros_like(theta),
            mode="lines", line=dict(color=col, width=wid), showlegend=False,
        ))

    # Tick marks
    for i in range(60):
        ang = 2 * np.pi * i / 60
        r_in = 0.82 if i % 5 == 0 else 0.86
        fig_w.add_trace(go.Scatter3d(
            x=[r_in * np.cos(ang), 0.96 * np.cos(ang)],
            y=[r_in * np.sin(ang), 0.96 * np.sin(ang)],
            z=[0, 0], mode="lines",
            line=dict(color=GOLD if i % 5 == 0 else "#446677", width=3 if i % 5 == 0 else 1),
            showlegend=False,
        ))

    # Metric arcs
    for pct, color, radius, label in [
        (0.72, TEAL, 0.76, "Glucose 72%"),
        (0.58, SKY, 0.65, "Hydration 58%"),
        (0.33, CORAL, 0.55, "Stress 33%"),
    ]:
        arc = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi * pct, 80)
        fig_w.add_trace(go.Scatter3d(
            x=radius * np.cos(arc), y=radius * np.sin(arc),
            z=np.ones_like(arc) * 0.05, mode="lines",
            line=dict(color=color, width=10), name=label,
        ))

    # HRV waveform
    t_hrv = np.linspace(-0.45, 0.45, 120)
    y_hrv = 0.08 * np.sin(2 * np.pi * t_hrv / 0.18) * np.exp(-((t_hrv / 0.32) ** 2))
    fig_w.add_trace(go.Scatter3d(
        x=t_hrv, y=np.full_like(t_hrv, -0.60), z=0.08 + y_hrv,
        mode="lines", line=dict(color=LIME, width=3), name="HRV Wave",
    ))

    fig_w.update_layout(
        title=dict(text="NOURISH BAND — 3D Watch Face", font=dict(color=MINT, size=16), x=0.5),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor=NAVY,
            camera=dict(eye=dict(x=0, y=0, z=2.6)),
            aspectmode="cube",
        ),
        height=520,
        paper_bgcolor=NAVY,
        legend=dict(bgcolor="rgba(0,30,50,0.8)", bordercolor=TEAL, borderwidth=1,
                    font=dict(color=MINT, size=11)),
    )
    st.plotly_chart(fig_w, use_container_width=True)

    st.markdown(
        "**Legend:**  "
        "🔵 *Teal arc* = Blood glucose (72% of safe range) &nbsp;|&nbsp; "
        "🔵 *Blue arc* = Hydration (58%) &nbsp;|&nbsp; "
        "🔴 *Coral arc* = Stress (33%) &nbsp;|&nbsp; "
        "🟢 *Green wave* = Live HRV pulse"
    )


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — BIOMETRICS
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("📡 24-Hour Biometric Data Streams")

    step = 3
    ts, gs, hs, ss, es = t[::step], glucose[::step], hydration[::step], stress[::step], energy[::step]

    fig2 = make_subplots(rows=2, cols=2,
        subplot_titles=["🩸 Blood Glucose (mmol/L)", "💧 Hydration (%)",
                        "❤️ Stress Score (%)", "⚡ Energy Index"])

    for (row, col, data, color, name, threshold, th_label) in [
        (1, 1, gs, TEAL, "Glucose", 4.2, "Trigger 4.2"),
        (1, 2, hs, SKY, "Hydration", 60, "Min 60%"),
        (2, 1, ss, CORAL, "Stress", 55, "High >55"),
        (2, 2, es, LIME, "Energy", 35, "Low <35"),
    ]:
        fig2.add_trace(go.Scatter(
            x=ts, y=data, mode="lines", line=dict(color=color, width=2.5),
            fill="tozeroy", fillcolor=color.replace("#", "rgba(") + ",0.08)",
            name=name,
        ), row=row, col=col)
        fig2.add_hline(y=threshold, line_dash="dash", line_color="#888",
                       annotation_text=th_label, row=row, col=col)

    # Mark triggers
    triggers = np.where(np.diff((gs < 4.2).astype(int)) > 0)[0]
    for idx in triggers[:5]:
        fig2.add_vline(x=ts[idx], line_dash="dot", line_color=GOLD, row=1, col=1)

    fig2.update_layout(height=540, paper_bgcolor="white", font=dict(color=NAVY),
                       showlegend=False,
                       title=dict(text="📡 Biometric Streams — Automatic Meal Triggers (gold lines)",
                                  font=dict(color=NAVY, size=15), x=0.5))
    fig2.update_xaxes(title_text="Hour of Day")
    st.plotly_chart(fig2, use_container_width=True)

    # 3D state space
    st.subheader("Biometric State Space (3D)")
    fig2b = go.Figure()
    fig2b.add_trace(go.Scatter3d(
        x=gs, y=hs, z=ss, mode="lines+markers",
        line=dict(color=es, colorscale="Viridis", width=4),
        marker=dict(size=2, color=es, colorscale="Viridis", opacity=0.6,
                    colorbar=dict(title="Energy", x=1.02)),
        name="Bio State",
    ))
    if len(triggers) > 0:
        fig2b.add_trace(go.Scatter3d(
            x=gs[triggers], y=hs[triggers], z=ss[triggers],
            mode="markers", name="Meal Trigger",
            marker=dict(size=10, color=GOLD, symbol="diamond",
                        line=dict(color=CORAL, width=2)),
        ))
    fig2b.update_layout(height=520, paper_bgcolor="white", font=dict(color=NAVY),
                         scene=dict(
                             xaxis=dict(title="Glucose (mmol/L)", backgroundcolor=LIGHT),
                             yaxis=dict(title="Hydration (%)", backgroundcolor=LIGHT),
                             zaxis=dict(title="Stress (%)", backgroundcolor=LIGHT),
                             bgcolor=LIGHT,
                             camera=dict(eye=dict(x=1.8, y=-2, z=1.4)),
                         ),
                         title=dict(text="3D Biometric State Space (colour = Energy level)",
                                    font=dict(color=NAVY), x=0.5))
    st.plotly_chart(fig2b, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — PREDICTIONS
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("🧠 Predictive Analytics — 30-Minute Glucose Forecast")

    curr_g = np.linspace(3.5, 7.5, 50)
    t_meal = np.linspace(0, 5, 50)
    CG, TM = np.meshgrid(curr_g, t_meal)
    Z = np.clip(CG - 0.25 * TM - 0.05 * TM ** 2 + 0.02 * (CG - 5.5) * TM, 2.8, 8.5)

    fig3 = go.Figure()
    fig3.add_trace(go.Surface(
        x=CG, y=TM, z=Z,
        colorscale=[[0, CORAL], [0.25, "#FF9966"], [0.5, GOLD], [0.75, LIME], [1, TEAL]],
        cmin=3.0, cmax=7.5, opacity=0.88,
        colorbar=dict(title=dict(text="Predicted Glucose<br>(mmol/L)", font=dict(color=NAVY))),
        hovertemplate=(
            "Current Glucose: %{x:.1f} mmol/L<br>"
            "Hours since meal: %{y:.1f}h<br>"
            "Predicted in 30 min: %{z:.2f} mmol/L<extra></extra>"
        ),
        contours=dict(z=dict(show=True, start=3, end=7.5, size=0.5, color="white", width=1)),
    ))

    z_plane = np.full_like(CG, 4.0)
    fig3.add_trace(go.Surface(
        x=CG, y=TM, z=z_plane,
        colorscale=[[0, "rgba(232,71,42,0.3)"], [1, "rgba(232,71,42,0.3)"]],
        showscale=False, opacity=0.35, name="Danger Threshold",
    ))

    fig3.add_trace(go.Scatter3d(
        x=[4.6, 4.3, 5.0, 4.1], y=[3.2, 4.1, 2.8, 4.8], z=[3.8, 3.4, 4.1, 2.9],
        mode="markers+text",
        marker=dict(size=12, color=GOLD, symbol="diamond", line=dict(color=NAVY, width=2)),
        text=["Breakfast", "Lunch", "Snack", "Dinner"],
        textfont=dict(color=NAVY, size=10), textposition="top center",
        name="AI Trigger Points",
    ))

    fig3.update_layout(
        height=600, paper_bgcolor="white", font=dict(color=NAVY),
        title=dict(text="🧠 Predictive Glucose Surface — Red Zone = Meal Trigger",
                   font=dict(color=NAVY, size=15), x=0.5),
        scene=dict(
            xaxis=dict(title="Current Glucose (mmol/L)", backgroundcolor=LIGHT),
            yaxis=dict(title="Hours Since Last Meal", backgroundcolor=LIGHT),
            zaxis=dict(title="Predicted Glucose in 30 min", backgroundcolor=LIGHT),
            bgcolor=LIGHT,
            camera=dict(eye=dict(x=1.8, y=-2.0, z=1.4)),
        ),
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(
        "🔴 **Red plane** = Hypoglycaemic danger threshold (4.0 mmol/L).  \n"
        "When the predicted trajectory falls below this plane, the AI triggers a meal **automatically**.  \n"
        "🟡 **Gold diamonds** = Real-world trigger moments from a typical user day."
    )


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — USER JOURNEY
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("🗺️ Nourish — Full Autonomous User Journey (3D Flow)")

    nodes = [
        (0, 0, 0, "💪 Body", NAVY, 20),
        (-2, 1, 1, "🩸 Glucose", TEAL, 16),
        (-2, 0, 1, "💧 Hydration", SKY, 16),
        (-2, -1, 1, "❤️ HRV", LIME, 16),
        (-2, -2, 1, "🌡️ Temp/GSR", PURPLE, 14),
        (0, -0.5, 2, "🧠 Nourish AI", GOLD, 28),
        (0, 1.5, 2, "🕐 Circadian", "#8B6914", 18),
        (0, 3.0, 2, "😌 Mood", CORAL, 18),
        (2, 0.5, 3, "🍱 Meal Decision", TEAL, 22),
        (4, 1.5, 3, "🏭 Prep Node", LIME, 18),
        (4, -0.5, 3, "🛒 Partner", PURPLE, 16),
        (6, 0.5, 4, "🚴 Delivery", NAVY, 18),
        (8, 0.5, 4, "👤 User Eats", GOLD, 24),
        (8, -1.5, 5, "📊 Insights", TEAL, 18),
        (6, -2.5, 5, "🔄 Richer Data", LIME, 16),
        (4, -2.5, 5, "⚡ AI Smarter", GOLD, 16),
    ]

    edges = [
        (0,1),(0,2),(0,3),(0,4),
        (1,5),(2,5),(3,5),(4,5),
        (6,5),(7,5),
        (5,8),(8,9),(8,10),
        (9,11),(10,11),(11,12),
        (12,13),(13,14),(14,15),(15,5),
    ]

    fig4 = go.Figure()
    for idx, (i, j) in enumerate(edges):
        is_loop = idx >= 16
        fig4.add_trace(go.Scatter3d(
            x=[nodes[i][0], nodes[j][0], None],
            y=[nodes[i][1], nodes[j][1], None],
            z=[nodes[i][2], nodes[j][2], None],
            mode="lines",
            line=dict(color=GOLD if is_loop else TEAL,
                      width=4 if not is_loop else 3,
                      dash="dash" if is_loop else "solid"),
            showlegend=False,
        ))

    fig4.add_trace(go.Scatter3d(
        x=[n[0] for n in nodes], y=[n[1] for n in nodes], z=[n[2] for n in nodes],
        mode="markers+text",
        marker=dict(
            size=[n[5] for n in nodes],
            color=[n[4] for n in nodes],
            line=dict(color="white", width=2), opacity=0.95,
        ),
        text=[n[3] for n in nodes],
        textfont=dict(size=9, color=NAVY),
        textposition="middle center",
        name="Journey Nodes",
        hovertemplate="%{text}<extra></extra>",
    ))

    fig4.update_layout(
        height=620, paper_bgcolor="white", font=dict(color=NAVY), showlegend=False,
        title=dict(text="🗺️ Complete Autonomous Journey — Zero User Input Required",
                   font=dict(color=NAVY, size=15), x=0.5),
        scene=dict(
            xaxis=dict(title="Journey Stage", backgroundcolor=LIGHT),
            yaxis=dict(visible=False),
            zaxis=dict(title="Layer", backgroundcolor=LIGHT),
            bgcolor=LIGHT,
            camera=dict(eye=dict(x=2.0, y=-2.5, z=1.6)),
        ),
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown(
        "🔵 **Teal lines** = Primary signal/delivery flow  \n"
        "🟡 **Gold dashed** = Compounding data loop (health improves → AI learns → loop repeats)"
    )


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — KITCHEN NETWORK
# ════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("🏭 Hyperlocal Prep Node Network")

    node_x = np.random.uniform(0, 12, n_nodes)
    node_y = np.random.uniform(0, 12, n_nodes)
    node_load = np.random.randint(2, 9, n_nodes)

    n_users = 40
    user_x = np.random.uniform(0.5, 11.5, n_users)
    user_y = np.random.uniform(0.5, 11.5, n_users)

    fig5 = go.Figure()

    # Coverage circles
    theta_c = np.linspace(0, 2 * np.pi, 50)
    for i in range(n_nodes):
        cx = node_x[i] + 2.0 * np.cos(theta_c)
        cy = node_y[i] + 2.0 * np.sin(theta_c)
        fig5.add_trace(go.Scatter3d(
            x=cx, y=cy, z=np.zeros_like(theta_c) + 0.02,
            mode="lines", line=dict(color="rgba(0,168,150,0.3)", width=2),
            showlegend=False,
        ))

    # Prep nodes
    fig5.add_trace(go.Scatter3d(
        x=node_x, y=node_y, z=np.zeros(n_nodes),
        mode="markers+text",
        marker=dict(
            size=10 + node_load * 1.2,
            color=node_load, colorscale="RdYlGn_r", cmin=2, cmax=9,
            line=dict(color=NAVY, width=2), opacity=0.9,
            colorbar=dict(title=dict(text="Active Orders", font=dict(color=NAVY))),
        ),
        text=[f"Node {i+1}" for i in range(n_nodes)],
        textfont=dict(size=8, color=NAVY),
        textposition="top center",
        name="🏭 Prep Nodes",
    ))

    # Users
    fig5.add_trace(go.Scatter3d(
        x=user_x, y=user_y, z=np.zeros(n_users) + 0.1,
        mode="markers",
        marker=dict(size=5, color=SKY, opacity=0.7, line=dict(color=NAVY, width=1)),
        name="👤 Users",
    ))

    # Demand surface
    xi, yi = np.mgrid[0:12:25j, 0:12:25j]
    density = np.zeros_like(xi)
    for ux, uy in zip(user_x, user_y):
        density += np.exp(-((xi - ux) ** 2 + (yi - uy) ** 2) / 3.0)
    density = density / density.max() * 0.8

    fig5.add_trace(go.Surface(
        x=xi, y=yi, z=density - 0.05,
        colorscale=[[0, "rgba(240,249,247,0)"], [1, "rgba(0,168,150,0.4)"]],
        showscale=False, opacity=0.5, name="Demand Density",
    ))

    fig5.update_layout(
        height=620, paper_bgcolor="white", font=dict(color=NAVY),
        title=dict(text="🏭 Kitchen Network — Prep Nodes + User Demand Heatmap",
                   font=dict(color=NAVY, size=15), x=0.5),
        scene=dict(
            xaxis=dict(title="City East-West (km)", backgroundcolor=LIGHT),
            yaxis=dict(title="City North-South (km)", backgroundcolor=LIGHT),
            zaxis=dict(title="", showticklabels=False),
            bgcolor=LIGHT,
            camera=dict(eye=dict(x=1.5, y=-2.0, z=2.0)),
        ),
        legend=dict(x=0.02, y=0.98),
    )
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown(
        "🟢 **Large circles** = Prep nodes (size = load, colour = red→busy, green→free)  \n"
        "🔵 **Small dots** = Active users with live triggers  \n"
        "🌊 **Teal surface** = Demand density — node placement optimised for coverage"
    )


# ════════════════════════════════════════════════════════════════════════════
# TAB 6 — FLYWHEEL
# ════════════════════════════════════════════════════════════════════════════
with tab6:
    st.subheader("📈 Compounding Personalisation Flywheel — 24-Month Simulation")

    months = np.linspace(0, 24, 200)
    accuracy = 96 - 31 * np.exp(-0.18 * months)
    health   = 45 + 40 * (1 - np.exp(-0.12 * months))
    data_pts = 500 + 2200 * (1 - np.exp(-0.09 * months))

    current_idx = int(user_month / 24 * 199)

    col1, col2, col3 = st.columns(3)
    col1.metric("🎯 AI Accuracy",   f"{accuracy[current_idx]:.1f}%",    delta=f"+{accuracy[current_idx]-65:.1f}% vs start")
    col2.metric("💪 Health Score",  f"{health[current_idx]:.1f}/100",   delta=f"+{health[current_idx]-45:.1f} vs start")
    col3.metric("📊 Data Points",   f"{int(data_pts[current_idx]):,}",  delta=f"+{int(data_pts[current_idx]-500):,} vs start")

    st.info(
        f"📅 At **Month {user_month}**: AI accuracy = **{accuracy[current_idx]:.1f}%** · "
        f"Health score = **{health[current_idx]:.0f}/100**. "
        "A new competitor starting today starts at 65% accuracy — you're already at "
        f"**{accuracy[current_idx]:.1f}%** and pulling away."
    )

    fig6 = make_subplots(rows=1, cols=3,
        subplot_titles=["AI Prediction Accuracy (%)", "User Health Score", "Biometric Data Points"])

    for col, y, color, name in [
        (1, accuracy, TEAL, "Accuracy"),
        (2, health,   LIME, "Health"),
        (3, data_pts, GOLD, "Data"),
    ]:
        fig6.add_trace(go.Scatter(
            x=months, y=y, mode="lines", line=dict(color=color, width=3),
            fill="tozeroy", fillcolor=color + "22", name=name,
        ), row=1, col=col)
        fig6.add_trace(go.Scatter(
            x=[months[current_idx]], y=[y[current_idx]], mode="markers",
            marker=dict(size=14, color=CORAL, symbol="diamond",
                        line=dict(color=NAVY, width=2)),
            name=f"Month {user_month}", showlegend=(col == 1),
        ), row=1, col=col)

    fig6.update_layout(
        height=380, paper_bgcolor="white", font=dict(color=NAVY),
        showlegend=True, legend=dict(x=0.98, y=0.98, xanchor="right"),
    )
    fig6.update_xaxes(title_text="Months")
    st.plotly_chart(fig6, use_container_width=True)

    # 3D flywheel spiral
    st.subheader("3D Compounding Flywheel")
    theta_s = np.linspace(0, 6 * np.pi, 200)
    r_s     = 0.3 + 0.7 * (months / 24)
    sx = r_s * np.cos(theta_s)
    sy = r_s * np.sin(theta_s)
    sz = months / 24

    fig6b = go.Figure()
    fig6b.add_trace(go.Scatter3d(
        x=sx, y=sy, z=sz, mode="lines",
        line=dict(color=accuracy, colorscale="RdYlGn", width=7, cmin=65, cmax=96,
                  colorbar=dict(title=dict(text="AI Accuracy (%)", font=dict(color=NAVY)), x=1.02)),
        name="Flywheel",
    ))

    milestones = [(0.04, "Month 1"), (0.12, "Month 3"), (0.25, "Month 6"),
                  (0.50, "Month 12"), (1.0, "Month 24")]
    for frac, label in milestones:
        idx = int(frac * 199)
        fig6b.add_trace(go.Scatter3d(
            x=[sx[idx]], y=[sy[idx]], z=[sz[idx]], mode="markers+text",
            marker=dict(size=12, color=GOLD, symbol="diamond", line=dict(color=NAVY, width=2)),
            text=[label], textfont=dict(size=9, color=NAVY), textposition="top center",
            showlegend=False,
        ))

    fig6b.update_layout(
        height=520, paper_bgcolor="white", font=dict(color=NAVY),
        title=dict(text="The compounding spiral — each loop = more data, smarter AI, better health",
                   font=dict(color=NAVY, size=14), x=0.5),
        scene=dict(
            xaxis=dict(showticklabels=False, backgroundcolor=LIGHT),
            yaxis=dict(showticklabels=False, backgroundcolor=LIGHT),
            zaxis=dict(title="Time (0→Month 24)", backgroundcolor=LIGHT),
            bgcolor=LIGHT,
            camera=dict(eye=dict(x=1.8, y=-2.2, z=1.4)),
        ),
        showlegend=False,
    )
    st.plotly_chart(fig6b, use_container_width=True)

    st.success(
        "**The data moat:** A competitor entering at Month 24 starts at 65% AI accuracy "
        f"while your system is at {accuracy[-1]:.1f}%. They can copy the app. "
        "They cannot copy your biometric history. **The moat is permanent.**"
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    '<p style="text-align:center;color:#888;font-size:0.85rem;">'
    "Nourish · SP Jain GMBA · Blue Ocean Strategy · Dr. Umesh Kothari · 2026 &nbsp;|&nbsp; "
    "Built with Plotly + Streamlit</p>",
    unsafe_allow_html=True,
)
