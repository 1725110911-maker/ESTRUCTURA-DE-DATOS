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
        paciente = {
            'turno': self.contador_turno,
            'nombre': nombre,
            'edad': edad,
            'motivo': motivo,
            'tipo_atencion': tipo_atencion,
            'tiempo_estimado': tiempo_estimado,
            'hora_registro': time.time()
        }
        
        if tipo_atencion == '1':
            paciente['tipo_str'] = 'Prioritaria'
            self.fila_prioritaria.append(paciente)
            print(f"\n✅ Paciente asignado a la FILA PRIORITARIA con el Turno #{paciente['turno']}.")
        else:
            paciente['tipo_str'] = 'General'
            self.fila_general.append(paciente)
            print(f"\n✅ Paciente asignado a la FILA GENERAL con el Turno #{paciente['turno']}.")
            
        self.contador_turno += 1

    def atender_paciente(self):
        paciente_actual = None
        
        if self.fila_prioritaria:
            paciente_actual = self.fila_prioritaria.popleft()
            self.atendidos_prioritarios += 1
        elif self.fila_general:
            paciente_actual = self.fila_general.popleft()
            self.atendidos_generales += 1
            
        if paciente_actual:
            self.total_atendidos += 1
            self.tiempo_total_consulta += paciente_actual['tiempo_estimado']
            self.ultimo_atendido = paciente_actual
            
            tiempo_espera_min = int((time.time() - paciente_actual['hora_registro']) / 60)
            
            print("\n🩺 --- CONSULTA MÉDICA EN PROCESO ---")
            print(f"• Turno asignado: #{paciente_actual['turno']}")
            print(f"• Paciente: {paciente_actual['nombre']} ({paciente_actual['edad']} años)")
            print(f"• Tipo de atención: {paciente_actual['tipo_str']}")
            print(f"• Motivo de consulta: {paciente_actual['motivo']}")
            print(f"• Tiempo estimado de consulta: {paciente_actual['tiempo_estimado']} minutos")
            print(f"• Tiempo en sala de espera: {tiempo_espera_min} minutos")
            print("---------------------------------------")
        else:
            print("\n⚠️ No hay pacientes en espera en ninguna de las filas.")

    def mostrar_filas(self):
        print("\n📋 --- PACIENTES EN SALA DE ESPERA ---")
        print(f"\n🔴 FILA PRIORITARIA ({len(self.fila_prioritaria)} en espera):")
        if not self.fila_prioritaria:
            print("   (Fila vacía)")
        else:
            for p in self.fila_prioritaria:
                espera = int((time.time() - p['hora_registro']) / 60)
                print(f"   • Turno #{p['turno']} | {p['nombre']} ({p['edad']} años) - Motivo: {p['motivo']} | Est: {p['tiempo_estimado']} min | Espera: {espera} min")
                
        print(f"\n🔵 FILA GENERAL ({len(self.fila_general)} en espera):")
        if not self.fila_general:
            print("   (Fila vacía)")
        else:
            for p in self.fila_general:
                espera = int((time.time() - p['hora_registro']) / 60)
                print(f"   • Turno #{p['turno']} | {p['nombre']} ({p['edad']} años) - Motivo: {p['motivo']} | Est: {p['tiempo_estimado']} min | Espera: {espera} min")

    def mostrar_estadisticas(self):
        print("\n📊 --- ESTADÍSTICAS DE ATENCIÓN HOSPITALARIA ---")
        print(f"• Total de pacientes atendidos: {self.total_atendidos}")
        print(f"  - Atención Prioritaria: {self.atendidos_prioritarios}")
        print(f"  - Atención General: {self.atendidos_generales}")
        print(f"• Tiempo total acumulado en consultas: {self.tiempo_total_consulta} minutos")
        
        if self.total_atendidos > 0:
            promedio = self.tiempo_total_consulta / self.total_atendidos
            print(f"• Promedio por consulta: {promedio:.1f} minutos")
            print(f"• Último paciente atendido: Turno #{self.ultimo_atendido['turno']} ({self.ultimo_atendido['nombre']})")
        else:
            print("• Aún no se han completado consultas.")


def menu():
    hospital = SistemaTurnosHospital()
    
    while True:
        print("\n==========================================")
        print("   SISTEMA DE GESTIÓN DE TURNOS HOSPITAL  ")
        print("==========================================")
        print("1. Registrar nuevo paciente")
        print("2. Atender siguiente paciente")
        print("3. Ver pacientes en espera")
        print("4. Generar estadísticas de atención")
        print("5. Salir del programa")
        print("==========================================")
        
        opcion = input("Selecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            print("\n--- REGISTRO DE PACIENTE ---")
            nombre = input("Nombre del paciente: ").strip()
            
            while True:
                try:
                    edad = int(input("Edad: "))
                    if edad >= 0:
                        break
                    print("⚠️ La edad debe ser un número mayor o igual a 0.")
                except ValueError:
                    print("⚠️ Ingresa un número entero válido para la edad.")
                    
            motivo = input("Motivo de consulta: ").strip()
            
            print("\nTipo de atención (Clasificación de Urgencia):")
            print("  1. Atención Prioritaria (Urgencia leve, embarazo, adultos mayores, movilidad reducida)")
            print("  2. Atención General")
            while True:
                tipo = input("Selecciona opción (1 o 2): ").strip()
                if tipo in ['1', '2']:
                    break
                print("⚠️ Selección inválida. Elige 1 o 2.")
                
            while True:
                try:
                    tiempo = int(input("Tiempo estimado de consulta (en minutos): "))
                    if tiempo > 0:
                        break
                    print("⚠️ El tiempo debe ser mayor a 0.")
                except ValueError:
                    print("⚠️ Ingresa un entero válido para el tiempo estimado.")
                    
            hospital.registrar_paciente(nombre, edad, motivo, tipo, tiempo)
            
        elif opcion == "2":
            hospital.atender_paciente()
            
        elif opcion == "3":
            hospital.mostrar_filas()
            
        elif opcion == "4":
            hospital.mostrar_estadisticas()
            
        elif opcion == "5":
            print("\n👋 Cerrando sistema de atención médica. ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Ingresa un número del 1 al 5.")

if __name__ == "__main__":
    menu()