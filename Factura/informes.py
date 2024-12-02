import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer  # Importar Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from decimal import Decimal

class ConversorNumeros:
    # Diccionarios extendidos
    __unidades = {
        0: '', 1: 'un', 2: 'dos', 3: 'tres', 4: 'cuatro', 5: 'cinco', 6: 'seis', 7: 'siete', 8: 'ocho', 9: 'nueve'
    }

    __decenas = {
        10: 'diez', 11: 'once', 12: 'doce', 13: 'trece', 14: 'catorce', 15: 'quince', 16: 'dieciséis', 17: 'diecisiete', 
        18: 'dieciocho', 19: 'diecinueve', 20: 'veinte', 30: 'treinta', 40: 'cuarenta', 50: 'cincuenta', 60: 'sesenta', 
        70: 'setenta', 80: 'ochenta', 90: 'noventa'
    }

    __centenas = {
        100: 'ciento', 200: 'doscientos', 300: 'trescientos', 400: 'cuatrocientos', 500: 'quinientos', 
        600: 'seiscientos', 700: 'setecientos', 800: 'ochocientos', 900: 'novecientos'
    }
    
    __miles = {
        1000: 'mil', 2000: 'dos mil', 3000: 'tres mil', 4000: 'cuatro mil', 5000: 'cinco mil', 6000: 'seis mil',
        7000: 'siete mil', 8000: 'ocho mil', 9000: 'nueve mil'
    }

    @classmethod
    def convertir_unidades(cls, n):
        return cls.__unidades.get(n, '')

    @classmethod
    def convertir_decenas(cls, n):
        if 10 <= n <= 19:
            return cls.__decenas[n]
        elif n >= 20:
            unidad = n % 10
            decena = n - unidad
            if unidad == 0:
                return cls.__decenas[decena]
            else:
                if decena == 20:
                    return f"veinti{cls.convertir_unidades(unidad)}"
                elif unidad == 1:
                    return f"{cls.__decenas[decena]} y un"
                else:
                    return f"{cls.__decenas[decena]} y {cls.convertir_unidades(unidad)}"
        else:
            return cls.convertir_unidades(n)

    @classmethod
    def convertir_centenas(cls, n):
        centena = n // 100 * 100
        resto = n % 100
        if centena == 100 and resto == 0:
            return 'cien'
        elif centena > 0 and resto > 0:
            return f"{cls.__centenas[centena]} {cls.convertir_decenas(resto)}"
        elif centena > 0:
            return cls.__centenas[centena]
        else:
            return cls.convertir_decenas(n)
        
    
    @classmethod
    def convertir_miles(cls, n):
        millar = n // 1000
        resto = n % 1000
        
        if millar == 1:
            miles_str = "mil"
        else:
            miles_str = cls.convertir_centenas(millar) + " mil"
        
        if resto > 0:
            return f"{miles_str} {cls.convertir_centenas(resto)}"
        else:
            return miles_str

    @classmethod
    def convertir_a_letras(cls, n):
        if n == 0:
            return "cero"
        elif n > 99999:
            return "El número está fuera del rango permitido."
        elif n >= 1000:
            return cls.convertir_miles(n)
        else:
            letras = cls.convertir_centenas(n)
            if 100 < n < 200:
                letras = letras.replace("cien ", "ciento ")
            return letras

    @staticmethod
    def convertir_decimales(decimal_str):
        if len(decimal_str) == 1:
            decimal_str += '0'
        elif len(decimal_str) > 2:
            decimal_str = decimal_str[:2]
        return decimal_str
class InformesFrame(tk.Frame):
    def __init__(self, master, cnn):
        super().__init__(master, bg="#f0f0f0")
        self.cnn = cnn

        # Encabezado
        tk.Label(self, text="Informes de Facturación", font=("Arial", 18, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=3, pady=10)

        # Tabla de facturas
        columns = ("Folio", "Cliente", "Fecha", "Monto", "Empresa")
        self.invoice_table = ttk.Treeview(self, columns=columns, show="headings", height=10)
        for col in columns:
            self.invoice_table.heading(col, text=col)
            self.invoice_table.column(col, width=100 if col == "Folio" else 150)
            self.invoice_table.grid(row=1, column=0, columnspan=3, pady=10, padx=10)

        # Botones
        tk.Button(self, text="Ver Detalles", bg="#0073e6", fg="white", command=self.show_invoice_details).grid(row=2, column=0, pady=10)
        tk.Button(self, text="Exportar PDF", bg="green", fg="white", command=self.export_invoice_to_pdf).grid(row=2, column=1, pady=10)
        tk.Button(self, text="Regresar", bg="gray", fg="white", command=self.go_back).grid(row=2, column=2, pady=10)

        self.load_invoices()
    
        # Título con botón de ayuda
        title_frame = tk.Frame(self, bg="#f0f0f0")  # Un marco para organizar el título y el botón
        title_frame.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")  # Mantiene alineación en la parte superior

        tk.Label(title_frame, text="Informes de Facturación", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=10)

        tk.Button(title_frame, text="Ayuda", bg="#0073e6", fg="white", font=("Arial", 12),
                  command=self.master.switch_to_help_informes).pack(side=tk.RIGHT, padx=10)

    def switch_to_help(self):
        """Redirige a la ayuda de informes."""
        self.master.switch_to_help_informes()

    def load_invoices(self):
        """Carga las facturas desde la base de datos en la tabla."""
        for row in self.invoice_table.get_children():
            self.invoice_table.delete(row)
        
        cursor = self.cnn.cursor()
        cursor.execute("SELECT folio, (SELECT nombre FROM clientes WHERE clientes.id = fact_encab.idCliente) AS Cliente, fecha, monto, empresa FROM fact_encab ORDER BY fecha DESC")
        for invoice in cursor.fetchall():
            self.invoice_table.insert("", "end", values=invoice)
        cursor.close()

    def show_invoice_details(self):
        """Muestra los detalles de la factura seleccionada."""
        selected_item = self.invoice_table.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una factura para ver detalles.")
            return

        folio = self.invoice_table.item(selected_item)["values"][0]
        DetailsWindow(folio, self.cnn).grab_set()

    def export_invoice_to_pdf(self):
        """Genera un archivo PDF de la factura seleccionada con diseño mejorado."""
        selected_item = self.invoice_table.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una factura para exportar a PDF.")
            return

        folio = self.invoice_table.item(selected_item)["values"][0]
        cursor = self.cnn.cursor()
        cursor.execute("""
        SELECT 
            f.folio, f.fecha, c.nombre, c.direccion, c.rfc, f.empresa, d.idProd, p.nombre, d.cant, d.precio_unitario, 
            (d.cant * d.precio_unitario) AS importe
        FROM 
            fact_encab f
        JOIN 
            fact_detalle d ON f.folio = d.folio
        JOIN 
            productos p ON d.idProd = p.id
        JOIN 
            clientes c ON f.idCliente = c.id
        WHERE 
            f.folio = %s
    """, (folio,))
        factura = cursor.fetchall()
        cursor.close()

        if not factura:
            messagebox.showerror("Error", "No se encontraron detalles de la factura.")
            return

        # Configurar PDF
        pdf_name = f"Factura_{folio}.pdf"
        doc = SimpleDocTemplate(pdf_name, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Determinar el título
        empresa = factura[0][5]
        titulo = empresa if empresa else f"Factura No: {factura[0][0]}"
        elements.append(Paragraph(titulo, styles['Title']))

        # Datos de la factura
        elements.extend([
            Paragraph(f"Fecha: {factura[0][1]}", styles['Normal']),
            Paragraph(f"Cliente: {factura[0][2]}", styles['Normal']),
            Paragraph(f"Dirección: {factura[0][3]}", styles['Normal']),
            Paragraph(f"RFC: {factura[0][4]}", styles['Normal']),
            Spacer(1, 12),
        ])

        # Tabla de productos
        data = [["Producto", "Cantidad", "Precio Unitario", "Importe"]]
        total_neto = Decimal(0)

        for item in factura:
            data.append([item[7], item[8], f"${item[9]:.2f}", f"${item[10]:.2f}"])
            total_neto += Decimal(item[10])

        iva = total_neto * Decimal('0.19')
        total = total_neto + iva

        # Agregar subtotales y totales solo en las últimas filas
        data.extend([
            ["", "", "Subtotal:", f"${total_neto:.2f}"],
            ["", "", "IVA (19%):", f"${iva:.2f}"],
            ["", "", "Total:", f"${total:.2f}"]
        ])

        table = Table(data, colWidths=[200, 100, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -2), 1, colors.black),
            ('GRID', (-2, -3), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))

        elements.append(table)

        total_letras = ConversorNumeros.convertir_a_letras(int(total)) + " pesos con " + ConversorNumeros.convertir_decimales(str(round(total % 1, 2)).split(".")[1]) + "/100 M.N."
        elements.append(Paragraph(f"Total con letra: {total_letras}.", styles['Normal']))

        # Generar PDF
        doc.build(elements)
        messagebox.showinfo("Éxito", f"Factura exportada como {pdf_name}")

    def go_back(self):
        """Regresa al menú principal."""
        self.master.switch_to_main_interface()
    
class DetailsWindow(tk.Toplevel):
    def __init__(self, folio, cnn):
        super().__init__()
        self.title(f"Detalles de la Factura: {folio}")
        self.geometry("700x400")
        self.cnn = cnn

        tk.Label(self, text=f"Detalles de la Factura: {folio}", font=("Arial", 16, "bold")).pack(pady=10)

        columns = ("ID Producto", "Nombre", "Cantidad", "Precio Unitario", "Importe")
        details_table = ttk.Treeview(self, columns=columns, show="headings", height=10)
        for col in columns:
            details_table.heading(col, text=col)
            details_table.column(col, width=120)
        details_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_invoice_details(folio, details_table)

    def load_invoice_details(self, folio, details_table):
        cursor = self.cnn.cursor()
        query = """
            SELECT d.idProd, p.nombre, d.cant, d.precio_unitario, (d.cant * d.precio_unitario) AS importe
            FROM fact_detalle d
            JOIN productos p ON d.idProd = p.id
            WHERE d.folio = %s
        """
        cursor.execute(query, (folio,))
        for row in cursor.fetchall():
            details_table.insert("", "end", values=row)
        cursor.close()