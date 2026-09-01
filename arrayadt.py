import datetime

class Array:
    def __init__(self, tamano):
        self.__tamano = tamano
        self.__datos = [None for _ in range(self.__tamano)]

    def get_length(self):
        return self.__tamano

    def set_item(self, indice, dato):
        if 0 <= indice < self.__tamano:
            self.__datos[indice] = dato

    def get_item(self, indice):
        if 0 <= indice < self.__tamano:
            return self.__datos[indice]
        return None

    def __iter__(self):
        return _IteradorArray(self.__datos)


class _IteradorArray:
    def __init__(self, datos):
        self.__datos = datos
        self.__indice = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__indice < len(self.__datos):
            dato = self.__datos[self.__indice]
            self.__indice += 1
            return dato
        raise StopIteration


class Empleado:
    def __init__(self, num, nombres, paterno, materno, horas_extra, sueldo_base, anio_ingreso):
        self.num = int(num)
        self.nombres = nombres
        self.paterno = paterno
        self.materno = materno
        self.horas_extra = int(horas_extra)
        self.sueldo_base = float(sueldo_base)
        self.anio_ingreso = int(anio_ingreso)

    def calcular_sueldo(self, anio_actual=2026):
        antiguedad = anio_actual - self.anio_ingreso
        pago_horas_extra = self.horas_extra * 276.5
        prestacion_antiguedad = self.sueldo_base * (0.03 * antiguedad)
        return self.sueldo_base + pago_horas_extra + prestacion_antiguedad


class NominaADT:
    def __init__(self, ruta_archivo):
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            lineas = [linea.strip() for linea in archivo if linea.strip()]

        self.__empleados = Array(len(lineas) - 1)

        for i in range(1, len(lineas)):
            datos = lineas[i].split(',')
            emp = Empleado(
                num=datos[0],
                nombres=datos[1],
                paterno=datos[2],
                materno=datos[3],
                horas_extra=datos[4],
                sueldo_base=datos[5],
                anio_ingreso=datos[6]
            )
            self.__empleados.set_item(i - 1, emp)

    def mostrar_extremos_antiguedad(self):
        emp_mayor = self.__empleados.get_item(0)
        emp_menor = self.__empleados.get_item(0)

        for emp in self.__empleados:
            if emp.anio_ingreso < emp_mayor.anio_ingreso:
                emp_mayor = emp
            if emp.anio_ingreso > emp_menor.anio_ingreso:
                emp_menor = emp

        anio_actual = datetime.datetime.now().year
        print("=== TRABAJADOR CON MAYOR ANTIGÜEDAD ===")
        print(f"ID: {emp_mayor.num} | Nombre: {emp_mayor.nombres} {emp_mayor.paterno} {emp_mayor.materno}")
        print(f"Año de ingreso: {emp_mayor.anio_ingreso} ({anio_actual - emp_mayor.anio_ingreso} años de antigüedad)\n")

        print("=== TRABAJADOR CON MENOR ANTIGÜEDAD ===")
        print(f"ID: {emp_menor.num} | Nombre: {emp_menor.nombres} {emp_menor.paterno} {emp_menor.materno}")
        print(f"Año de ingreso: {emp_menor.anio_ingreso} ({anio_actual - emp_menor.anio_ingreso} años de antigüedad)\n")

    def mostrar_sueldos_totales(self):
        anio_actual = datetime.datetime.now().year
        print("=== REPORTE DE NÓMINA (SUELDOS A PAGAR) ===")
        print(f"{'ID':<6} | {'NOMBRE COMPLETO':<32} | {'H.EXTRA':<7} | {'INGRESO':<7} | {'SUELDO A PAGAR':<14}")
        print("-" * 78)
        
        for emp in self.__empleados:
            nombre_completo = f"{emp.nombres} {emp.paterno} {emp.materno}"
            sueldo_total = emp.calcular_sueldo(anio_actual)
            print(f"{emp.num:<6} | {nombre_completo:<32} | {emp.horas_extra:<7} | {emp.anio_ingreso:<7} | ${sueldo_total:,.2f}")


if __name__ == "__main__":
    archivo_datos = "junio.dat"

    # Instanciación y ejecución del ADT
    nomina = NominaADT(archivo_datos)
    nomina.mostrar_extremos_antiguedad()
    nomina.mostrar_sueldos_totales()
