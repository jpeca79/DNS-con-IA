import json
from datetime import datetime

ARCHIVO_RESULTADOS = "resultados_dns.json"

def guardar_resultado(datos):
    entrada = {
        "fecha": datetime.now().isoformat(),
        **datos
    }
    try:
        with open(ARCHIVO_RESULTADOS, "a") as f:
            f.write(json.dumps(entrada) + "\n")
        print(f"[✓] Resultado guardado para {datos['ip']}")
    except Exception as e:
        print(f"[!] Error al guardar: {e}")

