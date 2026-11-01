from bisect import bisect_left
from pasajero import Pasajero


class ListaPython:
    """Las mismas operaciones usando los métodos del list de Python."""

    def __init__(self):
        self.pasajeros = []

    def añadir(self, pasajero):
        if self.buscar(pasajero.numero) != -1:
            print(f"  Ya existe un pasajero con el número {pasajero.numero}")
            return False
        self.pasajeros.append(pasajero)
        return True

    def listar(self):
        if not self.pasajeros:
            print("  (lista vacía)")
            return
        for i, p in enumerate(self.pasajeros):
            print(f"  [{i}] {p}")

    def insertar(self, posicion, pasajero):
        if posicion < 0 or posicion > len(self.pasajeros):
            print("  Posición inválida")
            return False
        if self.buscar(pasajero.numero) != -1:
            print(f"  Ya existe un pasajero con el número {pasajero.numero}")
            return False
        self.pasajeros.insert(posicion, pasajero)
        return True

    def buscar(self, numero):
        indices = [i for i, p in enumerate(self.pasajeros) if p.numero == numero]
        return indices[0] if indices else -1

    def buscar_binaria(self, numero):
        keys = [p.numero for p in self.pasajeros]
        idx = bisect_left(keys, numero)
        if idx < len(self.pasajeros) and self.pasajeros[idx].numero == numero:
            return idx
        return -1

    def modificar(self, numero, nuevo_destino, nuevo_asiento):
        idx = self.buscar(numero)
        if idx != -1:
            self.pasajeros[idx].destino = nuevo_destino
            self.pasajeros[idx].asiento = nuevo_asiento
            return True
        return False

    def eliminar_por_posicion(self, posicion):
        if posicion < 0 or posicion >= len(self.pasajeros):
            print("  Posición inválida")
            return None
        return self.pasajeros.pop(posicion)

    def eliminar_por_valor(self, numero):
        idx = self.buscar(numero)
        if idx != -1:
            antes = len(self.pasajeros)
            self.pasajeros = [p for p in self.pasajeros if p.numero != numero]
            return len(self.pasajeros) < antes
        return False

    def ordenar_asc(self):
        self.pasajeros.sort(key=lambda p: p.numero)

    def ordenar_desc(self):
        self.pasajeros.sort(key=lambda p: p.numero, reverse=True)

    def reversar(self):
        self.pasajeros.reverse()

    def copiar(self):
        nueva = ListaPython()
        nueva.pasajeros = self.pasajeros.copy()
        return nueva

    def longitud(self):
        return len(self.pasajeros)

    def filtrar_por_destino(self, destino):
        return [p for p in self.pasajeros if p.destino.lower() == destino.lower()]

    def mayores_de_edad(self):
        return [p for p in self.pasajeros if p.es_mayor_de_edad()]