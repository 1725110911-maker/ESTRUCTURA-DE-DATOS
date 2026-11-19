import web
from models.models_servicios import SistemaServiciosEscolares

render = web.template.render('views/', base='layout')
servicios = SistemaServiciosEscolares()


class Index:
    def GET(self, mensaje=None, tipo_mensaje="info"):
        datos = servicios.obtener_estado()
        return render.index(datos, mensaje, tipo_mensaje)

    def POST(self):
        formulario = web.input(
            accion="",
            matricula="",
            nombre="",
            tramite="",
            numero_turno=""
        )

        accion = formulario.accion

        if accion == "registrar":
            matricula = formulario.matricula.strip()
            nombre = formulario.nombre.strip()
            tramite = formulario.tramite.strip()

            if not matricula or not nombre or not tramite:
                return self.GET("Completa todos los campos para registrar al estudiante.", "error")

            msg = servicios.registrar_estudiante(matricula, nombre, tramite)
            return self.GET(msg, "success")

        elif accion == "atender":
            exito, msg = servicios.atender_siguiente()
            return self.GET(msg, "success" if exito else "warning")

        elif accion == "consultar":
            siguiente = servicios.consultar_siguiente()
            if siguiente:
                msg = (
                    f"Proximo en ser atendido: Turno #{siguiente['turno']} - "
                    f"{siguiente['nombre']} (Matricula: {siguiente['matricula']} | Tramite: {siguiente['tramite']})."
                )
                return self.GET(msg, "info")
            return self.GET("La fila se encuentra vacia.", "warning")

        elif accion == "cancelar":
            try:
                turno = int(formulario.numero_turno)
            except ValueError:
                return self.GET("Ingresa un numero de turno valido.", "error")

            exito, msg = servicios.cancelar_turno(turno)
            return self.GET(msg, "success" if exito else "warning")

        return self.GET()