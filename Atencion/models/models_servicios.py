
from collections import deque
import time


class SistemaServiciosEscolares:
    def __init__(self):
        # Cola unica bajo principio FIFO (Primeras Entradas, Primeras Salidas)
        self.fila = deque()
        self.contador_turno = 1

        # Control de ventanilla y estadisticas
        self.en_ventanilla = None
        self.total_atendidos = 0
        self.total_cancelados = 0
        self.tiempo_espera_total = 0

    def registrar_estudiante(self, matricula, nombre, tramite):
        """Agrega al estudiante al final de la fila (Enqueue)."""
        estudiante = {
            'turno': self.contador_turno,
            'matricula': matricula,
            'nombre': nombre,
            'tramite': tramite,
            'hora_llegada': time.strftime("%H:%M:%S"),
            'timestamp': time.time()
        }

        self.fila.append(estudiante)
        mensaje = (
            f"Turno #{estudiante['turno']} asignado a {nombre} "
            f"(Matricula: {matricula}) para {tramite}."
        )
        self.contador_turno += 1
        return mensaje

    def atender_siguiente(self):
        """Atiende al primer estudiante que llego a la fila (Dequeue / FIFO)."""
        if not self.fila:
            return False, "No hay estudiantes en espera en la fila."

        estudiante = self.fila.popleft()
        espera_min = int((time.time() - estudiante['timestamp']) / 60)
        estudiante['tiempo_espera'] = espera_min

        self.en_ventanilla = estudiante
        self.total_atendidos += 1
        self.tiempo_espera_total += espera_min

        return True, (
            f"Atendiendo en ventanilla: Turno #{estudiante['turno']} - "
            f"{estudiante['nombre']} ({estudiante['tramite']})."
        )

    def consultar_siguiente(self):
        """Consulta quien sigue en la fila sin sacarlo (Peek)."""
        if self.fila:
            return self.fila[0]
        return None

    def cancelar_turno(self, numero_turno):
        """Elimina un turno de la fila si el estudiante se retira."""
        for estudiante in self.fila:
            if estudiante['turno'] == numero_turno:
                self.fila.remove(estudiante)
                self.total_cancelados += 1
                return True, f"Turno #{numero_turno} ({estudiante['nombre']}) eliminado de la fila."

        return False, f"No se encontro el Turno #{numero_turno} en la fila de espera."

    def obtener_estado(self):
        """Prepara los datos de la fila FIFO y estadisticas para la vista HTML."""
        ahora = time.time()
        lista_espera = []

        for posicion, est in enumerate(self.fila, start=1):
            copia = est.copy()
            copia['posicion'] = posicion
            copia['espera_actual'] = int((ahora - est['timestamp']) / 60)
            lista_espera.append(copia)

        promedio_espera = 0.0
        if self.total_atendidos > 0:
            promedio_espera = round(self.tiempo_espera_total / self.total_atendidos, 1)

        return {
            'fila': lista_espera,
            'total_pendientes': len(lista_espera),
            'en_ventanilla': self.en_ventanilla,
            'siguiente': self.consultar_siguiente(),
            'total_atendidos': self.total_atendidos,
            'total_cancelados': self.total_cancelados,
            'promedio_espera': promedio_espera
        }