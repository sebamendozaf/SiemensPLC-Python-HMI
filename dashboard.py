"""SCADA Monitor — Dashboard web en tiempo real."""

import time
from collections import deque
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import (
    HISTORY_POINTS,
    PLC_IP,
    PLC_VARIABLES,
    REFRESH_INTERVAL_SEC,
    SIMULATION_MODE,
)

st.set_page_config(page_title="SCADA Monitor", layout="wide")


def get_data_source():
    if SIMULATION_MODE:
        from simulator import ProcessSimulator
        if "simulator" not in st.session_state:
            st.session_state.simulator = ProcessSimulator()
        return st.session_state.simulator
    else:
        from plc_connector import S7Connector
        if "plc" not in st.session_state:
            st.session_state.plc = S7Connector()
            st.session_state.plc.connect()
        return st.session_state.plc


def init_history():
    if "history" not in st.session_state:
        st.session_state.history = {
            "timestamp": deque(maxlen=HISTORY_POINTS),
            "Nivel Tanque (%)": deque(maxlen=HISTORY_POINTS),
            "Temperatura (°C)": deque(maxlen=HISTORY_POINTS),
            "Presión (bar)": deque(maxlen=HISTORY_POINTS),
            "Caudal (L/min)": deque(maxlen=HISTORY_POINTS),
        }


def create_gauge(value, title, min_val, max_val, unit, thresholds=None):
    """Crea un indicador tipo gauge."""
    if thresholds is None:
        thresholds = {"low": max_val * 0.3, "mid": max_val * 0.7, "high": max_val}

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"size": 16}},
        number={"suffix": f" {unit}", "font": {"size": 24}},
        gauge={
            "axis": {"range": [min_val, max_val]},
            "bar": {"color": "#1f77b4"},
            "steps": [
                {"range": [min_val, thresholds["low"]], "color": "#d4edda"},
                {"range": [thresholds["low"], thresholds["mid"]], "color": "#fff3cd"},
                {"range": [thresholds["mid"], thresholds["high"]], "color": "#f8d7da"},
            ],
        },
    ))
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=10))
    return fig


def create_trend_chart(history):
    """Crea gráfico de tendencia histórica."""
    if len(history["timestamp"]) < 2:
        return None

    df = pd.DataFrame({
        "Tiempo": list(history["timestamp"]),
        "Nivel (%)": list(history["Nivel Tanque (%)"]),
        "Temp (°C)": list(history["Temperatura (°C)"]),
        "Presión (bar)": list(history["Presión (bar)"]),
        "Caudal (L/min)": list(history["Caudal (L/min)"]),
    })

    fig = go.Figure()
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    for i, col in enumerate(["Nivel (%)", "Temp (°C)", "Presión (bar)", "Caudal (L/min)"]):
        fig.add_trace(go.Scatter(x=df["Tiempo"], y=df[col], name=col, line=dict(color=colors[i], width=2)))

    fig.update_layout(
        title="Tendencia en Tiempo Real",
        height=350,
        margin=dict(l=40, r=20, t=40, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis_title="",
        yaxis_title="",
    )
    return fig


# --- UI Principal ---

source = get_data_source()
init_history()

# Header
mode_label = "SIMULACIÓN" if SIMULATION_MODE else f"PLC {PLC_IP}"
mode_color = "orange" if SIMULATION_MODE else "green"

st.markdown(f"""
# SCADA Monitor
**Modo:** :{mode_color}[{mode_label}] &nbsp; | &nbsp;
**Variables:** {len(PLC_VARIABLES)} &nbsp; | &nbsp;
**Refresco:** {REFRESH_INTERVAL_SEC}s
""")

st.divider()

# Leer datos
values = source.read_all()
now = datetime.now().strftime("%H:%M:%S")

# Guardar en historial
st.session_state.history["timestamp"].append(now)
for key in ["Nivel Tanque (%)", "Temperatura (°C)", "Presión (bar)", "Caudal (L/min)"]:
    st.session_state.history[key].append(values.get(key, 0))

# --- Gauges ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    fig = create_gauge(values["Nivel Tanque (%)"], "Nivel Tanque", 0, 100, "%",
                       {"low": 30, "mid": 70, "high": 100})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = create_gauge(values["Temperatura (°C)"], "Temperatura", 0, 100, "°C",
                       {"low": 30, "mid": 60, "high": 100})
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = create_gauge(values["Presión (bar)"], "Presión", 0, 6, "bar",
                       {"low": 2, "mid": 4, "high": 6})
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = create_gauge(values["Caudal (L/min)"], "Caudal", 0, 60, "L/min",
                       {"low": 20, "mid": 40, "high": 60})
    st.plotly_chart(fig, use_container_width=True)

# --- Estados digitales ---
st.subheader("Estado de Equipos")
col1, col2, col3, col4, col5, col6 = st.columns(6)

def status_indicator(col, name, value, on_label="ON", off_label="OFF"):
    with col:
        if value:
            st.success(f"{name}\n\n**{on_label}**")
        else:
            st.error(f"{name}\n\n**{off_label}**")

status_indicator(col1, "Bomba 1", values["Bomba 1"])
status_indicator(col2, "Bomba 2", values["Bomba 2"])
status_indicator(col3, "V. Entrada", values["Válvula Entrada"], "ABIERTA", "CERRADA")
status_indicator(col4, "V. Salida", values["Válvula Salida"], "ABIERTA", "CERRADA")

with col5:
    if values["Alarma Nivel Alto"]:
        st.warning("Alarma Nivel\n\n**ACTIVA**")
    else:
        st.info("Alarma Nivel\n\n**Normal**")

with col6:
    if values["Alarma Temperatura"]:
        st.warning("Alarma Temp\n\n**ACTIVA**")
    else:
        st.info("Alarma Temp\n\n**Normal**")

# --- Gráfico de tendencia ---
st.subheader("Historial")
trend = create_trend_chart(st.session_state.history)
if trend:
    st.plotly_chart(trend, use_container_width=True)
else:
    st.info("Acumulando datos para el gráfico...")

# --- Tabla de valores ---
with st.expander("Tabla de valores actuales"):
    table_data = []
    for var in PLC_VARIABLES:
        val = values.get(var["name"])
        if var["type"] == "bool":
            display = "ON" if val else "OFF"
        else:
            display = f"{val} {var['unit']}"
        table_data.append({"Variable": var["name"], "Valor": display, "Tipo": var["type"].upper()})
    st.table(pd.DataFrame(table_data))

# --- Footer ---
st.caption(f"Última lectura: {now} — SCADA Monitor v1.0")

# Auto-refresh
time.sleep(REFRESH_INTERVAL_SEC)
st.rerun()
