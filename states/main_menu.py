#Menu principal desde el que se accede a las demas categorias, ademas contine la salida del programa

from states.base import State
from states.cleaning import LimpiezaDeDatos
from states.representation import RepresentacionDatos

class Salir(State):
    def ejecutar(self):
        print('Saliendo del programa!')
        self.context.running = False

class Main(State):
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
                # Permanecemos en el menú principal tras guardar
            elif tarea == 0:
                self.context.transition_to(Salir())
                return
            else:
                print("Opción no reconocida, intenta de nuevo.")
