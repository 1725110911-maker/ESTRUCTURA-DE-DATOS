from collections import deque
import time

class SistemaTurnosHospital:
    def __init__(self):
        # Filas FIFO usando deque
        self.fila_general = deque()
        self.fila_prioritaria = deque()
        self.contador_turno = 1
        
        # Estadísticas de atención
        self.total_atendidos = 0
        self.atendidos_prioritarios = 0
        self.atendidos_generales = 0
        self.tiempo_total_consulta = 0
        self.ultimo_atendido = None

    def registrar_paciente(self, nombre, edad, motivo, tipo_atencion, tiempo_estimado):
        """Registra un paciente en la fila correspondiente y retorna un mensaje de estado."""
        paciente = {
            'turno': self.contador_turno,
            'nombre': nombre,
            'edad': int(edad),
            'motivo': motivo,
            'tipo_atencion': tipo_atencion,
            'tiempo_estimado': int(tiempo_estimado),
            'hora_registro': time.time()
        }

        if tipo_atencion == '1':
            paciente['tipo_str'] = 'Prioritaria'
            self.fila_prioritaria.append(paciente)
            mensaje = f"Paciente {nombre} asignado a la FILA PRIORITARIA con el Turno #{paciente['turno']}."
        else:
            paciente['tipo_str'] = 'General'
            self.fila_general.append(paciente)
            mensaje = f"Paciente {nombre} asignado a la FILA GENERAL con el Turno #{paciente['turno']}."

        self.contador_turno += 1
        return mensaje

    def atender_paciente(self):
        """Atiende al siguiente paciente respetando prioridad sobre general (FIFO)."""
        paciente_actual = None

        if self.fila_prioritaria:
            paciente_actual = self.fila_prioritaria.popleft()
            self.atendidos_prioritarios += 1
        elif self.fila_general:
            paciente_actual = self.fila_general.popleft()
            self.atendidos_generales += 1

        if paciente_actual:
            tiempo_espera_min = int((time.time() - paciente_actual['hora_registro']) / 60)
            paciente_actual['tiempo_espera'] = tiempo_espera_min

            self.total_atendidos += 1
            self.tiempo_total_consulta += paciente_actual['tiempo_estimado']
            self.ultimo_atendido = paciente_actual

            return True, f"Atendiendo Turno #{paciente_actual['turno']} - {paciente_actual['nombre']} ({paciente_actual['tipo_str']})."

        return False, "No hay pacientes en espera en ninguna de las filas."

    def obtener_estado(self):
        """Prepara los datos actuales de las colas y estadísticas para la vista HTML."""
        ahora = time.time()

        lista_prioritaria = []
        for p in self.fila_prioritaria:
            copia = p.copy()
            copia['espera'] = int((ahora - p['hora_registro']) / 60)
            lista_prioritaria.append(copia)

        lista_general = []
        for p in self.fila_general:
            copia = p.copy()
            copia['espera'] = int((ahora - p['hora_registro']) / 60)
            lista_general.append(copia)

        promedio = 0.0
        if self.total_atendidos > 0:
            promedio = round(self.tiempo_total_consulta / self.total_atendidos, 1)

        return {
            'fila_prioritaria': lista_prioritaria,
            'fila_general': lista_general,
            'total_espera': len(lista_prioritaria) + len(lista_general),
            'total_atendidos': self.total_atendidos,
            'atendidos_prioritarios': self.atendidos_prioritarios,
            'atendidos_generales': self.atendidos_generales,
            'tiempo_total_consulta': self.tiempo_total_consulta,
            'promedio_consulta': promedio,
            'ultimo_atendido': self.ultimo_atendido
        }