import os
import json
import shodan
import dns.resolver
import dns.message
import dns.query
import dns.flags
import socket
from tabulate import tabulate

API_KEY = "WMTqOFxBYrRPgqJaXmFbWuERTKBBXaWA"  # Reemplázala con tu API key válida
MAX_IPS = 10
DOMINIOS_FILE = "dominios.txt"
RESULTADOS_FILE = "resultados_dns.json"

def limpiar_resultados():
    with open(RESULTADOS_FILE, 'w') as f:
        json.dump([], f)

def cargar_dominios():
    if not os.path.exists(DOMINIOS_FILE):
        with open(DOMINIOS_FILE, 'w') as f:
            f.write("google.com\ncloudflare.com\nexample.com\n")
    with open(DOMINIOS_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()][:3]

def obtener_organizacion(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "N/A"

def buscar_dns_shodan(limit=10):
    print("[*] Buscando servidores DNS expuestos en Shodan...")
    api = shodan.Shodan(API_KEY)
    try:
        resultados = api.search('port:53 country:CO', limit=limit)
        ips = []
        for r in resultados['matches']:
            ip = r['ip_str']
            org = r.get('org', 'N/A')
            loc = r.get('location', {})
            pais = loc.get('country_name', 'N/A')
            ips.append((ip, org, pais))
        print(f"[+] Se analizarán {len(ips)} servidores DNS expuestos.\n")
        return ips
    except shodan.APIError as e:
        print(f"[!] Error en Shodan: {e}")
        return []

def probar_resolucion_dns(ip, dominios):
    for dominio in dominios:
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [ip]
            respuesta = resolver.resolve(dominio, lifetime=3)
            return True, dominio, respuesta[0].to_text()
        except:
            continue
    return False, "-", "-"

def probar_recursividad(ip):
    try:
        dominio_fake = "subdominio-no-existe-ejemplo.com"
        query = dns.message.make_query(dominio_fake, dns.rdatatype.A)
        response = dns.query.udp(query, ip, timeout=3)
        return bool(response.answer or response.additional or response.authority)
    except:
        return False

def detectar_amplificacion(ip):
    try:
        dominio = "google.com"
        query = dns.message.make_query(dominio, dns.rdatatype.ANY)
        response = dns.query.udp(query, ip, timeout=3)
        return len(response.to_wire()) > 512
    except:
        return False

def guardar_resultado(info):
    if os.path.exists(RESULTADOS_FILE):
        with open(RESULTADOS_FILE, 'r') as f:
            datos = json.load(f)
    else:
        datos = []
    datos.append(info)
    with open(RESULTADOS_FILE, 'w') as f:
        json.dump(datos, f, indent=2)

def main():
    limpiar_resultados()
    dominios = cargar_dominios()
    servidores = buscar_dns_shodan()

    resultados_tabla = []
    for ip, org, pais in servidores:
        print(f"[>] Analizando IP {ip} ({org}, {pais})")
        resuelve, dominio_usado, respuesta = probar_resolucion_dns(ip, dominios)
        recursiva = probar_recursividad(ip)
        amplificacion = detectar_amplificacion(ip)

        resultado = {
            "ip": ip,
            "organizacion": org,
            "pais": pais,
            "resuelve": resuelve,
            "dominio": dominio_usado,
            "respuesta": respuesta,
            "recursiva": recursiva,
            "amplificacion": amplificacion
        }

        guardar_resultado(resultado)
        print(f"[✓] Resultado guardado para {ip}")

        resultados_tabla.append([
            ip,
            org,
            pais,
            "✅" if resuelve else "❌",
            f"{dominio_usado} → {respuesta}" if resuelve else "-",
            "✅" if recursiva else "❌",
            "🟢" if amplificacion else "⚠"
        ])

    print("\n📋 Resultados del análisis:")
    print(tabulate(
        resultados_tabla,
        headers=["IP", "Organización", "País", "Resuelve", "Dominio → Respuesta", "Recursiva", "Amplificación"],
        tablefmt="grid"
    ))

if __name__ == "__main__":
    main()
