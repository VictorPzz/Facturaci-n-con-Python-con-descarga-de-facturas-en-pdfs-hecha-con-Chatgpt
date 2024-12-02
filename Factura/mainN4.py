import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from productos import ProductFrame
from clientes import ClientFrame
from facturacion import RedesignedFacturacionFrame
from informes import InformesFrame
from ayuda import HelpMenuFrame, HelpProductosFrame, HelpClientesFrame, HelpFacturacionFrame, HelpInformesFrame
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de facturacion")
        self.geometry("420x500")
        self.configure(bg="#0073e6")  

        # Conexión a la base de datos
        try:
            self.cnn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                passwd="",
                database="usuarios"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}")
            self.destroy()
            return
        
        self.switch_to_login()

    def switch_to_login(self):
        self.clear_frames()
        print("Switching to LoginFrame")
        LoginFrame(self, self.cnn).pack(pady=20)

    def switch_to_forgot_password(self):
        self.clear_frames()
        print("Switching to ForgotPasswordFrame")
        ForgotPasswordFrame(self, self.cnn).pack(pady=20)

    def switch_to_register(self):
        self.clear_frames()
        print("Switching to RegisterFrame")
        RegisterFrame(self, self.cnn).pack(pady=20)

    def clear_frames(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def switch_to_main_interface(self):
        self.clear_frames()
        print("Switching to MainInterfaceFrame")
        MainInterfaceFrame(self).pack(pady=20)

    def switch_to_catalog_interface(self):
        self.clear_frames()
        print("Switching to CatalogInterfaceFrame")
        CatalogInterfaceFrame(self).pack(pady=20)
    
    def switch_to_facturacion(self):
        self.clear_frames()
        print("Switching to FacturacionFrame")
        RedesignedFacturacionFrame(self, self.cnn).pack(pady=20)
    
    def switch_to_reports(self):
        self.clear_frames()
        InformesFrame(self, self.cnn).pack(pady=20)
        
    def switch_to_help_menu(self):
        self.clear_frames()
        HelpMenuFrame(self).pack(pady=20)

    def switch_to_help_productos(self):
        self.clear_frames()
        HelpProductosFrame(self).pack(pady=20)

    def switch_to_help_clientes(self):
        self.clear_frames()
        HelpClientesFrame(self).pack(pady=20)

    def switch_to_help_facturacion(self):
        self.clear_frames()
        HelpFacturacionFrame(self).pack(pady=20)

    def switch_to_help_informes(self):
        self.clear_frames()
        HelpInformesFrame(self).pack(pady=20)


class LoginFrame(tk.Frame):
    def __init__(self, master, cnn):
        super().__init__(master, bg="#add8e6", padx=20, pady=20)
        self.cnn = cnn
        
        tk.Label(self, text="Inicio de Sesión", font=("Arial", 16), bg="#add8e6", fg="#333333").pack(pady=10)
        
        form_frame = tk.Frame(self, bg="#add8e6")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Usuario", bg="#add8e6", fg="#333333").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = tk.Entry(form_frame, width=20, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Contraseña", bg="#add8e6", fg="#333333").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(form_frame, show="*", width=20, font=("Arial", 12))
        self.password_entry.grid(row=1, column=1, pady=5)

        button_frame = tk.Frame(self, bg="#add8e6")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Ingresar", command=self.login, bg="#333333", fg="white", width=15).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Olvidé mi contraseña", command=self.switch_to_forgot_password, bg="#888888", fg="white", width=20).grid(row=1, column=0, pady=10)
        tk.Button(button_frame, text="Registrar nuevo usuario", command=self.switch_to_register, bg="#888888", fg="white", width=20).grid(row=2, column=0)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        cursor = self.cnn.cursor()
        query = "SELECT * FROM users WHERE Username = %s AND Password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            messagebox.showinfo("Éxito", "¡Bienvenido!")
            self.master.switch_to_main_interface()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrecta")

    def switch_to_forgot_password(self):
        self.master.switch_to_forgot_password()

    def switch_to_register(self):
        self.master.switch_to_register()
    

import tkinter as tk

class MainInterfaceFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")  
        
        tk.Label(self, text="Facturación", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333333").pack(pady=10)

        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="Catálogos", font=("Arial", 12), width=20, bg="#666666", fg="white", command=master.switch_to_catalog_interface).pack(pady=5)
        tk.Button(button_frame, text="Facturación", font=("Arial", 12), width=20, bg="#666666", fg="white", command=master.switch_to_facturacion).pack(pady=5)
        tk.Button(button_frame, text="Informes", font=("Arial", 12), width=20, bg="#666666", fg="white", command=master.switch_to_reports).pack(pady=5)
        tk.Button(button_frame, text="Ayuda", font=("Arial", 12), width=20, bg="#666666", fg="white", command=master.switch_to_help_menu).pack(pady=5)
        tk.Button(self, text="Cerrar Sesión", command=self.logout, bg="#888888", fg="white", width=22, font=("Arial", 12)).pack(pady=20)

    def logout(self):
        self.master.switch_to_login()

class CatalogInterfaceFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")  

        tk.Label(self, text="Catálogo", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333333").pack(pady=10)

        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="Productos", font=("Arial", 12), width=20, bg="#666666", fg="white", command=self.open_productos).pack(pady=5)
        tk.Button(button_frame, text="Clientes", font=("Arial", 12), width=20, bg="#666666", fg="white", command=self.open_clientes).pack(pady=5)

        tk.Button(self, text="Volver", command=self.volver, bg="#888888", fg="white", width=22, font=("Arial", 12)).pack(pady=20)

    def volver(self):
        self.master.switch_to_main_interface()
        
    def open_productos(self):
        self.master.clear_frames()
        ProductFrame(self.master, self.master.cnn).pack(pady=20)
    
    def open_clientes(self):
        self.master.clear_frames()
        from clientes import ClientFrame  
        ClientFrame(self.master, self.master.cnn).pack(pady=20)


import tkinter as tk
from tkinter import messagebox

class ForgotPasswordFrame(tk.Frame):
    def __init__(self, master, cnn):
        super().__init__(master, bg="#D7D8DA")
        self.cnn = cnn

        tk.Label(self, text="Recuperación de Contraseña", font=("Arial", 18, "bold"), bg="#D7D8DA", fg="#333333").pack(pady=10)

        form_frame = tk.Frame(self, bg="#D7D8DA")
        form_frame.pack(pady=15)

        tk.Label(form_frame, text="Correo Electrónico o Usuario", bg="#D7D8DA", fg="#333333", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.email_or_user_entry = tk.Entry(form_frame, width=22, font=("Arial", 12))
        self.email_or_user_entry.grid(row=0, column=1, pady=5)

        button_frame = tk.Frame(self, bg="#D7D8DA")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Enviar", command=self.recover_password, bg="#333333", fg="white", width=18, font=("Arial", 12)).grid(row=0, column=0, padx=5)
        
        back_button = tk.Button(self, text="Regresar", command=self.switch_to_login, bg="#888888", fg="white", font=("Arial", 10))
        back_button.pack(side="bottom", pady=10)

    def recover_password(self):
        email_or_user = self.email_or_user_entry.get()

        if not email_or_user:
            messagebox.showwarning("Advertencia", "Por favor ingrese su correo electrónico o nombre de usuario")
            return

        cursor = self.cnn.cursor()
        query = "SELECT Email, Password FROM users WHERE Email = %s OR Username = %s"
        cursor.execute(query, (email_or_user, email_or_user))
        result = cursor.fetchone()
        cursor.close()

        if result:
            recipient_email, user_password = result
            self.send_recovery_email(recipient_email, user_password)
            messagebox.showinfo("Recuperación de Contraseña", "Se ha enviado un correo de recuperación a su dirección de correo electrónico.")
        else:
            messagebox.showerror("Error", "No se encontró un usuario con ese correo o nombre de usuario")

    def send_recovery_email(self, recipient_email, user_password):
        """Enviar correo de recuperación al usuario."""
        sender_email = "vcalderondd@gmail.com"  
        sender_password = "lbxo tzba hhce abct" 
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        subject = "Recuperación de Contraseña - Sistema de Facturación"
        body = f"Hola,\n\nSu contraseña es: {user_password}.\n\nSaludos,\nEquipo de Soporte."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  
                server.login(sender_email, sender_password)  
                server.send_message(msg)
                print(f"Correo enviado a {recipient_email}.")
        except smtplib.SMTPAuthenticationError:
            messagebox.showerror("Error", "Fallo de autenticación. Verifique las credenciales.")
        except smtplib.SMTPConnectError:
            messagebox.showerror("Error", "No se pudo conectar al servidor SMTP.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo: {e}")


    def switch_to_login(self):
        self.master.switch_to_login()

import tkinter as tk
from tkinter import messagebox

class RegisterFrame(tk.Frame):
    def __init__(self, master, cnn):
        super().__init__(master, bg="#D7D8DA", padx=20, pady=20)  # Fondo del frame de registro con padding
        self.cnn = cnn

        tk.Label(self, text="Registro de Usuario", font=("Arial", 18, "bold"), bg="#D7D8DA", fg="#333333").pack(pady=10)

        # Formulario
        form_frame = tk.Frame(self, bg="#D7D8DA")
        form_frame.pack(pady=10)

        fields = [
            ("Correo Electrónico", 0),
            ("Número Telefónico", 1),
            ("Nombre de Usuario", 2),
            ("Contraseña", 3, "*"),
            ("Confirmar Contraseña", 4, "*")
        ]
        
        self.entries = {}
        for label, row, *show in fields:
            tk.Label(form_frame, text=label, bg="#D7D8DA", fg="#333333", font=("Arial", 12)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
            
            entry = tk.Entry(form_frame, width=22, font=("Arial", 12), show=show[0] if show else None)
            entry.grid(row=row, column=1, pady=5)
            self.entries[label] = entry

        # Botones
        button_frame = tk.Frame(self, bg="#D7D8DA")
        button_frame.pack(pady=20)

        # Botón de registro
        tk.Button(button_frame, text="Registrar", command=self.register, bg="#333333", fg="white", width=18, font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        
        # Botón para volver al login
        tk.Button(button_frame, text="Volver al Login", command=self.switch_to_login, bg="#888888", fg="white", width=18, font=("Arial", 12)).grid(row=1, column=0, pady=5)

    def register(self):
        email = self.entries["Correo Electrónico"].get()
        phone = self.entries["Número Telefónico"].get()
        username = self.entries["Nombre de Usuario"].get()
        password = self.entries["Contraseña"].get()
        confirm_password = self.entries["Confirmar Contraseña"].get()
        
        if not (email and phone and username and password and confirm_password):
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos")
            return
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Por favor ingrese un correo electrónico válido")
            return
        
        if not (phone.isdigit() and len(phone) == 10):
            messagebox.showerror("Error", "El número de teléfono no es valido, debe contener 10 dígitos")
            return
        
        
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        cursor = self.cnn.cursor()
        query = "INSERT INTO users (Email, PhoneNumber, Username, Password, ConfirmPassword) VALUES (%s, %s, %s, %s, %s)"
        
        try:
            cursor.execute(query, (email, phone, username, password, confirm_password))
            self.cnn.commit()
            messagebox.showinfo("Registro Exitoso", "Usuario registrado exitosamente")
            self.switch_to_login()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al registrar: {err}")
        finally:
            cursor.close()

    def switch_to_login(self):
        self.master.switch_to_login()


if __name__ == "__main__":
    app = App()
    app.mainloop()
