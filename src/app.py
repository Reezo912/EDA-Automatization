import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod  # Se importa ABC y abstractmethod para definir clases abstractas
import sys


# TODO Refactorizar codigo, try/catch dentro de context y division en scripts
# TODO Eliminar funcion eliminar filas(No es necesaria) y reemplazar por eliminar duplicados
# TODO Implementar que todas las salidas de menu sean el 0
# TODO Implementar describe en Class Info
# TODO Hacer esta clase accesible en cualquier momento.
# Implementar mas funciones de visualizacion de datos, por ahora en test.
# TODO Separar logica de IU, cambio de estados y carga de archivo

# --------------------------------------------------------------------
# Clase Context
# --------------------------------------------------------------------
# La clase Context es la encargada de gestionar el estado actual del programa y
# de almacenar los datos (DataFrame) cargados desde un archivo CSV. Además, 
# se encarga de cambiar el estado (transición) según las acciones del usuario.

class Context:

    _state = None         # Atributo que guarda el estado actual del programa
    _dataframe = None     # Atributo que contiene el DataFrame con los datos cargados

    def __init__(self):
        # Incio las listas que mas tarde utilizare para almacenar los valores numericos y categoricos
        self.valores_cat = []
        self.valores_num = []
               
        while True:             # Se utiliza un bucle para asegurarse de que el usuario ingrese un archivo válido.
            # Se solicita el nombre del archivo al usuario.
            n_archivo = input('Introduce el nombre del archivo, "abort" para salir: ')
            # Funcion de salida
            if n_archivo.lower() == 'abort':
                print("Cerrando.")
                return

            try:
                # Se intenta cargar el archivo CSV en un DataFrame.
                self._dataframe = pd.read_csv(f'.//data/{n_archivo}')
                                                                                    #df = pd.read_csv('.//data/Data.csv') -- Activar para acceso rapido
                # Si se carga el archivo correctamente, salimos del bucle.
                break
            except FileNotFoundError:
                # Si el archivo no existe, se notifica al usuario y se repite el proceso.
                print('No existe ese archivo')
                

        # Una vez cargado el archivo correctamente, se inicia la transición al estado principal.
        self.transition_to(Main())

    # Método para cambiar (transicionar) el estado actual del programa.
    def transition_to(self, state):

        self._state = state              # Se asigna el nuevo estado
        self._state.context = self       # Se pasa la referencia del Context al nuevo estado
        self._state.ejecutar()           # Se ejecuta la acción definida en el nuevo estado



# --------------------------------------------------------------------
# Clase State y uso de la librería abc
# --------------------------------------------------------------------
# La clase State es una clase abstracta (no se puede instanciar directamente) que 
# define la interfaz para los distintos estados del programa. Utilizamos la librería 
# abc para forzar que todas las subclases implementen el método abstracto 'ejecutar'.

class State(ABC):
    
    # Propiedad que almacena el contexto (la instancia de Context) asociada a este estado.
    @property
    def context(self) -> Context:
        return self._context

    # Setter para asignar el contexto al estado.
    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    # Método abstracto que obliga a todas las subclases a definir su propia implementación.
    @abstractmethod
    def ejecutar(self) -> None:
        # Este método se usará para definir las acciones que realiza cada estado.
        pass


class Salir(State):
    def ejecutar(self):
        print('Saliendo del programa!')
        #sys.exit()
        return


class Main(State):  # Menu incial y principal
    def ejecutar(self):
        # Solicita input para cambio de menu.
        while True:
            tarea: int = int(input('¿Que deseas hacer? Limpieza(1) Representacion(2) Guardar(3) salir(0))'))

            try:
                if tarea == 1:              # Entra dentro del menu Limpieza de Datos
                    self.context.transition_to(LimpiezaDeDatos())

                elif tarea == 2:            # Entra dentro del menu Representacion de Datos
                    self.context.transition_to(RepresentacionDatos())

                elif tarea == 3:            # Guardar archivo
                    nombre_archivo = input('¿Como deseas llamar a tu archivo?')
                    self.context._dataframe.to_csv(f'.//data/{nombre_archivo}.csv')

                elif tarea == 0:            # Salir y cerrar programa
                    self.context.transition_to(Salir())
                    break
                # Devuelve un error si no exite el input
                else:
                    print("Opción no reconocida, intenta de nuevo.")

            except:
                print(f'Error: No existe esa función, volviendo a Main menu.')


class LimpiezaDeDatos(State):           # Menu limpieza de datos y manipulacion del dataFrame
    def ejecutar(self) -> None:
        #Solicita input al usuario para entrar en siguiente menu
        tarea = int(input('¿Que deseas hacer? NAs(1) Borrar(2) Duplicados(3) Info(4) TestMostrar(5) Atras(0)'))   
        
        if tarea == 1:              #Menu limpiar NAs
            self.context.transition_to(MissingData())

        elif tarea == 2:            # Menu Borrar datos
            self.context.transition_to(Borrar())

        elif tarea == 3:            # Menu duplicados
            self.context.transition_to(Duplicados())

        elif tarea == 4:            # Menu Info
            self.context.transition_to(Info())

        elif tarea == 5:            # Mostrar datos
            self.context.transition_to(MostrarDatos())

        elif tarea == 0:            # Vuelve al estado anterior
            self.context.transition_to(Main())

        else:
            print('No existe esa funcion o input invalido, volviendo a Main_menu.')



class MissingData(State):               # Menu de comprobacion de NAs y Nulls
    def ejecutar(self):

        running = True
        print(self.context._dataframe.head(10))         # Se imprimen las 10 primeras filas para dar contexto de los datos
        
        while running:
            miss_option: int = int(input('Que deseas hacer? Comprobar NAs en todo el DF(1), en una columna(2) o volver(3): '))
            
            if miss_option == 1:                # Comprobar NAs en todo el DataFrame
                print(f'Hay {self.context._dataframe.isna().sum()} valores NA en el Dataframe')
            
            elif miss_option == 2:                # Funcion comprobar NAs en columnas
                miss_input: str = input(f'Escribe el nombre de la columna que deseas comprobar NAs, escribe "atras" para volver: ').strip()
            
                if miss_input.lower() == 'atras':
                    running = False
                
                elif miss_input not in self.context._dataframe.columns:
                    print(f"La columna '{miss_input}' no existe. Las columnas disponibles son: {list(self.context._dataframe.columns)}")

                else:
                    try:
                        print(f'Hay {self.context._dataframe[miss_input].isna().sum()} NAs en la columna {miss_input}')

                    except:
                        print('Esa columna no existe.')

            else:
                running = False

        self.context.transition_to(LimpiezaDeDatos())



class Borrar(State):         # Menu borrado de elementos
    def ejecutar(self):
    
        print(self.context._dataframe.head(10))
        keep_deleting = True

        while keep_deleting:            # Bucle para mantenerse dentro del menu
            del_options: int = int(input('¿Deseas borrar una fila(1) o borrar una columna(2)? O volver atras (3): '))
            
            if del_options == 1:                # Seleccionar fila para borrar
                del_fila: int = int(input('Escribe el indice de la fila deseas borrar, escribe "atras" para volver: '))
                
                if del_fila == 'atras':
                    keep_deleting = False

                elif del_fila not in self.context._dataframe.index:
                    print(f"La fila con indice '{del_fila}' no existe. Las medidas del dataframe son: {self.context._dataframe.shape}")

                else:
                    try:
                        self.context._dataframe.drop(del_fila, axis=0, inplace=True)
                        print('Indices actuales:', self.context._dataframe.index)
                    except:
                        print('Esa fila no existe.')

            elif del_options == 2:              # Seleccionar columna para borrar
                del_col: str = input('Que columna deseas borrar, escribe "atras" para volver: ').strip()
            
                if del_col.lower() == 'atras': # Salir del menu y volver al anterior
                    keep_deleting = False

                elif del_col not in self.context._dataframe.columns:
                    print(f"La columna '{del_col}' no existe. Las columnas disponibles son: {list(self.context._dataframe.columns)}")

                else:
                    try:
                        self.context._dataframe.drop(del_col, axis=1, inplace=True)
                        print(self.context._dataframe.columns)
                    except:
                        print('Esa columna no existe.')
            else:
                keep_deleting = False
        
        self.context.transition_to(LimpiezaDeDatos())


class Duplicados(State):
    def ejecutar(self):
    
        print(self.context._dataframe.head(10))

        keep_looking = True

        while keep_looking:
            dup_option: int = int(input('Que deseas hacer? Comprobar si hay filas duplicadas(1), o duplicados en una columna(2) o volver(3): '))
            
            if dup_option == 1:
                print(f'Hay {self.context._dataframe.duplicated().sum()} columnas duplicadas en el Dataframe')
                      
            elif dup_option == 2:
                dup_input: str = input('Que columna deseas comprobar duplicados, escribe "atras" para volver: ')
                
                if dup_input.lower() == 'atras':
                    keep_looking = False
                 
                elif dup_input not in self.context._dataframe.columns:
                    print(f"La columna '{dup_input}' no existe. Las columnas disponibles son: {list(self.context._dataframe.columns)}")

                else:
                    duplicate_count = self.context._dataframe[dup_input].duplicated().sum()
                    print(f'Hay {duplicate_count} valores duplicados en la columna {dup_input}')
            else:
                keep_looking = False

        
        
        self.context.transition_to(LimpiezaDeDatos())


class Info(State):
    def ejecutar(self):
        
        print(self.context._dataframe.info())
        
        self.context.transition_to(LimpiezaDeDatos())


class MostrarDatos(State):
    def ejecutar(self) -> None:
        opcion:int = int(input('Que deseas hacer? Mostrar 10 primeras filas(1) o una fila en concreto(2): '))
        
        if opcion == 1:
            print(self.context._dataframe.head(10))
        
        elif opcion == 2:
            fila_i: int = int(input('Escribe el indice de la fila que quieres comprobar: '))
            print(self.context._dataframe.iloc[fila_i])
        
        else:
            print('Esa opcion no existe, volviendo a menu anterior.')

        self.context.transition_to(LimpiezaDeDatos())






#TODO Añadir representacion de datos

class RepresentacionDatos(State):
    def ejecutar(self) -> None:
        opcion = int(input('Que quieres? Elegir variables categoricas y numericas(1) o volver(2): '))
        if opcion == 1:             # Clasificar valores numericos y categoricos
            self.context.transition_to(IdentificacionVariables())
        else:
            self.context.transition_to(Main())

class IdentificacionVariables(State):
    def ejecutar(self) -> None:
        while True:
            
            _opcion = int(input('Indica que variables son categoricas(1), eliminar de la lista(2) visualizar(3), o salir(0)'))
            

            if _opcion == 0:                        # Salir del menu
                break

            elif _opcion == 1:                      # Añadir valores a la lista
                var_cat = input('Escribe el nombre exacto de la columna: ')
                self.context.valores_cat.append(var_cat)

            elif _opcion == 2:                      # Borrar indice lista
                del_var_cat = input('Escribe el nombre exacto del valor que deseas eliminar: ')
                self.context.valores_cat.remove(del_var_cat)

            elif _opcion == 3:                      # Mostrar lista
                print(self.context.valores_cat)
        
        self.context.transition_to(RepresentacionDatos())






if __name__ == "__main__":
    # The client code.

    context = Context()