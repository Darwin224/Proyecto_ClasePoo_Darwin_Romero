#
#@autor: diromero@unah.hn
#Clase login, en ella esta la implementacion de las clases y hace funcionar el inicio de sesion
#
#

import clasesImportantes as cli
import sqlite3
####################################################################CLASE LOGIN#######################################################################################
class LoginSystem:

    ##########################################################
    # Crea las tablas e implementa la base de datos en sqlite3#
    #si estas no existen las crea: Tabla que maneja los trabajadores#  
    def __init__(self):
        self.conn = sqlite3.connect('trabajadores.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS trabajadores (
                id TEXT PRIMARY KEY,
                nombre TEXT,
                apellido TEXT,
                cargo TEXT,
                contraseña TEXT,  -- Agregar la columna de contraseña
                Salario REAL,
                registrado_por TEXT
            )
        ''')
        self.conn.commit()
     ##########################################################
    # Crea las tablas e implementa la base de datos en sqlite3#
    #si estas no existen las crea: Tabla que maneja las horas #
    #trabajadas y el costo de las mismas de los trabajadores por hora#
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS horas_trabajadas (
                id INTEGER PRIMARY KEY,
                trabajador_id TEXT,
                horas REAL,
                costo_por_hora REAL,
                FOREIGN KEY(trabajador_id) REFERENCES trabajadores(id)
            )
        ''')
        self.conn.commit()
    ##########################################################
    # Crea las tablas e implementa la base de datos en sqlite3#
    #si estas no existen las crea: Tabla que maneja las actividades #
    #y el costo de las mismas de los trabajadores por obra#
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS actividades (
                id_Actividad INTEGER PRIMARY KEY,
                trabajador_id TEXT,
                descripcion TEXT,
                costo REAL,
                fecha_inicio TEXT,
                fecha_finalizacion TEXT,
                FOREIGN KEY(trabajador_id) REFERENCES trabajadores(id)
            )
        ''')
        
        self.conn.commit()

     #obtiene los trabajadores por id
    def obtener_trabajador_por_id(self, trabajador_id):
        trabajador = self.cursor.execute('''
            SELECT * FROM trabajadores WHERE id = ?
        ''', (trabajador_id,)).fetchone()

        if trabajador:
            if trabajador[3] == "Trabajador por hora":
                return cli.TrabajadorPorHora(trabajador[0], trabajador[1], trabajador[2], trabajador[5], trabajador[3], trabajador[6], trabajador[4])
            else:
                 return None  # No es un trabajador por hora
        else:
            return None  # No se encontró un trabajador con ese ID

    #obtiene los trabajadores por obra por id
    def obtener_trabajadores_por_obra(self, user_id):
        trabajadores_por_obra = []
        tb = "Trabajador por obra"
        trabajadores = self.cursor.execute('''
            SELECT * FROM trabajadores WHERE registrado_por = ? AND cargo = ?
        ''', (user_id, tb)).fetchall()

        for trabajador in trabajadores:
            trabajador_por_obra = cli.TrabajadorPorObra(
                trabajador[0], trabajador[1], trabajador[2], trabajador[5], trabajador[3], trabajador[6])
            actividades = self.cursor.execute('''
                SELECT * FROM actividades WHERE trabajador_id = ?
            ''', (trabajador[0],)).fetchall()

            for actividad in actividades:
                descripcion = actividad[2]
                costo = actividad[3]
                fecha_inicio = actividad[4]
                fecha_finalizacion = actividad[5]
                actividad_obj = cli.Actividad(descripcion=descripcion, costo= costo,fecha_inicio= fecha_inicio, fecha_finalizacion=fecha_finalizacion)
                trabajador_por_obra.agregar_actividad(actividad_obj)

            trabajadores_por_obra.append(trabajador_por_obra)

        return trabajadores_por_obra
     #obtiene los trabajadores por hora por id
    def obtener_trabajadores_por_hora(self, user_id):
        trabajadores_por_hora = []

        tb = "Trabajador por hora"
        trabajadores = self.cursor.execute('''
            SELECT * FROM trabajadores WHERE registrado_por = ? AND cargo = ?
        ''', (user_id, tb)).fetchall()

        for trabajador in trabajadores:
            costo_por_hora = trabajador[5]
            trabajador_por_hora = cli.TrabajadorPorHora(
                trabajador[0], trabajador[1], trabajador[2], trabajador[5], trabajador[3], trabajador[6], costo_por_hora)
            trabajadores_por_hora.append(trabajador_por_hora)

        return trabajadores_por_hora


    def imprimir_lista_trabajadores_por_hora(self, user_id):
        tb = "Trabajador por hora"

        trabajadores_por_hora = self.cursor.execute('''
            SELECT * FROM trabajadores WHERE registrado_por = ? AND cargo = ?
        ''', (user_id, tb)).fetchall()

        if trabajadores_por_hora:
            print("\nMis trabajadores por hora:")
            for trabajador in trabajadores_por_hora:
                print("ID:", trabajador[0])
                print("Nombre:", trabajador[1])
                print("------------------------")
        else:
            print("No hay trabajadores por hora registrados por ti.")


    def imprimir_lista_trabajadores_por_obra(self, user_id):
        tb = "Trabajador por obra"

        trabajadores_por_obra = self.cursor.execute('''
            SELECT * FROM trabajadores WHERE registrado_por = ? AND cargo = ?
        ''', (user_id, tb)).fetchall()

        if trabajadores_por_obra:
            print("\nMis trabajadores por obra:")
            for trabajador in trabajadores_por_obra:
                print("ID:", trabajador[0])
                print("Nombre:", trabajador[1])

                # Obtener las actividades del trabajador
                actividades = self.obtener_actividades(trabajador[0])
                if actividades:
                    print("Actividades:")
                    for actividad in actividades:
                        print("Id Actividad",actividad.id)
                        print("  Descripción:", actividad.descripcion)
                        print("  Estado:", actividad.estado)
                        print("  Costo:", actividad.costo)
                        print("  Fecha de inicio:", actividad.fecha_inicio)
                        print("  Fecha de finalización:", actividad.fecha_finalizacion)
                        print("------------------------")
                else:
                    print("No hay actividades asociadas a este trabajador por obra.")
                    print("------------------------")
        else:
            print("No hay trabajadores por obra registrados por ti.")


    def obtener_actividades(self, trabajador_id):
        actividades = self.cursor.execute('''
            SELECT * FROM actividades WHERE trabajador_id = ?
        ''', (trabajador_id,)).fetchall()

        lista_actividades = []
        for actividad in actividades:
            actividad_id = actividad[0]
            descripcion = actividad[2]
            costo = actividad[3]
            fecha_inicio = actividad[4]
            fecha_finalizacion = actividad[5]
            estado = actividad[6]

            nueva_actividad = cli.Actividad(descripcion, costo, fecha_inicio, fecha_finalizacion)
            nueva_actividad.id = actividad_id
            nueva_actividad.estado = estado
            lista_actividades.append(nueva_actividad)

        return lista_actividades



    def menu_trabajador(self, trabajador):
        while True:
            print("\nBienvenido: ", trabajador[1])
            print("1. Mi informacion personal")
            print("2. Añadir trabajadores")
            print("3. Modificar Estado de la actividad")
            print("4. Mi equipo")
            print("5. Eliminar cuenta")
            print("6. Agregar horas a Trabajador por hora")
            print("7. Calcular planilla")
            print("8. Establecer fecha de corte")
            print("9. Mostrar planilla")
            print("10. Salir")
            try:
                opcion = int(input("\nSeleccione una opción: "))
            except ValueError:
                print("Ingrese un número válido.")
                continue
            #imprime la informacion del usuario que inicio sesion
            if opcion == 1:
                self.imprimir_informacion_trabajador(trabajador[0])

            #agrega nuevos trabajadoresa
            elif opcion == 2:
                self.registrar_nuevo_trabajador(
                    trabajador[0])
                
            #imprime la lista de trabajadores por obra para modificar el estado o progreso de la actividad
            elif opcion == 3:
                    self.imprimir_lista_trabajadores_por_obra(trabajador[0])
                    trabajador_encontrado = self.obtener_trabajadores_por_obra(trabajador[0])
                    
                    # Obtener la descripción de la actividad
                    id_actividad = input("Ingrese la descripción de la actividad: ")
                    actividad_encontrada = None
                    
                    for trabaj in trabajador_encontrado:
                        for actividad in trabaj.actividades:
                            if actividad.descripcion == id_actividad:
                                actividad_encontrada = actividad
                                break
                    #verifica si hay una actividad encontrada y luego ejecuta el bloque de código que sigue si es cierto
                    # luego ejecuta el bloque de código que sigue si es cierto

                    if actividad_encontrada is not None:
                        print("Estado actual:", actividad_encontrada.estado)  # Imprime el estado actual
                        
                        print("Seleccione el nuevo estado de la actividad:")
                        print("1. Actividad en progreso")
                        print("2. Actividad finalizada")
                        opcion_estado = input("Ingrese el número de la opción: ")
                        
                        nuevo_estado = None
                        if opcion_estado == "1":
                            nuevo_estado = "En Progreso"
                        elif opcion_estado == "2":
                            nuevo_estado = "Finalizada"
                        else:
                            print("Opción inválida. No se realizó ninguna modificación.")

                        if nuevo_estado is not None:
                            actividad_encontrada.estado = nuevo_estado
                            descripcion_actividad = actividad_encontrada.descripcion  # Obtener la descripción de la actividad
                            # Actualizar el estado en la base de datos
                            self.cursor.execute('''
                                UPDATE actividades
                                SET estado = ?
                                WHERE descripcion = ?
                            ''', (nuevo_estado, descripcion_actividad))
                            self.conn.commit()
                            print("Estado de la actividad actualizado en la base de datos.")
                        else:
                            print("No se encontró ninguna actividad con la descripción proporcionada.")
            #imprime los trabajadores que han sido registrados por el usuario que inicio sesion
            elif opcion == 4:
                self.imprimir_lista_trabajadores(trabajador[0])

            #elimina la cuenta
            elif opcion == 5:
                confirmacion = input(
                    "¿Estás seguro de eliminar tu cuenta? (si/no): ")
                if confirmacion.lower() == "si":
                    self.cursor.execute('''
                    DELETE FROM trabajadores WHERE id = ? AND registrado_por = ?
                ''', (trabajador[0], trabajador[0]))
                    self.conn.commit()
                    print("Cuenta eliminada exitosamente.")
                    break

            #Agrega las horas y los costes por hora a los trabajadores por hora
            elif opcion == 6:
                self.imprimir_lista_trabajadores_por_hora(trabajador[0])
                trabajador_id = input("\nIngrese el ID del trabajador por hora: ")
                trabajador_encontrado = self.obtener_trabajador_por_id(trabajador_id)

                if trabajador_encontrado and isinstance(trabajador_encontrado, cli.TrabajadorPorHora):
                    if trabajador_encontrado.registrado_por == trabajador[0]:
                        trabajador_encontrado.registrar_horas_trabajadas(self.conn,trabajador_id=trabajador_encontrado.id)
                    else:
                        print("No tienes permiso para registrar horas para este trabajador.")
                else:
                    print("No se encontró un trabajador por hora con ese ID.")
            #calcula el salario individual de los trabajadores por hora, obra y hace la suma correspondiente para calcular toda la planilla
            elif opcion == 7:
                print("Calculando planilla: ")
                
                # Crea una instancia de la clase Planilla y pasa el cursor como parametro
                planilla = cli.Planilla(self.conn.cursor())

                # Obtén los trabajadores por obra y por hora
                trabajadores_por_obra = self.obtener_trabajadores_por_obra(trabajador[0])
                trabajadores_por_hora = self.obtener_trabajadores_por_hora(trabajador[0])

                # Agrega los trabajadores a la planilla
                for trabajador_por_obra in trabajadores_por_obra:
                    planilla.agregar_trabajador_por_obra(trabajador_por_obra)

                for trabajador_por_hora in trabajadores_por_hora:
                    planilla.agregar_trabajador_por_hora(trabajador_por_hora)

                # Calcula y muestra la planilla
                planilla.calcular_planilla()

            #establece la fecha de corte, en esta solo se sumaran los salarios hasta esta fecha, 
            # cualquier actividad o hora trabajada queda fuera de la planilla
            elif opcion == 8:
                planilla = cli.Planilla(self.conn.cursor())
                nueva_fecha_str = input("Ingrese la nueva fecha de corte (YYYY-MM-DD): ")
                try:
                    nueva_fecha = cli.datetime.datetime.strptime(nueva_fecha_str, '%Y-%m-%d').date()
                    f= cli.Trabajador(None,None,None,None,None,None)
                    f.set_fecha_corte(nueva_fecha)
                    print("Fecha de corte actualizada para todos los trabajadores.")
                except ValueError:
                    print("Formato de fecha incorrecto.")
                   
            
            elif opcion==9:
                 print("Imprimiendo planilla:\n")
    
                 # Crea una instancia de la clase Planilla y pásale el cursor
                 planilla = cli.Planilla(self.conn.cursor())

                            # Obtiene los trabajadores por obra y por hora
                 trabajadores_por_obra = self.obtener_trabajadores_por_obra(trabajador[0])
                 trabajadores_por_hora = self.obtener_trabajadores_por_hora(trabajador[0])

                            # Agrega los trabajadores a la planilla
                 for trabajador_por_obra in trabajadores_por_obra:
                     planilla.agregar_trabajador_por_obra(trabajador_por_obra)

                 for trabajador_por_hora in trabajadores_por_hora:
                     planilla.agregar_trabajador_por_hora(trabajador_por_hora)

                            # Imprime la planilla completa
                 planilla.imprimir_planilla_completa()
            
            elif opcion == 10:
                print("Cerrando sesión...")
                break        
            else:
                print("Opción inválida. Seleccione una opción válida.")

    def registrar_trabajador(self, trabajador):
        bandera=None
        try:
            self.cursor.execute('''
                INSERT INTO trabajadores (id, nombre, apellido, salario, cargo, registrado_por)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (trabajador.id, trabajador.nombre, trabajador.apellido, trabajador.salario, trabajador.cargo, trabajador.registrado_por))
            self.conn.commit()

            if isinstance(trabajador, cli.TrabajadorPorObra):
                for actividad in trabajador.actividades:
                    self.cursor.execute('''
                    INSERT INTO actividades (trabajador_id, descripcion, costo, fecha_inicio, fecha_finalizacion)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (trabajador.id, actividad.descripcion, actividad.costo, actividad.fecha_inicio, actividad.fecha_finalizacion))
                self.conn.commit()

            print("\n\t\tTrabajador registrado con éxito.\n")

        except sqlite3.IntegrityError:
            print("Ya existe un trabajador con ese ID. Introduce un ID único.")
        

    def registrar_nuevo_trabajador(self, user_id):
        print("\nRegistro de nuevo trabajador:")

        cargo = input(
            "Cargo (1 - Trabajador por hora, 2 - Trabajador por obra): ")

        if cargo == "1":
            # *******************
            # Trabajador por Hora
            # *******************
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            id = input("ID: ")

            trabajador = cli.TrabajadorPorHora(
            id, nombre, apellido, 0, "Trabajador por hora", user_id, 0)
            self.registrar_trabajador(trabajador)
        
        elif cargo == "2":
            # *******************
            # Trabajador por Obra
            # *******************
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            id = input("ID: ")
            descripcion_actividad = input("Descripción de la actividad: ")
            costo_actividad = float(input("Costo de la actividad: "))
            fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
            fecha_finalizacion = input("Fecha de finalización (YYYY-MM-DD): ")

            actividad = cli.Actividad(descripcion_actividad, costo_actividad, fecha_inicio, fecha_finalizacion)
            trabajador = cli.TrabajadorPorObra(id, nombre, apellido, 0, "Trabajador por obra", user_id)
            trabajador.agregar_actividad(actividad)
            self.registrar_trabajador(trabajador)
        else:
            print("Opción inválida. El trabajador no ha sido registrado.")
        return True

    def imprimir_informacion_trabajador(self, id_trabajador):
        trabajador = self.cursor.execute('''
        SELECT * FROM trabajadores WHERE id = ?
    ''', (id_trabajador,)).fetchone()
        if trabajador is not None:
            print("\nInformación del trabajador:")
            print("Nombre:", trabajador[1])
            print("ID:", trabajador[0])
            print("Apellido:", trabajador[2])
            print("Cargo:", trabajador[3])
            print("Contraseña:", trabajador[4])
            print("Registrado por:", trabajador[5])  # Agregar esta línea
        else:
            print("No se encontró ningún trabajador con ese ID.")

    def imprimir_lista_trabajadores(self, user_id):
        trabajadores = self.cursor.execute('''
        SELECT * FROM trabajadores WHERE registrado_por = ?
    ''', (user_id,)).fetchall()
        if trabajadores:
            print("\nMi equipo:")
            for trabajador in trabajadores:
                print("ID:", trabajador[0])
                print("Nombre:", trabajador[1])
                print("Apellido:", trabajador[2])
                print("Cargo:", trabajador[3])
                print("Salario:", trabajador[5])
                print("------------------------")
        else:
            print("No hay trabajadores registrados por ti.")

    def iniciar_sesion(self):
        print("Gestor de planilla\n",
              "*******************************************")
        while True:
            print("Opciones:")
            print("1. Registrarse")
            print("2. Iniciar sesión")
            print("3. Salir")
            try:
                opcion = int(input("\nSeleccione una opción: "))
                print("*" * 12)
            except ValueError:
                print("Ingresa un numero valido")
                continue
            if opcion == 1:
                print("Ingrese sus datos\n")
                nombre = input("Nombre:")
                apellido = input("Apellido:")
                id = input("Id:")
                cargo = input("Cargo:")
                salario = None
                contraseña = input("Contraseñá:")
                self.cursor.execute('''
                INSERT INTO trabajadores (id, nombre, apellido,  contraseña,  cargo, salario)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (id, nombre, apellido, contraseña, cargo, salario))
                self.conn.commit()
            elif opcion == 2:
                print("\nIniciar Sesion")
                print("*" * 12)
                usuario = input("Ingrese su nombre de usuario (id): ")
                contraseña = input("Ingrese su Contraseña: ")
                ValidarUsuario = self.cursor.execute('''
                SELECT * FROM trabajadores WHERE id = ? AND contraseña = ?
            ''', (usuario, contraseña)).fetchone()
                print("\n" * 2)
                if ValidarUsuario is not None:
                    self.menu_trabajador(ValidarUsuario)
                else:
                    print("Credenciales inválidas.")
            elif opcion == 3:
                print("Saliendo...")
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")
        print("Fin del programa")


