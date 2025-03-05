# Contiene todos los menus y funciones del modulo Limpieza de Datos


from states.base import State

class LimpiezaDeDatos(State):
    def ejecutar(self):
        try:
            tarea = int(input('¿Qué deseas hacer? NAs(1) Borrar(2) Duplicados(3) Info(4) TestMostrar(5) Atrás(0): '))
        except ValueError:
            print("Entrada inválida. Volviendo al menú principal.")
            from states.main_menu import Main
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
            from states.main_menu import Main
            self.context.transition_to(Main())
            return
        else:
            print('Opción no reconocida, volviendo a Main menu.')
            from states.main_menu import Main
            self.context.transition_to(Main())
            return

class MissingData(State):
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
        from states.cleaning import LimpiezaDeDatos
        self.context.transition_to(LimpiezaDeDatos())
        return

class Borrar(State):
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
        from states.cleaning import LimpiezaDeDatos
        self.context.transition_to(LimpiezaDeDatos())
        return

class Duplicados(State):
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
        from states.cleaning import LimpiezaDeDatos
        self.context.transition_to(LimpiezaDeDatos())
        return

class Info(State):
    def ejecutar(self):
        print(self.context._dataframe.info())
        from states.cleaning import LimpiezaDeDatos
        self.context.transition_to(LimpiezaDeDatos())
        return

class MostrarDatos(State):
    def ejecutar(self):
        try:
            opcion = int(input('¿Qué deseas hacer? Mostrar 10 primeras filas(1) o una fila en concreto(2): '))
        except ValueError:
            print("Entrada inválida. Volviendo al menú anterior.")
            from states.cleaning import LimpiezaDeDatos
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
        from states.cleaning import LimpiezaDeDatos
        self.context.transition_to(LimpiezaDeDatos())
        return
