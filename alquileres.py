import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import csv


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario")
        self.root.geometry("600x400")
        self.root.configure(bg='#add8e6')  # Fondo azul claro

        # Inicializar la base de datos
        self.conn = sqlite3.connect("inventario.db")
        print('Connected !!!!')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS productos 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        nombre TEXT, tipo TEXT, cantidad INTEGER)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS prestamos 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         cedula TEXT, 
                        nombre TEXT, tel TEXT, valor INTEGER, cantidad INTEGER)''')

        # Insertar algunos datos de ejemplo
        self.c.execute(
            "INSERT INTO productos (nombre, tipo, cantidad) VALUES ('Silla A', 'silla', 30)")
        self.c.execute(
            "INSERT INTO productos (nombre, tipo, cantidad) VALUES ('Mesa B', 'mesa', 50)")
        self.c.execute(
            "INSERT INTO productos (nombre, tipo, cantidad) VALUES ('Silla C', 'silla', 40)")
        self.c.execute(
            "INSERT INTO productos (nombre, tipo, cantidad) VALUES ('Mesa D', 'mesa', 20)")
        print('Elementos insertados !!!')

        print('Query executed !!')

        # Inicio de sesión
        self.login_frame = tk.Frame(self.root, bg='#add8e6')
        self.login_frame.pack(pady=50)
        tk.Label(self.login_frame, text="Usuario:",
                 bg='#add8e6').grid(row=0, column=0)
        tk.Label(self.login_frame, text="Contraseña:",
                 bg='#add8e6').grid(row=1, column=0)
        self.user_entry = tk.Entry(self.login_frame)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.user_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        tk.Button(self.login_frame, text="Iniciar Sesión", command=self.login,
                  bg='#87ceeb', height=1).grid(row=2, column=0, columnspan=2)

        # Sección de gestión de inventario
        self.inventory_frame = tk.Frame(self.root, bg='#add8e6')
        self.inventory_frame.pack_forget()

        tk.Label(self.inventory_frame, text="Gestión de Inventario",
                 font=("Helvetica", 16), bg='#add8e6').pack(pady=10)

        tk.Button(self.inventory_frame, text="Mostrar Inventario",
                  command=self.show_inventory_dialog, bg='#87ceeb', height=1).pack(pady=10)
        tk.Button(self.inventory_frame, text="Insertar producto",
                  command=self.insert_product, bg='#87ceeb', height=1).pack(pady=10)
        tk.Button(self.inventory_frame, text="Hacer Préstamo",
                  command=self.loan, bg='#87ceeb', height=1).pack(pady=10)
        tk.Button(self.inventory_frame, text="Actualizar Inventario",
                  command=self.update_inventory, bg='#87ceeb', height=1).pack(pady=10)
        tk.Button(self.inventory_frame, text="Eliminar del inventario",
                  command=self.delete_operation, bg='#87ceeb', height=1).pack(pady=10)
        tk.Button(self.inventory_frame, text="Descargar reporte prestamos",
                  command=self.descargar_datos, bg='#87ceeb', height=1).pack(pady=10)
        tk.Button(self.inventory_frame, text="Cerrar Sesión",
                  command=self.logout, bg='#87ceeb', height=1).pack(pady=10)
        
        # Configurar el evento de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Función que se ejecutará al cerrar la aplicación
        self.conn.close()  # Cerrar la conexión a la base de datos
        self.root.destroy()  # Cerrar la aplicación

    def login(self):
        user = self.user_entry.get()
        password = self.password_entry.get()

        if user == "admin" and password == "admin123":
            messagebox.showinfo("Inicio de Sesión",
                                "Inicio de sesión exitoso.")
            self.login_frame.pack_forget()
            self.inventory_frame.pack()
        else:
            messagebox.showerror("Inicio de Sesión",
                                 "Credenciales incorrectas.")

    def logout(self):
        self.inventory_frame.pack_forget()
        self.login_frame.pack()

    def show_inventory_dialog(self):
        # Crear un diálogo para mostrar los resultados en una tabla
        dialog = tk.Toplevel(self.root)
        dialog.title("Mostrar Inventario")

        # Crear Treeview para mostrar la tabla
        tree = ttk.Treeview(dialog)
        tree["columns"] = ("Id", "Nombre", "Tipo", "Cantidad")
        tree.column("#0", anchor=tk.W, width=100)
        tree.column("Id", anchor=tk.W, width=100)
        tree.column("Nombre", anchor=tk.W, width=100)
        tree.column("Tipo", anchor=tk.W, width=100)
        tree.column("Cantidad", anchor=tk.W, width=100)

        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Id", text="Id", anchor=tk.W)
        tree.heading("Nombre", text="Nombre", anchor=tk.W)
        tree.heading("Tipo", text="Tipo", anchor=tk.W)
        tree.heading("Cantidad", text="Cantidad", anchor=tk.W)

        # Obtener datos del inventario
        cursor = self.c.execute(
            "SELECT * FROM productos")
        fila = cursor.fetchone()
        if fila != None:
            print(fila)
        else:
            print("No existe un artículo")
        rows = self.c.fetchall()

        # Insertar datos en el Treeview
        for row in rows:
            tree.insert("", tk.END, values=row)

        tree.pack()

    def loan(self):
        loan_window = tk.Toplevel(self.root)
        loan_window.title("Hacer Préstamo")

        tk.Label(loan_window, text="Cédula:",
                 bg='#add8e6').grid(row=0, column=0)
        tk.Label(loan_window, text="Nombre:",
                 bg='#add8e6').grid(row=1, column=0)
        tk.Label(loan_window, text="Teléfono:",
                 bg='#add8e6').grid(row=2, column=0)
        tk.Label(loan_window, text="Pago:", bg='#add8e6').grid(row=3, column=0)
        tk.Label(loan_window, text="Id_prod:",
                 bg='#add8e6').grid(row=4, column=0)
        tk.Label(loan_window, text="Cantidad:",
                 bg='#add8e6').grid(row=5, column=0)

        cedula_entry = tk.Entry(loan_window)
        nombre_entry = tk.Entry(loan_window)
        telefono_entry = tk.Entry(loan_window)
        pago_entry = tk.Entry(loan_window)
        id_prod_entry = tk.Entry(loan_window)
        cantidad_entry = tk.Entry(loan_window)

        cedula_entry.grid(row=0, column=1)
        nombre_entry.grid(row=1, column=1)
        telefono_entry.grid(row=2, column=1)
        pago_entry.grid(row=3, column=1)
        id_prod_entry.grid(row=4, column=1)
        cantidad_entry.grid(row=5, column=1)

        tk.Button(loan_window, text="Realizar Préstamo", command=lambda: self.make_loan(cedula_entry.get(),
                                                                                        nombre_entry.get(),
                                                                                        telefono_entry.get(),
                                                                                        pago_entry.get(),
                                                                                        id_prod_entry.get(),
                                                                                        cantidad_entry.get()), bg='#87ceeb', height=1).grid(row=6, column=0, columnspan=2)

    def make_loan(self, cedula, nombre, telefono, pago, id_prod, cantidad):
        cursor = self.c.execute(
            "SELECT cantidad FROM productos WHERE id = " + id_prod)
        fila = cursor.fetchone()
        if fila != None:
            print(fila)
            if int(fila[0]) - int(cantidad)  > 0:
                diferencia_cantidad = int(fila[0]) - int(cantidad)
                self.c.execute("INSERT INTO prestamos (cedula, nombre, tel, valor, cantidad) VALUES (?, ?, ?, ?, ?)",
                               (cedula, nombre, telefono, pago, cantidad))
                self.c.execute("UPDATE productos SET cantidad=? WHERE id=?", (diferencia_cantidad, id_prod))
                print("Query prestamo realizada !!")
                # Disminuir cantidad de elementos del inventario
                
                messagebox.showinfo("Préstamo", "Préstamo realizado con éxito.")
            else: 
                print("No cumple cantidad")
                messagebox.showinfo("Préstamo", "La cantidad supera el stock !!!")
        else:
            print("No existe un prestamo")
            messagebox.showinfo("Préstamo", "No existe un prestamo con ese id")
        rows = self.c.fetchall()
        
    

    def update_inventory(self):
        update_window = tk.Toplevel(self.root)
        update_window.title("Actualizar Inventario")

        tk.Label(update_window, text="Nombre:",
                 bg='#add8e6').grid(row=0, column=0)
        tk.Label(update_window, text="Tipo:",
                 bg='#add8e6').grid(row=1, column=0)
        tk.Label(update_window, text="Cantidad:", 
                 bg='#add8e6').grid(row=2, column=0)
        tk.Label(update_window, text="Id_prod:", 
                 bg='#add8e6').grid(row=3, column=0)

        nombre_entry = tk.Entry(update_window)
        tipo_entry = tk.Entry(update_window)
        cantidad_entry = tk.Entry(update_window)
        id_prod_entry = tk.Entry(update_window)

        nombre_entry.grid(row=0, column=1)
        tipo_entry.grid(row=1, column=1)
        cantidad_entry.grid(row=2, column=1)
        id_prod_entry.grid(row=3, column=1)
        

        tk.Button(update_window, text="Actualizar", command=lambda: self.update_product(nombre_entry.get(),
                                                                                        tipo_entry.get(),
                                                                                        cantidad_entry.get(),
                                                                                        id_prod_entry.get()), bg='#87ceeb', height=1).grid(row=6, column=0, columnspan=2)


    def update_product(self, nombre, tipo, cantidad, id_prod):
        # validar el elemento a actualizar 
        datos=nombre,tipo,cantidad
        query1 = "SELECT * FROM productos WHERE id = " + id_prod
        print(query1)
        cursor = self.c.execute(query1)
        print("ID query exec !!!")
        fila = cursor.fetchone()
        if fila != None:
            print(fila)
            self.c.execute("UPDATE productos SET nombre=?, tipo=?, cantidad=?" + "WHERE id =" + id_prod,(datos))
            print("Query prestamo realizada !!")
            messagebox.showinfo("Actualización", "Actualización realizada con éxito.")
        else:
            print("No existe un producto con el id proporcionado")
            messagebox.showinfo("Actualización", "No existe un producto con el id proporcionado")
        rows = self.c.fetchall()
        
        
    def delete_operation(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Eliminar Producto")

        tk.Label(delete_window, text="Id:",
                 bg='#add8e6').grid(row=0, column=0)

        id_entry = tk.Entry(delete_window)

        id_entry.grid(row=0, column=1)

        tk.Button(delete_window, text="Eliminar Producto", command=lambda: self.delete_prod(id_entry.get()), bg='#87ceeb', height=1).grid(row=3, column=0, columnspan=2)
        
        
  
    def delete_prod(self, id_del):
        # Obtener datos de los prestamos
        cursor = self.c.execute("SELECT * FROM productos WHERE id = " + id_del)
        fila = cursor.fetchone()
        if fila != None:
            print(fila)
            query2 = "DELETE FROM productos WHERE id = " + id_del
            self.c.execute(query2)
            print("Query eliminar realizada !!")
            messagebox.showinfo("Eliminar", "Producto eliminado con éxito.")
        else:
            print("No existe un producto con el ID proporcionado")
            messagebox.showinfo("Eliminar", "No existe un producto con el ID proporcionado.")
        rows = self.c.fetchall()
        
    def insert_product(self):
        insert_window = tk.Toplevel(self.root)
        insert_window.title("Insertar producto")

        tk.Label(insert_window, text="Nombre:",
                 bg='#add8e6').grid(row=0, column=0)
        tk.Label(insert_window, text="Tipo:",
                 bg='#add8e6').grid(row=1, column=0)
        tk.Label(insert_window, text="Cantidad:", 
                 bg='#add8e6').grid(row=2, column=0)

        nombre_entry = tk.Entry(insert_window)
        tipo_entry = tk.Entry(insert_window)
        cantidad_entry = tk.Entry(insert_window)

        nombre_entry.grid(row=0, column=1)
        tipo_entry.grid(row=1, column=1)
        cantidad_entry.grid(row=2, column=1)
        

        tk.Button(insert_window, text="Actualizar", command=lambda: self.nuevo_producto(nombre_entry.get(),
                                                                                        tipo_entry.get(),
                                                                                        cantidad_entry.get()), bg='#87ceeb', height=1).grid(row=4, column=0, columnspan=2)
        
    def nuevo_producto(self, nombre, tipo, cantidad):
        self.c.execute(
            "INSERT INTO productos (nombre, tipo, cantidad) VALUES (?, ?, ?)", (nombre, tipo, cantidad))
        print("Producto ingresado con exito !!")
        messagebox.showinfo("Insertar", "Producto insertado con éxito.")
        
        
    def descargar_datos(self):
        # Obtener datos de la tabla prestamos
        self.c.execute("SELECT * FROM prestamos")
        rows = self.c.fetchall()

        # Abrir un archivo para escritura
        with open("datos_prestamos.txt", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter='\t')  # Separador de tabulaciones para un archivo .txt
            # Escribir encabezados
            writer.writerow(["Id_prestamo","Cedula_prestamo", "Nombre_prestamo", "telefono_prestamo", "valor_prestamo", "cantidad_prestamo"])
            # Escribir filas de datos
            writer.writerows(rows)

        messagebox.showinfo("Descarga Completada", "Los datos se han descargado correctamente en datos_prestamos.txt")
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
