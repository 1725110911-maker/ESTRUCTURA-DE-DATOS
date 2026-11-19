import web
from models.models_hospital import SistemaTurnosHospital

render = web.template.render('views/', base='layout')

# Instancia en memoria para conservar los turnos mientras el servidor esté activo
hospital = SistemaTurnosHospital()


class Index:
    def GET(self, mensaje=None, tipo_mensaje="info"):
        datos = hospital.obtener_estado()
        return render.index(datos, mensaje, tipo_mensaje)

    def POST(self):
        formulario = web.input(
            accion="",
            nombre="",
            edad="0",
            motivo="",
            tipo_atencion="2",
            tiempo_estimado="15"
        )

        if formulario.accion == "registrar":
            nombre = formulario.nombre.strip()
            motivo = formulario.motivo.strip()

            try:
                edad = int(formulario.edad)
                tiempo = int(formulario.tiempo_estimado)
            except ValueError:
                return self.GET("Error: La edad y el tiempo deben ser números válidos.", "error")

            if not nombre or not motivo or edad < 0 or tiempo <= 0:
                return self.GET("Completa todos los campos con valores válidos.", "error")

            msg = hospital.registrar_paciente(
                nombre=nombre,
                edad=edad,
                motivo=motivo,
                tipo_atencion=formulario.tipo_atencion,
                tiempo_estimado=tiempo
            )
            return self.GET(msg, "success")

        elif formulario.accion == "atender":
            exito, msg = hospital.atender_paciente()
            tipo = "success" if exito else "warning"
            return self.GET(msg, tipo)

        return self.GET()