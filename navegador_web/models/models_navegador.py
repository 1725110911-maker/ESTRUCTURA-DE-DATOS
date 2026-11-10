class HistorialNavegador:
    def __init__(self):
        # La pila se representa mediante una lista en Python (LIFO)
        self.pila = []

    def esta_vacio(self):
        """Verifica si la pila de páginas está vacía."""
        return len(self.pila) == 0

    def visitar_pagina(self, url):
        """Agrega (Push) una nueva página al tope de la pila."""
        self.pila.append(url)
        print(f"\n🌐 Visitando: {url}")

    def regresar_pagina(self):
        """Elimina (Pop) la última página visitada para regresar a la anterior."""
        if self.esta_vacio():
            print("\n⚠️ No hay páginas anteriores en el historial.")
        else:
            pagina_saliente = self.pila.pop()
            print(f"\n⬅️ Regresando desde: {pagina_saliente}")
            if not self.esta_vacio():
                print(f"📍 Página actual: {self.pila[-1]}")
            else:
                print("ℹ️ Llegaste al inicio (historial vacío).")

    def mostrar_pagina_actual(self):
        """Muestra el tope de la pila (Peek) sin desapilar nada."""
        if self.esta_vacio():
            print("\n⚠️ No estás navegando en ninguna página (historial vacío).")
        else:
            print(f"\n📍 Página actual: {self.pila[-1]}")

    def mostrar_historial(self):
        """Muestra el historial ordenado desde la página actual hacia las anteriores (LIFO)."""
        if self.esta_vacio():
            print("\n📜 El historial está vacío.")
        else:
            print("\n📜 --- HISTORIAL DE NAVEGACIÓN ---")
            # Recorremos la pila en orden inverso para mostrar primero el tope
            for i, url in enumerate(reversed(self.pila), start=1):
                estado = " (Página Actual)" if i == 1 else ""
                print(f"  {i}. {url}{estado}")

    def eliminar_historial(self):
        """Vacía por completo la pila del historial."""
        self.pila.clear()
        print("\n🧹 Historial eliminado correctamente.")


def menu():
    navegador = HistorialNavegador()
    
    while True:
        print("\n==========================================")
        print("   SISTEMA DE NAVEGACIÓN WEB (PILA LIFO)  ")
        print("==========================================")
        print("1. Visitar una página web")
        print("2. Regresar a la página anterior")
        print("3. Mostrar la página actual")
        print("4. Mostrar historial de páginas visitadas")
        print("5. Verificar si el historial está vacío")
        print("6. Eliminar historial")
        print("7. Salir del programa")
        print("==========================================")
        
        opcion = input("Selecciona una opción (1-7): ").strip()
        
        if opcion == "1":
            url = input("\nIngresa la dirección web (URL): ").strip()
            if url:
                navegador.visitar_pagina(url)
            else:
                print("⚠️ La dirección URL no puede estar vacía.")
                
        elif opcion == "2":
            navegador.regresar_pagina()
            
        elif opcion == "3":
            navegador.mostrar_pagina_actual()
            
        elif opcion == "4":
            navegador.mostrar_historial()
            
        elif opcion == "5":
            if navegador.esta_vacio():
                print("\nℹ️ El historial se encuentra VACÍO.")
            else:
                print(f"\nℹ️ El historial contiene {len(navegador.pila)} página(s) registrada(s).")
                
        elif opcion == "6":
            navegador.eliminar_historial()
            
        elif opcion == "7":
            print("\n👋 Saliendo del navegador web. ¡Hasta luego!")
            break
            
        else:
            print("\n❌ Opción no válida. Ingresa un número del 1 al 7.")

if __name__ == "__main__":
    menu()