from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import EstudianteController, MateriaController, MatriculaController
from models import Materia

estudiantes = EstudianteController()
materias = MateriaController()
matriculas = MatriculaController(estudiantes, materias)


def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def pedir_float(etiqueta):
    try:
        return float(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    if not objetos:
        imprimir_info(vacio)
        return
    for objeto in objetos:
        print(f"  {objeto}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


# =====================================================================
# MENÚ DE ESTUDIANTES
# =====================================================================

def crear_estudiante():
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "carnet": input("Carnet (ej. EST2026001): "),
        "carrera": input("Carrera: "),
        "telefono": input("Teléfono (opcional): "),
    }
    mostrar_resultado(*estudiantes.crear(datos))
    pausa()


def listar_estudiantes():
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(estudiantes.leer(), "Todavía no hay estudiantes.")
    pausa()


def buscar_estudiante():
    imprimir_titulo("BUSCAR ESTUDIANTE (Lineal)")
    termino = input("Nombre, apellido, email, carnet o carrera: ")
    encontrados = estudiantes.buscar(termino)
    mostrar_lista(encontrados, f"Ningún estudiante coincide con '{termino}'.")
    pausa()


def buscar_estudiante_binario():
    imprimir_titulo("BÚSQUEDA BINARIA DE ESTUDIANTE")
    id_buscado = pedir_entero("Ingrese el ID exacto a buscar: ")
    if id_buscado is None:
        imprimir_error("ID no válido")
        return pausa()
    est = estudiantes.buscar_binario_por_id(id_buscado)
    if est:
        imprimir_exito("¡Encontrado mediante búsqueda binaria!")
        mostrar_detalle(est)
    else:
        imprimir_error("No se encontró ningún estudiante con ese ID.")
    pausa()


def ordenar_estudiantes_asc():
    estudiantes.ordenar_ascendente()
    imprimir_exito("Estudiantes ordenados de forma ascendente (A-Z).")
    listar_estudiantes()


def ordenar_estudiantes_desc():
    estudiantes.ordenar_descendente()
    imprimir_exito("Estudiantes ordenados de forma descendente (Z-A).")
    listar_estudiantes()


def reversar_estudiantes():
    estudiantes.reversar_lista()
    imprimir_exito("Lista de estudiantes invertida (reversada).")
    listar_estudiantes()


def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    est = estudiantes.obtener(pedir_entero("Id: "))
    if est is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(est)
    pausa()


def actualizar_estudiante():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_est = pedir_entero("Id: ")
    est = estudiantes.obtener(id_est)
    if est is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {est.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "apellido", "email", "carnet", "carrera", "telefono"):
        actual = getattr(est, campo, "")
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*estudiantes.actualizar(id_est, cambios))
    pausa()


def eliminar_estudiante():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_est = pedir_entero("Id: ")
    est = estudiantes.obtener(id_est)
    if est is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminará: {est.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*estudiantes.eliminar(id_est))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE MATERIAS
# =====================================================================

def crear_materia():
    imprimir_titulo("CREAR MATERIA")
    datos = {
        "nombre": input("Nombre: "),
        "codigo": input("Código (ej. MAT101): "),
        "creditos": input("Créditos (1-10): "),
        "cupos": input(f"Cupos (máx {Materia.CUPOS_MAXIMOS}): "),
    }
    mostrar_resultado(*materias.crear(datos))
    pausa()


def listar_materias():
    imprimir_titulo("MATERIAS")
    mostrar_lista(materias.leer(), "Todavía no hay materias.")
    pausa()


def buscar_materia():
    imprimir_titulo("BUSCAR MATERIA")
    termino = input("Nombre o código: ")
    mostrar_lista(materias.buscar(termino), "Sin coincidencias.")
    pausa()


def buscar_materia_binario():
    imprimir_titulo("BÚSQUEDA BINARIA DE MATERIA")
    id_buscado = pedir_entero("Ingrese el ID exacto a buscar: ")
    if id_buscado is None:
        imprimir_error("ID no válido")
        return pausa()
    mat = materias.buscar_binario_por_id(id_buscado)
    if mat:
        imprimir_exito("¡Encontrada mediante búsqueda binaria!")
        mostrar_detalle(mat)
    else:
        imprimir_error("No se encontró ninguna materia con ese ID.")
    pausa()


def ordenar_materias_asc():
    materias.ordenar_ascendente()
    imprimir_exito("Materias ordenadas de forma ascendente (A-Z).")
    listar_materias()


def ordenar_materias_desc():
    materias.ordenar_descendente()
    imprimir_exito("Materias ordenadas de forma descendente (Z-A).")
    listar_materias()


def reversar_materias():
    materias.reversar_lista()
    imprimir_exito("Lista de materias invertida (reversada).")
    listar_materias()


def ver_materia():
    imprimir_titulo("VER MATERIA POR ID")
    mat = materias.obtener(pedir_entero("Id: "))
    if mat is None:
        imprimir_error("No encontrada")
    else:
        mostrar_detalle(mat)
    pausa()


def actualizar_materia():
    imprimir_titulo("ACTUALIZAR MATERIA")
    id_mat = pedir_entero("Id: ")
    mat = materias.obtener(id_mat)
    if mat is None:
        imprimir_error("No encontrada")
        return pausa()

    imprimir_info(f"Editando: {mat.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "codigo", "creditos", "cupos"):
        actual = getattr(mat, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*materias.actualizar(id_mat, cambios))
    pausa()


def eliminar_materia():
    imprimir_titulo("ELIMINAR MATERIA")
    id_mat = pedir_entero("Id: ")
    mat = materias.obtener(id_mat)
    if mat is None:
        imprimir_error("No encontrada")
        return pausa()

    imprimir_info(f"Se eliminará: {mat.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*materias.eliminar(id_mat))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE MATRÍCULAS
# =====================================================================

def registrar_matricula():
    imprimir_titulo("REGISTRAR MATRÍCULA")
    imprimir_info("Estudiantes:")
    mostrar_lista(estudiantes.leer())
    imprimir_info("\nMaterias:")
    mostrar_lista(materias.leer())

    datos = {
        "estudiante_id": pedir_entero("\nId del estudiante: "),
        "materia_id": pedir_entero("Id de la materia: "),
        "periodo": input("Periodo académico (ej. 2026-1): "),
    }
    if None in (datos["estudiante_id"], datos["materia_id"]):
        imprimir_error("Los IDs deben ser números enteros")
        return pausa()

    mostrar_resultado(*matriculas.crear(datos))
    pausa()


def listar_matriculas():
    imprimir_titulo("MATRÍCULAS")
    mostrar_lista(matriculas.leer(), "Todavía no hay matrículas.")
    pausa()


def buscar_matricula_binario():
    imprimir_titulo("BÚSQUEDA BINARIA DE MATRÍCULA")
    id_buscado = pedir_entero("Ingrese el ID exacto de la matrícula: ")
    if id_buscado is None:
        imprimir_error("ID no válido")
        return pausa()
    mat = matriculas.buscar_binario_por_id(id_buscado)
    if mat:
        imprimir_exito("¡Encontrada mediante búsqueda binaria!")
        mostrar_detalle(mat)
    else:
        imprimir_error("No se encontró ninguna matrícula con ese ID.")
    pausa()


def ordenar_matriculas_asc():
    matriculas.ordenar_ascendente()
    imprimir_exito("Matrículas ordenadas ascendentemente por periodo.")
    listar_matriculas()


def ordenar_matriculas_desc():
    matriculas.ordenar_descendente()
    imprimir_exito("Matrículas ordenadas descendentemente por periodo.")
    listar_matriculas()


def reversar_matriculas():
    matriculas.reversar_lista()
    imprimir_exito("Lista de matrículas invertida (reversada).")
    listar_matriculas()


def registrar_nota_matricula():
    imprimir_titulo("REGISTRAR NOTA")
    mostrar_lista(matriculas.leer())
    id_mat = pedir_entero("\nId de la matrícula: ")
    if id_mat is None:
        imprimir_error("ID inválido")
        return pausa()

    nota = pedir_float(f"Nota (0 a 20, aprobación >= {Materia.NOTA_APROBACION}): ")
    if nota is None:
        imprimir_error("Nota inválida")
        return pausa()

    mostrar_resultado(*matriculas.registrar_nota(id_mat, nota))
    pausa()


def ver_certificado():
    imprimir_titulo("CERTIFICADO")
    texto = matriculas.certificado(pedir_entero("Id de la matrícula: "))
    if texto is None:
        imprimir_error("No existe esa matrícula")
    else:
        print(texto)
    pausa()


def retirar_matricula():
    imprimir_titulo("RETIRAR MATRÍCULA")
    id_mat = pedir_entero("Id de la matrícula: ")
    if id_mat and confirmar("Se devolverá el cupo a la materia. ¿Confirma?"):
        mostrar_resultado(*matriculas.retirar_matricula(id_mat))
    else:
        imprimir_info("Operación cancelada")
    pausa()


def resumen():
    imprimir_titulo("RESUMEN INSTITUCIONAL")
    print(f"  Estudiantes         : {len(estudiantes.leer())}")
    print(f"  Carreras distintas  : {', '.join(estudiantes.carreras()) or '-'}")
    sin_cupo = materias.materias_sin_cupo()
    print(f"  Materias sin cupo   : {', '.join(m.nombre for m in sin_cupo) or 'ninguna'}")
    aprobadas = sum(1 for mat in matriculas.leer() if mat.esta_aprobada())
    print(f"  Matrículas aprobadas: {aprobadas}")
    pausa()


# =====================================================================
# DICCIONARIOS DE MENÚS 
# =====================================================================

MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante),
    "4": ("Búsqueda binaria por ID", buscar_estudiante_binario),
    "5": ("Ordenar Ascendente (A-Z)", ordenar_estudiantes_asc),
    "6": ("Ordenar Descendente (Z-A)", ordenar_estudiantes_desc),
    "7": ("Reversar lista", reversar_estudiantes),
    "8": ("Ver por id", ver_estudiante),
    "9": ("Actualizar", actualizar_estudiante),
    "10": ("Eliminar", eliminar_estudiante),
    "0": ("Volver", None),
}

MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia),
    "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia),
    "4": ("Búsqueda binaria por ID", buscar_materia_binario),
    "5": ("Ordenar Ascendente (A-Z)", ordenar_materias_asc),
    "6": ("Ordenar Descendente (Z-A)", ordenar_materias_desc),
    "7": ("Reversar lista", reversar_materias),
    "8": ("Ver por id", ver_materia),
    "9": ("Actualizar", actualizar_materia),
    "10": ("Eliminar", eliminar_materia),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Matricular", registrar_matricula),
    "2": ("Ver todas", listar_matriculas),
    "3": ("Búsqueda binaria por ID", buscar_matricula_binario),
    "4": ("Ordenar Ascendente (Periodo)", ordenar_matriculas_asc),
    "5": ("Ordenar Descendente (Periodo)", ordenar_matriculas_desc),
    "6": ("Reversar lista", reversar_matriculas),
    "7": ("Registrar nota", registrar_nota_matricula),
    "8": ("Ver certificado", ver_certificado),
    "9": ("Retirar matrícula", retirar_matricula),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _funcion) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()

        tecla = input("Opción: ").strip()
        if tecla not in opciones:
            imprimir_error("Opción no válida")
            pausa()
            continue

        _texto, funcion = opciones[tecla]
        if funcion is None:
            break
        funcion()


def main():
    while True:
        imprimir_titulo("SISTEMA ACADÉMICO - UNIDAD EDUCATIVA")
        print("  1. Estudiantes")
        print("  2. Materias")
        print("  3. Matrículas")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1":
            ejecutar_menu("ESTUDIANTES", MENU_ESTUDIANTES)
        elif tecla == "2":
            ejecutar_menu("MATERIAS", MENU_MATERIAS)
        elif tecla == "3":
            ejecutar_menu("MATRÍCULAS", MENU_MATRICULAS)
        elif tecla == "4":
            resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opción no válida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")