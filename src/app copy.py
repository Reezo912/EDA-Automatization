import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
from io import StringIO

class DataManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Manager GUI")
        self.dataframe = None

        # Botón para cargar un archivo CSV
        self.btn_load = tk.Button(master, text="Cargar Archivo", command=self.load_file)
        self.btn_load.pack(pady=10)
        
        # Botón para mostrar información del DataFrame
        self.btn_info = tk.Button(master, text="Mostrar Info", command=self.show_info, state="disabled")
        self.btn_info.pack(pady=10)
        
        # Botón para mostrar las primeras 10 filas del DataFrame
        self.btn_head = tk.Button(master, text="Mostrar Head", command=self.show_head, state="disabled")
        self.btn_head.pack(pady=10)
        
        # Botón para borrar una columna
        self.btn_delete = tk.Button(master, text="Borrar Columna", command=self.delete_column, state="disabled")
        self.btn_delete.pack(pady=10)
        
        # Botón para guardar el DataFrame en un archivo CSV
        self.btn_save = tk.Button(master, text="Guardar Archivo", command=self.save_file, state="disabled")
        self.btn_save.pack(pady=10)
    
    def load_file(self):
        # Se abre un cuadro de diálogo para seleccionar el archivo CSV
        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo CSV", 
            filetypes=[("CSV Files", "*.csv")]
        )
        if file_path:
            try:
                self.dataframe = pd.read_csv(file_path)
                messagebox.showinfo("Éxito", "Archivo cargado correctamente!")
                # Habilitar botones una vez que se carga el archivo
                self.btn_info.config(state="normal")
                self.btn_head.config(state="normal")
                self.btn_delete.config(state="normal")
                self.btn_save.config(state="normal")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {e}")
    
    def show_info(self):
        if self.dataframe is not None:
            # Redirige la salida de info() a un StringIO para capturar la información
            buffer = StringIO()
            self.dataframe.info(buf=buffer)
            info_str = buffer.getvalue()
            messagebox.showinfo("Info del DataFrame", info_str)
    
    def show_head(self):
        if self.dataframe is not None:
            head_str = str(self.dataframe.head(10))
            messagebox.showinfo("Primeras 10 filas", head_str)
    
    def delete_column(self):
        if self.dataframe is not None:
            # Se solicita al usuario el nombre de la columna a borrar
            col = simpledialog.askstring("Borrar Columna", "Introduce el nombre de la columna a borrar:")
            if col:
                if col not in self.dataframe.columns:
                    messagebox.showerror("Error", f"La columna '{col}' no existe.\nColumnas disponibles: {list(self.dataframe.columns)}")
                else:
                    self.dataframe.drop(col, axis=1, inplace=True)
                    messagebox.showinfo("Éxito", f"Columna '{col}' borrada.\nColumnas restantes: {list(self.dataframe.columns)}")
    
    def save_file(self):
        if self.dataframe is not None:
            # Se abre un cuadro de diálogo para seleccionar dónde guardar el archivo CSV
            file_path = filedialog.asksaveasfilename(
                title="Guardar archivo CSV",
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv")]
            )
            if file_path:
                try:
                    self.dataframe.to_csv(file_path, index=False)
                    messagebox.showinfo("Éxito", "Archivo guardado correctamente!")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al guardar el archivo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataManagerGUI(root)
    root.mainloop()