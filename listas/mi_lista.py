from pasajero import Pasajero


class MiLista:
    
    def __init__(self, capacidad=10):
        self.datos = [None] * capacidad
        self.capacidad = capacidad
        self.cantidad = 0

    def añadir(self, pasajero):
        if self.cantidad == self.capacidad:
            print("  ⚠ La lista está llena")
            return False
        if self.buscar(pasajero.numero) != -1:
            print(f"  ⚠ Ya existe un pasajero con el número {pasajero.numero}")
            return False
        self.datos[self.cantidad] = pasajero
        self.cantidad = self.cantidad + 1
        return True

    def listar(self):
        if self.cantidad == 0:
            print("  (lista vacía)")
            return
        for i in range(self.cantidad):
            print(f"  [{i}] {self.datos[i]}")

    def insertar(self, posicion, pasajero):
        if self.cantidad == self.capacidad:
            print("  ⚠ La lista está llena")
            return False
        if posicion < 0 or posicion > self.cantidad:
            print("  ⚠ Posición inválida")
            return False
        if self.buscar(pasajero.numero) != -1:
            print(f"  ⚠ Ya existe un pasajero con el número {pasajero.numero}")
            return False
        for i in range(self.cantidad, posicion, -1):
            self.datos[i] = self.datos[i - 1]
        self.datos[posicion] = pasajero
        self.cantidad = self.cantidad + 1
        return True

    def buscar(self, numero):
        for i in range(self.cantidad):
            if self.datos[i].numero == numero:
                return i
        return -1

    def buscar_binaria(self, numero):
        inicio = 0
        fin = self.cantidad - 1
        while inicio <= fin:
            medio = (inicio + fin) // 2
            if self.datos[medio].numero == numero:
                return medio
            elif self.datos[medio].numero < numero:
                inicio = medio + 1
            else:
                fin = medio - 1
        return -1

    def modificar(self, numero, nuevo_destino, nuevo_asiento):
        idx = self.buscar(numero)
        if idx != -1:
            self.datos[idx].destino = nuevo_destino
            self.datos[idx].asiento = nuevo_asiento
            return True
        return False

    def eliminar_por_posicion(self, posicion):
        if posicion < 0 or posicion >= self.cantidad:
            print("  ⚠ Posición inválida")
            return None
        pasajero_eliminado = self.datos[posicion]
        for i in range(posicion, self.cantidad - 1):
            self.datos[i] = self.datos[i + 1]
        self.datos[self.cantidad - 1] = None
        self.cantidad = self.cantidad - 1
        return pasajero_eliminado

    def eliminar_por_valor(self, numero):
        idx = self.buscar(numero)
        if idx != -1:
            pasajero = self.eliminar_por_posicion(idx)
            return pasajero is not None
        return False

    def ordenar_asc(self):
        for i in range(self.cantidad - 1):
            for j in range(self.cantidad - 1 - i):
                if self.datos[j].numero > self.datos[j + 1].numero:
                    aux = self.datos[j]
                    self.datos[j] = self.datos[j + 1]
                    self.datos[j + 1] = aux

    def ordenar_desc(self):
        for i in range(self.cantidad - 1):
            for j in range(self.cantidad - 1 - i):
                if self.datos[j].numero < self.datos[j + 1].numero:
                    aux = self.datos[j]
                    self.datos[j] = self.datos[j + 1]
                    self.datos[j + 1] = aux

    def reversar(self):
        inicio = 0
        fin = self.cantidad - 1
        while inicio < fin:
            aux = self.datos[inicio]
            self.datos[inicio] = self.datos[fin]
            self.datos[fin] = aux
            inicio = inicio + 1
            fin = fin - 1

    def copiar(self):
        nueva = MiLista(self.capacidad)
        for i in range(self.cantidad):
            nueva.añadir(self.datos[i])
        return nueva

    def longitud(self):
        return self.cantidad