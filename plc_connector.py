"""Conexión a PLC Siemens S7 usando python-snap7."""

import struct
import snap7
from snap7.util import get_bool
from config import PLC_IP, PLC_RACK, PLC_SLOT, PLC_VARIABLES


class S7Connector:
    def __init__(self, ip=PLC_IP, rack=PLC_RACK, slot=PLC_SLOT):
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.client = snap7.client.Client()
        self.connected = False

    def connect(self):
        try:
            self.client.connect(self.ip, self.rack, self.slot)
            self.connected = self.client.get_connected()
            return self.connected
        except Exception as e:
            print(f"Error conectando a PLC {self.ip}: {e}")
            self.connected = False
            return False

    def disconnect(self):
        if self.connected:
            self.client.disconnect()
            self.connected = False

    def read_all(self):
        """Lee todas las variables en una sola lectura eficiente."""
        if not self.connected:
            return {}
        try:
            data = self.client.db_read(1, 0, 18)
            return {
                "Nivel Tanque (%)":    round(struct.unpack(">f", data[0:4])[0], 1),
                "Temperatura (°C)":    round(struct.unpack(">f", data[4:8])[0], 1),
                "Presión (bar)":       round(struct.unpack(">f", data[8:12])[0], 2),
                "Caudal (L/min)":      round(struct.unpack(">f", data[12:16])[0], 1),
                "Bomba 1":             bool(data[16] & 0x01),
                "Bomba 2":             bool(data[16] & 0x02),
                "Válvula Entrada":     bool(data[16] & 0x04),
                "Válvula Salida":      bool(data[16] & 0x08),
                "Alarma Nivel Alto":   bool(data[16] & 0x10),
                "Alarma Temperatura":  bool(data[16] & 0x20),
            }
        except Exception as e:
            print(f"Error leyendo PLC: {e}")
            return {}

    def write_bool(self, db, offset, value):
        """Escribe un valor booleano al PLC."""
        try:
            data = bytearray(1)
            if value:
                data[0] = 0x01
            self.client.db_write(db, offset, data)
            return True
        except Exception as e:
            print(f"Error escribiendo DB{db}.{offset}: {e}")
            return False

    def write_real(self, db, offset, value):
        """Escribe un valor real (float) al PLC."""
        try:
            data = bytearray(struct.pack(">f", value))
            self.client.db_write(db, offset, data)
            return True
        except Exception as e:
            print(f"Error escribiendo DB{db}.{offset}: {e}")
            return False
