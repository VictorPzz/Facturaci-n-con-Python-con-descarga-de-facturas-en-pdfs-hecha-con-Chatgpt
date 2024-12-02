import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import random
import string

class ClientFrame(tk.Frame):
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

        # Campos de entrada
        self.entries = {}
        fields = ["Nombre", "Apellido Paterno", "Apellido Materno", "Fecha de Nacimiento (YYYY-MM-DD)", "Dirección", "Teléfono", "Email"]
        for idx, field in enumerate(fields):
            tk.Label(self, text=f"{field}:").grid(row=idx, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(self, width=20)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.entries[field] = entry

        # RFC no editable
        tk.Label(self, text="RFC:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.rfc_entry = tk.Entry(self, width=20, state="disabled")
        self.rfc_entry.grid(row=7, column=1, padx=5, pady=5)

        # Botones (inicialmente no visibles)
        self.add_button = tk.Button(self, text="Agregar", bg="green", fg="white", command=self.add_client, width=10)
        self.modify_button = tk.Button(self, text="Modificar", bg="blue", fg="white", command=self.modify_client, width=10)
        self.delete_button = tk.Button(self, text="Eliminar", bg="red", fg="white", command=self.delete_client, width=10)
        self.clear_button = tk.Button(self, text="Limpiar", bg="orange", fg="white", command=self.clear_fields, width=10)
        self.back_button = tk.Button(self, text="Regresar", bg="#888888", fg="white", command=self.volver_menu_principal, width=10)

        self.back_button.grid(row=0, column=2, pady=10)

        # Tabla de clientes
        self.table = ttk.Treeview(self, columns=("ID", "Nombre", "Apellido Paterno", "Apellido Materno", "Fecha Nac", "Dirección", "Teléfono", "Email", "RFC"), show="headings", height=8)
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=100)

        self.table.grid(row=10, column=0, columnspan=3, padx=5, pady=10)
        self.table.bind("<ButtonRelease-1>", self.on_client_select)

        self.load_clients()
        self.setup_entry_tracking()
        self.check_fields()
        tk.Button(self, text="Ayuda", bg="#0073e6", fg="white", font=("Arial", 12), command=self.switch_to_help).grid(row=1, column=2, padx=5, pady=5)

        # Tabla de clientes (ya definida)...

    def switch_to_help(self):
        """Redirige a la ayuda de clientes."""
        self.master.switch_to_help_clientes()

    def volver_menu_principal(self):
        self.master.switch_to_main_interface()

    def load_clients(self):
        """Cargar clientes desde la base de datos a la tabla."""
        for row in self.table.get_children():
            self.table.delete(row)
        self.cursor.execute("SELECT * FROM clientes")
        for row in self.cursor.fetchall():
            self.table.insert("", "end", values=row)

    def clear_fields(self):
        """Limpiar campos y volver al modo de agregar."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.rfc_entry.config(state="normal")
        self.rfc_entry.delete(0, tk.END)
        self.rfc_entry.config(state="disabled")
        self.switch_to_add_mode()

    def switch_to_add_mode(self):
        """Configurar botones para agregar un cliente."""
        self.hide_all_buttons()
        if self.all_fields_filled():
            self.add_button.grid(row=8, column=0, padx=5, pady=5)
        if self.any_field_filled():
            self.clear_button.grid(row=9, column=0, columnspan=2, pady=5)

    def switch_to_edit_mode(self):
        """Configurar botones para editar un cliente."""
        self.hide_all_buttons()
        self.modify_button.grid(row=8, column=0, padx=5, pady=5)
        self.delete_button.grid(row=8, column=1, padx=5, pady=5)
        self.clear_button.grid(row=9, column=0, columnspan=2, pady=5)

    def on_client_select(self, event):
        """Cargar los datos del cliente seleccionado en los campos."""
        selected_item = self.table.selection()
        if not selected_item:
            return
        client_data = self.table.item(selected_item)["values"]
        for idx, field in enumerate(self.entries):
            self.entries[field].delete(0, tk.END)
            self.entries[field].insert(0, client_data[idx + 1])  # Saltar ID
        self.rfc_entry.config(state="normal")
        self.rfc_entry.delete(0, tk.END)
        self.rfc_entry.insert(0, client_data[8])
        self.rfc_entry.config(state="disabled")
        self.switch_to_edit_mode()

    def add_client(self):
        """Agregar un cliente nuevo."""
        values = tuple(entry.get() for entry in self.entries.values())
        rfc = self.calculate_rfc(values)
        values = values + (rfc,)
        query = "INSERT INTO clientes (nombre, apellido_paterno, apellido_materno, fecha_nacimiento, direccion, telefono, email, rfc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            self.load_clients()
            self.clear_fields()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar cliente: {e}")

    def modify_client(self):
        """Modificar el cliente seleccionado."""
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para modificar.")
            return

        client_id = self.table.item(selected_item)["values"][0]
        values = tuple(entry.get() for entry in self.entries.values())
        rfc = self.calculate_rfc(values)
        values = values + (rfc, client_id)
        query = "UPDATE clientes SET nombre=%s, apellido_paterno=%s, apellido_materno=%s, fecha_nacimiento=%s, direccion=%s, telefono=%s, email=%s, rfc=%s WHERE id=%s"
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            self.load_clients()
            self.clear_fields()
            messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar cliente: {e}")

    def delete_client(self):
        """Eliminar el cliente seleccionado."""
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")
            return

        client_id = self.table.item(selected_item)["values"][0]
        query = "DELETE FROM clientes WHERE id=%s"
        try:
            self.cursor.execute(query, (client_id,))
            self.conn.commit()
            self.load_clients()
            self.clear_fields()
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar cliente: {e}")

    def hide_all_buttons(self):
        """Ocultar todos los botones."""
        self.add_button.grid_forget()
        self.modify_button.grid_forget()
        self.delete_button.grid_forget()
        self.clear_button.grid_forget()

    def setup_entry_tracking(self):
        """Configurar seguimiento de cambios en los campos."""
        for entry in self.entries.values():
            entry.bind("<KeyRelease>", lambda event: self.check_fields())

    def check_fields(self):
        """Revisar los campos para mostrar botones relevantes."""
        if self.all_fields_filled():
            self.switch_to_add_mode()
            self.rfc_entry.config(state="normal")
            self.rfc_entry.delete(0, tk.END)
            self.rfc_entry.insert(0, self.calculate_rfc(tuple(entry.get() for entry in self.entries.values())))
            self.rfc_entry.config(state="disabled")
        elif self.any_field_filled():
            self.clear_button.grid(row=9, column=0, columnspan=2, pady=5)
        else:
            self.hide_all_buttons()

    def all_fields_filled(self):
        """Verificar si todos los campos están llenos."""
        return all(entry.get() for entry in self.entries.values())

    def any_field_filled(self):
        """Verificar si al menos un campo está lleno."""
        return any(entry.get() for entry in self.entries.values())

    def calculate_rfc(self, values):
        """Generar un RFC basado en nombre y apellidos."""
        nombre, apellido_paterno, apellido_materno, fecha_nac = values[:4]
        fecha_rfc = fecha_nac.replace("-", "")[2:8]  # Tomar fecha en formato YYMMDD
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        rfc = f"{apellido_paterno[:2].upper()}{apellido_materno[:1].upper()}{nombre[:1].upper()}{fecha_rfc}{random_chars}"
        return rfc
