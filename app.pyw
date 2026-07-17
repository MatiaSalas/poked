import tkinter as tk
import json
import os
from datetime import datetime

# Versión de la aplicación
VERSION = "2.5"

# Directorio en tu carpeta de usuario para evitar bloqueos
CARPETA_USUARIO = os.path.expanduser("~")
ARCHIVO_DATOS = os.path.join(CARPETA_USUARIO, "poked_datos.json")
ARCHIVO_HISTORIAL = os.path.join(CARPETA_USUARIO, "poked_historial.json")
RUTA_ICONO = os.path.join(CARPETA_USUARIO, "poked_icono.ico")

# --- AUTOGENERADOR DE ÍCONO ---
def crear_icono_local():
    if not os.path.exists(RUTA_ICONO):
        datos_ico = b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x01\x00\x00\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00\x08\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x1e\'\x2c\x00\xf1\xc4\x0f\x00\xff\xff\xff\x00' + b'\x00'*1012 + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\x01\x01\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\x01\x01\x01\x01\x01\x02\x00\x00\x00\x00\x00\x00\x02\x01\x01\x01\x01\x01\x01\x01\x01\x01\x02\x00\x00\x00\x00\x00\x00\x02\x01\x01\x01\x01\x01\x01\x01\x01\x01\x02\x00\x00\x00\x00\x00\x00\x00\x02\x01\x01\x01\x01\x01\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\x01\x01\x01\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\x01\x01\x01\x01\x02\x00\x00\x00\x00\x00\x00\x00\x02\x01\x01\x02\x02\x01\x01\x02\x00\x00\x00\x00\x00\x00\x02\x01\x01\x02\x00\x02\x01\x01\x02\x00\x00\x00\x00\x00\x02\x01\x02\x00\x00\x00\x02\x01\x02\x00\x00\x00\x00\x00\x02\x02\x00\x00\x00\x00\x00\x02\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\xff\xff\x00\x00\xfc\x3f\x00\x00\xf8\x1f\x00\x00\xf0\x0f\x00\x00\xe0\x07\x00\x00\xc0\x03\x00\x00\x80\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\x00\x00\xc0\x03\x00\x00\xe0\x07\x00\x00\xf0\x0f\x00\x00\xf8\x1f\x00\x00\xfc\x3f\x00\x00'
        try:
            with open(RUTA_ICONO, "wb") as f:
                f.write(datos_ico)
        except:
            pass

crear_icono_local()

class PokedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Poked")
        
        # --- CONFIGURACIÓN ULTRA COMPACTA ---
        self.root.attributes("-topmost", True)  # Siempre visible arriba
        self.root.overrideredirect(True)       # Sin bordes nativos
        self.root.geometry("280x40")           
        
        # Intentar cargar el ícono generado
        if os.path.exists(RUTA_ICONO):
            try:
                self.root.iconbitmap(RUTA_ICONO)
            except:
                pass
        
        # Arrastre de ventana con el mouse
        self.root.bind("<ButtonPress-1>", self.iniciar_movimiento)
        self.root.bind("<B1-Motion>", self.mover_ventana)
        
        # Paleta de colores
        self.bg_principal = "#1E272C"
        self.bg_card = "#2C3E50"
        self.fg_blanco = "#ECF0F1"
        self.verde_abrir = "#2ECC71"
        self.rojo_cerrar = "#E74C3C"
        self.azul_agregar = "#3498DB"
        self.color_estrella = "#F1C40F"
        self.color_apagado = "#7F8C8D"
        self.color_version = "#5D6D7E"  # Gris sutil para la versión
        
        self.root.config(bg=self.bg_principal)
        
        self.tareas = self.cargar_tareas()
        self.caja_abierta = False
        
        # Contenedor principal
        self.frame_principal = tk.Frame(root, bg=self.bg_principal)
        self.frame_principal.pack(fill="both", expand=True, padx=4, pady=4)
        
        # Botón verde para abrir (visible solo cuando está cerrada)
        self.btn_accion = tk.Button(
            self.frame_principal, 
            text="Abrir Caja", 
            command=self.conmutar_caja, 
            bg=self.verde_abrir, 
            fg="white", 
            font=("Arial", 9, "bold"), 
            bd=0, 
            height=1, 
            relief="flat",
            cursor="hand2",
            activebackground="#27AE60",
            activeforeground="white"
        )
        self.btn_accion.pack(fill="x", side="top")
        
        # Contenedor para todo lo que aparece al abrir la caja
        self.frame_contenido = tk.Frame(self.frame_principal, bg=self.bg_principal)
        
        # Barra de entrada de texto para nueva tarea
        self.frame_entrada = tk.Frame(self.frame_contenido, bg=self.bg_principal)
        
        self.txt_nueva_tarea = tk.Entry(
            self.frame_entrada, 
            font=("Arial", 9), 
            bg="#2C3E50", 
            fg="white", 
            insertbackground="white", 
            bd=0, 
            highlightthickness=1, 
            highlightbackground="#34495E", 
            highlightcolor=self.azul_agregar
        )
        self.txt_nueva_tarea.bind("<Return>", lambda event: self.agregar_tarea())
        
        self.btn_agregar = tk.Button(
            self.frame_entrada, 
            text=" + ", 
            command=self.agregar_tarea, 
            bg=self.azul_agregar, 
            fg="white", 
            font=("Arial", 9, "bold"), 
            bd=0, 
            padx=8, 
            cursor="hand2",
            activebackground="#2980B9",
            activeforeground="white"
        )

        # --- SISTEMA DE SCROLL ---
        self.contenedor_scroll = tk.Frame(self.frame_contenido, bg=self.bg_principal)
        self.canvas = tk.Canvas(self.contenedor_scroll, bg=self.bg_principal, bd=0, highlightthickness=0)
        self.lista_frame = tk.Frame(self.canvas, bg=self.bg_principal)
        
        self.window_id = self.canvas.create_window((0, 0), window=self.lista_frame, anchor="nw")
        
        self.canvas.bind('<Configure>', self.ajustar_ancho_interno)
        self.lista_frame.bind('<Configure>', self.actualizar_scroll_region)
        self.root.bind_all("<MouseWheel>", self.on_mousewheel)

        # --- PIE DE VENTANA (Versión + Botón Cierre real y grande) ---
        self.frame_pie = tk.Frame(self.frame_contenido, bg=self.bg_principal)
        
        self.lbl_version = tk.Label(
            self.frame_pie, 
            text=f"v{VERSION}", 
            bg=self.bg_principal, 
            fg=self.color_version, 
            font=("Arial", 8, "italic")
        )
        
        self.btn_cierre_rapido = tk.Button(
            self.frame_pie,
            text="Cierre de caja",
            command=self.conmutar_caja,
            bg=self.rojo_cerrar,
            fg="white",
            font=("Arial", 8, "bold"),
            bd=0,
            padx=16,
            pady=4,
            cursor="hand2",
            activebackground="#C0392B",
            activeforeground="white"
        )

    def ajustar_ancho_interno(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)

    def actualizar_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        if self.caja_abierta:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def iniciar_movimiento(self, event):
        self.x = event.x
        self.y = event.y

    def mover_ventana(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def cargar_tareas(self):
        if os.path.exists(ARCHIVO_DATOS):
            try:
                with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                    importadas = json.load(f)
                    tareas_limpias = []
                    for t in importadas:
                        if isinstance(t, str):
                            tareas_limpias.append({"texto": t, "prioridad": False})
                        else:
                            tareas_limpias.append(t)
                    return tareas_limpias
            except:
                return []
        return []

    def guardar_tareas(self):
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(self.tareas, f, ensure_ascii=False)

    def registrar_en_historial(self, tarea_texto):
        historial = []
        if os.path.exists(ARCHIVO_HISTORIAL):
            try:
                with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
                    historial = json.load(f)
            except:
                pass
        
        registro = {
            "tarea": tarea_texto,
            "fecha_completada": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        historial.append(registro)
        
        with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as f:
            json.dump(historial, f, ensure_ascii=False, indent=4)

    def conmutar_caja(self):
        alto_cerrado = 40
        alto_abierto = 340  
        ancho = 280
        
        x_actual = self.root.winfo_x()
        y_actual = self.root.winfo_y()
        alto_pantalla = self.root.winfo_screenheight()
        en_mitad_inferior = y_actual > (alto_pantalla / 2)

        if not self.caja_abierta:
            self.caja_abierta = True
            self.btn_accion.pack_forget()
            
            if en_mitad_inferior:
                nueva_y = y_actual - (alto_abierto - alto_cerrado)
                self.root.geometry(f"{ancho}x{alto_abierto}+{x_actual}+{nueva_y}")
            else:
                self.root.geometry(f"{ancho}x{alto_abierto}+{x_actual}+{y_actual}")
                
            self.frame_contenido.pack(fill="both", expand=True)
            
            # 1. ENTRADA ARRIBA
            self.frame_entrada.pack(fill="x", side="top", pady=(3, 4))
            self.txt_nueva_tarea.pack(side="left", fill="x", expand=True, padx=(0, 4), ipady=2)
            self.btn_agregar.pack(side="right", ipady=1)
            
            # 2. PIE ABAJO (Inamovible, con prioridad total de espacio)
            self.frame_pie.pack(fill="x", side="bottom", pady=(6, 4))
            self.lbl_version.pack(side="left", padx=(4, 0))
            self.btn_cierre_rapido.pack(side="right", padx=(0, 4))
            
            # 3. SCROLL EN EL MEDIO (Toma el resto)
            self.contenedor_scroll.pack(fill="both", expand=True, pady=(2, 2))
            self.canvas.pack(fill="both", expand=True)
                
            self.actualizar_lista_visual()
        else:
            self.caja_abierta = False
            self.frame_contenido.pack_forget()
            self.frame_entrada.pack_forget()
            self.contenedor_scroll.pack_forget()
            self.canvas.pack_forget()
            self.frame_pie.pack_forget()
            self.lbl_version.pack_forget()
            self.btn_cierre_rapido.pack_forget()
            
            # Al presionar el botón rojo cuando ya está abierta, cerramos la app por completo
            self.root.destroy()

    def agregar_tarea(self):
        texto = self.txt_nueva_tarea.get().strip()
        if texto:
            self.tareas.append({"texto": texto, "prioridad": False})
            self.guardar_tareas()
            self.txt_nueva_tarea.delete(0, tk.END)
            self.actualizar_lista_visual()
            self.canvas.yview_moveto(1.0)

    def gestionar_check(self, indice_real):
        tarea_resuelta = self.tareas.pop(indice_real)
        self.registrar_en_historial(tarea_resuelta["texto"])
        self.guardar_tareas()
        self.actualizar_lista_visual()

    def conmutar_prioridad(self, indice_real):
        tarea = self.tareas[indice_real]
        cant_prioritarias = sum(1 for t in self.tareas if t["prioridad"])
        
        if not tarea["prioridad"]:
            if cant_prioritarias >= 3:
                return
            tarea["prioridad"] = True
        else:
            tarea["prioridad"] = False
            
        self.guardar_tareas()
        self.actualizar_lista_visual()

    def actualizar_lista_visual(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
            
        tareas_con_id = [(idx, t) for idx, t in enumerate(self.tareas)]
        prioritarias = [item for item in tareas_con_id if item[1]["prioridad"]]
        normales = [item for item in tareas_con_id if not item[1]["prioridad"]]
        lista_ordenada = prioritarias + normales
        
        for idx_real, tarea in lista_ordenada:
            frame_item = tk.Frame(self.lista_frame, bg=self.bg_card, bd=0)
            frame_item.pack(fill="x", pady=2, ipady=1)
            
            btn_check = tk.Button(
                frame_item, 
                text="●", 
                command=lambda idx=idx_real: self.gestionar_check(idx), 
                bg=self.verde_abrir, 
                fg="white", 
                font=("Arial", 7, "bold"),
                width=2,
                height=1,
                bd=0,
                cursor="hand2",
                activebackground="#27AE60"
            )
            btn_check.pack(side="left", padx=(4, 6))
            
            peso_letra = "bold" if tarea["prioridad"] else "normal"
            lbl_tarea = tk.Label(
                frame_item, 
                text=tarea["texto"], 
                anchor="w", 
                font=("Arial", 9, peso_letra), 
                bg=self.bg_card, 
                fg=self.fg_blanco, 
                justify="left"
            )
            lbl_tarea.pack(side="left", fill="x", expand=True)
            
            color_star = self.color_estrella if tarea["prioridad"] else self.color_apagado
            btn_star = tk.Button(
                frame_item,
                text="★",
                command=lambda idx=idx_real: self.conmutar_prioridad(idx),
                bg=self.bg_card,
                fg=color_star,
                font=("Arial", 10),
                bd=0,
                cursor="hand2",
                activebackground=self.bg_card,
                activeforeground=self.color_estrella
            )
            btn_star.pack(side="right", padx=(3, 5))
            
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = PokedApp(root)
    root.mainloop()
