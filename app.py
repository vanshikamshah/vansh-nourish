"""
Nourish — BOS Dashboard  |  Streamlit Cloud-compatible
SP Jain GMBA · Blue Ocean Strategy · Dr. Umesh Kothari
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nourish — BOS Dashboard",
    page_icon="🌿",
    layout="wide",
)

# ── Colour palette ────────────────────────────────────────────────────────────
NAVY   = "#0B1D3A"
TEAL   = "#00A896"
CORAL  = "#E8472A"
GOLD   = "#F7B731"
LIME   = "#52B788"
SKY    = "#3A86FF"
PURPLE = "#7B2D8B"
MINT   = "#D0F0EB"
LIGHT  = "#F0F9F7"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/organic-food.png", width=72)
    st.title("🌿 Nourish")
    st.caption("Autonomous Nutrition Platform")
    st.divider()
    seed       = st.slider("Random seed",        0, 99,  42)
    n_nodes    = st.slider("Kitchen nodes",       5, 30,  18)
    user_month = st.slider("Subscription month",  1, 24,   6)
    day_type   = st.selectbox("Day type", ["Workday", "Weekend", "High-Stress"])
    st.divider()
    st.caption("SP Jain GMBA · Dubai 2026")

# ── Simulate biometrics ───────────────────────────────────────────────────────
@st.cache_data
def simulate_day(seed=42, mode="Workday", n=1440):
    rng = np.random.default_rng(seed)
    t   = np.linspace(0, 24, n)
    stress_amp = 1.4 if mode == "High-Stress" else (0.7 if mode == "Weekend" else 1.0)
    g = (4.8 + 0.4 * np.sin(2 * np.pi * t / 24 - 1)
         + 1.2 * np.exp(-((t - 8.5)  / 0.4) ** 2)
         + 0.9 * np.exp(-((t - 13.0) / 0.4) ** 2)
         + 0.7 * np.exp(-((t - 19.5) / 0.4) ** 2)
         + 0.08 * rng.standard_normal(n))
    h = np.clip(
        85 - 0.8*t
        + 8 * np.exp(-((t - 9)  / 0.3) ** 2)
        + 6 * np.exp(-((t - 14) / 0.3) ** 2)
        + 5 * np.exp(-((t - 20) / 0.3) ** 2)
        + 1.5 * rng.standard_normal(n),
        40, 100)
    s = np.clip(
        stress_amp * (20 + 15 * np.exp(-((t - 11) / 2)  ** 2)
                      + 12 * np.exp(-((t - 16) / 1.5) ** 2))
        + 3 * rng.standard_normal(n),
        5, 80)
    e = np.clip(
        50 + 20 * np.sin(2 * np.pi * t / 24 - np.pi / 4)
        - 15 * np.exp(-((t - 14.5) / 1) ** 2)
        + 2 * rng.standard_normal(n),
        0, 100)
    return t, g, h, s, e

t, glucose, hydration, stress, energy = simulate_day(seed, day_type)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs(["⌚ Wearable UI", "📡 Biometrics", "🧠 Predictions",
                "🗺️ Journey", "🏭 Kitchen Network", "📈 Flywheel"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — 3D Watch Face
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.subheader("⌚  The Nourish Band — 3D Watch Face")
    st.caption("Rotate · Zoom · Hover — real-time biometric arcs rendered in 3D")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Blood Glucose", f"{glucose[720]:.2f} mmol/L", "-0.3 ↓")
    col2.metric("Hydration",     f"{hydration[720]:.0f}%",      "+5% ↑")
    col3.metric("Stress",        f"{stress[720]:.0f}%",         "-8% ↓")
    col4.metric("Energy",        f"{energy[720]:.0f}/100",      "+12 ↑")

    theta = np.linspace(0, 2 * np.pi, 200)
    fig = go.Figure()

    # Outer ring
    for r, c, w in [(1.05, NAVY, 22), (0.98, "#1A3A5C", 10)]:
        fig.add_trace(go.Scatter3d(
            x=r*np.cos(theta), y=r*np.sin(theta), z=np.zeros(200),
            mode='lines', line=dict(color=c, width=w), showlegend=False))

    # Tick marks
    for i in range(60):
        a  = 2 * np.pi * i / 60
        ri = 0.82 if i % 5 == 0 else 0.88
        fig.add_trace(go.Scatter3d(
            x=[ri*np.cos(a), 0.96*np.cos(a)],
            y=[ri*np.sin(a), 0.96*np.sin(a)],
            z=[0, 0], mode='lines',
            line=dict(color=GOLD if i % 5 == 0 else "#446677",
                      width=3 if i % 5 == 0 else 1),
            showlegend=False))

    # Biometric arcs
    g_pct = np.clip((glucose[720] - 3.0) / (7.5 - 3.0), 0, 1)
    h_pct = hydration[720] / 100
    s_pct = stress[720]    / 100
    for pct, col, rad, nm in [
        (g_pct, TEAL,   0.76, f"🩸 Glucose {g_pct*100:.0f}%"),
        (h_pct, SKY,    0.65, f"💧 Hydration {h_pct*100:.0f}%"),
        (1-s_pct, LIME, 0.55, f"❤️ Calm {(1-s_pct)*100:.0f}%"),
    ]:
        arc = np.linspace(np.pi/2, np.pi/2 + 2*np.pi*pct, 80)
        fig.add_trace(go.Scatter3d(
            x=rad*np.cos(arc), y=rad*np.sin(arc), z=np.ones(80)*0.05,
            mode='lines', line=dict(color=col, width=10), name=nm))

    # HRV waveform
    th2 = np.linspace(-0.45, 0.45, 120)
    yh  = 0.08 * np.sin(2*np.pi*th2/0.18) * np.exp(-(th2/0.32)**2)
    fig.add_trace(go.Scatter3d(
        x=th2, y=np.full(120, -0.60), z=0.08 + yh,
        mode='lines', line=dict(color=LIME, width=3), name="🟢 HRV"))

    # Centre text markers
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0.05], z=[0.25], mode='text',
        text=[f"<b>{glucose[720]:.2f} mmol/L</b>"],
        textfont=dict(size=13, color=TEAL), showlegend=False))
    fig.add_trace(go.Scatter3d(
        x=[0], y=[-0.32], z=[0.18], mode='text',
        text=["🍽  MEAL IN ~18 MIN"],
        textfont=dict(size=10, color=GOLD), showlegend=False))

    fig.update_layout(
        height=560,
        paper_bgcolor=NAVY,
        font=dict(color=MINT),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor=NAVY,
            camera=dict(eye=dict(x=0, y=0, z=2.5)),
            aspectmode='cube'),
        legend=dict(bgcolor="rgba(0,20,40,0.85)", bordercolor=TEAL, borderwidth=1,
                    font=dict(color=MINT, size=11), x=0.75, y=0.92),
        margin=dict(l=0, r=0, t=30, b=0))

    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Biometric Streams
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.subheader("📡  Real-Time Biometric Streams")
    st.caption("24-hour continuous sampling · gold markers = auto meal triggers")

    step = 4
    ts, gs, hs, ss, es = t[::step], glucose[::step], hydration[::step], stress[::step], energy[::step]
    trig_idx = np.where((gs < 4.5) | (es < 32))[0]

    fig2 = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "scatter3d"}, {"type": "scatter3d"}]],
        subplot_titles=["Glucose × Hydration × Time", "Energy × Stress State Space"])

    fig2.add_trace(go.Scatter3d(
        x=ts, y=gs, z=hs, mode='lines+markers',
        line=dict(color=ss, colorscale='RdYlGn_r', width=4),
        marker=dict(size=2, color=ss, colorscale='RdYlGn_r', opacity=0.5,
                    colorbar=dict(title="Stress %", x=0.45, len=0.7)),
        name='Bio Stream'), row=1, col=1)

    if len(trig_idx):
        t_idx = trig_idx[::max(1, len(trig_idx)//6)][:6]
        fig2.add_trace(go.Scatter3d(
            x=ts[t_idx], y=gs[t_idx], z=hs[t_idx], mode='markers',
            marker=dict(size=10, color=GOLD, symbol='diamond',
                        line=dict(color=CORAL, width=2)),
            name='🍽 Meal Trigger'), row=1, col=1)

    fig2.add_trace(go.Scatter3d(
        x=es, y=ss, z=gs, mode='markers',
        marker=dict(size=3, color=ts, colorscale='Viridis', opacity=0.6,
                    colorbar=dict(title="Hour", x=1.02, len=0.7)),
        name='State Space'), row=1, col=2)

    scene_common = dict(
        xaxis=dict(backgroundcolor=LIGHT),
        yaxis=dict(backgroundcolor=LIGHT),
        zaxis=dict(backgroundcolor=LIGHT),
        bgcolor=LIGHT,
        camera=dict(eye=dict(x=1.8, y=-1.8, z=1.2)))

    fig2.update_layout(
        height=560, paper_bgcolor='white', font=dict(color=NAVY),
        scene=dict(xaxis_title='Hour', yaxis_title='Glucose (mmol/L)',
                   zaxis_title='Hydration (%)', **{k: v for k, v in scene_common.items() if k != 'xaxis'}),
        scene2=dict(xaxis_title='Energy', yaxis_title='Stress (%)',
                    zaxis_title='Glucose (mmol/L)', **{k: v for k, v in scene_common.items() if k != 'xaxis'}),
        margin=dict(l=0, r=0, t=40, b=0))

    st.plotly_chart(fig2, use_container_width=True)
    st.info(f"**{len(trig_idx)} automatic meal triggers** detected today — zero user input required.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Predictive Surface
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.subheader("🧠  Predictive Analytics — 30-Min Glucose Forecast")
    st.caption("When the forecast crosses 4.0 mmol/L, Nourish fires a meal trigger automatically")

    cg = np.linspace(3.5, 7.5, 50)
    tm = np.linspace(0, 5,   50)
    CG, TM = np.meshgrid(cg, tm)
    Z = np.clip(CG - 0.25*TM - 0.05*TM**2 + 0.02*(CG - 5.5)*TM, 2.8, 8.5)

    fig3 = go.Figure()
    fig3.add_trace(go.Surface(
        x=CG, y=TM, z=Z,
        colorscale=[[0, CORAL], [0.25, "#FF9966"], [0.5, GOLD], [0.75, LIME], [1, TEAL]],
        cmin=3.0, cmax=7.5, opacity=0.88,
        colorbar=dict(title=dict(text="Predicted<br>Glucose", font=dict(color=NAVY))),
        hovertemplate="Current: %{x:.1f} mmol/L<br>Hours since meal: %{y:.1f}h<br>Predicted: %{z:.2f}<extra></extra>",
        contours=dict(z=dict(show=True, start=3, end=7.5, size=0.5, color='white', width=1))))

    # Danger plane
    fig3.add_trace(go.Surface(
        x=CG, y=TM, z=np.full_like(CG, 4.0),
        colorscale=[[0, "rgba(232,71,42,0.25)"], [1, "rgba(232,71,42,0.25)"]],
        showscale=False, opacity=0.35, name="⚠️ Danger 4.0"))

    # Trigger points
    fig3.add_trace(go.Scatter3d(
        x=[4.6, 4.3, 5.0, 4.1], y=[3.2, 4.1, 2.8, 4.8], z=[3.8, 3.4, 4.1, 2.9],
        mode='markers+text',
        marker=dict(size=12, color=GOLD, symbol='diamond', line=dict(color=NAVY, width=2)),
        text=['Breakfast', 'Lunch', 'Snack', 'Dinner'],
        textfont=dict(color=NAVY, size=10), textposition='top center',
        name='AI Trigger Points'))

    fig3.update_layout(
        height=580, paper_bgcolor='white', font=dict(color=NAVY),
        scene=dict(
            xaxis=dict(title='Current Glucose (mmol/L)', backgroundcolor=LIGHT),
            yaxis=dict(title='Hours Since Last Meal', backgroundcolor=LIGHT),
            zaxis=dict(title='Predicted Glucose in 30 min', backgroundcolor=LIGHT),
            bgcolor=LIGHT,
            camera=dict(eye=dict(x=1.8, y=-2.0, z=1.4))),
        margin=dict(l=0, r=0, t=30, b=0))

    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — User Journey Flow
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.subheader("🗺️  Autonomous User Journey — 3D Flow Network")
    st.caption("From biometric signal to meal delivery — zero user input at any stage")

    nodes = [
        (0,  0,   0,  "💪 Body",       NAVY,   20),
        (-2, 1,   1,  "🩸 Glucose",    TEAL,   16),
        (-2, 0,   1,  "💧 Hydration",  SKY,    16),
        (-2, -1,  1,  "❤️ HRV",        LIME,   16),
        (-2, -2,  1,  "🌡️ Temp",       PURPLE, 14),
        (0,  -0.5,2,  "🧠 AI Engine",  GOLD,   30),
        (0,  1.5, 2,  "🕐 Circadian",  "#8B6914", 18),
        (0,  3.0, 2,  "😌 Mood",       CORAL,  18),
        (2,  0.5, 3,  "🍱 Decision",   TEAL,   22),
        (4,  1.5, 3,  "🏭 Prep Node",  LIME,   18),
        (4,  -0.5,3,  "🛒 Partner",    PURPLE, 16),
        (6,  0.5, 4,  "🚴 Delivery",   NAVY,   18),
        (8,  0.5, 4,  "👤 User Eats",  GOLD,   26),
        (8,  -1.5,5,  "📊 Insights",   TEAL,   18),
        (6,  -2.5,5,  "🔄 Richer AI",  LIME,   16),
        (4,  -2.5,5,  "⚡ Smarter",    GOLD,   16),
    ]
    edges_main = [(0,1),(0,2),(0,3),(0,4),(1,5),(2,5),(3,5),(4,5),(6,5),(7,5),
                  (5,8),(8,9),(8,10),(9,11),(10,11),(11,12),(12,13)]
    edges_loop = [(13,14),(14,15),(15,5)]

    fig4 = go.Figure()
    for i, j in edges_main:
        fig4.add_trace(go.Scatter3d(
            x=[nodes[i][0], nodes[j][0], None],
            y=[nodes[i][1], nodes[j][1], None],
            z=[nodes[i][2], nodes[j][2], None],
            mode='lines', line=dict(color=TEAL, width=4), showlegend=False))
    for i, j in edges_loop:
        fig4.add_trace(go.Scatter3d(
            x=[nodes[i][0], nodes[j][0], None],
            y=[nodes[i][1], nodes[j][1], None],
            z=[nodes[i][2], nodes[j][2], None],
            mode='lines', line=dict(color=GOLD, width=3), showlegend=False))

    fig4.add_trace(go.Scatter3d(
        x=[n[0] for n in nodes], y=[n[1] for n in nodes], z=[n[2] for n in nodes],
        mode='markers+text',
        marker=dict(size=[n[5] for n in nodes], color=[n[4] for n in nodes],
                    line=dict(color='white', width=2), opacity=0.95),
        text=[n[3] for n in nodes],
        textfont=dict(size=9, color=NAVY),
        textposition='middle center', name='Nodes',
        hovertemplate="%{text}<extra></extra>"))

    fig4.update_layout(
        height=600, paper_bgcolor='white', font=dict(color=NAVY), showlegend=False,
        scene=dict(
            xaxis=dict(title='Journey Stage ▶', backgroundcolor=LIGHT),
            yaxis=dict(visible=False),
            zaxis=dict(title='System Layer', backgroundcolor=LIGHT),
            bgcolor=LIGHT,
            camera=dict(eye=dict(x=2.0, y=-2.5, z=1.6))),
        margin=dict(l=0, r=0, t=30, b=0))

    st.plotly_chart(fig4, use_container_width=True)
    col1, col2 = st.columns(2)
    col1.info("🔵 **Teal lines** = body → AI → kitchen → user")
    col2.warning("🟡 **Gold lines** = data flywheel — AI gets smarter every meal")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — Kitchen Network
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.subheader("🏭  Hyperlocal Kitchen Network")
    st.caption("Proprietary prep nodes — fresh, nutritionally-precise, 15-min cook time")

    rng2 = np.random.default_rng(seed + 10)
    nx  = rng2.uniform(0, 12, n_nodes)
    ny  = rng2.uniform(0, 12, n_nodes)
    nld = rng2.integers(2, 9, n_nodes)
    n_u = 40
    ux  = rng2.uniform(0.5, 11.5, n_u)
    uy  = rng2.uniform(0.5, 11.5, n_u)

    fig5 = go.Figure()

    # Coverage rings
    theta_c = np.linspace(0, 2*np.pi, 50)
    for i in range(n_nodes):
        fig5.add_trace(go.Scatter3d(
            x=nx[i] + 2.0*np.cos(theta_c),
            y=ny[i] + 2.0*np.sin(theta_c),
            z=np.zeros(50) + 0.02,
            mode='lines', line=dict(color="rgba(0,168,150,0.3)", width=2),
            showlegend=False))

    # Demand surface
    xi6, yi6 = np.mgrid[0:12:25j, 0:12:25j]
    d6 = np.zeros_like(xi6)
    for uxx, uyy in zip(ux, uy):
        d6 += np.exp(-((xi6 - uxx)**2 + (yi6 - uyy)**2) / 3.0)
    d6 = d6 / d6.max() * 0.8
    fig5.add_trace(go.Surface(
        x=xi6, y=yi6, z=d6 - 0.05,
        colorscale=[[0, "rgba(240,249,247,0)"], [1, "rgba(0,168,150,0.4)"]],
        showscale=False, opacity=0.5, name='Demand Heat'))

    # Prep nodes
    fig5.add_trace(go.Scatter3d(
        x=nx, y=ny, z=np.zeros(n_nodes),
        mode='markers+text',
        marker=dict(size=10 + nld*1.2, color=nld,
                    colorscale='RdYlGn_r', cmin=2, cmax=9,
                    line=dict(color=NAVY, width=2), opacity=0.9,
                    colorbar=dict(title=dict(text="Orders", font=dict(color=NAVY)))),
        text=[f"N{i+1}" for i in range(n_nodes)],
        textfont=dict(size=8, color=NAVY), textposition='top center',
        name='🏭 Prep Nodes'))

    # Users
    fig5.add_trace(go.Scatter3d(
        x=ux, y=uy, z=np.zeros(n_u) + 0.1, mode='markers',
        marker=dict(size=5, color=SKY, opacity=0.7, line=dict(color=NAVY, width=1)),
        name='👤 Users'))

    fig5.update_layout(
        height=580, paper_bgcolor='white', font=dict(color=NAVY),
        scene=dict(
            xaxis=dict(title='City E-W (km)', backgroundcolor=LIGHT),
            yaxis=dict(title='City N-S (km)', backgroundcolor=LIGHT),
            zaxis=dict(title='', showticklabels=False),
            bgcolor=LIGHT,
            camera=dict(eye=dict(x=1.5, y=-2.0, z=2.0))),
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.9)'),
        margin=dict(l=0, r=0, t=30, b=0))

    st.plotly_chart(fig5, use_container_width=True)
    st.metric("Active Prep Nodes", n_nodes, f"+{n_nodes-5} vs baseline")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — Compounding Flywheel
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.subheader("📈  The Compounding Personalisation Flywheel")
    st.caption("Every meal = more data = smarter AI = better health = deeper lock-in. The moat is permanent.")

    months = np.linspace(0, 24, 200)
    acc    = 96 - 31 * np.exp(-0.18 * months)
    hlth   = 45 + 40 * (1 - np.exp(-0.12 * months))
    dpts   = 500 + 2200 * (1 - np.exp(-0.09 * months))

    # 3D spiral
    theta_s = np.linspace(0, 6*np.pi, 200)
    rs = 0.3 + 0.7 * (months / 24)
    sx = rs * np.cos(theta_s)
    sy = rs * np.sin(theta_s)
    sz = months / 24

    fig6a = go.Figure()
    fig6a.add_trace(go.Scatter3d(
        x=sx, y=sy, z=sz, mode='lines',
        line=dict(color=acc, colorscale='RdYlGn', width=8, cmin=65, cmax=96,
                  colorbar=dict(title=dict(text="AI Accuracy (%)", font=dict(color=NAVY)))),
        name='Flywheel'))

    for frac, label in [(0.04,"M1"), (0.12,"M3"), (0.25,"M6"), (0.50,"M12"), (1.0,"M24")]:
        idx = int(frac * 199)
        fig6a.add_trace(go.Scatter3d(
            x=[sx[idx]], y=[sy[idx]], z=[sz[idx]], mode='markers+text',
            marker=dict(size=12, color=GOLD, symbol='diamond', line=dict(color=NAVY, width=2)),
            text=[label], textfont=dict(size=10, color=NAVY),
            textposition='top center', showlegend=False))

    fig6a.update_layout(
        height=480, paper_bgcolor='white', font=dict(color=NAVY), showlegend=False,
        scene=dict(
            xaxis=dict(showticklabels=False, backgroundcolor=LIGHT),
            yaxis=dict(showticklabels=False, backgroundcolor=LIGHT),
            zaxis=dict(title='Time: M0 → M24', backgroundcolor=LIGHT),
            bgcolor=LIGHT,
            camera=dict(eye=dict(x=1.8, y=-2.2, z=1.4))),
        margin=dict(l=0, r=0, t=30, b=0))

    st.plotly_chart(fig6a, use_container_width=True)

    # 2D trend lines
    fig6b = make_subplots(rows=1, cols=3,
                          subplot_titles=["AI Accuracy (%)", "Health Score", "Data Points"])
    cur = user_month - 1
    for col, y, color, fill_c in [
        (1, acc,  TEAL,  "rgba(0,168,150,0.13)"),
        (2, hlth, LIME,  "rgba(82,183,136,0.13)"),
        (3, dpts, GOLD,  "rgba(247,183,49,0.13)"),
    ]:
        fig6b.add_trace(go.Scatter(
            x=months, y=y, mode='lines',
            line=dict(color=color, width=2.5),
            fill='tozeroy', fillcolor=fill_c, showlegend=False), row=1, col=col)
        # current month marker
        m_idx = int((user_month / 24) * 199)
        fig6b.add_trace(go.Scatter(
            x=[months[m_idx]], y=[y[m_idx]], mode='markers',
            marker=dict(size=10, color=CORAL, line=dict(color=NAVY, width=2)),
            showlegend=False, name=f"Month {user_month}"), row=1, col=col)

    fig6b.update_layout(
        height=280, paper_bgcolor='white', font=dict(color=NAVY),
        margin=dict(l=0, r=0, t=40, b=0))
    fig6b.update_xaxes(title_text="Month")

    st.plotly_chart(fig6b, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    m_idx = int((user_month / 24) * 199)
    col1.metric("AI Accuracy",  f"{acc[m_idx]:.1f}%",  f"+{acc[m_idx]-65:.1f}pp vs Day 1")
    col2.metric("Health Score", f"{hlth[m_idx]:.0f}/100", f"+{hlth[m_idx]-45:.0f} pts")
    col3.metric("Data Points",  f"{int(dpts[m_idx]):,}", f"Month {user_month}")
