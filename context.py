import pandas as pd
from states.main_menu import Main

class Context:
    def __init__(self):
        # Inicializo listas para almacenar variables categóricas y numéricas
        self.valores_cat = []
        self.valores_num = []
        self.running = True
        self._dataframe = None

        # Carga del archivo CSV hasta que se ingrese uno válido o se decida abortar
        while True:
            n_archivo = input('Introduce el nombre del archivo, "abort" para salir: ')
            if n_archivo.lower() == 'abort':
                print("Cerrando.")
                self.running = False
                return
            try:
                self._dataframe = pd.read_csv(f'.//data/{n_archivo}')
                break
            except FileNotFoundError:
                print('No existe ese archivo')
        
        # Estado inicial: menú principal
        self.transition_to(Main())
        # Ejecuta el bucle principal
        self.run()

    def transition_to(self, state):
        """Cambia el estado actual asignando el nuevo estado.
        No se invoca ejecutar() directamente; la ejecución se centraliza en run()."""
        self._state = state
        self._state.context = self

    def run(self):
        """Bucle principal que sigue ejecutando el estado actual mientras running sea True."""
        while self.running:
            self._state.ejecutar()