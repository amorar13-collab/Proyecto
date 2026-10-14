from views import EstudianteController, MateriaController, MatriculaController
from models import Materia  # <-- Añade esta línea
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, 
    imprimir_info, confirmar, limpiar_pantalla
)
import datetime


def mostrar_lista(elementos):
    if not elementos:
        imprimir_info("No hay registros para mostrar.")
        return
    for item in elementos:
        print(f" - {item.etiqueta()}")
    print()


def mostrar_detalle(item):
    if not item:
        imprimir_error("Elemento no encontrado.")
        return
    print("-" * 40)
    print(f" Detalle: {item.etiqueta()}")
    print("-" * 40)


def menu_estudiantes(ctrl):
    while True:
        imprimir_titulo("GESTIÓN DE ESTUDIANTES")
        print("1. Crear estudiante")
        print("2. Ver todos los estudiantes")
        print("3. Buscar estudiante")
        print("4. Ver estudiante por ID")
        print("5. Actualizar estudiante")
        print("6. Eliminar estudiante")
        print("0. Volver al menú principal")
        
        opcion = input("\nElige una opción: ").strip()
        
        if opcion == "1":
            imprimir_titulo("CREAR ESTUDIANTE")
            datos = {
                "nombre": input("Nombre: "),
                "apellido": input("Apellido: "),
                "email": input("Email: "),
                "carnet": input("Carnet (ej. EST2026001): "),
                "carrera": input("Carrera: ")
            }
            exito, mensaje = ctrl.crear(datos)
            imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "2":
            imprimir_titulo("LISTA DE ESTUDIANTES")
            mostrar_lista(ctrl.leer())
            input("Presiona Enter para continuar...")
            
        elif opcion == "3":
            imprimir_titulo("BUSCAR ESTUDIANTE")
            texto = input("Texto a buscar (nombre, carnet, etc.): ")
            resultados = ctrl.buscar(texto)
            imprimir_info(f"Se encontraron {len(resultados)} resultados:")
            mostrar_lista(resultados)
            input("Presiona Enter para continuar...")
            
        elif opcion == "4":
            imprimir_titulo("VER ESTUDIANTE POR ID")
            try:
                id_reg = int(input("ID del estudiante: "))
                mostrar_detalle(ctrl.obtener(id_reg))
            except ValueError:
                imprimir_error("ID inválido.")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "5":
            imprimir_titulo("ACTUALIZAR ESTUDIANTE")
            try:
                id_reg = int(input("ID del estudiante a actualizar: "))
                est = ctrl.obtener(id_reg)
                if not est:
                    imprimir_error("Estudiante no encontrado.")
                else:
                    print(f"Actualizando a: {est.etiqueta()}")
                    print("Deje en blanco el campo si no desea cambiarlo.")
                    datos = {}
                    for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
                        val = input(f"Nuevo {campo} [{getattr(est, campo)}]: ").strip()
                        if val:
                            datos[campo] = val
                    exito, mensaje = ctrl.actualizar(id_reg, datos)
                    imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
            except ValueError:
                imprimir_error("ID inválido.")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "6":
            imprimir_titulo("ELIMINAR ESTUDIANTE")
            try:
                id_reg = int(input("ID del estudiante a eliminar: "))
                if confirmar("¿Está seguro de eliminar este estudiante?"):
                    exito, mensaje = ctrl.eliminar(id_reg)
                    imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
            except ValueError:
                imprimir_error("ID inválido.")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "0":
            break
        else:
            imprimir_error("Opción inválida.")
            input("Presiona Enter para continuar...")


def menu_materias(ctrl):
    while True:
        imprimir_titulo("GESTIÓN DE MATERIAS")
        print("1. Crear materia")
        print("2. Ver todas las materias")
        print("3. Buscar materia")
        print("4. Ver materia por ID")
        print("5. Actualizar materia")
        print("6. Eliminar materia")
        print("0. Volver al menú principal")
        
        opcion = input("\nElige una opción: ").strip()
        
        if opcion == "1":
            imprimir_titulo("CREAR MATERIA")
            datos = {
                "nombre": input("Nombre de la materia: "),
                "codigo": input("Código (ej. MAT101): "),
                "creditos": input("Créditos (1-10): "),
                "cupos": input(f"Cupos (máximo {Materia.CUPOS_MAXIMOS}): ")
            }
            exito, mensaje = ctrl.crear(datos)
            imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "2":
            imprimir_titulo("LISTA DE MATERIAS")
            mostrar_lista(ctrl.leer())
            input("Presiona Enter para continuar...")
            
        elif opcion == "3":
            imprimir_titulo("BUSCAR MATERIA")
            texto = input("Texto a buscar: ")
            resultados = ctrl.buscar(texto)
            imprimir_info(f"Se encontraron {len(resultados)} resultados:")
            mostrar_lista(resultados)
            input("Presiona Enter para continuar...")
            
        elif opcion == "4":
            imprimir_titulo("VER MATERIA POR ID")
            try:
                id_reg = int(input("ID de la materia: "))
                mostrar_detalle(ctrl.obtener(id_reg))
            except ValueError:
                imprimir_error("ID inválido.")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "5":
            imprimir_titulo("ACTUALIZAR MATERIA")
            try:
                id_reg = int(input("ID de la materia a actualizar: "))
                mat = ctrl.obtener(id_reg)
                if not mat:
                    imprimir_error("Materia no encontrada.")
                else:
                    print(f"Actualizando a: {mat.etiqueta()}")
                    datos = {}
                    for campo in ("nombre", "codigo", "creditos", "cupos"):
                        val = input(f"Nuevo {campo} [{getattr(mat, campo)}]: ").strip()
                        if val:
                            datos[campo] = val
                    exito, mensaje = ctrl.actualizar(id_reg, datos)
                    imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
            except ValueError:
                imprimir_error("ID inválido.")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "6":
            imprimir_titulo("ELIMINAR MATERIA")
            try:
                id_reg = int(input("ID de la materia a eliminar: "))
                if confirmar("¿Está seguro de eliminar esta materia?"):
                    exito, mensaje = ctrl.eliminar(id_reg)
                    imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
            except ValueError:
                imprimir_error("ID inválido.")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "0":
            break
        else:
            imprimir_error("Opción inválida.")
            input("Presiona Enter para continuar...")


def menu_matriculas(ctrl):
    while True:
        imprimir_titulo("GESTIÓN DE MATRÍCULAS")
        print("1. Matricular estudiante")
        print("2. Ver todas las matrículas")
        print("3. Registrar nota")
        print("4. Ver certificado")
        print("5. Retirar matrícula")
        print("0. Volver al menú principal")
        
        opcion = input("\nElige una opción: ").strip()
        
        if opcion == "1":
            imprimir_titulo("NUEVA MATRÍCULA")
            datos = {
                "estudiante_id": input("ID del Estudiante: "),
                "materia_id": input("ID de la Materia: "),
                "periodo": input("Periodo académico (ej. 2026-1): "),
                "nota": input("Nota inicial (opcional, por defecto 0): ") or "0.0",
                "fecha": datetime.date.today().strftime("%Y-%m-%d")
            }
            exito, mensaje = ctrl.crear(datos)
            imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "2":
            imprimir_titulo("LISTA DE MATRÍCULAS")
            mostrar_lista(ctrl.leer())
            input("Presiona Enter para continuar...")
            
        elif opcion == "3":
            imprimir_titulo("REGISTRAR NOTA")
            try:
                id_reg = int(input("ID de la matrícula: "))
                nota_val = float(input("Ingrese la nota (0 a 20): "))
                exito, mensaje = ctrl.registrar_nota(id_reg, nota_val)
                imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
            except ValueError:
                imprimir_error("Datos numéricos inválidos.")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "4":
            imprimir_titulo("CERTIFICADO DE MATRÍCULA")
            try:
                id_reg = int(input("ID de la matrícula: "))
                cert = ctrl.certificado(id_reg)
                if cert:
                    print(cert)
                else:
                    imprimir_error("Matrícula no encontrada.")
            except ValueError:
                imprimir_error("ID inválido.")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "5":
            imprimir_titulo("RETIRAR MATRÍCULA")
            try:
                id_reg = int(input("ID de la matrícula a retirar: "))
                if confirmar("¿Está seguro de retirar esta matrícula?"):
                    exito, mensaje = ctrl.retirar_matricula(id_reg)
                    imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
            except ValueError:
                imprimir_error("ID inválido.")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "0":
            break
        else:
            imprimir_error("Opción inválida.")
            input("Presiona Enter para continuar...")


def mostrar_resumen(estudiantes_ctrl, materias_ctrl, matriculas_ctrl):
    imprimir_titulo("RESUMEN DEL SISTEMA ACADÉMICO")
    
    total_estudiantes = len(estudiantes_ctrl.leer())
    # Conjunto ordenado de carreras distintas
    carreras = sorted({e.carrera for e in estudiantes_ctrl.leer() if e.carrera})
    materias_agotadas = len(materias_ctrl.materias_sin_cupo())
    aprobadas = sum(1 for m in matriculas_ctrl.leer() if m.esta_aprobada())
    
    print(f"• Total de estudiantes registrados : {total_estudiantes}")
    print(f"• Carreras distintas               : {', '.join(carreras) if carreras else 'Ninguna'}")
    print(f"• Materias sin cupo disponible     : {materias_agotadas}")
    print(f"• Matrículas aprobadas             : {aprobadas}")
    print()


def main():
    estudiantes_ctrl = EstudianteController()
    materias_ctrl = MateriaController()
    matriculas_ctrl = MatriculaController(estudiantes_ctrl, materias_ctrl)
    
    while True:
        imprimir_titulo("SISTEMA ACADÉMICO UNIDAD EDUCATIVA")
        print("1. Estudiantes")
        print("2. Materias")
        print("3. Matrículas")
        print("4. Resumen del sistema")
        print("0. Salir")
        
        opcion = input("\nElige una opción: ").strip()
        
        if opcion == "1":
            menu_estudiantes(estudiantes_ctrl)
        elif opcion == "2":
            menu_materias(materias_ctrl)
        elif opcion == "3":
            menu_matriculas(matriculas_ctrl)
        elif opcion == "4":
            mostrar_resumen(estudiantes_ctrl, materias_ctrl, matriculas_ctrl)
            input("Presiona Enter para continuar...")
        elif opcion == "0":
            imprimir_info("¡Hasta luego!")
            break
        else:
            imprimir_error("Opción inválida. Intente de nuevo.")
            input("Presiona Enter para continuar...")


if __name__ == "__main__":
    main()