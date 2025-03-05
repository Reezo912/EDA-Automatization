import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod  # Se importa ABC y abstractmethod para definir clases abstractas


# TODO Eliminar funcion eliminar filas(No es necesaria) y reemplazar por eliminar duplicados
# TODO Implementar que todas las salidas de menu sean el 0
# TODO Implementar describe en Class Info
# TODO Hacer esta clase accesible en cualquier momento.
# Implementar mas funciones de visualizacion de datos, por ahora en test.
# TODO Separar logica de IU, cambio de estados y carga de archivo


# --------------------------------------------------------------------
# Clase Context
# --------------------------------------------------------------------
# La clase Context gestiona el estado actual del programa, almacena el
# DataFrame cargado y ejecuta un bucle principal que invoca el método
# ejecutar() del estado actual.
class Context:
    
    _state = None         # Estado actual del programa
    _dataframe = None     # DataFrame con los datos cargados

    def __init__(self):
        # Inicializo las listas para almacenar valores categóricos y numéricos
        self.valores_cat = []
        self.valores_num = []
        self.running = True

        # Solicita al usuario el nombre del archivo hasta que se ingrese uno válido
        while True:
            n_archivo = input('Introduce el nombre del archivo, "abort" para salir: ')
            if n_archivo.lower() == 'abort':
                print("Cerrando.")
                self.running = False
                return  # Finaliza la carga del archivo y no se inicia el bucle principal

            try:
                self._dataframe = pd.read_csv(f'.//data/{n_archivo}')
                break
            except FileNotFoundError:
                print('No existe ese archivo')
        
        # Estado inicial: menú principal
        self.transition_to(Main())
        # Inicia el bucle principal de ejecución
        self.run()

    # Método para cambiar el estado actual (sin ejecutar inmediatamente)
    def transition_to(self, state):
        self._state = state
        self._state.context = self

    # Bucle principal: se invoca ejecutar() del estado actual mientras running sea True
    def run(self):
        while self.running:
            self._state.ejecutar()


# --------------------------------------------------------------------
# Clase State: Interfaz abstracta para los diferentes estados
# --------------------------------------------------------------------
class State(ABC):
    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def ejecutar(self) -> None:
        pass


# --------------------------------------------------------------------
# Estados del programa
# --------------------------------------------------------------------
class Salir(State):
    def ejecutar(self):
        print('Saliendo del programa!')
        self.context.running = False
        return


class Main(State):  # Menú inicial y principal
    def ejecutar(self):
        while True:
            try:
                tarea = int(input('¿Qué deseas hacer? Limpieza(1) Representacion(2) Guardar(3) Salir(0): '))
            except ValueError:
                print("Entrada inválida. Por favor, ingresa un número.")
                continue

            if tarea == 1:
                self.context.transition_to(LimpiezaDeDatos())
                return
            elif tarea == 2:
                self.context.transition_to(RepresentacionDatos())
                return
            elif tarea == 3:
                nombre_archivo = input('¿Cómo deseas llamar a tu archivo? ')
                self.context._dataframe.to_csv(f'.//data/{nombre_archivo}.csv')
                print("Archivo guardado.")
                # Se permanece en el menú principal tras guardar
            elif tarea == 0:
                self.context.transition_to(Salir())
                return
            else:
                print("Opción no reconocida, intenta de nuevo.")


class LimpiezaDeDatos(State):  # Menú de limpieza y manipulación de datos
    def ejecutar(self) -> None:
        try:
            tarea = int(input('¿Qué deseas hacer? NAs(1) Borrar(2) Duplicados(3) Info(4) TestMostrar(5) Atrás(0): '))
        except ValueError:
            print("Entrada inválida. Volviendo al menú principal.")
            self.context.transition_to(Main())
            return

        if tarea == 1:
            self.context.transition_to(MissingData())
            return
        elif tarea == 2:
            self.context.transition_to(Borrar())
            return
        elif tarea == 3:
            self.context.transition_to(Duplicados())
            return
        elif tarea == 4:
            self.context.transition_to(Info())
            return
        elif tarea == 5:
            self.context.transition_to(MostrarDatos())
            return
        elif tarea == 0:
            self.context.transition_to(Main())
            return
        else:
            print('No existe esa función o input inválido, volviendo a Main menu.')
            self.context.transition_to(Main())
            return


class MissingData(State):  # Menú para comprobar NAs y valores nulos
    def ejecutar(self):
        print(self.context._dataframe.head(10))
        while True:
            try:
                miss_option = int(input('¿Qué deseas hacer? Comprobar NAs en todo el DF(1), en una columna(2) o volver(3): '))
            except ValueError:
                print("Entrada inválida.")
                continue

            if miss_option == 1:
                print(f'Hay {self.context._dataframe.isna().sum()} valores NA en el DataFrame')
            elif miss_option == 2:
                miss_input = input('Escribe el nombre de la columna que deseas comprobar NAs, escribe "atras" para volver: ').strip()
                if miss_input.lower() == 'atras':
                    break
                elif miss_input not in self.context._dataframe.columns:
                    print(f"La columna '{miss_input}' no existe. Las columnas disponibles son: {list(self.context._dataframe.columns)}")
                else:
                    print(f'Hay {self.context._dataframe[miss_input].isna().sum()} NAs en la columna {miss_input}')
            elif miss_option == 3:
                break
            else:
                print("Opción no reconocida.")
        self.context.transition_to(LimpiezaDeDatos())
        return


class Borrar(State):  # Menú para borrar filas o columnas
    def ejecutar(self):
        print(self.context._dataframe.head(10))
        while True:
            try:
                del_options = int(input('¿Deseas borrar una fila(1) o borrar una columna(2)? O volver atrás (3): '))
            except ValueError:
                print("Entrada inválida.")
                continue

            if del_options == 1:
                user_input = input('Escribe el índice de la fila que deseas borrar, escribe "atras" para volver: ')
                if user_input.lower() == 'atras':
                    break
                else:
                    try:
                        del_fila = int(user_input)
                        if del_fila not in self.context._dataframe.index:
                            print(f"La fila con índice '{del_fila}' no existe. Dimensiones del DataFrame: {self.context._dataframe.shape}")
                        else:
                            self.context._dataframe.drop(del_fila, axis=0, inplace=True)
                            print('Índices actuales:', self.context._dataframe.index)
                    except ValueError:
                        print("Entrada inválida. Ingresa un número o 'atras'.")
            elif del_options == 2:
                del_col = input('¿Qué columna deseas borrar, escribe "atras" para volver: ').strip()
                if del_col.lower() == 'atras':
                    break
                elif del_col not in self.context._dataframe.columns:
                    print(f"La columna '{del_col}' no existe. Las columnas disponibles son: {list(self.context._dataframe.columns)}")
                else:
                    self.context._dataframe.drop(del_col, axis=1, inplace=True)
                    print("Columnas actuales:", self.context._dataframe.columns)
            elif del_options == 3:
                break
            else:
                print("Opción no reconocida.")
        self.context.transition_to(LimpiezaDeDatos())
        return


class Duplicados(State):  # Menú para revisar duplicados
    def ejecutar(self):
        print(self.context._dataframe.head(10))
        while True:
            try:
                dup_option = int(input('¿Qué deseas hacer? Comprobar duplicados en todo el DF(1), en una columna(2) o volver(3): '))
            except ValueError:
                print("Entrada inválida.")
                continue

            if dup_option == 1:
                print(f'Hay {self.context._dataframe.duplicated().sum()} filas duplicadas en el DataFrame')
            elif dup_option == 2:
                dup_input = input('¿Qué columna deseas comprobar duplicados, escribe "atras" para volver: ')
                if dup_input.lower() == 'atras':
                    break
                elif dup_input not in self.context._dataframe.columns:
                    print(f"La columna '{dup_input}' no existe. Las columnas disponibles son: {list(self.context._dataframe.columns)}")
                else:
                    duplicate_count = self.context._dataframe[dup_input].duplicated().sum()
                    print(f'Hay {duplicate_count} valores duplicados en la columna {dup_input}')
            elif dup_option == 3:
                break
            else:
                print("Opción no reconocida.")
        self.context.transition_to(LimpiezaDeDatos())
        return


class Info(State):  # Menú para mostrar la información del DataFrame
    def ejecutar(self):
        print(self.context._dataframe.info())
        self.context.transition_to(LimpiezaDeDatos())
        return


class MostrarDatos(State):  # Menú para mostrar datos
    def ejecutar(self) -> None:
        try:
            opcion = int(input('¿Qué deseas hacer? Mostrar 10 primeras filas(1) o una fila en concreto(2): '))
        except ValueError:
            print("Entrada inválida. Volviendo al menú anterior.")
            self.context.transition_to(LimpiezaDeDatos())
            return

        if opcion == 1:
            print(self.context._dataframe.head(10))
        elif opcion == 2:
            try:
                fila_i = int(input('Escribe el índice de la fila que quieres comprobar: '))
                print(self.context._dataframe.iloc[fila_i])
            except Exception as e:
                print("Error:", e)
        else:
            print('Esa opción no existe, volviendo al menú anterior.')
        self.context.transition_to(LimpiezaDeDatos())
        return


class RepresentacionDatos(State):  # Menú para representación de datos
    def ejecutar(self) -> None:
        try:
            opcion = int(input('¿Qué quieres? Elegir variables categoricas y numericas(1) o volver(2): '))
        except ValueError:
            print("Entrada inválida. Volviendo al menú principal.")
            self.context.transition_to(Main())
            return
        if opcion == 1:
            self.context.transition_to(IdentificacionVariables())
            return
        else:
            self.context.transition_to(Main())
            return


class IdentificacionVariables(State):  # Menú para identificar variables categóricas
    def ejecutar(self) -> None:
        while True:
            try:
                _opcion = int(input('Indica que variables son categoricas(1), eliminar de la lista(2), visualizar(3), o salir(0): '))
            except ValueError:
                print("Entrada inválida.")
                continue

            if _opcion == 0:  # Salir del menú
                break
            elif _opcion == 1:  # Añadir valores a la lista
                var_cat = input('Escribe el nombre exacto de la columna: ')
                self.context.valores_cat.append(var_cat)
            elif _opcion == 2:  # Eliminar un valor de la lista
                del_var_cat = input('Escribe el nombre exacto del valor que deseas eliminar: ')
                try:
                    self.context.valores_cat.remove(del_var_cat)
                except ValueError:
                    print("El valor no se encuentra en la lista.")
            elif _opcion == 3:  # Mostrar la lista
                print(self.context.valores_cat)
            else:
                print("Opción no reconocida.")
        self.context.transition_to(RepresentacionDatos())
        return


# --------------------------------------------------------------------
# Ejecución del programa
# --------------------------------------------------------------------
if __name__ == "__main__":
    context = Context()