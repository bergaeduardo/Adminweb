"""
Comando de gestión para marcar automáticamente turnos RESERVADOS como NO CONFIRMADO
cuando no se confirman 30 minutos antes de la hora programada
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from consultasTango.models import TurnoReserva, EstadoTurno, HistorialEstadoTurno


class Command(BaseCommand):
    help = 'Marca turnos RESERVADOS como NO CONFIRMADO si no se confirmaron 30 min antes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular sin realizar cambios en la base de datos',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('Modo simulación - No se realizarán cambios'))
        
        try:
            # Obtener estados
            estado_reservado = EstadoTurno.objects.get(nombre='RESERVADO')
            estado_no_confirmado = EstadoTurno.objects.get(nombre='NO CONFIRMADO')
            
            # Calcular tiempo límite (30 minutos atrás desde ahora)
            ahora = timezone.now()
            limite_confirmacion = ahora - timedelta(minutes=30)
            
            # Buscar turnos RESERVADOS cuyo horario de inicio ya pasó el límite de 30 min
            turnos_a_marcar = TurnoReserva.objects.filter(
                estado=estado_reservado
            )
            
            turnos_actualizados = 0
            
            for turno in turnos_a_marcar:
                # Combinar fecha y hora del turno
                turno_datetime = timezone.make_aware(
                    datetime.combine(turno.fecha, turno.hora_inicio)
                )
                
                # Si el turno es en menos de 30 minutos (o ya pasó)
                if turno_datetime <= limite_confirmacion:
                    self.stdout.write(
                        f'Marcando turno {turno.id_turno_reserva} '
                        f'({turno.codigo_proveedor} - {turno.fecha} {turno.hora_inicio}) '
                        f'como NO CONFIRMADO'
                    )
                    
                    if not dry_run:
                        # Guardar estado anterior
                        estado_anterior = turno.estado
                        
                        # Cambiar estado
                        turno.estado = estado_no_confirmado
                        turno.estado_actual_desde = ahora
                        turno.save()
                        
                        # Registrar en historial
                        HistorialEstadoTurno.objects.create(
                            turno=turno,
                            estado_anterior=estado_anterior,
                            estado_nuevo=estado_no_confirmado,
                            usuario_cambio='SISTEMA',
                            observaciones='Cambio automático: turno no confirmado 30 min antes del horario'
                        )
                        
                    turnos_actualizados += 1
            
            if turnos_actualizados > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ {turnos_actualizados} turno(s) marcado(s) como NO CONFIRMADO'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('✓ No hay turnos para marcar como NO CONFIRMADO')
                )
                
        except EstadoTurno.DoesNotExist as e:
            self.stdout.write(
                self.style.ERROR(
                    f'✗ Error: No se encontró el estado requerido - {e}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error inesperado: {e}')
            )
