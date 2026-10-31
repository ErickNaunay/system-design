"""Ejercicio 3: decidir, lectura por lectura, si va a la primaria o a la
replica.

Corre las pruebas con:

    pytest test_servicio_replicado_ejercicio3.py

No cambies los nombres de la clase ni de los metodos, y lee siempre a
traves de self.base.leer_de_primaria() o self.base.leer_de_replica():
los tests cuentan en que nodo hiciste cada lectura.
"""

from datos_reservas import ReservaRegistrada

class ServicioDeReservasReplicado:
    def __init__(self, base):
        self.base = base
        self.siguiente_id = 1
        self.escritores_recientes = set()

    def cancha_disponible(self, campus, cancha, fecha, hora):
        reservas = self.base.leer_de_primaria()
        
        for r in reservas:
            if r.campus == campus and r.cancha == cancha and r.fecha == fecha and r.hora == hora:
                return False
        return True

    def reservar(self, id_estudiante, campus, cancha, fecha, hora):
        if not self.cancha_disponible(campus, cancha, fecha, hora):
            return None
        reserva = ReservaRegistrada(self.siguiente_id, id_estudiante, campus, cancha, fecha, hora)
        self.siguiente_id = self.siguiente_id + 1
        self.base.escribir(reserva)
        
        return reserva

    def mis_reservas(self, id_estudiante):
        if self.base.tiene_escrituras_pendientes_de(id_estudiante):
            reservas = self.base.leer_de_primaria()
        else:
            reservas = self.base.leer_de_replica()

        mis_reservas_list = []
        for r in reservas:
            if r.id_estudiante == id_estudiante:
                mis_reservas_list.append(r)

        return mis_reservas_list 

    def ocupacion_del_campus(self, campus):
        # TODO: devuelve cuantas reservas tiene el campus. Es el reporte
        # que mira la administracion una vez al dia: elige de que nodo leer.
        
        # LECTURA DE RÉPLICA: La consistencia eventual es perfecta para analítica/reportes.
        reservas = self.base.leer_de_replica()
        
        conteo = 0
        for r in reservas:
            if r.campus == campus:
                conteo += 1
                
        return conteo
