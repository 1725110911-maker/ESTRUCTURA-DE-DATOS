import web
from models.models_navegador import HistorialNavegador

render = web.template.render('views/', base='layout')

# Instancia
navegador = HistorialNavegador()


class Index:
    def GET(self, mensaje=None, tipo_mensaje="info"):
        datos = navegador.obtener_estado()
        return render.index(datos, mensaje, tipo_mensaje)

    def POST(self):
        formulario = web.input(accion="", url="")
        accion = formulario.accion

        if accion == "visitar":
            url = formulario.url.strip()
            if not url:
                return self.GET("La dirección URL no puede estar vacía.", "error")
            _, msg = navegador.visitar_pagina(url)
            return self.GET(msg, "success")

        elif accion == "regresar":
            exito, msg = navegador.regresar_pagina()
            return self.GET(msg, "success" if exito else "warning")

        elif accion == "verificar":
            if navegador.esta_vacio():
                return self.GET("Estado de la pila: El historial se encuentra VACÍO.", "warning")
            total = len(navegador.pila)
            return self.GET(f"Estado de la pila: El historial contiene {total} página(s) registrada(s).", "info")

        elif accion == "eliminar":
            exito, msg = navegador.eliminar_historial()
            return self.GET(msg, "success" if exito else "warning")

        return self.GET()