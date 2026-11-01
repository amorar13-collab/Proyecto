class Pasajero:
    """Representa a un pasajero de la aerolínea."""

    def __init__(self, numero, nombre, cedula, edad, fecha_vuelo, destino, asiento):
        self.numero = numero              # int -> 1002  (clave única)
        self.nombre = nombre              # str -> "Ana"
        self.cedula = cedula              # str -> "0912345678"
        self.edad = edad                  # int -> 28
        self.fecha_vuelo = fecha_vuelo    # str -> "2026-11-15"
        self.destino = destino            # str -> "Lima"
        self.asiento = asiento            # str -> "03C"

    def es_mayor_de_edad(self):
        return self.edad >= 18

    def __str__(self):
        return (f"#{self.numero} | {self.nombre:<8} | {self.cedula} | {self.edad:>2} años | "
                f"{self.fecha_vuelo} | {self.destino:<7} | asiento {self.asiento}")