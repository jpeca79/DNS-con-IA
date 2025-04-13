import tkinter as tk
from tkinter import ttk, messagebox
from dns_scanner import buscar_dns_shodan, probar_resolucion_dns, probar_recursividad, detectar_amplificacion

# ---------------- INTERFAZ PRINCIPAL ----------------

ventana = tk.Tk()
ventana.title("Auditor DNS con Shodan")
ventana.geometry("1000x700")
ventana.configure(bg="#eef2f5")

selecciones = []

# ---------------- FUNCIONES ----------------

def buscar_dns():
    global selecciones
    selecciones.clear()
    for widget in tabla_frame.winfo_children():
        widget.destroy()

    try:
        cantidad = int(entry_cantidad.get())
        dominios = [d.strip() for d in entry_dominios.get().split(",") if d.strip()]
        if not dominios:
            messagebox.showerror("Error", "Debes ingresar al menos un dominio.")
            return

        servidores = buscar_dns_shodan(limit=cantidad)

        encabezados = ["✔", "IP", "Organización", "País", "Resuelve", "Dominio → Respuesta", "Recursiva", "Amplificación"]
        for col, header in enumerate(encabezados):
            ttk.Label(tabla_frame, text=header, style="Header.TLabel").grid(row=0, column=col, padx=8, pady=6, sticky="nsew")

        for i, (ip, org, pais) in enumerate(servidores):
            resuelve, dominio_usado, respuesta = probar_resolucion_dns(ip, dominios)
            recursiva = probar_recursividad(ip)
            amplificacion = detectar_amplificacion(ip)

            var = tk.BooleanVar()
            chk = ttk.Checkbutton(tabla_frame, variable=var)
            chk.grid(row=i+1, column=0)

            valor_respuesta = f"{dominio_usado} → {respuesta}" if resuelve else "-"

            valores = [ip, org, pais,
                       "✅" if resuelve else "❌",
                       valor_respuesta,
                       "✅" if recursiva else "❌",
                       "🟢" if amplificacion else "⚠"]

            for j, val in enumerate(valores):
                ttk.Label(tabla_frame, text=val).grid(row=i+1, column=j+1, padx=5, pady=3)

            selecciones.append((var, ip, org, pais, resuelve, dominio_usado, respuesta, recursiva, amplificacion))

    except ValueError:
        messagebox.showerror("Error", "La cantidad de IPs debe ser un número válido.")

def guardar_seleccionados():
    seleccionados = []
    for var, ip, org, pais, resuelve, dominio, respuesta, recursiva, amplificacion in selecciones:
        if var.get():
            texto = (
                f"IP: {ip} ({org}, {pais})\n"
                f"  ├─ Resuelve: {'✅' if resuelve else '❌'} - {dominio} → {respuesta}\n"
                f"  ├─ Recursiva: {'✅' if recursiva else '❌'}\n"
                f"  └─ Amplificación: {'🟢' if amplificacion else '⚠'}\n"
            )
            seleccionados.append(texto)

    if not seleccionados:
        messagebox.showinfo("Sin selección", "No seleccionaste ningún resultado para guardar.")
        return

    with open("resultados_guardados.txt", "w") as f:
        f.write("\n\n".join(seleccionados))

    messagebox.showinfo("Guardado", "Resultados guardados en 'resultados_guardados.txt'.")

# ---------------- ESTILO ----------------

style = ttk.Style()
style.theme_use("clam")
style.configure("Header.TLabel", font=("Helvetica", 10, "bold"), background="#dbe9f4")
style.configure("TLabel", background="#eef2f5")
style.configure("TButton", font=("Helvetica", 10, "bold"))
style.configure("TCheckbutton", background="#ffffff")

# ---------------- INTERFAZ SUPERIOR ----------------

ttk.Label(ventana, text="Auditor DNS con Shodan", font=("Helvetica", 22, "bold"),
          background="#eef2f5", foreground="#003366").pack(pady=15)

inputs_frame = ttk.Frame(ventana)
inputs_frame.pack(pady=5)

ttk.Label(inputs_frame, text="Cantidad de IPs a buscar:").grid(row=0, column=0, sticky="w", padx=5)
entry_cantidad = ttk.Entry(inputs_frame, width=10)
entry_cantidad.insert(0, "5")
entry_cantidad.grid(row=0, column=1, padx=10)

ttk.Label(inputs_frame, text="Dominios (separados por coma):").grid(row=1, column=0, sticky="w", padx=5)
entry_dominios = ttk.Entry(inputs_frame, width=60)
entry_dominios.insert(0, "google.com, cloudflare.com, facebook.com")
entry_dominios.grid(row=1, column=1, padx=10, pady=5)

ttk.Button(ventana, text="🔍 Buscar DNS", command=buscar_dns).pack(pady=10)

# ---------------- TABLA SCROLLABLE ----------------

canvas_frame = tk.Frame(ventana, bg="#eef2f5")
canvas_frame.pack(fill="both", expand=True, padx=20, pady=10)

canvas = tk.Canvas(canvas_frame, bg="#ffffff", highlightthickness=1)
scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

tabla_frame = scrollable_frame  # alias para mantener compatibilidad con el resto del código

# ---------------- BOTÓN GUARDAR ----------------

ttk.Button(ventana, text="💾 Guardar seleccionados", command=guardar_seleccionados).pack(pady=10)

# ---------------- INICIAR ----------------

ventana.mainloop()
