from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")

CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


def carnets_registrados(excepto_id=None):
    """CONJUNTO con los carnet ya usados para detectar duplicados."""
    return {
        str(registro["carnet"]).lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id and "carnet" in registro
    }


def emails_registrados(excepto_id=None):
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id and "email" in registro
    }


def siguiente_id():
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_estudiante(datos):
    try:
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"

        if valores["carnet"].lower() in carnets_registrados():
            return False, "Ese carnet ya está registrado"

        estudiante = Estudiante(siguiente_id(), **valores)

        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"Estudiante {estudiante.obtener_nombre_completo()} creado con id {estudiante.id}"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    return [Estudiante.desde_diccionario(registro) for registro in gestor.leer()]


def obtener_por_id(id_estudiante):
    for est in obtener_todos():
        if est.id == id_estudiante:
            return est
    return None


# ===================== S · SEARCH =====================

def buscar_estudiantes(termino):
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    try:
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio"

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):
                return False, "Ese email ya lo usa otro estudiante"

        if "carnet" in cambios:
            if cambios["carnet"].lower() in carnets_registrados(excepto_id=id_estudiante):
                return False, "Ese carnet ya lo usa otro estudiante"

        registros = gestor.leer()
        posicion = None
        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        registros[posicion].update(cambios)
        gestor.guardar(registros)
        return True, f"Estudiante {id_estudiante} actualizado ({len(cambios)} campo/s)"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()
    quedan = [registro for registro in registros if registro["id"] != id_estudiante]

    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con id {id_estudiante}"

    gestor.guardar(quedan)
    return True, f"Estudiante {id_estudiante} eliminado"


# ===================== REQUISITOS ESPECÍFICOS =====================

def agregar_nota(id_estudiante, materia, nota):
    try:
        nota = float(nota)
        if not (0 <= nota <= 20):
            return False, "La nota debe ser un número entre 0 y 20"
    except ValueError:
        return False, "La nota debe ser un valor numérico válido"

    materia = materia.strip()
    if not materia:
        return False, "La materia no puede estar vacía"

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        return False, f"No existe un estudiante con id {id_estudiante}"

    estudiante.agregar_nota(materia, nota)

    registros = gestor.leer()
    for registro in registros:
        if registro["id"] == id_estudiante:
            registro["notas"] = estudiante.notas
            registro["materias"] = sorted(list(estudiante.materias))
            break

    if not gestor.guardar(registros):
        return False, "No se pudo guardar la nota en el archivo"

    return True, f"Nota {nota} agregada en '{materia}' para {estudiante.obtener_nombre_completo()}"


def materias_ofertadas():
    """Devuelve un conjunto con todas las materias registradas por todos los estudiantes."""
    materias = set()
    for registro in gestor.leer():
        materias.update(registro.get("materias", []))
    return sorted(materias)


def estudiantes_en_comun(id_a, id_b):
    """Usa la intersección de conjuntos para obtener materias compartidas."""
    est_a = obtener_por_id(id_a)
    est_b = obtener_por_id(id_b)

    if not est_a:
        return None, f"No existe el estudiante con id {id_a}"
    if not est_b:
        return None, f"No existe el estudiante con id {id_b}"

    comun = est_a.materias_en_comun(est_b)
    return sorted(comun), None