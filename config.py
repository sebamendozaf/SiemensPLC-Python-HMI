"""Configuración del proyecto SCADA Monitor."""

# --- Conexión PLC Siemens S7 ---
PLC_IP = "192.168.148.130"  # IP del PLC en PLCSIM Advanced
PLC_RACK = 0
PLC_SLOT = 1  # S7-1200/1500 = slot 1, S7-300/400 = slot 2

# --- Variables del PLC a monitorear ---
# Formato: (nombre, dirección DB, offset, tipo)
# Tipos: bool, int, real
PLC_VARIABLES = [
    {"name": "Nivel Tanque (%)",     "db": 1, "offset": 0,  "type": "real",  "unit": "%"},
    {"name": "Temperatura (°C)",     "db": 1, "offset": 4,  "type": "real",  "unit": "°C"},
    {"name": "Presión (bar)",        "db": 1, "offset": 8,  "type": "real",  "unit": "bar"},
    {"name": "Caudal (L/min)",       "db": 1, "offset": 12, "type": "real",  "unit": "L/min"},
    {"name": "Bomba 1",              "db": 1, "offset": 16, "bit": 0, "type": "bool",  "unit": ""},
    {"name": "Bomba 2",              "db": 1, "offset": 16, "bit": 1, "type": "bool",  "unit": ""},
    {"name": "Válvula Entrada",      "db": 1, "offset": 16, "bit": 2, "type": "bool",  "unit": ""},
    {"name": "Válvula Salida",       "db": 1, "offset": 16, "bit": 3, "type": "bool",  "unit": ""},
    {"name": "Alarma Nivel Alto",    "db": 1, "offset": 16, "bit": 4, "type": "bool",  "unit": ""},
    {"name": "Alarma Temperatura",   "db": 1, "offset": 16, "bit": 5, "type": "bool",  "unit": ""},
]

# --- Dashboard ---
REFRESH_INTERVAL_SEC = 2
HISTORY_POINTS = 100  # Puntos de historial en gráficos

# --- Modo simulación (True = sin PLC real) ---
SIMULATION_MODE = True
