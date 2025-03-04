import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod  # Se importa ABC y abstractmethod para definir clases abstractas

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
        archivo_no_existe = True
        
        # Se utiliza un bucle para asegurarse de que el usuario ingrese un archivo válido.
        while archivo_no_existe:
            archivo_no_existe = False

            try:
                # Se solicita el nombre del archivo al usuario.
                n_archivo = input('Introduce el nombre del archivo: ')
                # Se intenta cargar el archivo CSV en un DataFrame.
                self._dataframe = pd.read_csv(f'.//data/{n_archivo}')
                #df = pd.read_csv('.//data/Data.csv')

            except FileNotFoundError:
                # Si el archivo no existe, se notifica al usuario y se repite el proceso.
                print('No existe ese archivo')
                archivo_no_existe = True

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
        return


class Main(State):
    def ejecutar(self):
        
        tarea = input('Que quieres? (Limpieza/Representacion/Guardar/Stop)').lower()

        if tarea == 'limpieza':
            self.context.transition_to(LimpiezaDeDatos())

        elif tarea == 'representacion':
            self.context.transition_to(RepresentacionDatos())

        elif tarea == 'guardar':
            nombre_archivo = input('¿Como deseas llamar a tu archivo?')
            self.context._dataframe.to_csv(f'.//data/{nombre_archivo}.csv')

        elif tarea == 'salir':
            self.context.transition_to(Salir())


class LimpiezaDeDatos(State):
    def ejecutar(self) -> None:
        tarea = input('¿Que quieres? (NAs/Borrar/Duplicados/Info/Atras)').lower()   

        if tarea == 'borrar':
            self.context.transition_to(BorrarCol())

        elif tarea == 'duplicados':
            self.context.transition_to(DuplicadosCol())

        elif tarea == 'info':
            self.context.transition_to(Info())

        elif tarea == 'nas':
            self.context.transition_to(missing_data())

        elif tarea == 'atras':
            self.context.transition_to(Main())



class RepresentacionDatos(State):
    def ejecutar(self) -> None:
        tarea = input('Que quieres? (volver)').lower()
        self.context.transition_to(Main())

        
class BorrarCol(State):
    def ejecutar(self):
    
        print(self.context._dataframe.head(10))
        keep_deleting = True

        while keep_deleting:
        
            del_input = input('Que columna deseas borrar, escribe "salir" si quieres salir: ')
        
            if del_input.lower() == 'salir':
                keep_deleting = False

            elif del_input not in self.context._dataframe.columns:
                print(f"La columna '{del_input}' no existe. Las columnas disponibles son: {list(self.context._dataframe.columns)}")

            else:
                try:
                    self.context._dataframe.drop(del_input, axis=1, inplace=True)
                    print(self.context._dataframe.columns)
                except:
                    print('Esa columna no exite.')
        
        self.context.transition_to(LimpiezaDeDatos())
        
class missing_data(State):
    def ejecutar(self):

        running = True
        print(self.context._dataframe.head(10))
        while running:
            
            miss_input: str = input(f'Escribe el nombre de la columna que deseas comprobar NAs, escribe "salir" si quieres salir: ')
            
            if miss_input.lower() == 'salir':
                running = False
            
            elif miss_input not in self.context._dataframe.columns:
                print(f"La columna '{miss_input}' no existe. Las columnas disponibles son: {list(self.context._dataframe.columns)}")

            else:
                duplicate_count = self.context._dataframe[miss_input].duplicated().sum()
                print(f'Hay {duplicate_count} NAs en la columna {miss_input}')

        self.context.transition_to(LimpiezaDeDatos())


class DuplicadosCol(State):
    def ejecutar(self):
    
        print(self.context._dataframe.head(10))

        keep_looking = True

        while keep_looking:
            
            dup_input: str = input('Que columna deseas comprobar duplicados, escribe "salir" si quieres salir: ')
            
            if dup_input.lower() == 'salir':
                keep_looking = False
            
            elif dup_input not in self.context._dataframe.columns:
                print(f"La columna '{dup_input}' no existe. Las columnas disponibles son: {list(self.context._dataframe.columns)}")

            else:
                duplicate_count = self.context._dataframe[dup_input].duplicated().sum()
                print(f'Hay {duplicate_count} duplicados en la columna {dup_input}')
        
        
        self.context.transition_to(LimpiezaDeDatos())


class Info(State):
    def ejecutar(self):
        
        print(self.context._dataframe.info())
        
        self.context.transition_to(LimpiezaDeDatos())


#TODO Comprobar missing data en limpieza de datos
#     Añadir representacion de datos



if __name__ == "__main__":
    # The client code.

    context = Context()













'''

# Funcion principal con opciones posibles
def main(dataframe):

    active = True

    while active:

        tarea = input('Que quieres? (info/borrar/duplicados/salir/guardar)').lower()
        
        if tarea == 'salir':
            break
        
        elif tarea == 'borrar':
            borrar_columnas(dataframe)

        elif tarea == 'info':
            print(df.info())

        elif tarea == 'duplicados':
            comprobar_duplicados(dataframe)
        
        elif tarea == 'guardar':
            nombre_archivo = input('¿Como deseas llamar a tu archivo?')
            df.to_csv(f'.//data/{nombre_archivo}.csv')
        

categoricas = []

numericas = []



def comprobar_duplicados(dataframe):

    print(dataframe.head(10))

    keep_looking = True

    while keep_looking:
        
        dup_input: str = input('Que columna deseas comprobar duplicados, escribe "no" si quieres salir: ')
        
        if dup_input.lower() == 'no':
            keep_looking = False
          
        if dup_input not in dataframe.columns:
            print(f"La columna '{dup_input}' no existe. Las columnas disponibles son: {list(dataframe.columns)}")

        else:
            duplicate_count = dataframe[dup_input].duplicated().sum()
            print(f'Hay {duplicate_count} duplicados en la columna {dup_input}')
            
        print(dataframe.columns)




def borrar_columnas(dataframe):
    
    print(dataframe.head(10))
    keep_deleting = True

    while keep_deleting:
        
        del_input = input('Que columna deseas borrar, escribe no si quieres salir: ')
        
        if del_input.lower() == 'no':
            keep_deleting = False
          
        else:
            dataframe.drop(del_input, axis=1, inplace=True)
        print(dataframe.columns)



main(df)'''