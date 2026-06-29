"""Script para probar la conexión con el PLC Siemens."""

import sys
from config import PLC_IP, PLC_RACK, PLC_SLOT

print("=" * 50)
print("  SCADA Monitor — Test de Conexión S7")
print("=" * 50)
print(f"\nConectando a PLC: {PLC_IP} (rack={PLC_RACK}, slot={PLC_SLOT})")

try:
    import snap7
except ImportError:
    print("\n[ERROR] snap7 no está instalado.")
    print("Ejecuta: pip install python-snap7")
    sys.exit(1)

client = snap7.client.Client()
try:
    client.connect(PLC_IP, PLC_RACK, PLC_SLOT)
    if client.get_connected():
        print("[OK] Conexión exitosa!")

        info = client.get_cpu_info()
        print(f"\n  Módulo:    {info.ModuleTypeName.decode()}")
        print(f"  Serie:     {info.SerialNumber.decode()}")
        print(f"  Nombre:    {info.ModuleName.decode()}")

        state = client.get_cpu_state()
        print(f"  Estado:    {state}")

        print("\nLeyendo DB1 (primeros 24 bytes)...")
        try:
            data = client.db_read(1, 0, 24)
            print(f"  [OK] DB1 leído: {data.hex()}")
        except Exception as e:
            print(f"  [WARN] No se pudo leer DB1: {e}")
            print("  Asegúrate de tener un DB1 creado en tu programa TIA Portal.")

        client.disconnect()
        print("\n[OK] Test completado. ¡Todo listo para usar el dashboard!")
    else:
        print("[ERROR] No se pudo conectar.")
except Exception as e:
    print(f"\n[ERROR] {e}")
    print("\nVerifica:")
    print(f"  1. ¿El PLC/PLCSIM está corriendo en {PLC_IP}?")
    print("  2. ¿La IP es correcta? (edita config.py)")
    print("  3. ¿Hay conexión de red entre tu PC y la VM?")
    print("  4. ¿El programa del PLC tiene un DB1?")
    print('  5. ¿El acceso al DB está en "Full" (no optimizado) en TIA Portal?')
