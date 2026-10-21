import tkinter as tk
from tkinter import ttk, messagebox
from conexion import inicializar_base_de_datos
from datos import GestorDatos

# ============================================================
# COLORES
# ============================================================

BG        = "#ffffff"
MARRON    = "#57a076"
MARRON_CL = "#a4b693"
GRIS      = "#595959"
GRIS_TXT  = "#d9d9d9"
NEGRO     = "#1a1a1a"
CAMPO     = "#d3d0ca"
BORDE     = "#7a7a7a"
TEAL      = "#4ad3d7"

# ============================================================
# FUENTES / TAMAÑO
# ============================================================

F_TITULO = ("Arial", 20)
F_GRANDE = ("Arial", 16)
F_TXT    = ("Arial", 10)
F_CHICA  = ("Arial", 8)
F_BTN    = ("Arial", 9)

ANCHO, ALTO = 920, 580


# ============================================================
# FUNCIONES AUXILIARES DE TABLAS Y SELECCIÓN
# ============================================================

def filas_vacias(tv, n=7):
    for item in tv.get_children():
        tv.delete(item)
    for _ in range(n):
        tv.insert("", "end", values=[""] * len(tv["columns"]))


def cargar(tv, filas, minimo=7):
    for item in tv.get_children():
        tv.delete(item)
    for fila in filas:
        tv.insert("", "end", values=fila)
    for _ in range(max(0, minimo - len(filas))):
        tv.insert("", "end", values=[""] * len(tv["columns"]))


def id_seleccionado(tv):
    seleccion = tv.selection()
    if not seleccion:
        return None
    valores = tv.item(seleccion[0], "values")
    if not valores or str(valores[0]).strip() == "":
        return None
    try:
        return int(valores[0])
    except ValueError:
        return None


# ============================================================
# ENTRY CON PLACEHOLDER
# ============================================================

class EntradaPlaceholder(tk.Entry):
    def __init__(self, padre, texto_guia, oculto=False, **kw):
        super().__init__(padre, **kw)

        self.texto_guia = texto_guia
        self.oculto = oculto
        self._vacio = True

        self._poner_guia()

        self.bind(
            "<FocusIn>",
            self._entrar
        )

        self.bind(
            "<FocusOut>",
            self._salir
        )

    def _poner_guia(self):
        self.config(show="")
        self.delete(0, "end")
        self.insert(0, self.texto_guia)
        self._vacio = True

        self.config(fg="#888888")

    def _entrar(self, _=None):
        if self._vacio:
            self.delete(0, "end")
            self._vacio = False

            
            self.config(fg=NEGRO)

            if self.oculto:
                self.config(show="*")

    def _salir(self, _=None):
        if not self.get().strip():
            self._poner_guia()

    def valor(self):
        return "" if self._vacio else self.get()

# ============================================================
# PANTALLA BASE
# ============================================================

class Pantalla(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=BG)
        self.app = app
        self.construir()

    def construir(self):
        raise NotImplementedError


# ============================================================
# LOGIN
# ============================================================

class Login(Pantalla):
    def construir(self):
        
        centro = tk.Frame(self, bg=BG)
        centro.pack(pady=(40, 0))

        
        tk.Label(
            centro, text="CONTABILIDAD FACIL", bg=MARRON, fg=NEGRO, 
            font=F_TITULO, padx=300, pady=20
        ).pack(pady=(0, 100))

        
        caja_inputs = tk.Frame(centro, bg=BG)
        caja_inputs.pack()

       
        self.usuario = EntradaPlaceholder(
            caja_inputs, "Usuario", bg=MARRON_CL, fg=GRIS_TXT, font=F_GRANDE,
            justify="center", relief="flat", insertbackground=NEGRO, width=50
        )
        self.usuario.pack(pady=8, ipady=8)

        self.clave = EntradaPlaceholder(
            caja_inputs, "Contraseña", oculto=True, bg=MARRON_CL, fg=GRIS_TXT,
            font=F_GRANDE, justify="center", relief="flat", insertbackground=NEGRO, width=50
        )
        self.clave.pack(pady=8, ipady=8)

        btn = tk.Button(
            caja_inputs, text="INGRESAR", bg=MARRON_CL, fg=NEGRO, font=F_GRANDE,
            relief="flat", bd=0, activebackground="#ab948a",
            cursor="hand2", command=self.entrar
        )
        btn.pack(fill="x", pady=15, ipady=8)

        self.usuario.bind("<Return>", self.entrar)
        self.clave.bind("<Return>", self.entrar)

    def entrar(self, _=None):
        usuario_ingresado = self.usuario.valor()
        clave_ingresada = self.clave.valor()

        if not usuario_ingresado:
            messagebox.showwarning("Contabilidad Fácil", "Ingresá un usuario.")
            return
        if not clave_ingresada:
            messagebox.showwarning("Contabilidad Fácil", "Ingresá una contraseña.")
            return

        if self.app.verificar_usuario(usuario_ingresado, clave_ingresada):
            self.app.mostrar("Clientes")
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")

    

# ============================================================
# CLIENTES - MENÚ
# ============================================================

class Clientes(Pantalla):
    def construir(self):
        top_bar = tk.Frame(self, bg=BG)
        top_bar.pack(side="top", fill="x", padx=20, pady=20)

        tk.Button(
            top_bar, text="Gestionar clientes", bg=GRIS, fg=GRIS_TXT, font=F_BTN,
            relief="flat", bd=0, command=lambda: self.app.mostrar("GestionClientes")
        ).pack(side="right")

        centro = tk.Frame(self, bg=BG)
        centro.pack(expand=True)

        marco = tk.Frame(centro, bg=MARRON_CL)
        marco.pack(padx=20, pady=20, ipadx=20, ipady=20)

        tk.Label(marco, text="Clientes", bg=MARRON_CL, fg=NEGRO, font=F_TITULO).pack(pady=10)

        caja = tk.Frame(marco, bg="#e9e7e2", highlightthickness=2, highlightbackground="#8a8a8a", cursor="hand2")
        caja.pack(padx=20, pady=10, ipadx=40, ipady=40)

        self.texto_preview = tk.Text(
            caja, bg="#e9e7e2", fg=NEGRO, font=("Arial", 18),
            relief="flat", highlightthickness=0, width=32, height=6, wrap="word"
        )
        self.texto_preview.tag_configure("centro", justify="center")
        self.texto_preview.pack(padx=10, pady=10)
        
        self.texto_preview.config(state="disabled")

        self.texto_preview.bind("<Button-1>", lambda e: self.app.mostrar("GestionClientes"))
        caja.bind("<Button-1>", lambda e: self.app.mostrar("GestionClientes"))
        footer = tk.Frame(self, bg=BG)
        footer.pack(side="bottom", fill="x", padx=40, pady=20)

        self.lbl_activos = tk.Label(footer, text="Clientes activos: 0", bg=BG, fg=NEGRO, font=F_TXT)
        self.lbl_activos.pack(side="left")

        tk.Label(footer, text="Pendientes: 12", bg=BG, fg=NEGRO, font=F_TXT).pack(side="right")

    def al_mostrar(self):
        activos = sum(1 for c in self.app.clientes if c["activo"])
        self.lbl_activos.config(text=f"Clientes activos: {activos}")

        self.texto_preview.config(state="normal")
        self.texto_preview.delete("1.0", "end")

        if not self.app.clientes:
            self.texto_preview.insert("1.0", "(No hay clientes cargados)", "centro")
        else:
            # Unimos los nombres de los clientes con saltos de línea
            nombres = [c["nombre"] for c in self.app.clientes]
            texto_unido = "\n".join(nombres)
            self.texto_preview.insert("1.0", texto_unido, "centro")

        # Volvemos a bloquearlo para que no sea editable
        self.texto_preview.config(state="disabled")

# ============================================================
# GESTIÓN DE CLIENTES
# ============================================================

class GestionClientes(Pantalla):
    def construir(self):
        top_bar = tk.Frame(self, bg=BG)
        top_bar.pack(side="top", fill="x", padx=20, pady=20)

        tk.Button(
            top_bar, text="◀", bg="#111111", fg="white", font=("Arial", 7),
            relief="flat", bd=0, command=lambda: self.app.mostrar("Clientes")
        ).pack(side="left", padx=(0, 10))

        tk.Label(
            top_bar, text="Gestión de clientes", bg=MARRON, fg=NEGRO, font=F_TITULO, padx=60, pady=10
        ).pack(side="top")

        tk.Button(
            top_bar, text="[+ Nuevo]", bg=GRIS, fg=GRIS_TXT, font=F_BTN,
            relief="flat", bd=0, command=self.nuevo
        ).pack(side="right")

        search_bar = tk.Frame(self, bg=BG)
        search_bar.pack(side="top", fill="x", padx=40, pady=10)
        
        tk.Label(search_bar, text="Buscar:", bg=BG, fg=NEGRO, font=F_TXT).pack(side="left", padx=(0, 10))
        
        self.buscar = tk.Entry(
            search_bar, bg=CAMPO, fg=NEGRO, font=F_TXT, relief="flat",
            highlightthickness=1, highlightbackground="#b8b4ac"
        )
        self.buscar.pack(side="left", fill="x", expand=True, ipady=3)
        self.buscar.bind("<Return>", lambda ev: self.refrescar())

        tk.Button(
            search_bar, text="🔍", bg=TEAL, fg=NEGRO, font=F_TXT, relief="flat",
            command=self.refrescar
        ).pack(side="left", padx=10)

        table_frame = tk.Frame(self, bg="#ffffff", highlightthickness=2, highlightbackground=BORDE)
        table_frame.pack(side="top", fill="both", expand=True, padx=40, pady=10)

        columnas = ("id", "Nombre", "CUIT", "Activo")
        self.tabla = ttk.Treeview(table_frame, columns=columnas, show="headings", style="Maq.Treeview", selectmode="browse")
        anchos = (90, 280, 180, 140)
        for col, an in zip(columnas, anchos):
            self.tabla.heading(col, text=col, anchor="center")
            self.tabla.column(col, width=an, anchor="center", stretch=True)
        self.tabla.pack(fill="both", expand=True, padx=3, pady=3)
        self.tabla.bind("<Double-1>", lambda e: self.editar())
        filas_vacias(self.tabla)

        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(side="bottom", fill="x", padx=40, pady=20)

        tk.Button(btn_frame, text="[Ver]", bg=GRIS, fg=GRIS_TXT, font=F_BTN, relief="flat", command=lambda: self.app.mostrar("MenuMovimientos")).pack(side="left", expand=True, padx=5, ipady=5)
        tk.Button(btn_frame, text="[Editar]", bg=GRIS, fg=GRIS_TXT, font=F_BTN, relief="flat", command=self.editar).pack(side="left", expand=True, padx=5, ipady=5)
        tk.Button(btn_frame, text="[Eliminar]", bg=GRIS, fg=GRIS_TXT, font=F_BTN, relief="flat", command=self.eliminar).pack(side="left", expand=True, padx=5, ipady=5)

    def al_mostrar(self):
        self.refrescar()

    def refrescar(self):
        filtro = self.buscar.get().strip().lower()
        filas = []
        for c in self.app.clientes:
            if filtro and filtro not in c["nombre"].lower() and filtro not in c["cuit"].lower():
                continue
            filas.append((c["id_cliente"], c["nombre"], c["cuit"], "Sí" if c["activo"] else "No"))
        cargar(self.tabla, filas)

    def nuevo(self):
        self.app.cliente_edicion = None
        self.app.mostrar("EditarCliente")

    def editar(self):
        cliente_id = id_seleccionado(self.tabla)
        if cliente_id is None:
            messagebox.showinfo("Contabilidad Fácil", "Primero seleccioná un cliente.")
            return
        self.app.cliente_edicion = cliente_id
        self.app.mostrar("EditarCliente")

    def eliminar(self):
        cliente_id = id_seleccionado(self.tabla)
        if cliente_id is None:
            messagebox.showinfo("Contabilidad Fácil", "Primero seleccioná un cliente.")
            return
        cliente = self.app.obtener_cliente(cliente_id)
        if not messagebox.askyesno("Confirmar eliminación", f"¿Eliminar a «{cliente['nombre']}»?"):
            return
        self.app.eliminar_cliente(cliente_id)
        self.refrescar()


# ============================================================
# EDITAR CLIENTE
# ============================================================

class EditarCliente(Pantalla):
    CAMPOS = ["Nombre", "CUIT", "Email", "Teléfono", "Dirección"]

    def construir(self):
        top_bar = tk.Frame(self, bg=BG)
        top_bar.pack(side="top", fill="x", padx=20, pady=20)

        tk.Button(
            top_bar, text="◀", bg="#111111", fg="white", font=("Arial", 7),
            relief="flat", bd=0, command=lambda: self.app.mostrar("GestionClientes")
        ).pack(side="left", padx=(0, 10))

        self.titulo = tk.Label(top_bar, text="EDITAR CLIENTE", bg=BG, fg=NEGRO, font=("Arial", 18))
        self.titulo.pack(side="left")

        tk.Button(
            top_bar, text="[Guardar]", bg=GRIS, fg=GRIS_TXT, font=F_BTN,
            relief="flat", bd=0, command=self.guardar
        ).pack(side="right")

        form_frame = tk.Frame(self, bg=BG)
        form_frame.pack(side="top", fill="both", expand=True, padx=80, pady=20)

        self.entradas = {}
        for i, nombre in enumerate(self.CAMPOS):
            tk.Label(form_frame, text=f"{nombre}:", bg=BG, fg=NEGRO, font=F_TXT, anchor="e").grid(row=i, column=0, sticky="e", padx=10, pady=8)
            e = tk.Entry(form_frame, bg=CAMPO, fg=NEGRO, font=F_TXT, relief="flat", insertbackground=NEGRO)
            e.grid(row=i, column=1, sticky="ew", padx=10, pady=8, ipady=3)
            self.entradas[nombre] = e

        tk.Label(form_frame, text="Activo:", bg=BG, fg=NEGRO, font=F_TXT, anchor="e").grid(row=len(self.CAMPOS), column=0, sticky="e", padx=10, pady=8)
        self.activo = tk.BooleanVar(value=True)
        tk.Checkbutton(
            form_frame, variable=self.activo, bg=BG, activebackground=BG,
            selectcolor="#ffffff", bd=0, highlightthickness=0
        ).grid(row=len(self.CAMPOS), column=1, sticky="w", padx=10, pady=8)

        form_frame.columnconfigure(1, weight=1)

    def al_mostrar(self):
        for entrada in self.entradas.values():
            entrada.delete(0, "end")
        cliente_id = self.app.cliente_edicion
        if cliente_id is None:
            self.titulo.config(text="NUEVO CLIENTE")
            self.activo.set(True)
        else:
            self.titulo.config(text="EDITAR CLIENTE")
            cliente = self.app.obtener_cliente(cliente_id)
            for campo in self.CAMPOS:
                self.entradas[campo].insert(0, cliente.get(campo, ""))
            self.activo.set(bool(cliente.get("Activo", True)))
        self.entradas["Nombre"].focus_set()

    def guardar(self):
        datos_cliente = {campo: self.entradas[campo].get().strip() for campo in self.CAMPOS}
        if not datos_cliente["Nombre"]:
            messagebox.showwarning("Datos incompletos", "El nombre del cliente es obligatorio.")
            return
        datos_cliente["Activo"] = self.activo.get()
        if self.app.cliente_edicion is None:
            self.app.agregar_cliente(datos_cliente)
            messagebox.showinfo("Contabilidad Fácil", "Cliente agregado correctamente.")
        else:
            self.app.actualizar_cliente(self.app.cliente_edicion, datos_cliente)
            messagebox.showinfo("Contabilidad Fácil", "Cliente actualizado correctamente.")
        self.app.mostrar("GestionClientes")


# ============================================================
# MENÚ DE MOVIMIENTOS
# ============================================================

class MenuMovimientos(Pantalla):
    def construir(self):
        centro = tk.Frame(self, bg=BG)
        centro.pack(expand=True)

        tk.Button(
            centro, text="Pagos", bg=MARRON_CL, fg=NEGRO, font=F_GRANDE,
            relief="flat", bd=0, command=lambda: self.app.mostrar("Pagos")
        ).pack(fill="x", pady=10, ipady=15, ipadx=40)

        tk.Button(
            centro, text="Movimientos", bg=MARRON_CL, fg=NEGRO, font=F_GRANDE,
            relief="flat", bd=0, command=lambda: self.app.mostrar("Movimientos")
        ).pack(fill="x", pady=10, ipady=15, ipadx=40)

        tk.Button(
            centro, text="Facturas", bg=MARRON_CL, fg=NEGRO, font=F_GRANDE,
            relief="flat", bd=0, command=lambda: self.app.mostrar("Facturas")
        ).pack(fill="x", pady=10, ipady=15, ipadx=40)

        footer = tk.Frame(self, bg=BG)
        footer.pack(side="bottom", fill="x", padx=20, pady=20)
        tk.Button(
            footer, text="Atrás", bg=GRIS, fg=GRIS_TXT, font=F_BTN,
            relief="flat", bd=0, command=lambda: self.app.mostrar("GestionClientes")
        ).pack(side="right", ipadx=10, ipady=5)


# ============================================================
# FORMULARIO GENÉRICO DE FACTURA
# ============================================================

class EditarFactura(Pantalla):
    def construir(self):
        top_bar = tk.Frame(self, bg=BG)
        top_bar.pack(side="top", fill="x", padx=20, pady=20)

        tk.Button(
            top_bar, text="◀", bg="#111111", fg="white", font=("Arial", 7),
            relief="flat", bd=0, command=lambda: self.app.mostrar("Facturas")
        ).pack(side="left", padx=(0, 10))

        self.titulo = tk.Label(top_bar, text="NUEVA FACTURA", bg=BG, fg=NEGRO, font=("Arial", 18))
        self.titulo.pack(side="left")

        tk.Button(
            top_bar, text="[Guardar]", bg=GRIS, fg=GRIS_TXT, font=F_BTN,
            relief="flat", bd=0, command=self.guardar
        ).pack(side="right")

        form_frame = tk.Frame(self, bg=BG)
        form_frame.pack(side="top", fill="both", expand=True, padx=80, pady=20)

        self.entradas = {}
        campos = ["Cliente", "Fecha", "Importe", "Estado"]
        for i, nombre in enumerate(campos):
            tk.Label(form_frame, text=f"{nombre}:", bg=BG, fg=NEGRO, font=F_TXT, anchor="e").grid(row=i, column=0, sticky="e", padx=10, pady=8)
            e = tk.Entry(form_frame, bg=CAMPO, fg=NEGRO, font=F_TXT, relief="flat", insertbackground=NEGRO)
            e.grid(row=i, column=1, sticky="ew", padx=10, pady=8, ipady=3)
            self.entradas[nombre] = e

        tk.Label(form_frame, text="Ejemplo de estado: Pendiente / Pagada / Anulada", bg=BG, fg=GRIS, font=F_CHICA).grid(row=len(campos), column=1, sticky="w", padx=10)
        form_frame.columnconfigure(1, weight=1)

    def al_mostrar(self):
        for e in self.entradas.values():
            e.delete(0, "end")
        factura_id = self.app.factura_edicion
        if factura_id is None:
            self.titulo.config(text="NUEVA FACTURA")
            self.entradas["Fecha"].insert(0, "30/09/2026")
            self.entradas["Estado"].insert(0, "EMITIDA")
        else:
            self.titulo.config(text="EDITAR FACTURA")
            factura = self.app.obtener_factura(factura_id)
            for campo in self.entradas:
                self.entradas[campo].insert(0, factura.get(campo, ""))

    def guardar(self):
        datos = {campo: self.entradas[campo].get().strip() for campo in self.entradas}
        if not datos["Cliente"]:
            messagebox.showwarning("Datos incompletos", "Ingresá el cliente.")
            return
        if not datos["Importe"]:
            messagebox.showwarning("Datos incompletos", "Ingresá el importe.")
            return
        try:
            float(datos["Importe"].replace(",", "."))
        except ValueError:
            messagebox.showwarning("Importe inválido", "El importe debe ser numérico.")
            return
        if self.app.factura_edicion is None:
            self.app.agregar_factura(datos)
            messagebox.showinfo("Contabilidad Fácil", "Factura creada correctamente.")
        else:
            self.app.actualizar_factura(self.app.factura_edicion, datos)
            messagebox.showinfo("Contabilidad Fácil", "Factura actualizada correctamente.")
        self.app.mostrar("Facturas")


# ============================================================
# FACTURAS
# ============================================================

class Facturas(Pantalla):
    def construir(self):
        top_bar = tk.Frame(self, bg=BG)
        top_bar.pack(side="top", fill="x", padx=20, pady=20)

        tk.Button(
            top_bar, text="◀", bg="#111111", fg="white", font=("Arial", 7),
            relief="flat", bd=0, command=lambda: self.app.mostrar("MenuMovimientos")
        ).pack(side="left", padx=(0, 10))

        tk.Label(top_bar, text="Facturas", bg=MARRON, fg=NEGRO, font=F_TITULO, width=25, pady=10).pack(side="top")

        tk.Button(
            top_bar, text="[+ Nuevo]", bg=GRIS, fg=GRIS_TXT, font=F_BTN,
            relief="flat", bd=0, command=self.nuevo
        ).pack(side="right")

        search_bar = tk.Frame(self, bg=BG)
        search_bar.pack(side="top", fill="x", padx=40, pady=10)
        
        tk.Label(search_bar, text="Buscar:", bg=BG, fg=NEGRO, font=F_TXT).pack(side="left", padx=(0, 10))
        
        self.buscar = tk.Entry(
            search_bar, bg=CAMPO, fg=NEGRO, font=F_TXT, relief="flat",
            highlightthickness=1, highlightbackground="#b8b4ac"
        )
        self.buscar.pack(side="left", fill="x", expand=True, ipady=3)
        self.buscar.bind("<Return>", lambda ev: self.refrescar())

        tk.Button(
            search_bar, text="🔍", bg=TEAL, fg=NEGRO, font=F_TXT, relief="flat",
            command=self.refrescar
        ).pack(side="left", padx=10)

        table_frame = tk.Frame(self, bg="#ffffff", highlightthickness=2, highlightbackground=BORDE)
        table_frame.pack(side="top", fill="both", expand=True, padx=40, pady=10)

        columnas = ("N°", "Cliente", "Fecha", "Importe", "Estado")
        self.tabla = ttk.Treeview(table_frame, columns=columnas, show="headings", style="Maq.Treeview", selectmode="browse")
        anchos = (80, 230, 140, 140, 110)
        for col, an in zip(columnas, anchos):
            self.tabla.heading(col, text=col, anchor="center")
            self.tabla.column(col, width=an, anchor="center", stretch=True)
        self.tabla.pack(fill="both", expand=True, padx=3, pady=3)
        self.tabla.bind("<Double-1>", lambda e: self.editar())
        filas_vacias(self.tabla)

        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(side="bottom", fill="x", padx=40, pady=20)

        tk.Button(btn_frame, text="[Ver]", bg=GRIS, fg=GRIS_TXT, font=F_BTN, relief="flat", command=self.ver).pack(side="left", expand=True, padx=5, ipady=5)
        tk.Button(btn_frame, text="[Editar]", bg=GRIS, fg=GRIS_TXT, font=F_BTN, relief="flat", command=self.editar).pack(side="left", expand=True, padx=5, ipady=5)
        tk.Button(btn_frame, text="[Eliminar]", bg=GRIS, fg=GRIS_TXT, font=F_BTN, relief="flat", command=self.eliminar).pack(side="left", expand=True, padx=5, ipady=5)

    def al_mostrar(self):
        self.refrescar()

    def refrescar(self):
        filtro = self.buscar.get().strip().lower()
        filas = []
        for f in self.app.facturas:
            texto = (str(f["id"]) + f["Cliente"] + f["Fecha"] + f["Estado"]).lower()
            if filtro and filtro not in texto:
                continue
            filas.append((f["id"], f["Cliente"], f["Fecha"], f["Importe"], f["Estado"]))
        cargar(self.tabla, filas)

    def nuevo(self):
        self.app.factura_edicion = None
        self.app.mostrar("EditarFactura")

    def editar(self):
        factura_id = id_seleccionado(self.tabla)
        if factura_id is None:
            messagebox.showinfo("Facturas", "Seleccioná una factura.")
            return
        self.app.factura_edicion = factura_id
        self.app.mostrar("EditarFactura")

    def ver(self):
        factura_id = id_seleccionado(self.tabla)
        if factura_id is None:
            messagebox.showinfo("Facturas", "Seleccioná una factura.")
            return
        f = self.app.obtener_factura(factura_id)
        messagebox.showinfo(
            "Detalle de factura",
            f"N°: {f['id']}\nCliente: {f['Cliente']}\nFecha: {f['Fecha']}\nImporte: ${f['Importe']}\nEstado: {f['Estado']}"
        )

    def eliminar(self):
        factura_id = id_seleccionado(self.tabla)
        if factura_id is None:
            messagebox.showinfo("Facturas", "Seleccioná una factura.")
            return
        f = self.app.obtener_factura(factura_id)
        if not messagebox.askyesno("Eliminar factura", f"¿Eliminar la factura N° {f['id']}?"):
            return
        self.app.eliminar_factura(factura_id)
        self.refrescar()


# ============================================================
# FORMULARIO DE PAGO
# ============================================================

class EditarPago(Pantalla):
    def construir(self):
        top_bar = tk.Frame(self, bg=BG)
        top_bar.pack(side="top", fill="x", padx=20, pady=20)

        tk.Button(
            top_bar, text="◀", bg="#111111", fg="white", font=("Arial", 7),
            relief="flat", bd=0, command=lambda: self.app.mostrar("Pagos")
        ).pack(side="left", padx=(0, 10))

        self.titulo = tk.Label(top_bar, text="NUEVO PAGO", bg=BG, fg=NEGRO, font=("Arial", 18))
        self.titulo.pack(side="left")

        tk.Button(
            top_bar, text="[Guardar]", bg=GRIS, fg=GRIS_TXT, font=F_BTN,
            relief="flat", bd=0, command=self.guardar
        ).pack(side="right")

        form_frame = tk.Frame(self, bg=BG)
        form_frame.pack(side="top", fill="both", expand=True, padx=80, pady=20)

        self.entradas = {}
        campos = ["Cliente", "Fecha", "Monto", "Estado", "Medio de pago"]
        for i, nombre in enumerate(campos):
            tk.Label(form_frame, text=f"{nombre}:", bg=BG, fg=NEGRO, font=F_TXT, anchor="e").grid(row=i, column=0, sticky="e", padx=10, pady=8)
            e = tk.Entry(form_frame, bg=CAMPO, fg=NEGRO, font=F_TXT, relief="flat", insertbackground=NEGRO)
            e.grid(row=i, column=1, sticky="ew", padx=10, pady=8, ipady=3)
            self.entradas[nombre] = e

        form_frame.columnconfigure(1, weight=1)

    def al_mostrar(self):
        for e in self.entradas.values():
            e.delete(0, "end")
        pago_id = self.app.pago_edicion
        if pago_id is None:
            self.titulo.config(text="NUEVO PAGO")
            self.entradas["Fecha"].insert(0, "30/09/2026")
            self.entradas["Estado"].insert(0, "Confirmado")
        else:
            self.titulo.config(text="EDITAR PAGO")
            pago = self.app.obtener_pago(pago_id)
            for campo in self.entradas:
                self.entradas[campo].insert(0, pago.get(campo, ""))

    def guardar(self):
        datos = {campo: self.entradas[campo].get().strip() for campo in self.entradas}
        if not datos["Cliente"]:
            messagebox.showwarning("Datos incompletos", "Ingresá el cliente.")
            return
        if not datos["Monto"]:
            messagebox.showwarning("Datos incompletos", "Ingresá el monto.")
            return
        try:
            float(datos["Monto"].replace(",", "."))
        except ValueError:
            messagebox.showwarning("Monto inválido", "El monto debe ser numérico.")
            return
        try:
            if self.app.pago_edicion is None:
                self.app.agregar_pago(datos)
                messagebox.showinfo("Contabilidad Fácil", "Pago registrado correctamente.")
            else:
                self.app.actualizar_pago(self.app.pago_edicion, datos)
                messagebox.showinfo("Contabilidad Fácil", "Pago actualizado correctamente.")
            
            self.app.mostrar("Pagos")
        except Exception as e:
            # Esto mostrará la ventana emergente si el cliente no tiene facturas
            messagebox.showwarning("No se pudo registrar el pago", str(e))



# ============================================================
# PAGOS
# ============================================================

class Pagos(Pantalla):
    def construir(self):
        top_bar = tk.Frame(self, bg=BG)
        top_bar.pack(side="top", fill="x", padx=20, pady=20)

        tk.Button(
            top_bar, text="◀", bg="#111111", fg="white", font=("Arial", 7),
            relief="flat", bd=0, command=lambda: self.app.mostrar("MenuMovimientos")
        ).pack(side="left", padx=(0, 10))

        tk.Label(top_bar, text="Pagos", bg=MARRON, fg=NEGRO, font=F_TITULO, width=25, pady=10).pack(side="top")

        tk.Button(
            top_bar, text="[+ Nuevo]", bg=GRIS, fg=GRIS_TXT, font=F_BTN,
            relief="flat", bd=0, command=self.nuevo
        ).pack(side="right")

        search_bar = tk.Frame(self, bg=BG)
        search_bar.pack(side="top", fill="x", padx=40, pady=10)
        
        tk.Label(search_bar, text="Buscar:", bg=BG, fg=NEGRO, font=F_TXT).pack(side="left", padx=(0, 10))
        
        self.buscar = tk.Entry(
            search_bar, bg=CAMPO, fg=NEGRO, font=F_TXT, relief="flat",
            highlightthickness=1, highlightbackground="#b8b4ac"
        )
        self.buscar.pack(side="left", fill="x", expand=True, ipady=3)
        self.buscar.bind("<Return>", lambda ev: self.refrescar())

        tk.Button(
            search_bar, text="🔍", bg=TEAL, fg=NEGRO, font=F_TXT, relief="flat",
            command=self.refrescar
        ).pack(side="left", padx=10)

        table_frame = tk.Frame(self, bg="#ffffff", highlightthickness=2, highlightbackground=BORDE)
        table_frame.pack(side="top", fill="both", expand=True, padx=40, pady=10)

        columnas = ("ID", "Cliente", "Fecha", "Monto", "Estado", "Medio de pago")
        self.tabla = ttk.Treeview(table_frame, columns=columnas, show="headings", style="Maq.Treeview", selectmode="browse")
        anchos = (70, 170, 120, 120, 100, 120)
        for col, an in zip(columnas, anchos):
            self.tabla.heading(col, text=col, anchor="center")
            self.tabla.column(col, width=an, anchor="center", stretch=True)
        self.tabla.pack(fill="both", expand=True, padx=3, pady=3)
        self.tabla.bind("<Double-1>", lambda e: self.editar())
        filas_vacias(self.tabla)

        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(side="bottom", fill="x", padx=40, pady=20)

        tk.Button(btn_frame, text="[Ver]", bg=GRIS, fg=GRIS_TXT, font=F_BTN, relief="flat", command=self.ver).pack(side="left", expand=True, padx=5, ipady=5)
        tk.Button(btn_frame, text="[Editar]", bg=GRIS, fg=GRIS_TXT, font=F_BTN, relief="flat", command=self.editar).pack(side="left", expand=True, padx=5, ipady=5)
        tk.Button(btn_frame, text="[Eliminar]", bg=GRIS, fg=GRIS_TXT, font=F_BTN, relief="flat", command=self.eliminar).pack(side="left", expand=True, padx=5, ipady=5)

    def al_mostrar(self):
        self.refrescar()

    def refrescar(self):
        filtro = self.buscar.get().strip().lower()
        filas = []
        for p in self.app.pagos:
            texto = (str(p["id"]) + p["Cliente"] + p["Fecha"] + p["Estado"] + p["Medio de pago"]).lower()
            if filtro and filtro not in texto:
                continue
            filas.append((p["id"], p["Cliente"], p["Fecha"], p["Monto"], p["Estado"], p["Medio de pago"]))
        cargar(self.tabla, filas)

    def nuevo(self):
        self.app.pago_edicion = None
        self.app.mostrar("EditarPago")

    def editar(self):
        pago_id = id_seleccionado(self.tabla)
        if pago_id is None:
            messagebox.showinfo("Pagos", "Seleccioná un pago.")
            return
        self.app.pago_edicion = pago_id
        self.app.mostrar("EditarPago")

    def ver(self):
        pago_id = id_seleccionado(self.tabla)
        if pago_id is None:
            messagebox.showinfo("Pagos", "Seleccioná un pago.")
            return
        p = self.app.obtener_pago(pago_id)
        messagebox.showinfo(
            "Detalle del pago",
            f"ID: {p['id']}\nCliente: {p['Cliente']}\nFecha: {p['Fecha']}\nMonto: ${p['Monto']}\nEstado: {p['Estado']}\nMedio de pago: {p['Medio de pago']}"
        )

    def eliminar(self):
        pago_id = id_seleccionado(self.tabla)
        if pago_id is None:
            messagebox.showinfo("Pagos", "Seleccioná un pago.")
            return
        p = self.app.obtener_pago(pago_id)
        if not messagebox.askyesno("Eliminar pago", f"¿Eliminar el pago N° {p['id']}?"):
            return
        self.app.eliminar_pago(pago_id)
        self.refrescar()


# ============================================================
# MOVIMIENTOS
# ============================================================

class Movimientos(Pantalla):
    def construir(self):
        top_bar = tk.Frame(self, bg=BG)
        top_bar.pack(side="top", fill="x", padx=20, pady=20)

        tk.Button(
            top_bar, text="◀", bg="#111111", fg="white", font=("Arial", 7),
            relief="flat", bd=0, command=lambda: self.app.mostrar("MenuMovimientos")
        ).pack(side="left", padx=(0, 10))

        tk.Label(top_bar, text="Movimientos", bg=MARRON, fg=NEGRO, font=F_TITULO, width=25, pady=10).pack(side="top")

        tk.Button(top_bar, text="[+ Nuevo]", bg=GRIS, fg=GRIS_TXT, font=F_BTN, relief="flat", bd=0).pack(side="right")

        search_bar = tk.Frame(self, bg=BG)
        search_bar.pack(side="top", fill="x", padx=40, pady=10)
        
        tk.Label(search_bar, text="Buscar:", bg=BG, fg=NEGRO, font=F_TXT).pack(side="left", padx=(0, 10))
        
        self.buscar = tk.Entry(
            search_bar, bg=CAMPO, fg=NEGRO, font=F_TXT, relief="flat",
            highlightthickness=1, highlightbackground="#b8b4ac"
        )
        self.buscar.pack(side="left", fill="x", expand=True, ipady=3)

        table_frame = tk.Frame(self, bg="#ffffff", highlightthickness=2, highlightbackground=BORDE)
        table_frame.pack(side="top", fill="both", expand=True, padx=40, pady=10)

        columnas = ("ID", "Descripcion", "Fecha", "Importe", "Estado", "Categoría")
        self.tabla = ttk.Treeview(table_frame, columns=columnas, show="headings", style="Maq.Treeview", selectmode="browse")
        anchos = (70, 200, 110, 110, 100, 110)
        for col, an in zip(columnas, anchos):
            self.tabla.heading(col, text=col, anchor="center")
            self.tabla.column(col, width=an, anchor="center", stretch=True)
        self.tabla.pack(fill="both", expand=True, padx=3, pady=3)
        filas_vacias(self.tabla)

        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(side="bottom", fill="x", padx=40, pady=20)

        tk.Button(btn_frame, text="[Ver]", bg=GRIS, fg=GRIS_TXT, font=F_BTN, relief="flat").pack(side="left", expand=True, padx=5, ipady=5)
        tk.Button(btn_frame, text="[Editar]", bg=GRIS, fg=GRIS_TXT, font=F_BTN, relief="flat").pack(side="left", expand=True, padx=5, ipady=5)
        tk.Button(btn_frame, text="[Eliminar]", bg=GRIS, fg=GRIS_TXT, font=F_BTN, relief="flat").pack(side="left", expand=True, padx=5, ipady=5)


# ============================================================
# APP PRINCIPAL (CONTIENE EL GESTOR DE DATOS)
# ============================================================

class App(tk.Tk):
    ORDEN = [
        "Login", "Clientes", "GestionClientes", "EditarCliente",
        "MenuMovimientos", "Facturas", "Pagos", "Movimientos",
        "EditarFactura", "EditarPago"
    ]

    def __init__(self):
        super().__init__()
        self.title("Contabilidad Fácil")
        self.geometry(f"{ANCHO}x{ALTO}")
        self.resizable(False, False)
        self.configure(bg=BG)


        inicializar_base_de_datos()
        self.gestor_datos = GestorDatos()

        self._estilos()

        contenedor = tk.Frame(self, bg=BG)
        contenedor.pack(fill="both", expand=True)

        clases = (
            Login, Clientes, GestionClientes, EditarCliente,
            MenuMovimientos, Facturas, Pagos, Movimientos,
            EditarFactura, EditarPago
        )

        self.pantallas = {}
        for clase in clases:
            p = clase(contenedor, self)
            p.place(x=0, y=0, width=ANCHO, height=ALTO)
            self.pantallas[clase.__name__] = p

        for i, nombre in enumerate(self.ORDEN, start=1):
            self.bind(f"<F{i}>", lambda e, n=nombre: self.mostrar(n))

        self.mostrar("Login")


    @property
    def clientes(self): return self.gestor_datos.obtener_clientes()
    @property
    def facturas(self): return self.gestor_datos.obtener_facturas()
    @property
    def pagos(self): return self.gestor_datos.obtener_pagos()

    @property
    def cliente_edicion(self): return self.gestor_datos.cliente_edicion
    @cliente_edicion.setter
    def cliente_edicion(self, val): self.gestor_datos.cliente_edicion = val

    @property
    def factura_edicion(self): return self.gestor_datos.factura_edicion
    @factura_edicion.setter
    def factura_edicion(self, val): self.gestor_datos.factura_edicion = val

    @property
    def pago_edicion(self): return self.gestor_datos.pago_edicion
    @pago_edicion.setter
    def pago_edicion(self, val): self.gestor_datos.pago_edicion = val

    def agregar_cliente(self, d): return self.gestor_datos.agregar_cliente(d)
    def actualizar_cliente(self, i, d): return self.gestor_datos.actualizar_cliente(i, d)
    def eliminar_cliente(self, i): return self.gestor_datos.eliminar_cliente(i)
    def obtener_cliente(self, i): return self.gestor_datos.obtener_cliente(i)
    def verificar_usuario(self, usuario, password): 
        return self.gestor_datos.verificar_usuario(usuario, password)

    def agregar_factura(self, d): return self.gestor_datos.agregar_factura(d)
    def actualizar_factura(self, i, d): return self.gestor_datos.actualizar_factura(i, d)
    def eliminar_factura(self, i): return self.gestor_datos.eliminar_factura(i)
    def obtener_factura(self, i): return self.gestor_datos.obtener_factura(i)

    def agregar_pago(self, d): return self.gestor_datos.agregar_pago(d)
    def actualizar_pago(self, i, d): return self.gestor_datos.actualizar_pago(i, d)
    def eliminar_pago(self, i): return self.gestor_datos.eliminar_pago(i)
    def obtener_pago(self, i): return self.gestor_datos.obtener_pago(i)

    def _estilos(self):
        st = ttk.Style(self)
        try:
            st.theme_use("clam")
        except tk.TclError:
            pass

        st.configure(
            "Maq.Treeview", background="#fbfaf7", fieldbackground="#fbfaf7",
            foreground=NEGRO, rowheight=26, borderwidth=0, font=F_TXT
        )
        st.configure(
            "Maq.Treeview.Heading", background="#e4e1db", foreground=NEGRO,
            font=("Arial", 10), relief="raised", borderwidth=1
        )
        st.map("Maq.Treeview", background=[("selected", "#bfae9f")])

    def mostrar(self, nombre):
        pantalla = self.pantallas[nombre]
        pantalla.tkraise()
        if hasattr(pantalla, "al_mostrar"):
            pantalla.al_mostrar()