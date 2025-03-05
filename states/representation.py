# Contiene todos los menus y funciones del modulo Representacion de datos


from states.base import State

class RepresentacionDatos(State):
    def ejecutar(self):
        try:
            opcion = int(input('¿Qué quieres? Elegir variables categoricas y numéricas(1) o volver(2): '))
        except ValueError:
            print("Entrada inválida. Volviendo al menú principal.")
            from states.main_menu import Main
            self.context.transition_to(Main())
            return
        if opcion == 1:
            self.context.transition_to(IdentificacionVariables())
            return
        else:
            from states.main_menu import Main
            self.context.transition_to(Main())
            return

class IdentificacionVariables(State):
    def ejecutar(self):
        while True:
            try:
                _opcion = int(input('Indica que variables son categoricas(1), eliminar de la lista(2), visualizar(3), o salir(0): '))
            except ValueError:
                print("Entrada inválida.")
                continue

            if _opcion == 0:
                break
            elif _opcion == 1:
                var_cat = input('Escribe el nombre exacto de la columna: ')
                self.context.valores_cat.append(var_cat)
            elif _opcion == 2:
                del_var_cat = input('Escribe el nombre exacto del valor que deseas eliminar: ')
                try:
                    self.context.valores_cat.remove(del_var_cat)
                except ValueError:
                    print("El valor no se encuentra en la lista.")
            elif _opcion == 3:
                print(self.context.valores_cat)
            else:
                print("Opción no reconocida.")
        from states.representation import RepresentacionDatos
        self.context.transition_to(RepresentacionDatos())
        return
