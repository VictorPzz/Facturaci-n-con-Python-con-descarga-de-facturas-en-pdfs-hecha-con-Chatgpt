import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class RedesignedFacturacionFrame(tk.Frame):
    def __init__(self, master, cnn):
        super().__init__(master, bg="#dcdcdc")
        self.cnn = cnn

        # Encabezado
        tk.Label(self, text="Facturación", font=("Arial", 18, "bold"), bg="#dcdcdc").grid(row=0, column=0, columnspan=8, pady=10)

        # Folio (reposicionado a la derecha, encima de Fecha)
        tk.Label(self, text="Folio:", bg="#dcdcdc").grid(row=1, column=3, sticky="e", padx=5, pady=5)
        self.folio_label = tk.Label(self, text="", bg="#e6e6e6", width=15, anchor="w")
        self.folio_label.grid(row=1, column=4, padx=5, pady=5)
        self.load_next_folio()

        # Fecha
        tk.Label(self, text="Fecha:", bg="#dcdcdc").grid(row=2, column=3, sticky="e", padx=5, pady=5)
        self.fecha_entry = tk.Entry(self, width=20, state="readonly")
        self.fecha_entry.grid(row=2, column=4, padx=5, pady=5)
        self.autofill_date()

        # Datos Cliente
        tk.Label(self, text="ID Cliente:", bg="#dcdcdc").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.id_cliente_entry = tk.Entry(self, width=20)
        self.id_cliente_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self, text="Buscar Cliente", command=self.fill_client_data, bg="#0073e6", fg="white").grid(row=2, column=2, padx=5, pady=5)

        tk.Label(self, text="Nombre:", bg="#dcdcdc").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.nombre_cliente_label = tk.Label(self, text="", bg="#e6e6e6", width=30, anchor="w")
        self.nombre_cliente_label.grid(row=3, column=1, padx=5, pady=5, columnspan=2)

        tk.Label(self, text="Dirección:", bg="#dcdcdc").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.direccion_cliente_label = tk.Label(self, text="", bg="#e6e6e6", width=50, anchor="w")
        self.direccion_cliente_label.grid(row=4, column=1, padx=5, pady=5, columnspan=2)

        # Campo Empresa
        tk.Label(self, text="Empresa:", bg="#dcdcdc").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.empresa_entry = tk.Entry(self, width=30)
        self.empresa_entry.grid(row=5, column=1, padx=5, pady=5, columnspan=2)

        # Productos
        tk.Label(self, text="ID Producto:", bg="#dcdcdc").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.id_producto_entry = tk.Entry(self, width=20)
        self.id_producto_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(self, text="Buscar Producto", command=self.fill_product_data, bg="#0073e6", fg="white").grid(row=6, column=2, padx=5, pady=5)

        tk.Label(self, text="Nombre:", bg="#dcdcdc").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.nombre_producto_label = tk.Label(self, text="", bg="#e6e6e6", width=30, anchor="w")
        self.nombre_producto_label.grid(row=7, column=1, padx=5, pady=5, columnspan=2)

        tk.Label(self, text="Cantidad:", bg="#dcdcdc").grid(row=6, column=3, sticky="e", padx=5, pady=5)
        self.cantidad_entry = tk.Entry(self, width=10)
        self.cantidad_entry.grid(row=6, column=4, padx=5, pady=5)

        # Botón para agregar productos
        tk.Button(self, text="Agregar", command=self.add_product, bg="#0073e6", fg="white").grid(row=7, column=3, padx=5, pady=5)

        # Tabla de productos
        columns = ("ID Producto", "Nombre", "Cantidad", "Precio Unit", "Importe")
        self.invoice_table = ttk.Treeview(self, columns=columns, show="headings", height=10)
        for col in columns:
            self.invoice_table.heading(col, text=col)
            self.invoice_table.column(col, width=100)
        self.invoice_table.grid(row=8, column=0, columnspan=6, pady=10, padx=10)

        # Totales
        tk.Label(self, text="Total Neto:", bg="#dcdcdc").grid(row=9, column=3, sticky="e", padx=5, pady=5)
        self.total_neto_label = tk.Label(self, text="0.00", bg="#e6e6e6", width=15, anchor="e")
        self.total_neto_label.grid(row=9, column=4, padx=5, pady=5)

        tk.Label(self, text="IVA 19%:", bg="#dcdcdc").grid(row=10, column=3, sticky="e", padx=5, pady=5)
        self.iva_label = tk.Label(self, text="0.00", bg="#e6e6e6", width=15, anchor="e")
        self.iva_label.grid(row=10, column=4, padx=5, pady=5)

        tk.Label(self, text="Total:", bg="#dcdcdc", font=("Arial", 12, "bold")).grid(row=11, column=3, sticky="e", padx=5, pady=5)
        self.total_label = tk.Label(self, text="0.00", bg="#e6e6e6", width=15, font=("Arial", 12, "bold"), anchor="e")
        self.total_label.grid(row=11, column=4, padx=5, pady=5)
        
        # Botones de acción
        tk.Button(self, text="Guardar Factura", bg="#0073e6", fg="white", command=self.save_invoice).grid(row=12, column=4, pady=10)
        tk.Button(self, text="Limpiar Todo", bg="#ffcc00", command=self.clear_all).grid(row=12, column=3, pady=10)
        
        tk.Button(
            self, 
            text="Regresar", 
            bg="#888888", 
            fg="Green", 
            command=self.volver_menu_principal
        ).grid(row=12, column=5, sticky="w", pady=10)
    
# Botón de ayuda en Facturación
        # Botón de Ayuda en Facturación (ubicado abajo a la izquierda)
        tk.Button(self, text="Ayuda", bg="#0073e6", fg="white", font=("Arial", 11),
                  command=self.master.switch_to_help_facturacion).grid(row=12, column=0, pady=10, padx=10, sticky="w")

    def switch_to_help(self):
        """Redirige a la ayuda de facturación."""
        self.master.switch_to_help_facturacion()
        
    def volver_menu_principal(self):
        """Regresar al menú principal."""
        self.master.switch_to_main_interface()

    def load_next_folio(self):
        """Carga el próximo folio disponible."""
        cursor = self.cnn.cursor()
        cursor.execute("SELECT COALESCE(MAX(folio), 0) + 1 FROM fact_encab")
        next_folio = cursor.fetchone()[0]
        cursor.close()
        self.folio_label.config(text=str(next_folio))

    def autofill_date(self):
        """Llena automáticamente la fecha actual."""
        today = datetime.now().strftime("%Y-%m-%d")
        self.fecha_entry.config(state="normal")
        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, today)
        self.fecha_entry.config(state="readonly")


    def fill_client_data(self):
        """Rellena los datos del cliente según el ID proporcionado."""
        client_id = self.id_cliente_entry.get()
        cursor = self.cnn.cursor()
        cursor.execute("SELECT nombre, direccion FROM clientes WHERE id=%s", (client_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            self.nombre_cliente_label.config(text=result[0])
            self.direccion_cliente_label.config(text=result[1])
        else:
            messagebox.showerror("Error", "Cliente no encontrado.")

    def fill_product_data(self):
        """Rellena los datos del producto según el ID proporcionado."""
        product_id = self.id_producto_entry.get()
        cursor = self.cnn.cursor()
        cursor.execute("SELECT nombre, precio FROM productos WHERE id=%s", (product_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            self.nombre_producto_label.config(text=result[0])
            self.precio_producto = result[1]
        else:
            messagebox.showerror("Error", "Producto no encontrado.")

    def add_product(self):
        """Agrega un producto a la tabla de facturación."""
        product_id = self.id_producto_entry.get()
        nombre = self.nombre_producto_label.cget("text")
        cantidad = self.cantidad_entry.get()

        try:
            cantidad = int(cantidad)
            importe = cantidad * self.precio_producto
            self.invoice_table.insert("", "end", values=(product_id, nombre, cantidad, self.precio_producto, importe))
            self.update_totals()
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número válido.")

    def update_totals(self):
        total_neto = 0
        for row in self.invoice_table.get_children():
            total_neto += float(self.invoice_table.item(row)["values"][4])
        iva = total_neto * 0.19
        total = total_neto + iva

        self.total_neto_label.config(text=f"{total_neto:.2f}")
        self.iva_label.config(text=f"{iva:.2f}")
        self.total_label.config(text=f"{total:.2f}")

    def save_invoice(self):
        """Guarda la factura en la base de datos."""
        client_id = self.id_cliente_entry.get()
        fecha = self.fecha_entry.get()
        empresa = self.empresa_entry.get()
        total = float(self.total_label.cget("text"))

        cursor = self.cnn.cursor()
        try:
            cursor.execute("INSERT INTO fact_encab (idCliente, fecha, monto, empresa) VALUES (%s, %s, %s, %s)", 
                           (client_id, fecha, total, empresa))
            folio = cursor.lastrowid

            for row in self.invoice_table.get_children():
                product_id, _, cantidad, precio_unitario, _ = self.invoice_table.item(row)["values"]
                cursor.execute("INSERT INTO fact_detalle (folio, idProd, cant, precio_unitario) VALUES (%s, %s, %s, %s)", 
                               (folio, product_id, cantidad, precio_unitario))

            self.cnn.commit()
            messagebox.showinfo("Éxito", f"Factura guardada correctamente con folio #{folio}")
            self.clear_all()
            self.load_next_folio()  # Cargar el próximo folio después de guardar la factura
        except mysql.connector.Error as e:
            self.cnn.rollback()
            messagebox.showerror("Error", f"No se pudo guardar la factura: {e}")
        finally:
            cursor.close()

    def clear_all(self):
        """Limpia toda la interfaz."""
        for entry in [self.id_cliente_entry, self.id_producto_entry, self.cantidad_entry, self.empresa_entry]:
            entry.delete(0, tk.END)
        for label in [self.nombre_cliente_label, self.direccion_cliente_label, self.nombre_producto_label]:
            label.config(text="")
        for row in self.invoice_table.get_children():
            self.invoice_table.delete(row)
        self.total_neto_label.config(text="0.00")
        self.iva_label.config(text="0.00")
        self.total_label.config(text="0.00")
