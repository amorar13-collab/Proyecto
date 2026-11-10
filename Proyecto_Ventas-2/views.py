from abc import ABC, abstractmethod

from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


class CrudBase(ABC):

    @abstractmethod
    def leer(self):
        pass

    @abstractmethod
    def obtener(self, id_registro):
        pass

    @abstractmethod
    def buscar(self, texto):
        pass

    @abstractmethod
    def siguiente(self):
        pass

    @abstractmethod
    def crear(self, datos):
        pass

    @abstractmethod
    def actualizar(self, id_registro, datos):
        pass

    @abstractmethod
    def eliminar(self, id_registro):
        pass


# =====================================================================
# CONTROLADOR DE ESTUDIANTES
# =====================================================================
class EstudianteController(CrudBase):

    def __init__(self, archivo="data/estudiantes.json"):
        self.gestor = GestorJSON(archivo)
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Estudiante.desde_diccionario(datos))

    def guardar(self):
        datos = [est.a_diccionario() for est in self.lista]
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
        if id_actual is None:
            for campo in CAMPOS_OBLIGATORIOS:
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email):
                return f"Email inválido: '{email}'"
            emails_usados = {e.email.lower() for e in self.lista if e.id != id_actual}
            if email in emails_usados:
                return "Ese email ya está registrado"

        if "carnet" in datos:
            carnet = str(datos["carnet"]).strip()
            if carnet:
                carnets_usados = {e.carnet for e in self.lista if e.id != id_actual}
                if carnet in carnets_usados:
                    return f"El carnet '{carnet}' ya está registrado"

        telefono = str(datos.get("telefono", "")).strip()
        if telefono != "" and not telefono.isdigit():
            return "El teléfono solo puede tener números"
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_estudiante):
        for est in self.lista:
            if est.id == id_estudiante:
                return est
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for est in self.lista:
            if (texto in est.nombre.lower()
                    or texto in est.apellido.lower()
                    or texto in est.email.lower()
                    or texto in est.carnet.lower()
                    or texto in est.carrera.lower()):
                encontrados.append(est)
        return encontrados

    # --- BÚSQUEDA BINARIA (Por ID) ---
    def buscar_binario_por_id(self, id_buscado):
        """Búsqueda binaria eficiente por ID (requiere la lista ordenada por ID)."""
        # Aseguramos que la lista esté ordenada por ID temporalmente para la búsqueda binaria
        ordenados = sorted(self.lista, key=lambda x: x.id)
        izquierda = 0
        derecha = len(ordenados) - 1

        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            if ordenados[medio].id == id_buscado:
                return ordenados[medio]
            elif ordenados[medio].id < id_buscado:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        return None

    # --- MÉTODOS DE ORDENAMIENTO Y REVERSIÓN ---
    def ordenar_ascendente(self):
        """Ordena la lista de estudiantes alfabéticamente por nombre."""
        self.lista.sort(key=lambda x: x.nombre.lower())

    def ordenar_descendente(self):
        """Ordena la lista de estudiantes en orden alfabético inverso por nombre."""
        self.lista.sort(key=lambda x: x.nombre.lower(), reverse=True)

    def reversar_lista(self):
        """Invierte el orden actual de la lista de estudiantes."""
        self.lista.reverse()

    def siguiente(self):
        mayor = max([est.id for est in self.lista], default=0)
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        estudiante = Estudiante(
            self.siguiente(),
            str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(),
            str(datos["email"]).strip().lower(),
            str(datos.get("carnet", "")).strip(),
            str(datos.get("carrera", "")).strip().title()
        )
        self.lista.append(estudiante)
        self.guardar()
        return True, f"Estudiante creado: {estudiante.etiqueta()}"

    def actualizar(self, id_estudiante, datos):
        estudiante = self.obtener(id_estudiante)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"
        if not datos:
            return False, "No se indicó ningún cambio"

        permitidos = {"nombre", "apellido", "email", "carnet", "carrera", "telefono"}
        desconocidos = set(datos) - permitidos
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_estudiante)
        if error:
            return False, error

        for campo, valor in datos.items():
            valor = str(valor).strip()
            if campo in ("nombre", "apellido", "carrera"):
                valor = valor.title()
            elif campo == "email":
                valor = valor.lower()
            setattr(estudiante, campo, valor)

        self.guardar()
        return True, f"Estudiante {id_estudiante} actualizado"

    def eliminar(self, id_estudiante):
        estudiante = self.obtener(id_estudiante)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        self.lista.remove(estudiante)
        self.guardar()
        return True, f"Estudiante {id_estudiante} eliminado"

    def carreras(self):
        return sorted({e.carrera for e in self.lista if e.carrera != ""})


# =====================================================================
# CONTROLADOR DE MATERIAS
# =====================================================================
class MateriaController(CrudBase):

    def __init__(self, archivo="data/materias.json"):
        self.gestor = GestorJSON(archivo)
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Materia.desde_diccionario(datos))

    def guardar(self):
        datos = [m.a_diccionario() for m in self.lista]
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "codigo", "creditos"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "codigo" in datos:
            codigo = str(datos["codigo"]).strip().upper()
            codigos_usados = {m.codigo.upper() for m in self.lista if m.id != id_actual}
            if codigo in codigos_usados:
                return f"Ya existe una materia con el código '{codigo}'"

        if "creditos" in datos:
            try:
                creditos = int(datos["creditos"])
                if not (1 <= creditos <= 10):
                    return "Los créditos deben estar entre 1 y 10"
            except (TypeError, ValueError):
                return "Los créditos deben ser un número entero válido"

        if "cupos" in datos and str(datos["cupos"]).strip() != "":
            try:
                cupos = int(datos["cupos"])
                if not (0 <= cupos <= Materia.CUPOS_MAXIMOS):
                    return f"Los cupos deben estar entre 0 y {Materia.CUPOS_MAXIMOS}"
            except (TypeError, ValueError):
                return "El cupo debe ser un número entero"

        return None

    def leer(self):
        return self.lista

    def obtener(self, id_materia):
        for m in self.lista:
            if m.id == id_materia:
                return m
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for m in self.lista:
            if texto in m.nombre.lower() or texto in m.codigo.lower():
                encontrados.append(m)
        return encontrados

    # --- BÚSQUEDA BINARIA (Por ID) ---
    def buscar_binario_por_id(self, id_buscado):
        ordenados = sorted(self.lista, key=lambda x: x.id)
        izquierda = 0
        derecha = len(ordenados) - 1

        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            if ordenados[medio].id == id_buscado:
                return ordenados[medio]
            elif ordenados[medio].id < id_buscado:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        return None

    # --- MÉTODOS DE ORDENAMIENTO Y REVERSIÓN ---
    def ordenar_ascendente(self):
        self.lista.sort(key=lambda x: x.nombre.lower())

    def ordenar_descendente(self):
        self.lista.sort(key=lambda x: x.nombre.lower(), reverse=True)

    def reversar_lista(self):
        self.lista.reverse()

    def siguiente(self):
        mayor = max([m.id for m in self.lista], default=0)
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        cupos_val = datos.get("cupos", Materia.CUPOS_MAXIMOS)
        cupos = int(cupos_val) if str(cupos_val).strip() != "" else Materia.CUPOS_MAXIMOS

        materia = Materia(
            self.siguiente(),
            str(datos["nombre"]).strip().title(),
            str(datos["codigo"]).strip().upper(),
            int(datos["creditos"]),
            cupos
        )
        self.lista.append(materia)
        self.guardar()
        return True, f"Materia creada: {materia.etiqueta()}"

    def actualizar(self, id_materia, datos):
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe una materia con id {id_materia}"
        if not datos:
            return False, "No se indicó ningún cambio"

        permitidos = {"nombre", "codigo", "creditos", "cupos"}
        desconocidos = set(datos) - permitidos
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_materia)
        if error:
            return False, error

        for campo, valor in datos.items():
            if campo == "nombre":
                setattr(materia, campo, str(valor).strip().title())
            elif campo == "codigo":
                setattr(materia, campo, str(valor).strip().upper())
            elif campo in ("creditos", "cupos"):
                setattr(materia, campo, int(valor))

        self.guardar()
        return True, f"Materia {id_materia} actualizada"

    def eliminar(self, id_materia):
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe una materia con id {id_materia}"

        self.lista.remove(materia)
        self.guardar()
        return True, f"Materia {id_materia} eliminada"

    def materias_sin_cupo(self):
        return [m for m in self.lista if m.cupos == 0]


# =====================================================================
# CONTROLADOR DE MATRÍCULAS
# =====================================================================
class MatriculaController(CrudBase):

    def __init__(self, estudiantes, materias, archivo="data/matriculas.json"):
        self.estudiantes = estudiantes
        self.materias = materias
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Matricula.desde_diccionario(datos))

    def guardar(self):
        datos = [mat.a_diccionario() for mat in self.lista]
        self.gestor.guardar(datos)

    def validar(self, datos):
        try:
            estudiante_id = int(datos.get("estudiante_id", 0))
            materia_id = int(datos.get("materia_id", 0))
        except (TypeError, ValueError):
            return "estudiante_id y materia_id deben ser números enteros"

        periodo = str(datos.get("periodo", "")).strip()
        if not periodo:
            return "El periodo académico es obligatorio (ej. 2026-1)"

        if self.estudiantes.obtener(estudiante_id) is None:
            return f"No existe un estudiante con id {estudiante_id}"

        materia = self.materias.obtener(materia_id)
        if materia is None:
            return f"No existe una materia con id {materia_id}"

        if not materia.hay_cupo():
            return f"La materia {materia.nombre} no tiene cupos disponibles"

        for mat in self.lista:
            if (mat.estudiante_id == estudiante_id and 
                mat.materia_id == materia_id and 
                mat.periodo.lower() == periodo.lower()):
                return f"El estudiante ya está matriculado en esta materia para el periodo {periodo}"

        return None

    def leer(self):
        return self.lista

    def obtener(self, id_matricula):
        for mat in self.lista:
            if mat.id == id_matricula:
                return mat
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontradas = []
        if texto == "":
            return encontradas

        for mat in self.lista:
            if texto in mat.periodo.lower():
                encontradas.append(mat)
        return encontradas

    # --- BÚSQUEDA BINARIA (Por ID) ---
    def buscar_binario_por_id(self, id_buscado):
        ordenados = sorted(self.lista, key=lambda x: x.id)
        izquierda = 0
        derecha = len(ordenados) - 1

        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            if ordenados[medio].id == id_buscado:
                return ordenados[medio]
            elif ordenados[medio].id < id_buscado:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        return None

    # --- MÉTODOS DE ORDENAMIENTO Y REVERSIÓN ---
    def ordenar_ascendente(self):
        self.lista.sort(key=lambda x: x.periodo.lower())

    def ordenar_descendente(self):
        self.lista.sort(key=lambda x: x.periodo.lower(), reverse=True)

    def reversar_lista(self):
        self.lista.reverse()

    def siguiente(self):
        mayor = max([mat.id for mat in self.lista], default=0)
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        materia = self.materias.obtener(int(datos["materia_id"]))
        matricula = Matricula(
            self.siguiente(),
            int(datos["estudiante_id"]),
            materia.id,
            str(datos["periodo"]).strip(),
            float(datos.get("nota", 0.0))
        )

        materia.ocupar_cupo()
        self.materias.guardar()

        self.lista.append(matricula)
        self.guardar()
        return True, f"Matrícula registrada con ID {matricula.id}"

    def actualizar(self, id_matricula, datos):
        return False, "Las matrículas no se modifican directamente: use el registro de notas o anulación"

    def eliminar(self, id_matricula):
        return self.retirar_matricula(id_matricula)

    def retirar_matricula(self, id_matricula):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, f"No existe la matrícula {id_matricula}"

        materia = self.materias.obtener(matricula.materia_id)
        if materia is not None:
            materia.liberar_cupo()
            self.materias.guardar()

        self.lista.remove(matricula)
        self.guardar()
        return True, f"Matrícula {id_matricula} retirada y cupo devuelto"

    def registrar_nota(self, id_matricula, nota):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, f"No existe la matrícula {id_matricula}"

        if not Materia.es_nota_valida(nota):
            return False, f"Nota inválida ({nota}). Debe estar entre 0 y 20."

        matricula.nota = float(nota)
        self.guardar()
        return True, f"Nota registrada correctamente para la matrícula {id_matricula} ({matricula.estado()})"

    def certificado(self, id_matricula):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return None

        mapa_estudiantes = {e.id: e for e in self.estudiantes.leer()}
        mapa_materias = {m.id: m for m in self.materias.leer()}

        estudiante = mapa_estudiantes.get(matricula.estudiante_id)
        materia = mapa_materias.get(matricula.materia_id)

        est_nombre = estudiante.nombre_completo() if estudiante else "Eliminado"
        est_carnet = estudiante.carnet if estudiante else "N/A"
        mat_nombre = materia.nombre if materia else "Eliminada"
        mat_codigo = materia.codigo if materia else "N/A"
        mat_creditos = materia.creditos if materia else 0

        texto = f"CERTIFICADO #{matricula.id}    periodo: {matricula.periodo}\n"
        texto += f"Estudiante: {est_nombre}   ({est_carnet})\n"
        texto += f"Materia   : {mat_nombre}   ({mat_codigo}) · {mat_creditos} créditos\n"
        texto += "-" * 42 + "\n"
        texto += f"Nota      : {matricula.nota}\n"
        texto += f"Estado    : {matricula.estado()}"
        return texto

    def matriculas_por_estudiante(self):
        agrupadas = {}
        for mat in self.lista:
            agrupadas.setdefault(mat.estudiante_id, []).append(mat)
        return agrupadas

    def promedio_de_estudiante(self, estudiante_id):
        notas = [mat.nota for mat in self.lista if mat.estudiante_id == estudiante_id]
        if not notas:
            return 0.0
        return round(sum(notas) / len(notas), 2)