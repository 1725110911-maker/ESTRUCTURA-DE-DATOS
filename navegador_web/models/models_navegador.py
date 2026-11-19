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
        return True, f"Visitando: {url}"

    def regresar_pagina(self):
        """Elimina (Pop) la última página visitada para regresar a la anterior."""
        if self.esta_vacio():
            return False, "No hay páginas anteriores en el historial."

        pagina_saliente = self.pila.pop()
        if not self.esta_vacio():
            return True, f"Regresando desde '{pagina_saliente}'. Página actual: {self.pila[-1]}"
        return True, f"Regresando desde '{pagina_saliente}'. Llegaste al inicio (historial vacío)."

    def eliminar_historial(self):
        """Vacía por completo la pila del historial."""
        if self.esta_vacio():
            return False, "El historial ya está vacío."
        self.pila.clear()
        return True, "Historial eliminado correctamente."

    def obtener_estado(self):
        """Prepara los datos de la pila LIFO para renderizar en HTML."""
        vacio = self.esta_vacio()
        pagina_actual = self.pila[-1] if not vacio else None

        # Recorremos la pila en orden inverso (desde el tope hacia la base)
        historial_ordenado = []
        for i, url in enumerate(reversed(self.pila), start=1):
            historial_ordenado.append({
                'posicion': i,
                'url': url,
                'es_actual': (i == 1)
            })

        return {
            'esta_vacio': vacio,
            'total': len(self.pila),
            'pagina_actual': pagina_actual,
            'historial': historial_ordenado
        }