import web
from models.models_cafeteria import SistemaCafeteria

render = web.template.render('views/', base='layout')
cafeteria = SistemaCafeteria()


class Index:
    def GET(self, mensaje=None, tipo_mensaje="info"):
        datos = cafeteria.obtener_estado()
        return render.index(datos, mensaje, tipo_mensaje)

    def POST(self):
        formulario = web.input(
            accion="",
            nombre_cliente="",
            producto="",
            cantidad="1",
            tipo_pedido="2",
            tiempo_preparacion="5",
            numero_pedido=""
        )

        accion = formulario.accion

        if accion == "registrar":
            cliente = formulario.nombre_cliente.strip()
            producto = formulario.producto.strip()

            try:
                cantidad = int(formulario.cantidad)
                tiempo = int(formulario.tiempo_preparacion)
            except ValueError:
                return self.GET("Error: La cantidad y el tiempo deben ser numeros enteros.", "error")

            if not cliente or not producto or cantidad <= 0 or tiempo <= 0:
                return self.GET("Completa todos los campos con valores validos mayores a cero.", "error")

            msg = cafeteria.registrar_pedido(
                nombre_cliente=cliente,
                producto=producto,
                cantidad=cantidad,
                tipo_pedido=formulario.tipo_pedido,
                tiempo_preparacion=tiempo
            )
            return self.GET(msg, "success")

        elif accion == "preparar":
            exito, msg = cafeteria.preparar_siguiente()
            return self.GET(msg, "success" if exito else "warning")

        elif accion == "consultar_siguiente":
            siguiente = cafeteria.consultar_siguiente()
            if siguiente:
                msg = (
                    f"Siguiente en turno: Pedido #{siguiente['numero_pedido']} - "
                    f"{siguiente['cantidad']}x {siguiente['producto']} "
                    f"({siguiente['nombre_cliente']} | {siguiente['tipo_str']} | Est: {siguiente['tiempo_preparacion']} min)."
                )
                return self.GET(msg, "info")
            return self.GET("No hay pedidos pendientes por consultar.", "warning")

        elif accion == "cancelar":
            try:
                num_pedido = int(formulario.numero_pedido)
            except ValueError:
                return self.GET("Ingresa un numero de pedido valido para cancelar.", "error")

            exito, msg = cafeteria.cancelar_pedido(num_pedido)
            return self.GET(msg, "success" if exito else "warning")

        return self.GET()