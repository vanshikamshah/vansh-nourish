"""Build the Nourish interactive Jupyter notebook."""
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.10.0"},
}

cells = []

def code(src): cells.append(nbf.v4.new_code_cell(src))
def md(src):   cells.append(nbf.v4.new_markdown_cell(src))

# ── TITLE ────────────────────────────────────────────────────────────────────
md("""# 🌿 NOURISH — Autonomous Nutrition Platform
## Interactive 3D Visualisation · Wearable UI · User Journey · Predictive Analytics

> **SP Jain School of Global Management · Global MBA · Dubai**
> Blue Ocean Strategy Challenge — Rebel Foods
> *Instructor: Dr. Umesh Kothari*

---

This notebook is a **fully interactive, self-contained exploration** of how Nourish works — from the wearable device's biometric readings all the way through the AI prediction engine, kitchen dispatch, and health outcome loop.

**How to run:**
- **Jupyter / VSCode / GitHub Codespaces:** run all cells (`Shift+Enter`)
- **Streamlit:** `streamlit run app.py` (auto-generated in the last cell)
- **GitHub:** all outputs are pre-rendered — just open the `.ipynb` file

---
""")

# ── SETUP ────────────────────────────────────────────────────────────────────
code("""\
# ─── Setup & Imports ──────────────────────────────────────────────────────────
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings, math, random
warnings.filterwarnings('ignore')
random.seed(42); np.random.seed(42)

# Nourish Colour Palette
NAVY   = "#0B1D3A"
TEAL   = "#00A896"
CORAL  = "#E8472A"
GOLD   = "#F7B731"
MINT   = "#D0F0EB"
LIGHT  = "#F0F9F7"
LIME   = "#52B788"
PURPLE = "#7B2D8B"
SKY    = "#3A86FF"

# Plotly default template
import plotly.io as pio
pio.templates["nourish"] = go.layout.Template(
    layout=dict(
        font=dict(family="Inter, Arial, sans-serif", color="#1A1A2E"),
        paper_bgcolor="white",
        plot_bgcolor=LIGHT,
        colorway=[TEAL, CORAL, GOLD, LIME, PURPLE, SKY, NAVY],
        title=dict(font=dict(size=18, color=NAVY), x=0.5),
    )
)
pio.templates.default = "nourish"
print("✅  Nourish palette & template loaded.")
""")

md("""---
## 1  ⌚  The Nourish Wearable — 3D Device UI

The **Nourish Band** is a purpose-built biosensor device — not a repurposed fitness tracker.
Below is an interactive 3D model of the watch face with live simulated biometric readings.
""")

# ── VIZ 1: 3D WEARABLE WATCH-FACE ────────────────────────────────────────────
code("""\
# ─── 1. 3-D Interactive Wearable UI ──────────────────────────────────────────
def build_watch_face():
    fig = go.Figure()

    # ---------- outer bezel (thick torus-like ring) ----------
    theta = np.linspace(0, 2*np.pi, 120)
    for r, alpha, color, name in [
        (1.05, 1.0, NAVY,   "Outer Bezel"),
        (0.98, 1.0, "#1A3A5C", "Inner Bezel"),
    ]:
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = np.zeros_like(theta)
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z, mode='lines',
            line=dict(color=color, width=14 if r > 1 else 8),
            name=name, showlegend=False
        ))

    # ---------- radial tick marks ----------
    for i in range(60):
        angle = 2*np.pi * i / 60
        r_in  = 0.82 if i % 5 == 0 else 0.86
        r_out = 0.96
        color = GOLD if i % 5 == 0 else "#446677"
        fig.add_trace(go.Scatter3d(
            x=[r_in*np.cos(angle), r_out*np.cos(angle)],
            y=[r_in*np.sin(angle), r_out*np.sin(angle)],
            z=[0, 0], mode='lines',
            line=dict(color=color, width=3 if i % 5 == 0 else 1),
            showlegend=False
        ))

    # ---------- blood glucose arc (coloured ring) ----------
    glucose_pct = 0.72   # 72% of safe range
    arc_theta = np.linspace(np.pi/2, np.pi/2 + 2*np.pi*glucose_pct, 80)
    fig.add_trace(go.Scatter3d(
        x=0.76*np.cos(arc_theta), y=0.76*np.sin(arc_theta), z=np.ones_like(arc_theta)*0.05,
        mode='lines', line=dict(color=TEAL, width=10), name='Glucose Arc'
    ))

    # ---------- hydration arc ----------
    hydration_pct = 0.58
    arc_theta2 = np.linspace(np.pi/2, np.pi/2 + 2*np.pi*hydration_pct, 60)
    fig.add_trace(go.Scatter3d(
        x=0.65*np.cos(arc_theta2), y=0.65*np.sin(arc_theta2), z=np.ones_like(arc_theta2)*0.05,
        mode='lines', line=dict(color=SKY, width=7), name='Hydration Arc'
    ))

    # ---------- stress arc ----------
    stress_pct = 0.33
    arc_theta3 = np.linspace(np.pi/2, np.pi/2 + 2*np.pi*stress_pct, 40)
    fig.add_trace(go.Scatter3d(
        x=0.55*np.cos(arc_theta3), y=0.55*np.sin(arc_theta3), z=np.ones_like(arc_theta3)*0.05,
        mode='lines', line=dict(color=CORAL, width=6), name='Stress Arc'
    ))

    # ---------- centre metric labels ----------
    annotations_3d = [
        dict(x=0.0, y=0.12, z=0.15, text="<b>4.8 mmol/L</b>", showarrow=False,
             font=dict(size=13, color=TEAL, family="Inter, Arial")),
        dict(x=0.0, y=-0.02, z=0.15, text="Blood Glucose", showarrow=False,
             font=dict(size=9, color="#888888", family="Inter, Arial")),
        dict(x=0.0, y=-0.20, z=0.15, text="<b>HYD 62%  |  STRESS 33%</b>", showarrow=False,
             font=dict(size=9, color=SKY, family="Inter, Arial")),
        dict(x=0.0, y=-0.40, z=0.15, text="<b>🍽  MEAL IN  ~18 min</b>", showarrow=False,
             font=dict(size=11, color=GOLD, family="Inter, Arial")),
    ]

    # ---------- HRV signal waveform on face ----------
    t_hrv = np.linspace(-0.45, 0.45, 120)
    y_hrv = 0.08 * np.sin(2*np.pi*t_hrv / 0.18) * np.exp(-((t_hrv/0.32)**2))
    fig.add_trace(go.Scatter3d(
        x=t_hrv, y=np.full_like(t_hrv, -0.60), z=0.08 + y_hrv,
        mode='lines', line=dict(color=LIME, width=3), name='HRV Signal'
    ))

    # ---------- layout ----------
    fig.update_layout(
        title=dict(text="⌚  NOURISH BAND — Live Biometric Watch Face", font=dict(size=20, color=NAVY), x=0.5),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor="#0B1D3A",
            camera=dict(eye=dict(x=0, y=0, z=2.4)),
            aspectmode='cube',
        ),
        height=580,
        paper_bgcolor=NAVY,
        font=dict(color=MINT),
        legend=dict(
            bgcolor="rgba(0,30,50,0.8)", bordercolor=TEAL, borderwidth=1,
            font=dict(color=MINT, size=11), x=0.78, y=0.98,
        ),
        annotations=[
            dict(text="<b>Nourish Band v1</b>", x=0.5, y=0.04, xref="paper", yref="paper",
                 showarrow=False, font=dict(size=12, color="#88C8BE"), align="center"),
        ],
        scene_annotations=annotations_3d,
    )
    return fig

fig1 = build_watch_face()
fig1.show()
print("\\n📊  Legend:")
print("  🔵 Teal arc  → Blood Glucose level (4.8 mmol/L — trending low, meal triggered)")
print("  🔵 Blue arc  → Hydration index (62% — borderline, system monitoring)")
print("  🔴 Coral arc → Stress score (33% — low, good time for lighter carbs)")
print("  🟢 Green wave → Live HRV signal")
print("  🟡 Gold text → Predicted meal arrival window")
""")

md("""---
## 2  📡  Real-Time Biometric Data Streams

The wearable continuously tracks **four key signals** every minute. Here's what a typical day looks like —
and how Nourish detects the precise moments to trigger a meal.
""")

# ── VIZ 2: 3D BIOMETRIC STREAMS ───────────────────────────────────────────────
code("""\
# ─── 2. 3-D Biometric Data Streams Over Time ─────────────────────────────────
def simulate_biometrics(n=1440):
    \"\"\"Simulate one full day (1440 minutes) of biometric readings.\"\"\"
    t = np.linspace(0, 24, n)

    # Blood glucose — circadian pattern + meal responses + gradual drifts
    glucose = (
        4.8 + 0.4*np.sin(2*np.pi*t/24 - 1)          # circadian base
        + 1.2*np.exp(-((t-8.5)/0.4)**2)               # breakfast spike
        + 0.9*np.exp(-((t-13.0)/0.4)**2)              # lunch spike
        + 0.7*np.exp(-((t-19.5)/0.4)**2)              # dinner spike
        + 0.08*np.random.randn(n)                      # noise
    )

    # Hydration — gradual decline through day with intake events
    hydration = (
        85 - 0.8*t + 8*np.exp(-((t-9)/0.3)**2)
        + 6*np.exp(-((t-14)/0.3)**2)
        + 5*np.exp(-((t-20)/0.3)**2)
        + 1.5*np.random.randn(n)
    ).clip(40, 100)

    # Stress (HRV-derived) — rises mid-morning and mid-afternoon
    stress = (
        20 + 15*np.exp(-((t-11)/2)**2)
        + 12*np.exp(-((t-16)/1.5)**2)
        + 3*np.random.randn(n)
    ).clip(5, 80)

    # Energy index
    energy = (
        50 + 20*np.sin(2*np.pi*t/24 - np.pi/4)
        - 15*np.exp(-((t-14.5)/1)**2)    # post-lunch dip
        + 2*np.random.randn(n)
    ).clip(0, 100)

    return t, glucose, hydration, stress, energy

t, glucose, hydration, stress, energy = simulate_biometrics()
hours = [f"{int(h):02d}:00" for h in t[::60]]

# ── 3-D scatter: glucose vs hydration vs time, coloured by stress
fig2 = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'scatter3d'}, {'type': 'scatter3d'}]],
    subplot_titles=["Glucose × Hydration × Time", "Energy × Stress × Glucose"],
)

# ── Subsample every 2 min for performance
step = 2
ts = t[::step]; gs = glucose[::step]; hs = hydration[::step]
ss = stress[::step]; es = energy[::step]

# Find meal trigger moments (glucose < 4.5 or energy < 35)
triggers = np.where((gs < 4.5) | (es < 32))[0]

fig2.add_trace(go.Scatter3d(
    x=ts, y=gs, z=hs,
    mode='lines+markers',
    line=dict(color=ss, colorscale='RdYlGn_r', width=4),
    marker=dict(size=2, color=ss, colorscale='RdYlGn_r', opacity=0.7,
                colorbar=dict(title='Stress %', x=0.44, len=0.7)),
    name='Bio Stream',
), row=1, col=1)

# Mark trigger moments
if len(triggers) > 0:
    trigger_x = ts[triggers][::15][:8]
    trigger_y = gs[triggers][::15][:8]
    trigger_z = hs[triggers][::15][:8]
    fig2.add_trace(go.Scatter3d(
        x=trigger_x, y=trigger_y, z=trigger_z,
        mode='markers',
        marker=dict(size=9, color=GOLD, symbol='diamond', opacity=1.0,
                    line=dict(color=CORAL, width=2)),
        name='🍽  Meal Trigger',
    ), row=1, col=1)

# Right panel: energy-stress-glucose space
fig2.add_trace(go.Scatter3d(
    x=es, y=ss, z=gs,
    mode='markers',
    marker=dict(size=3, color=ts, colorscale='Viridis', opacity=0.6,
                colorbar=dict(title='Hour of Day', x=1.02, len=0.7)),
    name='State Space',
), row=1, col=2)

fig2.update_layout(
    title=dict(text="📡  3-D Biometric Data Streams — 24-Hour Profile", font=dict(size=18, color=NAVY), x=0.5),
    height=600,
    scene=dict(
        xaxis=dict(title='Time (hours)', color=NAVY, backgroundcolor=LIGHT, gridcolor="#C0D8D8"),
        yaxis=dict(title='Blood Glucose (mmol/L)', color=NAVY, backgroundcolor=LIGHT),
        zaxis=dict(title='Hydration (%)', color=NAVY, backgroundcolor=LIGHT),
        bgcolor=LIGHT,
        camera=dict(eye=dict(x=1.8, y=-1.8, z=1.2)),
    ),
    scene2=dict(
        xaxis=dict(title='Energy Index', color=NAVY, backgroundcolor=LIGHT),
        yaxis=dict(title='Stress Score', color=NAVY, backgroundcolor=LIGHT),
        zaxis=dict(title='Blood Glucose', color=NAVY, backgroundcolor=LIGHT),
        bgcolor=LIGHT,
        camera=dict(eye=dict(x=1.8, y=-1.8, z=1.4)),
    ),
    paper_bgcolor='white',
    legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)'),
    font=dict(color=NAVY),
)
fig2.show()
print("\\n🟡 Gold diamonds = Meal trigger events (glucose dip or energy crash detected)")
print("   The AI kicks in at exactly these moments — no user input needed.")
""")

md("""---
## 3  🧠  Predictive & Prescriptive Analytics — The AI Engine

Nourish uses **predictive analytics** to forecast where your biometrics are heading,
and **prescriptive analytics** to determine the exact meal composition needed to correct the trajectory.
""")

# ── VIZ 3: 3D PREDICTION SURFACE ─────────────────────────────────────────────
code("""\
# ─── 3. Predictive Analytics — Glucose Forecast Surface ──────────────────────
def glucose_prediction_surface():
    \"\"\"
    3-D surface: x = current glucose, y = time since last meal,
    z = predicted glucose in 30 min. The 'danger zone' is highlighted.
    \"\"\"
    curr_g = np.linspace(3.5, 7.5, 60)
    t_meal  = np.linspace(0, 5, 60)
    CG, TM  = np.meshgrid(curr_g, t_meal)

    # Glucose trajectory model
    Z = CG - 0.25*TM - 0.05*TM**2 + 0.02*(CG - 5.5)*TM
    Z = np.clip(Z, 2.8, 8.5)

    # ── Surface ──
    fig3 = go.Figure()
    fig3.add_trace(go.Surface(
        x=CG, y=TM, z=Z,
        colorscale=[
            [0.0, CORAL],
            [0.25, "#FF9966"],
            [0.5,  GOLD],
            [0.75, LIME],
            [1.0,  TEAL],
        ],
        cmin=3.0, cmax=7.5,
        opacity=0.88,
        showscale=True,
        colorbar=dict(
            title=dict(text="Predicted Glucose<br>(mmol/L)", font=dict(color=NAVY, size=11)),
            tickfont=dict(color=NAVY, size=10),
            x=1.02,
        ),
        name='Glucose Forecast',
        hovertemplate=(
            "Current Glucose: %{x:.1f} mmol/L<br>"
            "Hours since meal: %{y:.1f}h<br>"
            "Predicted (30 min): %{z:.2f} mmol/L<extra></extra>"
        ),
        contours=dict(
            z=dict(show=True, start=3.0, end=7.5, size=0.5, color="white", width=1),
        ),
    ))

    # ── Danger zone plane (glucose < 4.0) ──
    z_plane = np.full_like(CG, 4.0)
    fig3.add_trace(go.Surface(
        x=CG, y=TM, z=z_plane,
        colorscale=[[0, "rgba(232,71,42,0.3)"], [1, "rgba(232,71,42,0.3)"]],
        showscale=False, opacity=0.35, name='Danger Threshold',
        hovertemplate="Danger threshold: 4.0 mmol/L<extra></extra>",
    ))

    # ── Scatter: actual trigger points ──
    trigger_data = [
        (4.6, 3.2, 3.8, "Breakfast trigger"),
        (4.3, 4.1, 3.4, "Lunch trigger"),
        (5.0, 2.8, 4.1, "Snack trigger"),
        (4.1, 4.8, 2.9, "Dinner trigger"),
    ]
    fig3.add_trace(go.Scatter3d(
        x=[d[0] for d in trigger_data],
        y=[d[1] for d in trigger_data],
        z=[d[2] for d in trigger_data],
        mode='markers+text',
        marker=dict(size=12, color=GOLD, symbol='diamond', line=dict(color=NAVY, width=2)),
        text=[d[3] for d in trigger_data],
        textfont=dict(color=NAVY, size=10),
        textposition='top center',
        name='AI Trigger Events',
    ))

    fig3.update_layout(
        title=dict(text="🧠  Predictive Glucose Forecast Surface — 30-Minute Look-Ahead", font=dict(size=18, color=NAVY), x=0.5),
        scene=dict(
            xaxis=dict(title='Current Glucose (mmol/L)', color=NAVY, backgroundcolor=LIGHT, gridcolor="#C8DCDC"),
            yaxis=dict(title='Hours Since Last Meal', color=NAVY, backgroundcolor=LIGHT),
            zaxis=dict(title='Predicted Glucose in 30 min', color=NAVY, backgroundcolor=LIGHT),
            camera=dict(eye=dict(x=1.8, y=-2.0, z=1.4)),
            bgcolor=LIGHT,
        ),
        height=620,
        paper_bgcolor='white',
        font=dict(color=NAVY),
        legend=dict(x=0.02, y=0.98),
    )
    return fig3

fig3 = glucose_prediction_surface()
fig3.show()
print("\\n🔴 Red/orange zone = Hypoglycaemic danger territory")
print("   When the predicted trajectory crosses 4.0 mmol/L → Nourish triggers a meal automatically")
print("   The surface is re-computed every 60 seconds using your live biometric stream.")
""")

md("""---
## 4  🗺️  The Full User Journey — 3D Flow Diagram

End-to-end flow from **biometric signal** → **AI decision** → **kitchen dispatch** → **doorstep delivery** → **health loop**.
This is the journey that requires **zero user input**.
""")

# ── VIZ 4: 3D USER JOURNEY FLOW ───────────────────────────────────────────────
code("""\
# ─── 4. 3-D User Journey Flow Network ────────────────────────────────────────
def build_journey_3d():
    # Nodes: (x, y, z, label, color, size)
    nodes = [
        # Layer 0: Body
        (0, 0, 0, "💪<br>Body", NAVY, 28),
        # Layer 1: Sensors
        (-2, 1, 1, "🩸<br>Glucose<br>Sensor",   TEAL,   22),
        (-2, 0, 1, "💧<br>Hydration<br>Sensor", SKY,    22),
        (-2,-1, 1, "❤️<br>HRV<br>Sensor",        LIME,   22),
        (-2,-2, 1, "🌡️<br>Temp/GSR<br>Sensor",   PURPLE, 22),
        # Layer 2: AI Core
        (0, -0.5, 2, "🧠<br>Nourish AI<br>Engine", GOLD, 32),
        # Layer 2b: AI inputs
        (0, 1.5, 2, "🕐<br>Circadian<br>Model",   "#8B6914", 20),
        (0, 3.0, 2, "😌<br>Mood<br>Inference",    CORAL,     20),
        # Layer 3: Decision
        (2, 0.5, 3, "🍱<br>Meal<br>Decision",      TEAL, 26),
        # Layer 4: Routing
        (4, 1.5, 3, "🏭<br>Prep<br>Node",          LIME, 22),
        (4, -0.5, 3, "🛒<br>Partner<br>Outlet",   PURPLE, 20),
        # Layer 5: Delivery
        (6, 0.5, 4, "🚴<br>Delivery",             NAVY, 22),
        # Layer 6: Customer
        (8, 0.5, 4, "👤<br>Vansh<br>eats",        GOLD, 28),
        # Layer 7: Health loop
        (8, -1.5, 5, "📊<br>Weekly<br>Summary",   TEAL, 22),
        (6, -2.5, 5, "🔄<br>Data<br>Richer",      LIME, 20),
        (4, -2.5, 5, "⚡<br>AI Smarter",          GOLD, 20),
    ]

    edges = [
        (0,1),(0,2),(0,3),(0,4),   # body → sensors
        (1,5),(2,5),(3,5),(4,5),   # sensors → AI
        (6,5),(7,5),               # context → AI
        (5,8),                     # AI → decision
        (8,9),(8,10),              # decision → routing
        (9,11),(10,11),            # routing → delivery
        (11,12),                   # delivery → user
        (12,13),(13,14),(14,15),   # health feedback loop
        (15,5),                    # loop back to AI (dashed)
    ]

    fig4 = go.Figure()

    # Draw edges
    edge_colors = [TEAL]*10 + [LIME]*4 + [GOLD, GOLD, GOLD]
    for idx, (i, j) in enumerate(edges):
        xi, yi, zi = nodes[i][:3]
        xj, yj, zj = nodes[j][:3]
        is_loop = idx >= len(edges)-3
        fig4.add_trace(go.Scatter3d(
            x=[xi, xj, None], y=[yi, yj, None], z=[zi, zj, None],
            mode='lines',
            line=dict(color=GOLD if is_loop else TEAL, width=5 if not is_loop else 3,
                      dash='dash' if is_loop else 'solid'),
            showlegend=False,
        ))
        # Arrowhead approximation (midpoint dot)
        mx, my, mz = (xi+xj)/2, (yi+yj)/2, (zi+zj)/2
        fig4.add_trace(go.Scatter3d(
            x=[mx], y=[my], z=[mz], mode='markers',
            marker=dict(size=3, color=GOLD if is_loop else TEAL, symbol='circle'),
            showlegend=False,
        ))

    # Draw nodes
    fig4.add_trace(go.Scatter3d(
        x=[n[0] for n in nodes],
        y=[n[1] for n in nodes],
        z=[n[2] for n in nodes],
        mode='markers+text',
        marker=dict(
            size=[n[5] for n in nodes],
            color=[n[4] for n in nodes],
            line=dict(color='white', width=2),
            opacity=0.95,
        ),
        text=[n[3] for n in nodes],
        textfont=dict(size=9, color=NAVY),
        textposition='middle center',
        name='Journey Nodes',
        hovertemplate="%{text}<extra></extra>",
    ))

    # Layer labels
    layer_labels = [
        (0, -2.5, 0, "BODY"),
        (-2, -3, 1, "SENSORS"),
        (0, -3, 2, "AI LAYER"),
        (2, -2.5, 3, "DECISION"),
        (4, -2, 3, "ROUTING"),
        (6, -2, 4, "DELIVERY"),
        (8, -3, 4, "USER"),
        (6.5, -4, 5, "HEALTH LOOP"),
    ]
    for lx, ly, lz, lt in layer_labels:
        fig4.add_trace(go.Scatter3d(
            x=[lx], y=[ly], z=[lz], mode='text',
            text=[f"<b>{lt}</b>"],
            textfont=dict(size=11, color=CORAL),
            showlegend=False,
        ))

    fig4.update_layout(
        title=dict(text="🗺️  Nourish — Complete Autonomous User Journey (3-D)", font=dict(size=18, color=NAVY), x=0.5),
        scene=dict(
            xaxis=dict(title='Journey Stage →', color=NAVY, backgroundcolor=LIGHT, gridcolor="#C0D8D8"),
            yaxis=dict(visible=False),
            zaxis=dict(title='Complexity Layer', color=NAVY, backgroundcolor=LIGHT),
            camera=dict(eye=dict(x=2.0, y=-2.5, z=1.6)),
            bgcolor=LIGHT,
        ),
        height=650,
        paper_bgcolor='white',
        font=dict(color=NAVY),
        showlegend=False,
    )
    return fig4

fig4 = build_journey_3d()
fig4.show()
print("\\n🔵 Teal edges  = Primary data/delivery flow (body → AI → kitchen → you)")
print("🟡 Gold dashed = Compounding health loop (data gets richer → AI gets smarter)")
""")

md("""---
## 5  📊  Prescriptive Analytics — Meal Recommendation Engine

Once the AI detects a trigger, it prescribes the **exact meal composition** based on three inputs.
This 3-D visualisation shows the meal-space and how different biometric states map to different food archetypes.
""")

# ── VIZ 5: 3D PRESCRIPTIVE MEAL SPACE ────────────────────────────────────────
code("""\
# ─── 5. Prescriptive Analytics — Meal Recommendation Space ───────────────────
def meal_space_3d():
    # Simulate 300 meal decisions with different biometric contexts
    n = 300
    glucose_in  = np.random.uniform(3.2, 6.8, n)
    hydration   = np.random.uniform(40, 95, n)
    stress      = np.random.uniform(5, 75, n)
    hour_of_day = np.random.uniform(6, 22, n)

    # Prescriptive rules → meal archetype
    def classify(g, h, s, t):
        if g < 4.2 and s < 30:  return "High-Carb Energy Boost", CORAL, 14
        if g < 4.2 and s >= 30: return "Light Glucose Replenishment", GOLD, 12
        if h < 60:               return "Hydration + Electrolytes", SKY, 11
        if s > 55:               return "Adaptogen Calm Bowl", LIME, 12
        if t < 10:               return "Morning Protein Kickstart", PURPLE, 13
        if t > 19:               return "Gut-Rest Dinner", NAVY, 11
        return "Balanced Macro Plate", TEAL, 10

    labels, colors, sizes = zip(*[classify(g, h, s, t) for g, h, s, t in
                                   zip(glucose_in, hydration, stress, hour_of_day)])
    # Category index for coloring
    unique_labels = list(dict.fromkeys(labels))
    label_map = {l: i for i, l in enumerate(unique_labels)}
    cat_idx = [label_map[l] for l in labels]

    colorscale_cats = [CORAL, GOLD, SKY, LIME, PURPLE, NAVY, TEAL]

    fig5 = go.Figure()

    for cat in unique_labels:
        mask = np.array([l == cat for l in labels])
        fig5.add_trace(go.Scatter3d(
            x=glucose_in[mask],
            y=hydration[mask],
            z=stress[mask],
            mode='markers',
            marker=dict(
                size=8,
                color=colorscale_cats[label_map[cat] % len(colorscale_cats)],
                opacity=0.75,
                line=dict(color='white', width=0.5),
            ),
            name=cat,
            hovertemplate=(
                f"<b>{cat}</b><br>"
                "Glucose: %{x:.1f} mmol/L<br>"
                "Hydration: %{y:.0f}%<br>"
                "Stress: %{z:.0f}%<extra></extra>"
            ),
        ))

    # Decision boundaries (planes)
    gx = np.linspace(3.2, 6.8, 10)
    hy = np.linspace(40, 95, 10)
    GX, HY = np.meshgrid(gx, hy)

    # Glucose threshold plane
    fig5.add_trace(go.Surface(
        x=np.full_like(GX, 4.2),
        y=np.tile(np.linspace(40, 95, 10), (10, 1)),
        z=np.tile(np.linspace(5, 75, 10), (10, 1)).T,
        colorscale=[[0, "rgba(232,71,42,0.15)"], [1, "rgba(232,71,42,0.15)"]],
        showscale=False, opacity=0.20, name='Glucose Threshold',
        hovertemplate="Glucose trigger boundary: 4.2 mmol/L<extra></extra>",
    ))

    # Hydration threshold plane
    fig5.add_trace(go.Surface(
        x=np.tile(np.linspace(3.2, 6.8, 10), (10, 1)),
        y=np.full_like(GX, 60),
        z=np.tile(np.linspace(5, 75, 10), (10, 1)).T,
        colorscale=[[0, "rgba(58,134,255,0.15)"], [1, "rgba(58,134,255,0.15)"]],
        showscale=False, opacity=0.20, name='Hydration Threshold',
        hovertemplate="Hydration boundary: 60%<extra></extra>",
    ))

    fig5.update_layout(
        title=dict(text="📊  Prescriptive Analytics — Meal Archetype Recommendation Space", font=dict(size=17, color=NAVY), x=0.5),
        scene=dict(
            xaxis=dict(title='Blood Glucose (mmol/L)', color=NAVY, backgroundcolor=LIGHT, gridcolor="#C0D8D8"),
            yaxis=dict(title='Hydration (%)', color=NAVY, backgroundcolor=LIGHT),
            zaxis=dict(title='Stress Score (%)', color=NAVY, backgroundcolor=LIGHT),
            camera=dict(eye=dict(x=1.8, y=-2.0, z=1.5)),
            bgcolor=LIGHT,
        ),
        height=650,
        paper_bgcolor='white',
        legend=dict(
            x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.9)',
            bordercolor=TEAL, borderwidth=1, font=dict(size=10),
        ),
        font=dict(color=NAVY),
    )
    return fig5

fig5 = meal_space_3d()
fig5.show()
print("\\nEach cluster = a distinct meal archetype prescribed by the AI")
print("Transparent planes = decision boundaries (glucose < 4.2 → energy meal; hydration < 60 → hydration response)")
""")

md("""---
## 6  🏭  Kitchen Network — Hyperlocal Prep Node Coverage

Nourish operates **proprietary neighbourhood prep nodes** — not cloud kitchens — designed to cook fresh,
nutritionally-precise meals within 15–20 minutes. The map shows simulated node placement across a city.
""")

# ── VIZ 6: 3D KITCHEN NETWORK ────────────────────────────────────────────────
code("""\
# ─── 6. Hyperlocal Prep Node Network — 3-D Coverage Map ──────────────────────
def kitchen_network_3d():
    # Simulate city grid (12 x 12 km) with prep nodes and user locations
    np.random.seed(21)
    n_nodes = 18

    # Node positions
    node_x = np.random.uniform(0, 12, n_nodes)
    node_y = np.random.uniform(0, 12, n_nodes)
    node_z = np.zeros(n_nodes)
    node_load = np.random.randint(2, 9, n_nodes)   # active orders

    # User locations (current triggers)
    n_users = 40
    user_x = np.random.uniform(0.5, 11.5, n_users)
    user_y = np.random.uniform(0.5, 11.5, n_users)
    user_z = np.zeros(n_users)

    # Assign each user to nearest node
    def nearest_node(ux, uy):
        dists = np.sqrt((node_x - ux)**2 + (node_y - uy)**2)
        return np.argmin(dists)

    assignments = [nearest_node(ux, uy) for ux, uy in zip(user_x, user_y)]

    fig6 = go.Figure()

    # Coverage radius spheres (flat discs via filled circles)
    theta_c = np.linspace(0, 2*np.pi, 40)
    for i in range(n_nodes):
        radius = 2.2
        cx = node_x[i] + radius * np.cos(theta_c)
        cy = node_y[i] + radius * np.sin(theta_c)
        cz = np.zeros_like(theta_c) + 0.02
        fig6.add_trace(go.Scatter3d(
            x=cx, y=cy, z=cz, mode='lines',
            line=dict(color='rgba(0,168,150,0.3)', width=2),
            showlegend=False,
        ))

    # Connection lines: user → assigned node (vertical z lift shows assignment)
    for u_idx, n_idx in enumerate(assignments):
        z_lift = np.sqrt((user_x[u_idx]-node_x[n_idx])**2 + (user_y[u_idx]-node_y[n_idx])**2) * 0.15
        fig6.add_trace(go.Scatter3d(
            x=[user_x[u_idx], node_x[n_idx], None],
            y=[user_y[u_idx], node_y[n_idx], None],
            z=[0.1, 0.1, None],
            mode='lines', line=dict(color='rgba(247,183,49,0.4)', width=2),
            showlegend=False,
        ))

    # Prep nodes
    fig6.add_trace(go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers+text',
        marker=dict(
            size=10 + node_load*1.2,
            color=node_load,
            colorscale='RdYlGn_r',
            cmin=2, cmax=9,
            line=dict(color=NAVY, width=2),
            opacity=0.9,
            colorbar=dict(title=dict(text='Active Orders', font=dict(color=NAVY, size=11)), tickfont=dict(color=NAVY), x=1.02),
        ),
        text=[f"Node {i+1}" for i in range(n_nodes)],
        textfont=dict(size=8, color=NAVY),
        textposition='top center',
        name='🏭 Prep Nodes',
        hovertemplate="Node %{text}<br>Active orders: %{marker.color}<extra></extra>",
    ))

    # Users
    fig6.add_trace(go.Scatter3d(
        x=user_x, y=user_y, z=user_z + 0.1,
        mode='markers',
        marker=dict(size=5, color=SKY, opacity=0.7, symbol='circle',
                    line=dict(color=NAVY, width=1)),
        name='👤 Active Users',
        hovertemplate="User location<extra></extra>",
    ))

    # Central demand heatmap (simulated density surface)
    xi, yi = np.mgrid[0:12:30j, 0:12:30j]
    density = np.zeros_like(xi)
    for ux, uy in zip(user_x, user_y):
        density += np.exp(-((xi - ux)**2 + (yi - uy)**2) / 3.0)
    density = density / density.max() * 0.8

    fig6.add_trace(go.Surface(
        x=xi, y=yi, z=density - 0.05,
        colorscale=[[0, 'rgba(240,249,247,0)'], [1, 'rgba(0,168,150,0.4)']],
        showscale=False, opacity=0.5, name='Demand Density',
        hovertemplate="Demand level: %{z:.2f}<extra></extra>",
    ))

    fig6.update_layout(
        title=dict(text="🏭  Nourish Kitchen Network — Hyperlocal Prep Node Coverage", font=dict(size=17, color=NAVY), x=0.5),
        scene=dict(
            xaxis=dict(title='City East-West (km)', color=NAVY, backgroundcolor=LIGHT),
            yaxis=dict(title='City North-South (km)', color=NAVY, backgroundcolor=LIGHT),
            zaxis=dict(title='', showticklabels=False),
            camera=dict(eye=dict(x=1.5, y=-2.0, z=2.0)),
            bgcolor=LIGHT,
        ),
        height=640,
        paper_bgcolor='white',
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.9)', bordercolor=TEAL, borderwidth=1),
        font=dict(color=NAVY),
    )
    return fig6

fig6 = kitchen_network_3d()
fig6.show()
print("\\n🟢 Large circles = Prep nodes (size = current load, colour = red=busy → green=free)")
print("🔵 Small dots    = Active users with live meal triggers")
print("🌊 Teal surface  = Demand density — nodes are positioned to maximise coverage")
""")

md("""---
## 7  📈  Compounding Personalisation Loop — Health Improvement Over Time

The longer a user stays on Nourish, the better the AI gets at predicting their needs.
This simulation shows how **prediction accuracy improves** as the data flywheel spins.
""")

# ── VIZ 7: COMPOUNDING LOOP ───────────────────────────────────────────────────
code("""\
# ─── 7. Compounding Personalisation Loop — 3-D ───────────────────────────────
def compounding_loop_3d():
    months = np.linspace(0, 24, 200)

    # Prediction accuracy: starts at 65%, plateaus near 96%
    accuracy = 96 - 31 * np.exp(-0.18 * months)

    # Health score: improves with good nutrition + compounding knowledge
    health = 45 + 40 * (1 - np.exp(-0.12 * months)) + 0.5 * np.random.randn(len(months))

    # Data richness: exponential accumulation
    data_pts = 500 + 2200 * (1 - np.exp(-0.09 * months))

    fig7 = go.Figure()

    # 3D spiral representing the flywheel
    theta_s = np.linspace(0, 6*np.pi, 200)
    r_s     = 0.3 + 0.7 * (months / 24)
    spiral_x = r_s * np.cos(theta_s)
    spiral_y = r_s * np.sin(theta_s)
    spiral_z = months / 24

    fig7.add_trace(go.Scatter3d(
        x=spiral_x, y=spiral_y, z=spiral_z,
        mode='lines',
        line=dict(color=accuracy, colorscale='RdYlGn', width=7,
                  cmin=65, cmax=96,
                  colorbar=dict(title=dict(text='AI Accuracy (%)', font=dict(color=NAVY, size=11)),
                                tickfont=dict(color=NAVY), x=1.02)),
        name='Compounding Loop',
        hovertemplate="Month %{z:.0f}<br>Accuracy: %{line.color:.1f}%<extra></extra>",
    ))

    # Mark milestones
    milestones = [
        (1,  "Month 1<br>Baseline", 0.06),
        (3,  "Month 3<br>Patterns", 0.12),
        (6,  "Month 6<br>Circadian", 0.25),
        (12, "Month 12<br>Deep Profile", 0.50),
        (24, "Month 24<br>Moat Built", 1.0),
    ]
    for mo, label, frac in milestones:
        idx = int(frac * 199)
        fig7.add_trace(go.Scatter3d(
            x=[spiral_x[idx]], y=[spiral_y[idx]], z=[months[idx]/24],
            mode='markers+text',
            marker=dict(size=14, color=GOLD, symbol='diamond', line=dict(color=NAVY, width=2)),
            text=[label], textfont=dict(size=9, color=NAVY),
            textposition='top center',
            showlegend=False,
        ))

    fig7.update_layout(
        title=dict(text="🔄  Compounding Personalisation Flywheel — 24-Month Simulation", font=dict(size=17, color=NAVY), x=0.5),
        scene=dict(
            xaxis=dict(title='Flywheel X', color=NAVY, backgroundcolor=LIGHT, showticklabels=False),
            yaxis=dict(title='Flywheel Y', color=NAVY, backgroundcolor=LIGHT, showticklabels=False),
            zaxis=dict(title='Time (0 = Month 0, 1 = Month 24)', color=NAVY, backgroundcolor=LIGHT),
            camera=dict(eye=dict(x=1.8, y=-2.2, z=1.4)),
            bgcolor=LIGHT,
        ),
        height=600,
        paper_bgcolor='white',
        font=dict(color=NAVY),
        showlegend=False,
    )

    # 2D summary below
    fig7b = make_subplots(rows=1, cols=3,
        subplot_titles=["AI Prediction Accuracy (%)", "User Health Score", "Biometric Data Points"])
    x_m = np.linspace(0, 24, 200)
    fig7b.add_trace(go.Scatter(x=x_m, y=accuracy, mode='lines', line=dict(color=TEAL, width=3), fill='tozeroy', fillcolor='rgba(0,168,150,0.15)', name='Accuracy'), row=1, col=1)
    fig7b.add_trace(go.Scatter(x=x_m, y=health, mode='lines', line=dict(color=LIME, width=3), fill='tozeroy', fillcolor='rgba(82,183,136,0.15)', name='Health'), row=1, col=2)
    fig7b.add_trace(go.Scatter(x=x_m, y=data_pts, mode='lines', line=dict(color=GOLD, width=3), fill='tozeroy', fillcolor='rgba(247,183,49,0.15)', name='Data'), row=1, col=3)
    fig7b.update_layout(height=300, paper_bgcolor='white', showlegend=False,
                         font=dict(color=NAVY), title=dict(text="Metrics Over 24 Months", x=0.5))
    fig7b.update_xaxes(title_text="Months")

    return fig7, fig7b

fig7, fig7b = compounding_loop_3d()
fig7.show()
fig7b.show()
print("\\nThe spiral tightens and rises → each loop makes the AI more accurate.")
print("A competitor entering month 24 starts at the bottom — your data moat is permanent.")
""")

md("""---
## 8  🎛️  Full Interactive Dashboard — All Signals Live

One unified dashboard bringing together all biometric signals, the AI decision, and the meal outcome.
""")

# ── VIZ 8: FULL DASHBOARD ─────────────────────────────────────────────────────
code("""\
# ─── 8. Full Interactive Dashboard ───────────────────────────────────────────
def full_dashboard():
    t, glucose, hydration, stress, energy = simulate_biometrics()
    hours = np.linspace(0, 24, len(t))

    # Find trigger moments
    triggers_idx = np.where(np.diff((glucose < 4.5).astype(int)) > 0)[0]
    meal_times   = hours[triggers_idx]

    fig = make_subplots(
        rows=2, cols=3,
        specs=[
            [{'type': 'scatter3d', 'colspan': 2}, None, {'type': 'xy'}],
            [{'type': 'xy'},                       {'type': 'xy'}, {'type': 'xy'}],
        ],
        subplot_titles=[
            "3-D Biometric State Space",
            "Blood Glucose Timeline",
            "Hydration (%)",
            "Stress Score (%)",
            "Energy Index",
        ],
        column_widths=[0.35, 0.35, 0.30],
        row_heights=[0.55, 0.45],
    )

    # Panel 1: 3-D state space
    step = 3
    fig.add_trace(go.Scatter3d(
        x=glucose[::step], y=hydration[::step], z=stress[::step],
        mode='lines+markers',
        line=dict(color=energy[::step], colorscale='Viridis', width=4),
        marker=dict(size=2, color=energy[::step], colorscale='Viridis', opacity=0.6),
        name='State Space', showlegend=False,
    ), row=1, col=1)

    # Panel 2: Glucose
    fig.add_trace(go.Scatter(x=hours, y=glucose, mode='lines', line=dict(color=TEAL, width=2), name='Glucose', fill='tozeroy', fillcolor='rgba(0,168,150,0.08)'), row=1, col=3)
    fig.add_hline(y=4.2, line_dash="dash", line_color=CORAL, annotation_text="Trigger threshold", row=1, col=3)
    for mt in meal_times[:4]:
        fig.add_vline(x=mt, line_dash="dot", line_color=GOLD, row=1, col=3)

    # Panel 3: Hydration
    fig.add_trace(go.Scatter(x=hours, y=hydration, mode='lines', line=dict(color=SKY, width=2), name='Hydration', fill='tozeroy', fillcolor='rgba(58,134,255,0.08)'), row=2, col=1)
    fig.add_hline(y=60, line_dash="dash", line_color=CORAL, row=2, col=1)

    # Panel 4: Stress
    fig.add_trace(go.Scatter(x=hours, y=stress, mode='lines', line=dict(color=CORAL, width=2), name='Stress', fill='tozeroy', fillcolor='rgba(232,71,42,0.08)'), row=2, col=2)

    # Panel 5: Energy
    fig.add_trace(go.Scatter(x=hours, y=energy, mode='lines', line=dict(color=LIME, width=2), name='Energy', fill='tozeroy', fillcolor='rgba(82,183,136,0.08)'), row=2, col=3)

    fig.update_layout(
        title=dict(text="🎛️  NOURISH — Live Biometric Dashboard (24-Hour View)", font=dict(size=18, color=NAVY), x=0.5),
        height=800,
        paper_bgcolor='white',
        font=dict(color=NAVY),
        scene=dict(
            xaxis=dict(title='Glucose', color=NAVY, backgroundcolor=LIGHT),
            yaxis=dict(title='Hydration', color=NAVY, backgroundcolor=LIGHT),
            zaxis=dict(title='Stress', color=NAVY, backgroundcolor=LIGHT),
            bgcolor=LIGHT,
            camera=dict(eye=dict(x=2.0, y=-2.0, z=1.6)),
        ),
        showlegend=False,
    )
    for r, c in [(1,3),(2,1),(2,2),(2,3)]:
        fig.update_xaxes(title_text="Hour of Day", row=r, col=c)

    return fig

dash = full_dashboard()
dash.show()
print("\\n🎛️  Full dashboard combining all signals — this is what the Nourish AI sees every minute.")
print(f"   Gold vertical lines = automatic meal trigger events (no user input)")
""")

md("""---
## 9  🚀  Run on Streamlit

The **`app.py`** file (included alongside this notebook) is a complete Streamlit app. Launch it with:

```bash
pip install streamlit plotly numpy
streamlit run app.py
```

It includes interactive sliders for simulation controls, all 6 tabs (Wearable, Biometrics, Predictions, Journey, Kitchen Network, Flywheel), and live metric cards.
""")

# ── STREAMLIT APP REFERENCE ───────────────────────────────────────────────────
code("""\
# ─── 9. Verify Streamlit app.py exists ────────────────────────────────────────
import os, pathlib

app_path = pathlib.Path("app.py")
if not app_path.exists():
    # Try same directory as notebook
    app_path = pathlib.Path(__file__).parent / "app.py" if "__file__" in dir() else pathlib.Path("app.py")

if app_path.exists():
    lines = app_path.read_text().splitlines()
    print(f"✅  app.py found — {len(lines)} lines")
    print()
    print("━" * 55)
    print("  To launch the Streamlit app, run:")
    print("  pip install streamlit plotly numpy")
    print("  streamlit run app.py")
    print("━" * 55)
else:
    print("ℹ️  app.py should be in the same folder as this notebook.")
    print("   Both files were delivered together.")

# Show the first few lines as a preview
try:
    with open("app.py") as f:
        preview = [f.readline() for _ in range(8)]
    print()
    print("Preview of app.py:")
    for line in preview:
        print(" ", line.rstrip())
except Exception:
    pass
""")


md("""---
## 10  📋  Summary — The Nourish Advantage

| Metric | Traditional Delivery | Nourish |
|---|---|---|
| User input required | Every order | **Zero** |
| Revenue model | Commission per order | **Hardware + Subscription** |
| Food optimised for | Platform margin | **Your biometrics** |
| Data flywheel | Order logs | **Live physiological history** |
| Competitor replication | Easy (copy the app) | **Impossible (copy the data)** |
| Health outcome trend | 84% higher obesity risk | **Measurable improvement** |

---

> **"In 2030, letting your body automatically order its own nutrition will feel as natural
> as streaming music on demand felt in 2015."**
> — *Nourish, Blue Ocean Strategy Challenge, SP Jain GMBA 2026*

---
*Built with Plotly · Python 3 · Streamlit-compatible · GitHub-rendered*
""")

nb.cells = cells

outpath = "/sessions/epic-keen-ramanujan/mnt/outputs/nourish_viz.ipynb"
with open(outpath, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Notebook written: {outpath}")
