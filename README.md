# SiemensPLC-Python-HMI

Real-time web dashboard for monitoring Siemens S7 PLCs (S7-1200/1500) using Python.

Reads variables from a real PLC (or simulated via PLCSIM) and displays them in an interactive dashboard with gauges, digital indicators, and trend charts.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45-FF4B4B?logo=streamlit&logoColor=white)
![Siemens](https://img.shields.io/badge/Siemens-S7--1200%2F1500-009999)

## Architecture

```
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│   TIA Portal     │  S7     │   Python          │  HTTP   │   Browser        │
│   + PLCSIM       │◄───────►│   (snap7)         │────────►│   Dashboard      │
│   PLC Program    │  TCP/IP │   Read/Write      │         │   Streamlit      │
└──────────────────┘         └──────────────────┘         └──────────────────┘
```

## Features

- **Real-time gauges** — Level, temperature, pressure, flow rate
- **Digital indicators** — Pump status, valves, alarms
- **Trend charts** — Analog variable history
- **Simulation mode** — Works without a real PLC for demo purposes
- **Real PLC mode** — Direct connection to Siemens S7-1200/1500 via snap7

## Requirements

- Python 3.10+
- TIA Portal + PLCSIM (for real PLC mode)
- Network connection between PC and PLC/PLCSIM

## Installation

```bash
git clone https://github.com/sebamendozaf/SiemensPLC-Python-HMI.git
cd SiemensPLC-Python-HMI
pip install -r requirements.txt
```

## Usage

### Simulation mode (no PLC needed)

```bash
streamlit run dashboard.py
```

The dashboard starts with simulated data. No PLC or TIA Portal required.

### Real PLC mode

1. **Set the PLC IP** in `config.py`:
   ```python
   PLC_IP = "192.168.1.10"  # Your PLC or PLCSIM IP
   SIMULATION_MODE = False
   ```

2. **Test the connection**:
   ```bash
   python test_connection.py
   ```

3. **Start the dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

## PLC Configuration (TIA Portal)

For the connection to work, your TIA Portal project needs:

1. **A DB1 (Data Block)** with these variables:

   | Offset | Type | Variable |
   |--------|------|----------|
   | 0 | Real | Tank level (%) |
   | 4 | Real | Temperature (C) |
   | 8 | Real | Pressure (bar) |
   | 12 | Real | Flow rate (L/min) |
   | 16.0 | Bool | Pump 1 |
   | 16.1 | Bool | Pump 2 |
   | 16.2 | Bool | Inlet valve |
   | 16.3 | Bool | Outlet valve |
   | 16.4 | Bool | High level alarm |
   | 16.5 | Bool | Temperature alarm |

2. **DB access set to "Full"** (non-optimized):
   - Right-click DB1 → Properties → Uncheck "Optimized block access"

3. **PUT/GET enabled** on the CPU:
   - CPU Properties → Protection & Security → Permit access with PUT/GET

## Project Structure

```
SiemensPLC-Python-HMI/
├── dashboard.py        # Web dashboard (Streamlit)
├── plc_connector.py    # Siemens S7 PLC connection
├── simulator.py        # Industrial process simulator
├── config.py           # Configuration (IP, variables, thresholds)
├── test_connection.py  # Connection test script
├── requirements.txt    # Python dependencies
└── README.md
```

## Technologies

| Technology | Purpose |
|---|---|
| **python-snap7** | Siemens S7 PLC communication (S7comm protocol) |
| **Streamlit** | Interactive web dashboard |
| **Plotly** | Charts and gauges |
| **Pandas** | Tabular data handling |

## Simulated Process

The simulator models a tank with:
- Automatic level control (valves open/close based on level)
- Pumps activated on demand
- Oscillating temperature with noise
- Pressure correlated with level
- High level and high temperature alarms
