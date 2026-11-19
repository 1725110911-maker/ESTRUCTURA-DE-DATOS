from collections import deque
import time


class SistemaCafeteria:
    def __init__(self):
        self.fila_prioritarios = deque()
        self.fila_normales = deque()
        self.contador_pedido = 1

        self.total_preparados = 0
        self.preparados_prioritarios = 0
        self.preparados_normales = 0
        self.total_cancelados = 0
        self.unidades_preparadas = 0
        self.tiempo_total_preparacion = 0
        self.ultimo_preparado = None

    def registrar_pedido(self, nombre_cliente, producto, cantidad, tipo_pedido, tiempo_preparacion):
        """1. Registra un pedido y lo incorpora a la fila correspondiente."""
        pedido = {
            'numero_pedido': self.contador_pedido,
            'nombre_cliente': nombre_cliente,
            'producto': producto,
            'cantidad': int(cantidad),
            'tipo_pedido': tipo_pedido,
            'tiempo_preparacion': int(tiempo_preparacion),
            'hora_registro': time.time()
        }

        if tipo_pedido == '1':
            pedido['tipo_str'] = 'Prioritario'
            self.fila_prioritarios.append(pedido)
            mensaje = (
                f"Pedido #{pedido['numero_pedido']} ({nombre_cliente} - {cantidad}x {producto}) "
                f"agregado a la FILA PRIORITARIA."
            )
        else:
            pedido['tipo_str'] = 'Normal'
            self.fila_normales.append(pedido)
            mensaje = (
                f"Pedido #{pedido['numero_pedido']} ({nombre_cliente} - {cantidad}x {producto}) "
                f"agregado a la FILA NORMAL."
            )

        self.contador_pedido += 1
        return mensaje

    def preparar_siguiente(self):
        """2. Prepara el siguiente pedido dando prioridad a la fila prioritaria (FIFO)."""
        pedido_actual = None

        if self.fila_prioritarios:
            pedido_actual = self.fila_prioritarios.popleft()
            self.preparados_prioritarios += 1
        elif self.fila_normales:
            pedido_actual = self.fila_normales.popleft()
            self.preparados_normales += 1

        if pedido_actual:
            espera_min = int((time.time() - pedido_actual['hora_registro']) / 60)
            pedido_actual['tiempo_espera'] = espera_min

            self.total_preparados += 1
            self.unidades_preparadas += pedido_actual['cantidad']
            self.tiempo_total_preparacion += pedido_actual['tiempo_preparacion']
            self.ultimo_preparado = pedido_actual

            return True, (
                f"Preparando Pedido #{pedido_actual['numero_pedido']} - "
                f"{pedido_actual['cantidad']}x {pedido_actual['producto']} "
                f"para {pedido_actual['nombre_cliente']} ({pedido_actual['tipo_str']})."
            )

        return False, "No hay pedidos pendientes en ninguna de las filas."

    def consultar_siguiente(self):
        """3. Consulta el proximo pedido a preparar sin sacarlo de la fila (Peek)."""
        if self.fila_prioritarios:
            return self.fila_prioritarios[0]
        if self.fila_normales:
            return self.fila_normales[0]
        return None

    def cancelar_pedido(self, numero_pedido):
        """6. Busca y elimina un pedido pendiente por su numero de pedido."""
        for pedido in self.fila_prioritarios:
            if pedido['numero_pedido'] == numero_pedido:
                self.fila_prioritarios.remove(pedido)
                self.total_cancelados += 1
                return True, f"Pedido Prioritario #{numero_pedido} ({pedido['nombre_cliente']}) cancelado correctamente."

        for pedido in self.fila_normales:
            if pedido['numero_pedido'] == numero_pedido:
                self.fila_normales.remove(pedido)
                self.total_cancelados += 1
                return True, f"Pedido Normal #{numero_pedido} ({pedido['nombre_cliente']}) cancelado correctamente."

        return False, f"No se encontro ningun pedido pendiente con el numero #{numero_pedido}."

    def obtener_estado(self):
        """4 y 5. Prepara los pedidos pendientes y las estadisticas para la vista HTML."""
        ahora = time.time()

        pendientes_prioritarios = []
        for p in self.fila_prioritarios:
            copia = p.copy()
            copia['espera'] = int((ahora - p['hora_registro']) / 60)
            pendientes_prioritarios.append(copia)

        pendientes_normales = []
        for p in self.fila_normales:
            copia = p.copy()
            copia['espera'] = int((ahora - p['hora_registro']) / 60)
            pendientes_normales.append(copia)

        promedio = 0.0
        if self.total_preparados > 0:
            promedio = round(self.tiempo_total_preparacion / self.total_preparados, 1)

        return {
            'fila_prioritarios': pendientes_prioritarios,
            'fila_normales': pendientes_normales,
            'total_pendientes': len(pendientes_prioritarios) + len(pendientes_normales),
            'siguiente_pedido': self.consultar_siguiente(),
            'ultimo_preparado': self.ultimo_preparado,
            'total_preparados': self.total_preparados,
            'preparados_prioritarios': self.preparados_prioritarios,
            'preparados_normales': self.preparados_normales,
            'total_cancelados': self.total_cancelados,
            'unidades_preparadas': self.unidades_preparadas,
            'tiempo_total_preparacion': self.tiempo_total_preparacion,
            'promedio_preparacion': promedio
        }