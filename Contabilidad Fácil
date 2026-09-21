import tkinter as tk
from tkinter import ttk, messagebox

BG        = "#ffffff"
MARRON    = "#57a076"
MARRON_CL = "#a4b693"
GRIS      = "#595959"
GRIS_TXT  = "#d9d9d9"
NEGRO     = "#1a1a1a"
CAMPO     = "#d3d0ca"
BORDE     = "#7a7a7a"
TEAL      = "#4ad3d7"

F_TITULO = ("Arial", 20)
F_GRANDE = ("Arial", 16)
F_TXT    = ("Arial", 10)
F_CHICA  = ("Arial", 8)
F_BTN    = ("Arial", 9)


ANCHO, ALTO = 920, 580


def barra_titulo(padre, texto, x, y, w=440, h=44, font=F_TITULO, bg=MARRON):
    lbl = tk.Label(padre, text=texto, bg=bg, fg=NEGRO, font=font)
    lbl.place(x=x, y=y, width=w, height=h)
    return lbl


def boton_chico(padre, texto, x, y, w=115, h=26, cmd=None):
    b = tk.Button(padre, text=texto, bg=GRIS, fg=GRIS_TXT, font=F_BTN,
                  relief="flat", bd=0, activebackground="#6e6e6e",
                  activeforeground="white", cursor="hand2", command=cmd)
    b.place(x=x, y=y, width=w, height=h)
    return b


def boton_grande(padre, texto, x, y, w=300, h=85, cmd=None):
    """Botón marrón grande (menú y login)."""
    b = tk.Button(padre, text=texto, bg=MARRON_CL, fg=NEGRO, font=F_GRANDE,
                  relief="flat", bd=0, activebackground="#ab948a",
                  cursor="hand2", command=cmd)
    b.place(x=x, y=y, width=w, height=h)
    return b


def boton_atras(padre, cmd):
    b = tk.Button(padre, text="◀", bg="#111111", fg="white", font=("Arial", 7),
                  relief="flat", bd=0, activebackground="#333333",
                  activeforeground="white", cursor="hand2", command=cmd)
    b.place(x=14, y=14, width=18, height=18)
    return b


def lupa(padre, x, y, cmd=None):
    c = tk.Canvas(padre, width=28, height=28, bg=BG, highlightthickness=0,
                  cursor="hand2")
    c.place(x=x, y=y)
    c.create_oval(1, 1, 27, 27, fill=TEAL, outline="#2aa7ab")
    c.create_oval(8, 8, 18, 18, outline="#12494b", width=2)
    c.create_line(17, 17, 22, 22, fill="#12494b", width=2)
    if cmd:
        c.bind("<Button-1>", lambda e: cmd())
    return c


def barra_buscar(padre, y, x=200, ancho=300, cmd=None):
    tk.Label(padre, text="Buscar:", bg=BG, fg=NEGRO, font=F_TXT).place(x=x, y=y)
    e = tk.Entry(padre, bg=CAMPO, fg=NEGRO, font=F_TXT, relief="flat",
                 highlightthickness=1, highlightbackground="#b8b4ac")
    e.place(x=x + 62, y=y - 2, width=ancho, height=22)
    if cmd:
        e.bind("<Return>", lambda ev: cmd())
    lupa(padre, x + 62 + ancho + 30, y - 6, cmd)
    return e


def tabla(padre, columnas, anchos, x, y, w, h):
    marco = tk.Frame(padre, bg="#ffffff", highlightthickness=2,
                     highlightbackground=BORDE)
    marco.place(x=x, y=y, width=w, height=h)
    tv = ttk.Treeview(marco, columns=columnas, show="headings",
                      style="Maq.Treeview", selectmode="browse")
    for col, an in zip(columnas, anchos):
        tv.heading(col, text=col, anchor="center")
        tv.column(col, width=an, anchor="center", stretch=True)
    tv.pack(fill="both", expand=True, padx=3, pady=3)
    filas_vacias(tv)
    return tv


def filas_vacias(tv, n=7):
    for item in tv.get_children():
        tv.delete(item)
    for _ in range(n):
        tv.insert("", "end", values=[""] * len(tv["columns"]))


def cargar(tv, filas, minimo=7):
    """Vuelca las filas dadas y completa con renglones vacíos hasta 'minimo'."""
    for item in tv.get_children():
        tv.delete(item)
    for fila in filas:
        tv.insert("", "end", values=fila)
    for _ in range(max(0, minimo - len(filas))):
        tv.insert("", "end", values=[""] * len(tv["columns"]))


def id_seleccionado(tv):
    """Id de la fila elegida en la grilla, o None si no hay selección real."""
    seleccion = tv.selection()
    if not seleccion:
        return None
    valores = tv.item(seleccion[0], "values")
    if not valores or str(valores[0]).strip() == "":
        return None
    return int(valores[0])


class EntradaPlaceholder(tk.Entry):

    def __init__(self, padre, texto_guia, oculto=False, **kw):
        super().__init__(padre, **kw)
        self.texto_guia = texto_guia
        self.oculto = oculto
        self._vacio = True
        self._poner_guia()
        self.bind("<FocusIn>", self._entrar)
        self.bind("<FocusOut>", self._salir)

    def _poner_guia(self):
        self.config(show="")
        self.delete(0, "end")
        self.insert(0, self.texto_guia)
        self._vacio = True

    def _entrar(self, _=None):
        if self._vacio:
            self.delete(0, "end")
            self._vacio = False
            if self.oculto:
                self.config(show="*")

    def _salir(self, _=None):
        if not self.get().strip():
            self._poner_guia()

    def valor(self):
        return "" if self._vacio else self.get()


class Pantalla(tk.Frame):

    def __init__(self, padre, app):
        super().__init__(padre, bg=BG)
        self.app = app
        self.construir()

    def construir(self):
        raise NotImplementedError


class Login(Pantalla):
    def construir(self):
        barra_titulo(self, "CONTABILIDAD FACIL", x=230, y=62, w=460, h=48)

        self.usuario = EntradaPlaceholder(
            self, "Usuario", bg=MARRON_CL, fg=NEGRO, font=F_GRANDE,
            justify="center", relief="flat", insertbackground=NEGRO)
        self.usuario.place(x=270, y=180, width=380, height=58)

        self.clave = EntradaPlaceholder(
            self, "Contraseña", oculto=True, bg=MARRON_CL, fg=NEGRO,
            font=F_GRANDE, justify="center", relief="flat",
            insertbackground=NEGRO)
        self.clave.place(x=270, y=262, width=380, height=58)

        for w in (self.usuario, self.clave):
            w.bind("<Return>", self.entrar)

    def entrar(self, _=None):
        self.app.mostrar("Clientes")

    def al_mostrar(self):
        self.usuario.focus_set()


class Clientes(Pantalla):
    def construir(self):
        boton_chico(self, "Gestionar clientes", x=760, y=18, w=140, h=24,
                    cmd=lambda: self.app.mostrar("GestionClientes"))

        marco = tk.Frame(self, bg=MARRON_CL)
        marco.place(x=300, y=62, width=320, height=310)

        tk.Label(marco, text="Clientes", bg=MARRON_CL, fg=NEGRO,
                 font=F_TITULO).place(x=10, y=12, width=300, height=46)

        caja = tk.Frame(marco, bg="#e9e7e2", highlightthickness=2,
                        highlightbackground="#8a8a8a", cursor="hand2")
        caja.place(x=22, y=76, width=276, height=212)
        etiqueta = tk.Label(caja, text="Lista de\nclientes", bg="#e9e7e2",
                            fg=NEGRO, font=F_TITULO, justify="left")
        etiqueta.place(x=18, y=14)

        for w in (caja, etiqueta):
            w.bind("<Button-1>",
                   lambda e: self.app.mostrar("GestionClientes"))

        self.lbl_activos = tk.Label(self, text="Clientes activos: 0", bg=BG,
                                    fg=NEGRO, font=F_TXT)
        self.lbl_activos.place(x=200, y=470)
        tk.Label(self, text="Pendientes: 12", bg=BG, fg=NEGRO,
                 font=F_TXT).place(x=600, y=470)

    def al_mostrar(self):
        # Cuenta los clientes activos sobre la lista en memoria del App.
        activos = sum(1 for c in self.app.clientes if c["Activo"])
        self.lbl_activos.config(text=f"Clientes activos: {activos}")


class GestionClientes(Pantalla):
    def construir(self):
        boton_atras(self, lambda: self.app.mostrar("Clientes"))
        barra_titulo(self, "Gestión de clientes", x=240, y=18, w=440, h=44)
        boton_chico(self, "[+ Nuevo]", x=770, y=26, cmd=self.nuevo)

        self.buscar = barra_buscar(self, y=98, cmd=self.refrescar)

        self.tabla = tabla(self,
                           ("id", "Nombre", "CUIT", "Activo"),
                           (90, 280, 180, 140),
                           x=110, y=140, w=700, h=260)
        self.tabla.bind("<Double-1>", lambda e: self.editar())

        boton_chico(self, "[Ver]", x=180, y=425, w=130, h=28,
                    cmd=lambda: self.app.mostrar("MenuMovimientos"))
        boton_chico(self, "[Editar]", x=395, y=425, w=130, h=28,
                    cmd=self.editar)
        boton_chico(self, "[Eliminar]", x=610, y=425, w=130, h=28,
                    cmd=self.eliminar)

    def al_mostrar(self):
        self.refrescar()

    def refrescar(self):
        """Vuelve a leer self.app.clientes y arma las filas de la tabla."""
        filtro = self.buscar.get().strip().lower()
        filas = []
        for c in self.app.clientes:
            if filtro and filtro not in c["Nombre"].lower() \
                    and filtro not in c["CUIT"].lower():
                continue
            filas.append((c["id"], c["Nombre"], c["CUIT"],
                          "Sí" if c["Activo"] else "No"))
        cargar(self.tabla, filas)

    def nuevo(self):
        self.app.cliente_edicion = None
        self.app.mostrar("EditarCliente")

    def editar(self):
        cliente_id = id_seleccionado(self.tabla)
        if cliente_id is None:
            messagebox.showinfo("Contabilidad Fácil",
                                "Primero seleccioná un cliente de la tabla.")
            return
        self.app.cliente_edicion = cliente_id
        self.app.mostrar("EditarCliente")

    def eliminar(self):
        cliente_id = id_seleccionado(self.tabla)
        if cliente_id is None:
            messagebox.showinfo("Contabilidad Fácil",
                                "Primero seleccioná un cliente de la tabla.")
            return
        cliente = self.app.obtener_cliente(cliente_id)
        if not messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Eliminar a «{cliente['Nombre']}»?"):
            return
        self.app.eliminar_cliente(cliente_id)
        self.refrescar()


class EditarCliente(Pantalla):
    CAMPOS = ["Nombre", "CUIT", "Email", "Teléfono", "Dirección"]

    def construir(self):
        boton_atras(self, lambda: self.app.mostrar("GestionClientes"))
        self.titulo = tk.Label(self, text="EDITAR CLIENTE", bg=BG, fg=NEGRO,
                               font=("Arial", 18))
        self.titulo.place(x=95, y=62)
        boton_chico(self, "[Guardar]", x=740, y=68, cmd=self.guardar)

        self.entradas = {}
        y = 165
        for nombre in self.CAMPOS:
            tk.Label(self, text=f"{nombre}:", bg=BG, fg=NEGRO,
                     font=F_TXT, anchor="e").place(x=140, y=y, width=160)
            e = tk.Entry(self, bg=CAMPO, fg=NEGRO, font=F_TXT, relief="flat",
                         insertbackground=NEGRO)
            e.place(x=320, y=y - 3, width=420, height=24)
            tk.Frame(self, bg="#8a8a8a").place(x=330, y=y + 21,
                                               width=300, height=1)
            self.entradas[nombre] = e
            y += 44

        tk.Label(self, text="Activo:", bg=BG, fg=NEGRO, font=F_TXT,
                 anchor="e").place(x=140, y=y, width=160)
        self.activo = tk.BooleanVar(value=True)
        tk.Checkbutton(self, variable=self.activo, bg=BG, activebackground=BG,
                       selectcolor="#ffffff", bd=0, highlightthickness=0
                       ).place(x=322, y=y - 3)

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
        datos_cliente = {campo: self.entradas[campo].get().strip()
                         for campo in self.CAMPOS}
        if not datos_cliente["Nombre"]:
            messagebox.showwarning("Datos incompletos",
                                   "El nombre del cliente es obligatorio.")
            return
        datos_cliente["Activo"] = self.activo.get()

        if self.app.cliente_edicion is None:
            self.app.agregar_cliente(datos_cliente)
            messagebox.showinfo("Contabilidad Fácil",
                                "Cliente agregado correctamente.")
        else:
            self.app.actualizar_cliente(self.app.cliente_edicion, datos_cliente)
            messagebox.showinfo("Contabilidad Fácil",
                                "Cliente actualizado correctamente.")

        self.app.mostrar("GestionClientes")


class MenuMovimientos(Pantalla):
    def construir(self):
        boton_grande(self, "Pagos", x=310, y=60,
                     cmd=lambda: self.app.mostrar("Pagos"))
        boton_grande(self, "Movimientos", x=310, y=175,
                     cmd=lambda: self.app.mostrar("Movimientos"))
        boton_grande(self, "Facturas", x=310, y=290,
                     cmd=lambda: self.app.mostrar("Facturas"))
        boton_chico(self, "Atrás", x=760, y=480, w=120, h=28,
                    cmd=lambda: self.app.mostrar("GestionClientes"))


class Facturas(Pantalla):
    def construir(self):
        boton_atras(self, lambda: self.app.mostrar("MenuMovimientos"))
        barra_titulo(self, "Facturas", x=240, y=18, w=440, h=44)
        boton_chico(self, "[+ Nuevo]", x=770, y=26)

        self.buscar = barra_buscar(self, y=98)

        self.tabla = tabla(self,
                           ("N°", "Cliente", "Fecha", "Importe", "Estado"),
                           (80, 230, 140, 140, 110),
                           x=110, y=140, w=700, h=260)

        boton_chico(self, "[Ver]", x=180, y=425, w=130, h=28)
        boton_chico(self, "[Editar]", x=395, y=425, w=130, h=28)
        boton_chico(self, "[Eliminar]", x=610, y=425, w=130, h=28)


class Pagos(Pantalla):
    def construir(self):
        boton_atras(self, lambda: self.app.mostrar("MenuMovimientos"))
        barra_titulo(self, "Pagos", x=240, y=18, w=440, h=44)
        boton_chico(self, "[+ Nuevo]", x=770, y=26)

        self.buscar = barra_buscar(self, y=98)

        self.tabla = tabla(
            self,
            ("ID", "Cliente", "Fecha", "Monto", "Estado", "Medio de pago"),
            (70, 170, 120, 120, 100, 120),
            x=110, y=140, w=700, h=260)

        boton_chico(self, "[Ver]", x=180, y=425, w=130, h=28)
        boton_chico(self, "[Editar]", x=395, y=425, w=130, h=28)
        boton_chico(self, "[Eliminar]", x=610, y=425, w=130, h=28)


class Movimientos(Pantalla):
    def construir(self):
        boton_atras(self, lambda: self.app.mostrar("MenuMovimientos"))
        barra_titulo(self, "Movimientos", x=240, y=18, w=440, h=44)
        boton_chico(self, "[+ Nuevo]", x=770, y=26)

        self.buscar = barra_buscar(self, y=98)

        self.tabla = tabla(
            self,
            ("ID", "Descripcion", "Fecha", "Importe", "Estado", "Categoría"),
            (70, 200, 110, 110, 100, 110),
            x=110, y=140, w=700, h=260)

        boton_chico(self, "[Ver]", x=180, y=425, w=130, h=28)
        boton_chico(self, "[Editar]", x=395, y=425, w=130, h=28)
        boton_chico(self, "[Eliminar]", x=610, y=425, w=130, h=28)


class App(tk.Tk):
    ORDEN = ["Login", "Clientes", "GestionClientes", "EditarCliente",
             "MenuMovimientos", "Facturas", "Pagos", "Movimientos"]

    def __init__(self):
        super().__init__()
        self.title("Contabilidad Fácil")
        self.geometry(f"{ANCHO}x{ALTO}")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._estilos()

        self.clientes = []
        self.siguiente_id = 1
        self.cliente_edicion = None  

        contenedor = tk.Frame(self, bg=BG)
        contenedor.pack(fill="both", expand=True)

        clases = (Login, Clientes, GestionClientes, EditarCliente,
                  MenuMovimientos, Facturas, Pagos, Movimientos)
        self.pantallas = {}
        for clase in clases:
            p = clase(contenedor, self)
            p.place(x=0, y=0, width=ANCHO, height=ALTO)
            self.pantallas[clase.__name__] = p

        for i, nombre in enumerate(self.ORDEN, start=1):
            self.bind(f"<F{i}>", lambda e, n=nombre: self.mostrar(n))

        self.mostrar("Login")


    def agregar_cliente(self, datos_cliente):
        nuevo = dict(datos_cliente)
        nuevo["id"] = self.siguiente_id
        self.siguiente_id += 1
        self.clientes.append(nuevo)
        return nuevo["id"]

    def actualizar_cliente(self, cliente_id, datos_cliente):
        for cliente in self.clientes:
            if cliente["id"] == cliente_id:
                cliente.update(datos_cliente)
                return True
        return False

    def eliminar_cliente(self, cliente_id):
        self.clientes = [c for c in self.clientes if c["id"] != cliente_id]

    def obtener_cliente(self, cliente_id):
        for cliente in self.clientes:
            if cliente["id"] == cliente_id:
                return cliente
        return None

    def _estilos(self):
        st = ttk.Style(self)
        try:
            st.theme_use("clam")
        except tk.TclError:
            pass
        st.configure("Maq.Treeview", background="#fbfaf7",
                     fieldbackground="#fbfaf7", foreground=NEGRO,
                     rowheight=26, borderwidth=0, font=F_TXT)
        st.configure("Maq.Treeview.Heading", background="#e4e1db",
                     foreground=NEGRO, font=("Arial", 10), relief="raised",
                     borderwidth=1)
        st.map("Maq.Treeview", background=[("selected", "#bfae9f")])

    def mostrar(self, nombre):
        pantalla = self.pantallas[nombre]
        pantalla.tkraise()
        if hasattr(pantalla, "al_mostrar"):
            pantalla.al_mostrar()


if __name__ == "__main__":
    App().mainloop()
