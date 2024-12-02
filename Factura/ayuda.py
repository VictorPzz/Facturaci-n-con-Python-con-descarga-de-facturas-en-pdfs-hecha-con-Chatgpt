import tkinter as tk
from PIL import Image, ImageTk

class HelpMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        
        tk.Label(self, text="Menú de Ayuda", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        button_frame = tk.Frame(self, bg="#666666")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Productos", width=20, command=lambda: self.open_help_section("productos")).pack(pady=5)
        tk.Button(button_frame, text="Clientes", width=20, command=lambda: self.open_help_section("clientes")).pack(pady=5)
        tk.Button(button_frame, text="Facturación", width=20, command=lambda: self.open_help_section("facturacion")).pack(pady=5)
        tk.Button(button_frame, text="Informes", width=20, command=lambda: self.open_help_section("informes")).pack(pady=5)

        tk.Button(self, text="Regresar al Menú Principal", bg="#888888", fg="white", command=self.go_back).pack(pady=20)

    def open_help_section(self, section):
        """Abre la sección de ayuda específica según el botón presionado."""
        if section == "productos":
            self.master.switch_to_help_productos()
        elif section == "clientes":
            self.master.switch_to_help_clientes()
        elif section == "facturacion":
            self.master.switch_to_help_facturacion()
        elif section == "informes":
            self.master.switch_to_help_informes()

    def go_back(self):
        """Regresa al menú principal."""
        self.master.switch_to_main_interface()

class HelpProductosFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        
        # Marco blanco más ancho
        content_frame = tk.Frame(self, bg="white", padx=40, pady=20)  # Más espacio interno horizontal
        content_frame.pack(expand=True, fill="both", padx=50, pady=20)  # Expandir para ajustarse al contenedor

        # Marco para el título y el botón de regresar
        header_frame = tk.Frame(content_frame, bg="white")
        header_frame.pack(fill="x", pady=10)

        # Título
        tk.Label(header_frame, text="Ayuda - Productos", font=("Arial", 20, "bold"), bg="white").pack(side="left", padx=10)

        # Botón para regresar (al lado derecho del título)
        tk.Button(header_frame, text="Regresar", bg="#888888", fg="white", font=("Arial", 12), command=self.go_back).pack(side="right", padx=10)

        # Widget de texto
        text_widget = tk.Text(content_frame, wrap=tk.WORD, width=70, height=15, font=("Arial", 12), bg="white", relief="flat")
        
        # Texto completo
        help_text = (
            "En la sección de Productos puedes gestionar los productos de tu inventario.\n\n"
            "Funciones disponibles:\n\n"
            "1. Agregar Producto: Completa los campos en la parte superior e indica nombre, descripción, precio, existencia y unidad de medida, luego presiona 'Agregar'.\n\n"
            "2. Modificar Producto: Selecciona un producto en la tabla, edita los campos y presiona 'Modificar'.\n\n"
            "3. Eliminar Producto: Selecciona un producto en la tabla y presiona 'Eliminar' para removerlo.\n\n"
            "4. Tabla de Productos: Visualiza todos los productos registrados, incluyendo detalles como ID, precio y cantidad.\n\n"
            "5. Regresar: Presiona 'Regresar' para volver al menú principal.\n\n"
            "Nota: Usa la tabla para seleccionar y editar productos existentes."
        )
        
        text_widget.insert(tk.END, help_text)
        
        # Configurar estilos
        text_widget.tag_configure("highlight", foreground="blue", font=("Arial", 12, "bold"))
        
        # Resaltar dinámicamente los textos clave
        keywords = [
            "1. Agregar Producto:", 
            "2. Modificar Producto:", 
            "3. Eliminar Producto:", 
            "4. Tabla de Productos:", 
            "5. Regresar:"
        ]
        for keyword in keywords:
            start_idx = text_widget.search(keyword, "1.0", tk.END)  # Buscar palabra clave
            if start_idx:  # Si se encuentra la palabra clave
                end_idx = f"{start_idx}+{len(keyword)}c"  # Calcular posición final
                text_widget.tag_add("highlight", start_idx, end_idx)  # Aplicar etiqueta

        text_widget.config(state=tk.DISABLED)  # Desactivar edición del texto
        text_widget.pack(pady=10)

        # Imagen
        try:
            image = Image.open("ayuda.png")  # Reemplaza con la ruta correcta del archivo
            image = image.resize((500, 350), Image.Resampling.LANCZOS)  # Tamaño ajustado
            photo = ImageTk.PhotoImage(image)
            label_image = tk.Label(content_frame, image=photo, bg="white")
            label_image.image = photo  # Mantén una referencia para evitar problemas de recolección de basura
            label_image.pack(pady=10)
        except FileNotFoundError:
            tk.Label(content_frame, text="(Captura de pantalla no disponible)", bg="white", font=("Arial", 12, "italic")).pack(pady=10)

    def go_back(self):
        """Regresa al menú de ayuda."""
        self.master.switch_to_help_menu()
        
class HelpClientesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        
        # Marco blanco más ancho
        content_frame = tk.Frame(self, bg="white", padx=40, pady=20)  # Más espacio interno horizontal
        content_frame.pack(expand=True, fill="both", padx=50, pady=20)  # Expandir para ajustarse al contenedor

        # Marco para el título y el botón de regresar
        header_frame = tk.Frame(content_frame, bg="white")
        header_frame.pack(fill="x", pady=10)

        # Título
        tk.Label(header_frame, text="Ayuda - Clientes", font=("Arial", 20, "bold"), bg="white").pack(side="left", padx=10)

        # Botón para regresar (al lado derecho del título)
        tk.Button(header_frame, text="Regresar", bg="#888888", fg="white", font=("Arial", 12), command=self.go_back).pack(side="right", padx=10)

        # Widget de texto
        text_widget = tk.Text(content_frame, wrap=tk.WORD, width=70, height=15, font=("Arial", 12), bg="white", relief="flat")
        
        # Texto completo
        help_text = (
            "En la sección de Clientes puedes gestionar la información de los clientes registrados en el sistema.\n\n"
            "Funciones disponibles:\n\n"
            "1. **Agregar Cliente:** Completa los campos en la parte superior indicando el Nombre, Apellido Paterno, "
            "Apellido Materno, Fecha de Nacimiento (en formato YYYY-MM-DD), Dirección, Teléfono y Email. El campo de RFC "
            "se generará automáticamente una vez que los demás datos estén llenos. Presiona el botón 'Agregar' para añadir el cliente.\n\n"
            "2. **Modificar Cliente:** Selecciona un cliente de la tabla, edita los campos correspondientes y presiona 'Modificar' para actualizar su información.\n\n"
            "3. **Eliminar Cliente:** Selecciona un cliente de la tabla y presiona 'Borrar' para eliminarlo del sistema.\n\n"
            "4. **Limpiar Campos:** Si deseas agregar un nuevo cliente o eliminar la selección actual, presiona 'Limpiar' para vaciar los campos y restablecer el formulario.\n\n"
            "Nota: El sistema asegura que no se pueda agregar un cliente incompleto. Solo cuando todos los campos obligatorios están llenos, el botón 'Agregar' estará disponible.\n\n"
        )
        
        text_widget.insert(tk.END, help_text)
        
        # Configurar estilos
        text_widget.tag_configure("highlight", foreground="blue", font=("Arial", 12, "bold"))
        
        # Resaltar dinámicamente los textos clave
        keywords = [
            "1. **Agregar Cliente:**", 
            "2. **Modificar Cliente:**", 
            "3. **Eliminar Cliente:**", 
            "4. **Limpiar Campos:**"
        ]
        for keyword in keywords:
            start_idx = text_widget.search(keyword, "1.0", tk.END)  # Buscar palabra clave
            if start_idx:  # Si se encuentra la palabra clave
                end_idx = f"{start_idx}+{len(keyword)}c"  # Calcular posición final
                text_widget.tag_add("highlight", start_idx, end_idx)  # Aplicar etiqueta

        text_widget.config(state=tk.DISABLED)  # Desactivar edición del texto
        text_widget.pack(pady=10)

        # Imagen
        try:
            image = Image.open("ayuda2.png")  # Ruta al archivo de imagen
            image = image.resize((500, 350), Image.Resampling.LANCZOS)  # Tamaño ajustado
            photo = ImageTk.PhotoImage(image)
            label_image = tk.Label(content_frame, image=photo, bg="white")
            label_image.image = photo  # Mantén una referencia para evitar problemas de recolección de basura
            label_image.pack(pady=10)
        except FileNotFoundError:
            tk.Label(content_frame, text="(Captura de pantalla no disponible)", bg="white", font=("Arial", 12, "italic")).pack(pady=10)

    def go_back(self):
        """Regresa al menú de ayuda."""
        self.master.switch_to_help_menu()
        
class HelpFacturacionFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        
        content_frame = tk.Frame(self, bg="white", padx=40, pady=20)  # Más espacio interno horizontal
        content_frame.pack(expand=True, fill="both", padx=50, pady=20)  # Expandir para ajustarse al contenedor

        header_frame = tk.Frame(content_frame, bg="white")
        header_frame.pack(fill="x", pady=10)

        tk.Label(header_frame, text="Ayuda - Facturación", font=("Arial", 20, "bold"), bg="white").pack(side="left", padx=10)

        tk.Button(header_frame, text="Regresar", bg="#888888", fg="white", font=("Arial", 12), command=self.go_back).pack(side="right", padx=10)

        text_widget = tk.Text(content_frame, wrap=tk.WORD, width=70, height=15, font=("Arial", 12), bg="white", relief="flat")
        
        help_text = (
            "En la sección de Facturación puedes gestionar las facturas del sistema de forma sencilla y eficiente.\n\n"
            "Funciones disponibles:\n\n"
            "1. **Número de Factura y Fecha:** Estos campos se llenan automáticamente con la base de datos y el sistema de fecha, "
            "y no son editables.\n\n"
            "2. **Búsqueda de Cliente:** Ingresa el ID del cliente y presiona 'Buscar Cliente' para completar automáticamente "
            "los datos relacionados del cliente (como Nombre, Dirección, y Empresa).\n\n"
            "3. **Búsqueda de Producto:** Ingresa el ID del producto y presiona 'Buscar Producto' para completar automáticamente "
            "los datos relacionados del producto (como Nombre y Precio Unitario). Ingresa la cantidad y presiona 'Agregar' "
            "para incluir el producto en la factura.\n\n"
            "4. **Visualización de Factura:** Mientras agregas productos, estos se muestran en la tabla con los campos: "
            "ID Producto, Nombre, Cantidad, Precio Unitario e Importe. Los totales (Neto, IVA 19%, y Total) se calculan automáticamente.\n\n"
            "5. **Guardar o Limpiar:** Cuando termines, presiona 'Guardar Factura' para almacenarla en la base de datos, o presiona 'Limpiar Todo' "
            "para reiniciar la factura.\n\n"
        )
        
        text_widget.insert(tk.END, help_text)
        
        text_widget.tag_configure("highlight", foreground="blue", font=("Arial", 12, "bold"))
        
        keywords = [
            "1. **Número de Factura y Fecha:**", 
            "2. **Búsqueda de Cliente:**", 
            "3. **Búsqueda de Producto:**", 
            "4. **Visualización de Factura:**", 
            "5. **Guardar o Limpiar:**"
        ]
        for keyword in keywords:
            start_idx = text_widget.search(keyword, "1.0", tk.END)  
            if start_idx:  
                end_idx = f"{start_idx}+{len(keyword)}c" 
                text_widget.tag_add("highlight", start_idx, end_idx)  

        text_widget.config(state=tk.DISABLED)  
        text_widget.pack(pady=10)

        try:
            image = Image.open("ayuda3.png")  
            image = image.resize((450, 200), Image.Resampling.LANCZOS)  
            photo = ImageTk.PhotoImage(image)
            label_image = tk.Label(content_frame, image=photo, bg="white")
            label_image.image = photo  
            label_image.pack(pady=10)
        except FileNotFoundError:
            tk.Label(content_frame, text="(Captura de pantalla no disponible)", bg="white", font=("Arial", 12, "italic")).pack(pady=10)

    def go_back(self):
        """Regresa al menú de ayuda."""
        self.master.switch_to_help_menu()
        
class HelpInformesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        
        content_frame = tk.Frame(self, bg="white", padx=40, pady=20)  # Más espacio interno horizontal
        content_frame.pack(expand=True, fill="both", padx=50, pady=20)  # Expandir para ajustarse al contenedor

        header_frame = tk.Frame(content_frame, bg="white")
        header_frame.pack(fill="x", pady=10)

        tk.Label(header_frame, text="Ayuda - Informes", font=("Arial", 20, "bold"), bg="white").pack(side="left", padx=10)

        tk.Button(header_frame, text="Regresar", bg="#888888", fg="white", font=("Arial", 12), command=self.go_back).pack(side="right", padx=10)

        text_widget = tk.Text(content_frame, wrap=tk.WORD, width=70, height=15, font=("Arial", 12), bg="white", relief="flat")
        
        help_text = (
            "En la sección de Informes puedes consultar un historial de facturación completo y realizar varias acciones.\n\n"
            "Funciones disponibles:\n\n"
            "1. **Visualización de Facturas:** Las facturas se muestran en una tabla organizada por fecha, donde las más recientes "
            "aparecen primero. Cada fila incluye los campos: Folio, Cliente, Fecha, Monto y Empresa.\n\n"
            "2. **Ver Detalles:** Selecciona una factura y presiona el botón 'Ver Detalles' para consultar información más específica, "
            "como los productos incluidos, sus cantidades, precios unitarios y el importe total de cada uno.\n\n"
            "3. **Exportar PDF:** Selecciona una factura y presiona el botón 'Exportar PDF' para generar un archivo PDF "
            "con un formato detallado, listo para imprimir o compartir.\n\n"
            "4. **Regresar al Menú Principal:** Presiona el botón 'Regresar' para volver al menú principal de la aplicación.\n\n"
            "Nota: Asegúrate de seleccionar una factura antes de intentar ver sus detalles o exportarla como PDF."
        )
        
        text_widget.insert(tk.END, help_text)
        
        text_widget.tag_configure("highlight", foreground="blue", font=("Arial", 12, "bold"))
        
        keywords = [
            "1. **Visualización de Facturas:**", 
            "2. **Ver Detalles:**", 
            "3. **Exportar PDF:**", 
            "4. **Regresar al Menú Principal:**"
        ]
        for keyword in keywords:
            start_idx = text_widget.search(keyword, "1.0", tk.END)  
            if start_idx:  
                end_idx = f"{start_idx}+{len(keyword)}c" 
                text_widget.tag_add("highlight", start_idx, end_idx)  

        text_widget.config(state=tk.DISABLED)  
        text_widget.pack(pady=10)

        try:
            image = Image.open("ayuda4.png")  
            image = image.resize((450, 200), Image.Resampling.LANCZOS)  
            photo = ImageTk.PhotoImage(image)
            label_image = tk.Label(content_frame, image=photo, bg="white")
            label_image.image = photo  
            label_image.pack(pady=10)
        except FileNotFoundError:
            tk.Label(content_frame, text="(Captura de pantalla no disponible)", bg="white", font=("Arial", 12, "italic")).pack(pady=10)

    def go_back(self):
        """Regresa al menú de ayuda."""
        self.master.switch_to_help_menu()
