import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt





'''n_archivo = input('Introduce el nombre del archivo: ')

df = pd.read_csv(f'.//data/{n_archivo}')'''


df = pd.read_csv('.//data/Data.csv')


def comprobar_duplicados(dataframe):

    print(dataframe.head(10))

    keep_looking = True

    while keep_looking:
        
        user_input: str = input('Que columna deseas comprobar duplicados, escribe "no" si quieres salir: ')
        
        if user_input.lower() == 'no':
            keep_looking = False
          
        if user_input not in dataframe.columns:
            print(f"La columna '{user_input}' no existe. Las columnas disponibles son: {list(dataframe.columns)}")

        else:
            duplicate_count = dataframe[user_input].duplicated().sum()
            print(f'Hay {duplicate_count} duplicados en la columna {user_input}')
            
        print(dataframe.columns)




def borrar_columnas(dataframe):
    
    print(dataframe.head(10))
    keep_deleting = True

    while keep_deleting:
        
        user_input = input('Que columna deseas borrar, escribe no si quieres salir: ')
        
        if user_input.lower() == 'no':
            keep_deleting = False
          
        else:
            dataframe.drop(user_input, axis=1, inplace=True)
        print(dataframe.columns)

#comprobar_duplicados(df)
#borrar_columnas(df)

def main(dataframe):

    active = True

    while active:

        tarea = input('Que quieres? (info/borrar/duplicados/salir)').lower()
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

main(df)