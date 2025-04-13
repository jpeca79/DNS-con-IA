🛡️ DNS Auditor con Shodan (GUI)

Este proyecto permite auditar servidores DNS expuestos en Internet utilizando la API de Shodan. La herramienta detecta servidores DNS públicos, prueba si resuelven dominios, si son recursivos y si son susceptibles a amplificación. Todo se presenta en una interfaz gráfica amigable.

──────────────────────────────
⚙️ Requisitos

- Python 3.8 o superior  
- Sistema operativo: Linux (desarrollado y probado en Kali Linux)
- Cuenta en Shodan.io (para obtener tu API Key)

──────────────────────────────
📦 Instalación de librerías

Ejecuta lo siguiente en tu terminal para instalar las dependencias necesarias:

pip install shodan dnspython

──────────────────────────────
🔑 Configurar la Shodan API Key

1. Abre el archivo dns_scanner.py con un editor de texto (Bloc de Notas, VSCode, etc.).
2. Reemplaza "TU_API_KEY_AQUI" por tu propia API Key de Shodan:

API_KEY = "TU_API_KEY_AQUI"

──────────────────────────────
🚀 Ejecutar la herramienta

Desde el directorio del proyecto, ejecuta el siguiente comando:

python3 gui_dns.py

──────────────────────────────
🧪 ¿Qué hace la herramienta?

- Busca IPs con el puerto 53 (DNS) abierto usando Shodan.
- Verifica:
  - Si el servidor DNS resuelve dominios conocidos (como google.com).
  - Si permite recursividad (potencial mal uso).
  - Si es vulnerable a ataques de amplificación DNS.
- Muestra los resultados en una tabla visual (checkbox para seleccionar).
- Guarda los resultados seleccionados en un archivo de texto resultados_guardados.txt.

──────────────────────────────
📝 Archivos principales

- dns_scanner.py → Contiene toda la lógica del escaneo y análisis DNS.
- gui_dns.py → Interfaz gráfica para ejecutar la auditoría.

──────────────────────────────
📂 Estructura sugerida del proyecto

dns_auditor/
├── dns_scanner.py
├── gui_dns.py
├── dominios.txt
├── resultados_guardados.txt
├── resultados_dns.json
├── README.txt

──────────────────────────────
✨ Ejemplo de uso

1. Escribe la cantidad de IPs a auditar.
2. Ingresa los dominios separados por comas (máximo 3 sugeridos).
3. Haz clic en “🔍 Buscar DNS”.
4. Revisa la tabla y marca los servidores que deseas guardar.
5. Presiona “💾 Guardar seleccionados” para almacenarlos en resultados_guardados.txt.

──────────────────────────────

¡Listo para usar y auditar!
