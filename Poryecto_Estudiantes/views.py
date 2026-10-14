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


class EstudianteController(CrudBase):

    def __init__(self, archivo="data/estudiantes.json"):
        self.gestor = GestorJSON(archivo)
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Estudiante.desde_diccionario(datos))

    def guardar(self):
        datos = [e.a_diccionario() for e in self.lista]
        self.gestor.guardar(datos)

    def carnets_registrados(self, excepto_id=None):
        """CONJUNTO de carnets ya usados: preguntar 'x in conjunto' es instantáneo."""
        return {e.carnet.upper() for e in self.lista if e.id != excepto_id}

    def emails_registrados(self, excepto_id=None):
        """CONJUNTO de emails ya usados para validación rápida."""
        return {e.email.lower() for e in self.lista if e.id != excepto_id}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "carnet"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email):
                return f"Email inválido: '{email}'"
            if email in self.emails_registrados(id_actual):
                return "Ese email ya está registrado"

        if "carnet" in datos:
            carnet = str(datos["carnet"]).strip().upper()
            if carnet in self.carnets_registrados(id_actual):
                return f"El carnet '{carnet}' ya está registrado"

        return None

    def leer(self):
        return self.lista

    def obtener(self, id_estudiante):
        for e in self.lista:
            if e.id == id_estudiante:
                return e
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        if not texto:
            return []
        encontrados = []
        for e in self.lista:
            if (texto in e.nombre.lower() or
                texto in e.apellido.lower() or
                texto in e.email.lower() or
                texto in e.carnet.lower() or
                texto in e.carrera.lower()):
                encontrados.append(e)
        return encontrados

    def siguiente(self):
        mayor = max([e.id for e in self.lista], default=0)
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
            str(datos["carnet"]).strip().upper(),
            str(datos.get("carrera", "")).strip().title()
        )
        self.lista.append(estudiante)
        self.guardar()
        return True, f"Estudiante creado: {estudiante.etiqueta()}"

    def actualizar(self, id_estudiante, datos):
        estudiante = self.obtener(id_estudiante)
        if not estudiante:
            return False, f"No existe un estudiante con id {id_estudiante}"
        if not datos:
            return False, "No se indicó ningún cambio"

        permitidos = {"nombre", "apellido", "email", "carnet", "carrera"}
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
            elif campo == "carnet":
                valor = valor.upper()
            setattr(estudiante, campo, valor)

        self.guardar()
        return True, f"Estudiante {id_estudiante} actualizado"

    def eliminar(self, id_estudiante):
        estudiante = self.obtener(id_estudiante)
        if not estudiante:
            return False, f"No existe un estudiante con id {id_estudiante}"
        self.lista.remove(estudiante)
        self.guardar()
        return True, f"Estudiante {id_estudiante} eliminado"


class MateriaController(CrudBase):

    def __init__(self, archivo="data/materias.json"):
        self.gestor = GestorJSON(archivo)
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Materia.desde_diccionario(datos))

    def guardar(self):
        datos = [m.a_diccionario() for m in self.lista]
        self.gestor.guardar(datos)

    def codigos_registrados(self, excepto_id=None):
        """CONJUNTO de códigos de materias únicos."""
        return {m.codigo.upper() for m in self.lista if m.id != excepto_id}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "codigo", "creditos"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "codigo" in datos:
            codigo = str(datos["codigo"]).strip().upper()
            if codigo in self.codigos_registrados(id_actual):
                return f"El código '{codigo}' ya está registrado"

        if "creditos" in datos:
            try:
                creditos = int(datos["creditos"])
                if not (1 <= creditos <= 10):
                    return "Los créditos deben estar entre 1 y 10"
            except ValueError:
                return "Los créditos deben ser un número entero"

        if "cupos" in datos:
            try:
                cupos = int(datos["cupos"])
                if not (0 <= cupos <= Materia.CUPOS_MAXIMOS):
                    return f"Los cupos deben estar entre 0 y {Materia.CUPOS_MAXIMOS}"
            except ValueError:
                return "Los cupos deben ser un número entero"

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
        if not texto:
            return []
        encontrados = []
        for m in self.lista:
            if texto in m.nombre.lower() or texto in m.codigo.lower():
                encontrados.append(m)
        return encontrados

    def siguiente(self):
        mayor = max([m.id for m in self.lista], default=0)
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        cupos = int(datos.get("cupos", Materia.CUPOS_MAXIMOS))
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
        if not materia:
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

        if "nombre" in datos:
            materia.nombre = str(datos["nombre"]).strip().title()
        if "codigo" in datos:
            materia.codigo = str(datos["codigo"]).strip().upper()
        if "creditos" in datos:
            materia.creditos = int(datos["creditos"])
        if "cupos" in datos:
            materia.cupos = int(datos["cupos"])

        self.guardar()
        return True, f"Materia {id_materia} actualizada"

    def eliminar(self, id_materia):
        materia = self.obtener(id_materia)
        if not materia:
            return False, f"No existe una materia con id {id_materia}"
        self.lista.remove(materia)
        self.guardar()
        return True, f"Materia {id_materia} eliminada"

    def materias_sin_cupo(self):
        """Lista de materias con cupos agotados."""
        return [m for m in self.lista if not m.hay_cupo()]


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

        if not self.estudiantes.obtener(estudiante_id):
            return f"No existe un estudiante con id {estudiante_id}"

        materia = self.materias.obtener(materia_id)
        if not materia:
            return f"No existe una materia con id {materia_id}"

        if not materia.hay_cupo():
            return f"La materia {materia.nombre} no tiene cupos disponibles"

        periodo = str(datos.get("periodo", "")).strip()
        if not periodo:
            return "El periodo académico es obligatorio"

        # Validar duplicidad en la misma materia y periodo
        for mat in self.lista:
            if mat.estudiante_id == estudiante_id and mat.materia_id == materia_id and mat.periodo == periodo:
                return "El estudiante ya está matriculado en esta materia para este periodo"

        return None

    def leer(self):
        return self.lista

    def obtener(self, id_matricula):
        for mat in self.lista:
            if mat.id == id_matricula:
                return mat
        return None

    def buscar(self, texto):
        texto = texto.strip()
        if not texto:
            return []
        encontrados = []
        for mat in self.lista:
            if texto in mat.periodo or texto in mat.fecha:
                encontrados.append(mat)
        return encontrados

    def siguiente(self):
        mayor = max([mat.id for mat in self.lista], default=0)
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        materia = self.materias.obtener(int(datos["materia_id"]))
        
        # Ocupar el cupo en la materia y guardar cambios
        materia.ocupar_cupo()
        self.materias.guardar()

        matricula = Matricula(
            self.siguiente(),
            int(datos["estudiante_id"]),
            materia.id,
            str(datos["periodo"]).strip(),
            float(datos.get("nota", 0.0)),
            str(datos.get("fecha", "")).strip()
        )
        self.lista.append(matricula)
        self.guardar()
        return True, f"Matrícula #{matricula.id} registrada con éxito"

    def actualizar(self, id_matricula, datos):
        return False, "Las matrículas no se modifican directamente: use registrar nota o retire la matrícula"

    def eliminar(self, id_matricula):
        """Retirar matrícula: se borra y el cupo vuelve a la materia."""
        matricula = self.obtener(id_matricula)
        if not matricula:
            return False, f"No existe la matrícula {id_matricula}"

        materia = self.materias.obtener(matricula.materia_id)
        if materia:
            materia.liberar_cupo()
            self.materias.guardar()

        self.lista.remove(matricula)
        self.guardar()
        return True, f"Matrícula #{id_matricula} retirada y cupo devuelto"

    def registrar_nota(self, id_matricula, nota):
        if not Materia.es_nota_valida(nota):
            return False, "Nota inválida (debe ser un número entre 0 y 20)"
        
        matricula = self.obtener(id_matricula)
        if not matricula:
            return False, f"No existe la matrícula {id_matricula}"

        matricula.nota = float(nota)
        self.guardar()
        return True, f"Nota registrada para la matrícula #{id_matricula}: {matricula.nota} ({matricula.estado()})"

    def retirar_matricula(self, id_matricula):
        return self.eliminar(id_matricula)

    def certificado(self, id_matricula):
        """DICCIONARIO índice para cruzar entidades y armar el certificado."""
        matricula = self.obtener(id_matricula)
        if not matricula:
            return None

        estudiante = self.estudiantes.obtener(matricula.estudiante_id)
        materia = self.materias.obtener(matricula.materia_id)

        texto = f"CERTIFICADO #{matricula.id}   periodo: {matricula.periodo}\n"
        texto += f"Estudiante: {estudiante.nombre} {estudiante.apellido}   ({estudiante.carnet})\n"
        texto += f"Materia   : {materia.nombre}   ({materia.codigo}) · {materia.creditos} créditos\n"
        texto += "-" * 42 + "\n"
        texto += f"Nota      : {matricula.nota}\n"
        texto += f"Estado    : {matricula.estado()}"
        return texto

    def matriculas_por_estudiante(self):
        """DICCIONARIO de LISTAS: {estudiante_id: [matrículas de ese estudiante]} usando setdefault."""
        agrupadas = {}
        for mat in self.lista:
            agrupadas.setdefault(mat.estudiante_id, []).append(mat)
        return agrupadas

    def promedio_de_estudiante(self, estudiante_id):
        mats = self.matriculas_por_estudiante().get(estudiante_id, [])
        if not mats:
            return 0.0
        suma = sum(mat.nota for mat in mats)
        return round(suma / len(mats), 2)