import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class ProductFrame(tk.Frame):
    def __init__(self, master, cnn):
        super().__init__(master)
        self.master = master
        self.cnn = cnn
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usuarios"
        )
        self.cursor = self.conn.cursor()

        tk.Label(self, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = tk.Entry(self, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Descripción:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.desc_entry = tk.Entry(self, width=20)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Precio Unitario:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.price_entry = tk.Entry(self, width=20)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Existencia:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.stock_entry = tk.Entry(self, width=20)
        self.stock_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self, text="Unidad de Medida:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.unit_entry = tk.Entry(self, width=20)
        self.unit_entry.grid(row=4, column=1, padx=5, pady=5)

        # Botones (no visibles inicialmente)
        self.add_button = tk.Button(self, text="Agregar", bg="green", fg="white", command=self.add_product, width=10)
        self.modify_button = tk.Button(self, text="Modificar", bg="blue", fg="white", command=self.modify_product, width=10)
        self.delete_button = tk.Button(self, text="Eliminar", bg="red", fg="white", command=self.delete_product, width=10)
        self.clear_button = tk.Button(self, text="Limpiar", bg="orange", fg="white", command=self.clear_fields, width=10)

        # Botón de regresar
        self.back_button = tk.Button(self, text="Regresar", bg="#888888", fg="white", command=self.volver_menu_principal, width=10)
        self.back_button.grid(row=0, column=2, pady=10)

        # Tabla de productos
        self.table = ttk.Treeview(self, columns=("ID", "Producto", "Descripción", "Precio", "Existencia", "Unidad", "Fecha de alta"), show="headings", height=8)
        self.table.heading("ID", text="ID")
        self.table.heading("Producto", text="Producto")
        self.table.heading("Descripción", text="Descripción")
        self.table.heading("Precio", text="Precio")
        self.table.heading("Existencia", text="Existencia")
        self.table.heading("Unidad", text="Unidad")
        self.table.heading("Fecha de alta", text="Fecha de alta")

        self.table.column("ID", width=50)
        self.table.column("Producto", width=100)
        self.table.column("Descripción", width=150)
        self.table.column("Precio", width=80)
        self.table.column("Existencia", width=80)
        self.table.column("Unidad", width=100)
        self.table.column("Fecha de alta", width=120)

        self.table.grid(row=7, column=0, columnspan=3, padx=5, pady=10)
        self.table.bind("<ButtonRelease-1>", self.on_product_select)

        self.load_products()

        self.setup_entry_tracking()
        self.check_fields()
        
        tk.Button(self, text="Ayuda", bg="#0073e6", fg="white", font=("Arial", 12), command=self.switch_to_help).grid(row=1, column=2, padx=5, pady=5)

    def switch_to_help(self):
         """Redirige a la ayuda de productos."""
         self.master.switch_to_help_productos()


    def volver_menu_principal(self):
        self.master.switch_to_main_interface()

    def load_products(self):
        """Cargar productos desde la base de datos a la tabla."""
        for row in self.table.get_children():
            self.table.delete(row)
        self.cursor.execute("SELECT * FROM productos")
        for row in self.cursor.fetchall():
            self.table.insert("", "end", values=row)

    def clear_fields(self):
        """Limpiar campos de entrada y habilitar modo de agregar."""
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.unit_entry.delete(0, tk.END)
        self.switch_to_add_mode()

    def switch_to_add_mode(self):
        """Mostrar botón de agregar solo si todos los campos están llenos."""
        self.add_button.grid_forget()
        self.modify_button.grid_forget()
        self.delete_button.grid_forget()
        self.clear_button.grid_forget()

        if self.all_fields_filled():
            self.add_button.grid(row=5, column=0, padx=5, pady=10)
        elif self.any_field_filled():
            self.clear_button.grid(row=6, column=0, columnspan=3, pady=10)

    def switch_to_edit_mode(self):
        """Mostrar botones de edición cuando se selecciona un producto."""
        self.add_button.grid_forget()
        self.modify_button.grid(row=5, column=0, padx=5, pady=10)
        self.delete_button.grid(row=5, column=1, padx=5, pady=10)
        self.clear_button.grid(row=6, column=0, columnspan=3, pady=10)

    def on_product_select(self, event):
        """Cargar datos del producto seleccionado y habilitar modo de edición."""
        selected_item = self.table.selection()
        if not selected_item:
            return
        product_data = self.table.item(selected_item)["values"]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, product_data[1])
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, product_data[2])
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, product_data[3])
        self.stock_entry.delete(0, tk.END)
        self.stock_entry.insert(0, product_data[4])
        self.unit_entry.delete(0, tk.END)
        self.unit_entry.insert(0, product_data[5])
        self.switch_to_edit_mode()

    def add_product(self):
        """Agregar un nuevo producto a la base de datos."""
        nombre = self.name_entry.get()
        descripcion = self.desc_entry.get()
        precio = self.price_entry.get()
        existencia = self.stock_entry.get()
        unidad = self.unit_entry.get()

        query = "INSERT INTO productos (nombre, descripcion, precio, existencia, unidad) VALUES (%s, %s, %s, %s, %s)"
        values = (nombre, descripcion, precio, existencia, unidad)

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            self.load_products()
            self.clear_fields()
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {e}")

    def modify_product(self):
        """Modificar el producto seleccionado en la base de datos."""
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Atención", "Selecciona un producto para modificar.")
            return

        product_id = self.table.item(selected_item)["values"][0]
        nombre = self.name_entry.get()
        descripcion = self.desc_entry.get()
        precio = self.price_entry.get()
        existencia = self.stock_entry.get()
        unidad = self.unit_entry.get()

        query = "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, existencia=%s, unidad=%s WHERE id=%s"
        values = (nombre, descripcion, precio, existencia, unidad, product_id)

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            self.load_products()
            self.clear_fields()
            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar producto: {e}")

    def delete_product(self):
        """Eliminar el producto seleccionado de la base de datos."""
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Atención", "Selecciona un producto para eliminar.")
            return

        product_id = self.table.item(selected_item)["values"][0]

        query = "DELETE FROM productos WHERE id=%s"

        try:
            self.cursor.execute(query, (product_id,))
            self.conn.commit()
            self.load_products()
            self.clear_fields()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {e}")

    def setup_entry_tracking(self):
        """Configurar seguimiento de cambios en los campos de entrada."""
        self.name_entry.bind("<KeyRelease>", lambda event: self.check_fields())
        self.desc_entry.bind("<KeyRelease>", lambda event: self.check_fields())
        self.price_entry.bind("<KeyRelease>", lambda event: self.check_fields())
        self.stock_entry.bind("<KeyRelease>", lambda event: self.check_fields())
        self.unit_entry.bind("<KeyRelease>", lambda event: self.check_fields())

    def check_fields(self):
        """Revisar si los campos están llenos o vacíos."""
        if self.all_fields_filled():
            self.switch_to_add_mode()
        elif self.any_field_filled():
            self.clear_button.grid(row=6, column=0, columnspan=3, pady=10)
        else:
            self.clear_button.grid_forget()

    def all_fields_filled(self):
        """Verificar si todos los campos están llenos."""
        return all([
            self.name_entry.get(),
            self.desc_entry.get(),
            self.price_entry.get(),
            self.stock_entry.get(),
            self.unit_entry.get()
        ])

    def any_field_filled(self):
        """Verificar si al menos un campo está lleno."""
        return any([
            self.name_entry.get(),
            self.desc_entry.get(),
            self.price_entry.get(),
            self.stock_entry.get(),
            self.unit_entry.get()
        ])
