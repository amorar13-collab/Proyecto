from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, agregar_nota,
    materias_ofertadas, estudiantes_en_comun
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'CARNET':<12}{'NOMBRE':<25}{'EMAIL':<28}{'PROMEDIO':<10}")
    print("-" * 80)
    for est in estudiantes:
        print(f"{est.id:<5}{est.carnet:<12}{est.obtener_nombre_completo():<25}"
              f"{est.email:<28}{est.obtener_promedio():<10}")
    print("-" * 80)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


# ---------- C · CREAR ----------
def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ---------- R · LEER TODOS ----------
def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("Todavía no hay estudiantes. Use la opción 1 para crear el primero.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


# ---------- S · BUSCAR ----------
def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email o carnet: ")
    encontrados = buscar_estudiantes(termino)

    if not encontrados:
        imprimir_info(f"Ningún estudiante coincide con '{termino}'.")
    else:
        mostrar_tabla(encontrados)
    pausa()


# ---------- R · LEER UNO ----------
def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    try:
        id_est = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error(f"No existe un estudiante con id {id_est}")
    else:
        print(f"  ID        : {est.id}")
        print(f"  Carnet    : {est.carnet}")
        print(f"  Nombre    : {est.obtener_nombre_completo()}")
        print(f"  Email     : {est.email}")
        print(f"  Promedio  : {est.obtener_promedio()}")
        print(f"  Materias  : {', '.join(est.materias) if est.materias else 'Ninguna'}")
        print("  Notas:")
        if est.notas:
            for materia, notas_lista in est.notas.items():
                print(f"    - {materia}: {notas_lista}")
        else:
            print("    - Sin notas registradas")
    pausa()


# ---------- U · ACTUALIZAR ----------
def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    try:
        id_est = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error(f"No existe un estudiante con id {id_est}")
        return pausa()

    imprimir_info(f"Editando a {est.obtener_nombre_completo()}")
    print("Deje en blanco el campo que no quiera cambiar.\n")

    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(est, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_est, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ---------- D · ELIMINAR ----------
def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_est = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error(f"No existe un estudiante con id {id_est}")
        return pausa()

    imprimir_info(f"Se eliminará: {est}")
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_estudiante(id_est)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


# ---------- NUEVAS OPCIONES SOLICITADAS ----------

def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA A ESTUDIANTE")
    try:
        id_est = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    materia = input("Nombre de la materia: ")
    try:
        nota = float(input("Nota (0 a 20): "))
    except ValueError:
        imprimir_error("La nota debe ser un valor numérico")
        return pausa()

    exito, mensaje = agregar_nota(id_est, materia, nota)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_ver_promedio():
    imprimir_titulo("VER PROMEDIO DE ESTUDIANTE")
    try:
        id_est = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error(f"No existe un estudiante con id {id_est}")
    else:
        imprimir_info(f"Estudiante: {est.obtener_nombre_completo()} ({est.carnet})")
        print(f"  Promedio general: {est.obtener_promedio()}")
        if est.notas:
            print("  Detalle por materia:")
            for mat, n_list in est.notas.items():
                prom_mat = round(sum(n_list) / len(n_list), 2) if n_list else 0
                print(f"    - {mat}: {n_list} (Promedio: {prom_mat})")
    pausa()


def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN ENTRE DOS ESTUDIANTES")
    try:
        id_a = int(input("Id del primer estudiante: "))
        id_b = int(input("Id del segundo estudiante: "))
    except ValueError:
        imprimir_error("Los IDs deben ser números enteros")
        return pausa()

    comun, error = estudiantes_en_comun(id_a, id_b)
    if error:
        imprimir_error(error)
    else:
        est_a = obtener_por_id(id_a)
        est_b = obtener_por_id(id_b)
        imprimir_info(f"Materias compartidas entre {est_a.obtener_nombre_completo()} y {est_b.obtener_nombre_completo()}:")
        if comun:
            for m in comun:
                print(f"  - {m}")
        else:
            print("  No comparten ninguna materia.")
    pausa()


def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS OFERTADAS (TOTALES)")
    mats = materias_ofertadas()
    if not mats:
        imprimir_info("No hay materias registradas todavía.")
    else:
        imprimir_info(f"Total de materias únicas: {len(mats)}")
        for m in mats:
            print(f"  - {m}")
    pausa()


def salir():
    imprimir_info("¡Hasta luego! 👋")
    return "salir"


OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Agregar nota", opcion_agregar_nota),
    "8": ("Ver promedio", opcion_ver_promedio),
    "9": ("Materias en común", opcion_materias_en_comun),
    "10": ("Materias ofertadas", opcion_materias_ofertadas),
    "0": ("Salir", salir),
}


def mostrar_menu():
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    for tecla, (texto, _funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main():
    while True:
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()

        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue

        _texto, funcion = OPCIONES[tecla]
        if funcion() == "salir":
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")