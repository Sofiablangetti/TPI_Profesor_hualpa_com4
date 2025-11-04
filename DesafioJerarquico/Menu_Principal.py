import os
from crud import agregar_item, modificar_item, eliminar_item, mostrar_todos
from estadisticas import mostrar_estadisticas

def mostrar_menu():
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Agregar nueva ciudad")
    print("2. Mostrar todas las ciudades")
    print("3. Modificar una ciudad")
    print("4. Eliminar una ciudad")
    print("5. Ver estadísticas generales")
    print("0. Salir")

def main():
    os.makedirs("datos", exist_ok=True)
    while True:
        mostrar_menu()
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            agregar_item()
        elif opcion == "2":
            mostrar_todos()
        elif opcion == "3":
            modificar_item()
        elif opcion == "4":
            eliminar_item()
        elif opcion == "5":
            mostrar_estadisticas()
        elif opcion == "0":
            print(" ¡Hasta luego!")
            break
        else:
            print(" Opción inválida.")

if __name__ == "__main__":
    main()
