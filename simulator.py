"""Simulador de proceso industrial — funciona sin PLC real."""

import math
import random
import time


class ProcessSimulator:
    """Simula un tanque con control de nivel, temperatura y presión."""

    def __init__(self):
        self.start_time = time.time()
        self.nivel = 50.0
        self.temperatura = 25.0
        self.presion = 2.0
        self.caudal = 0.0
        self.bomba1 = False
        self.bomba2 = False
        self.valvula_entrada = True
        self.valvula_salida = False
        self.alarma_nivel = False
        self.alarma_temp = False

    def update(self):
        """Actualiza la simulación un paso."""
        t = time.time() - self.start_time

        # El nivel sube si la válvula de entrada está abierta, baja si la de salida está abierta
        if self.valvula_entrada:
            self.nivel += random.uniform(0.3, 0.8)
        if self.valvula_salida:
            self.nivel -= random.uniform(0.4, 1.0)
        # Las bombas también afectan
        if self.bomba1:
            self.nivel += random.uniform(0.1, 0.3)
        if self.bomba2:
            self.nivel += random.uniform(0.1, 0.3)

        self.nivel = max(0, min(100, self.nivel))

        # Temperatura oscila con algo de ruido
        self.temperatura = 45 + 15 * math.sin(t / 30) + random.uniform(-1, 1)
        self.temperatura = max(10, min(90, self.temperatura))

        # Presión correlacionada con nivel
        self.presion = 1.0 + (self.nivel / 100) * 4.0 + random.uniform(-0.1, 0.1)
        self.presion = max(0, min(6, self.presion))

        # Caudal depende de bombas
        base_caudal = 0
        if self.bomba1:
            base_caudal += 25
        if self.bomba2:
            base_caudal += 25
        self.caudal = base_caudal + random.uniform(-2, 2) if base_caudal > 0 else 0

        # Control automático simple
        if self.nivel > 85:
            self.valvula_entrada = False
            self.valvula_salida = True
        elif self.nivel < 15:
            self.valvula_entrada = True
            self.valvula_salida = False

        # Alarmas
        self.alarma_nivel = self.nivel > 80 or self.nivel < 10
        self.alarma_temp = self.temperatura > 70

        # Activar bombas según nivel
        self.bomba1 = self.nivel < 60
        self.bomba2 = self.nivel < 30

    def read_all(self):
        """Retorna todas las variables en el mismo formato que el PLC real."""
        self.update()
        return {
            "Nivel Tanque (%)":    round(self.nivel, 1),
            "Temperatura (°C)":    round(self.temperatura, 1),
            "Presión (bar)":       round(self.presion, 2),
            "Caudal (L/min)":      round(self.caudal, 1),
            "Bomba 1":             self.bomba1,
            "Bomba 2":             self.bomba2,
            "Válvula Entrada":     self.valvula_entrada,
            "Válvula Salida":      self.valvula_salida,
            "Alarma Nivel Alto":   self.alarma_nivel,
            "Alarma Temperatura":  self.alarma_temp,
        }
