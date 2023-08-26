#
#@Autor:diromero@unah.hn
#Modulo con las clases necesarias para que el gestor funcione
#
 

import sqlite3
import datetime
from datetime import datetime as tim

#Clase se encarga del manejo de una fecha de corte
class FechaCort:
    fecha_corte = datetime.date.today()

    @classmethod
    def set_fecha_corte(cls, fecha):
        cls.fecha_corte = fecha

class Trabajador(FechaCort):
    def __init__(self, id, nombre, apellido, salario, cargo, registrado_por):
        super().__init__()
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.salario = salario
        self.cargo = cargo
        self.registrado_por = registrado_por
        self.actividades = []
        self.horas_trabajadas = []
        self.deducciones = []
        
    def agregar_actividad(self, actividad):
        self.actividades.append(actividad)

    def registrar_horas_trabajadas(self, trabajador_id):
        if self.login_system is None:
            print("Error: No se ha establecido el sistema de login.")
            return

        print("\nRegistro de horas trabajadas:")
        try:
            horas = float(input("Horas trabajadas: "))
            costo_por_hora = float(input("Costo por hora: "))
        except ValueError:
            print("Ingresa valores numéricos válidos.")
            return

        self.login_system.cursor.execute('''
            INSERT INTO horas_trabajadas (trabajador_id, horas, costo_por_hora)
            VALUES (?, ?, ?)
        ''', (trabajador_id, horas, costo_por_hora))
        self.login_system.conn.commit()

        print("Horas registradas exitosamente.")

    def calcular_salario_neto(self):
        salario_bruto = self.salario

        for actividad in self.actividades:
            fecha_inicio_actividad = datetime.strptime(actividad.fecha_inicio, "%Y-%m-%d").date()
            if fecha_inicio_actividad <= self.fecha_corte:
                salario_bruto += actividad.costo

        for horas, costo_por_hora in self.horas_trabajadas:
            fecha_horas = datetime.strptime(horas.fecha, "%Y-%m-%d").date()
            if fecha_horas <= self.fecha_corte:
                salario_bruto += horas * costo_por_hora

        for deduccion in self.deducciones:
            salario_bruto -= deduccion.monto

        return salario_bruto

    def aplicar_deduccion(self, monto_deduccion):
        self.deducciones.append(Deduccion(monto_deduccion))

    def calcular_salario_neto(self):
        salario_bruto = self.salario

        for actividad in self.actividades:
            fecha_inicio_actividad = tim.strptime(actividad.fecha_inicio, "%Y-%m-%d").date()
            if fecha_inicio_actividad <= self.fecha_corte:
                salario_bruto += actividad.costo

        for horas, costo_por_hora in self.horas_trabajadas:
            fecha_horas = tim.strptime(horas.fecha, "%Y-%m-%d").date()
            if fecha_horas <= self.fecha_corte:
                salario_bruto += horas * costo_por_hora

        for deduccion in self.deducciones:
            salario_bruto -= deduccion.monto

        return salario_bruto

class TrabajadorPorHora(Trabajador):
    def __init__(self, id, nombre, apellido, salario, cargo,  registrado_por, costo_por_hora):
        super().__init__(id, nombre, apellido, salario, cargo,  registrado_por)
        self.costo_por_hora = costo_por_hora
    def registrar_horas_trabajadas(self, conn, trabajador_id):
        print("\nRegistro de horas trabajadas:")
        try:
            horas = float(input("Horas trabajadas: "))
            costo_por_hora = float(input("Costo por hora: "))
        except ValueError: 
            print("Ingresa valores numéricos válidos.")
            return

        conn.execute('''
            INSERT INTO horas_trabajadas (trabajador_id, horas, costo_por_hora)
            VALUES (?, ?, ?)
        ''', (trabajador_id, horas, costo_por_hora))
        conn.commit()

        print("Horas registradas exitosamente.")

    def calcular_salario_neto(self):
        total_salario = self.salario

        for horas, costo_por_hora in self.horas_trabajadas:
            total_salario += horas * costo_por_hora

        for deduccion in self.deducciones:
            total_salario -= deduccion.monto

        return total_salario

    def calcular_salario_neto(self):
        total_salario = self.salario

        for horas, costo_por_hora in self.horas_trabajadas:
            total_salario += horas * costo_por_hora

        for deduccion in self.deducciones:
            total_salario -= deduccion.monto

        return total_salario

class TrabajadorPorObra(Trabajador):
    def __init__(self, id, nombre, apellido, salario, cargo, registrado_por):
        super().__init__(id, nombre, apellido, salario, cargo, registrado_por)
        self.actividades = []  # Lista para almacenar las actividades

    def agregar_actividad(self, actividad):
        self.actividades.append(actividad)

    def calcular_pago(self, fecha_corte):
        total_pago = 0

        for actividad in self.actividades:
            fecha_inicio_actividad = datetime.strptime(actividad.fecha_inicio, "%Y-%m-%d").date()
            if fecha_inicio_actividad <= fecha_corte:
                total_pago += actividad.costo

        return total_pago

#Funciona para hacer las modificaciones de deduccion de los salarios de la planilla
class Deduccion:
    def __init__(self, monto):
        self.monto = monto
#maneja las actividades del trabajador por hora        
class Actividad:
    def __init__(self, descripcion, costo, fecha_inicio, fecha_finalizacion, estado='en progreso'):
        self.descripcion = descripcion
        self.costo = costo
        self.fecha_inicio = fecha_inicio
        self.fecha_finalizacion = fecha_finalizacion
        self.estado = estado  # Agregamos el atributo "estado"

    def marcar_actividad_completada(self):
        self.estado = 'finalizada'

    def __str__(self):
        return f"Actividad: {self.descripcion}\nDescripcion {self.costo}\nCosto: {self.fecha_inicio}\nFecha de inicio: {self.fecha_finalizacion}\nFecha de finalización: {self.fecha_finalizacion}\nEstado: {self.estado}"


class Planilla(FechaCort):   
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.trabajadores_por_obra = []
        self.trabajadores_por_hora = []

    def agregar_trabajador_por_obra(self, trabajador):
        if isinstance(trabajador, TrabajadorPorObra):
            self.trabajadores_por_obra.append(trabajador)
        else:
            print("Error: El trabajador no es de tipo TrabajadorPorObra.")

    def agregar_trabajador_por_hora(self, trabajador):
        if isinstance(trabajador, TrabajadorPorHora):
            self.trabajadores_por_hora.append(trabajador)
        else:
            print("Error: El trabajador no es de tipo TrabajadorPorHora.")

    def calcular_planilla(self):
        total_salarios = 0

        print("\nCalculando planilla:\n")

        for trabajador in self.trabajadores_por_obra:
            salario = trabajador.calcular_salario_neto()
            total_salarios += salario
            if self.fecha_corte > trabajador.fecha_corte:
                salario = 0
                total_salarios += salario
            print(f"{trabajador.nombre} {trabajador.apellido}: ${salario:.2f}")

        for trabajador in self.trabajadores_por_hora:
            salario = 0

            # Obtener las horas trabajadas y el costo por hora desde la tabla horas_trabajadas
            for horas_trabajadas, costo_por_hora in self.obtener_horas_trabajadas(trabajador.id):
                salario += horas_trabajadas * costo_por_hora

            trabajador.salario = salario  # Actualizar el salario del trabajador
            total_salarios += salario
            print(f"{trabajador.nombre} {trabajador.apellido}: ${salario:.2f}")

        print("\nTotal de salarios: ${:.2f}".format(total_salarios))

    def obtener_horas_trabajadas(self, trabajador_id):
        horas_trabajadas = self.cursor.execute('''
            SELECT horas, costo_por_hora FROM horas_trabajadas
            WHERE trabajador_id = ?
        ''', (trabajador_id,)).fetchall()

        return horas_trabajadas
    
    def imprimir_planilla_completa(self):
        total_salarios = 0

        print("\nPlanilla completa:\n")
        
        for trabajador in self.trabajadores_por_obra:
            salario = trabajador.calcular_salario_neto()
            total_salarios += salario
            print(f"{trabajador.nombre} {trabajador.apellido}: ${salario:.2f}")
            print("Actividades:")
            for actividad in trabajador.actividades:
                print("  Descripción:", actividad.descripcion)
                print("  Costo:", actividad.costo)
                print("  Fecha de inicio:", actividad.fecha_inicio)
                print("  Fecha de finalización:", actividad.fecha_finalizacion)
            print("-" * 20)

        for trabajador in self.trabajadores_por_hora:
            salario = 0

            # Obtener las horas trabajadas y el costo por hora desde la tabla horas_trabajadas
            for horas_trabajadas, costo_por_hora in self.obtener_horas_trabajadas(trabajador.id):
                salario += horas_trabajadas * costo_por_hora

            trabajador.salario = salario  # Actualizar el salario del trabajador
            total_salarios += salario
            print(f"{trabajador.nombre} {trabajador.apellido}: ${salario:.2f}")
            
            horas_trabajadas = self.obtener_horas_trabajadas(trabajador.id)
            if horas_trabajadas:
                print("Horas trabajadas:")
                for horas, costo_por_hora in horas_trabajadas:
                    print("  Horas:", horas)
                    print("  Costo por hora:", costo_por_hora)
                print("-" * 20)

        print("\nTotal de salarios en la planilla: ${:.2f}".format(total_salarios))