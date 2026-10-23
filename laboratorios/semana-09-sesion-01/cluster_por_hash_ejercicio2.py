"""Ejercicio 2: sharding por hash del estudiante, consulta dirigida y
scatter-gather.

Corre las pruebas con:

    pytest test_cluster_por_hash_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""

from datos_reservas import hash_estable


class ClusterPorHash:
    def __init__(self, cantidad_de_shards):
        self.cantidad_de_shards = cantidad_de_shards
        self.shards = []
        for _ in range(cantidad_de_shards):
            self.shards.append([])

    def shard_de(self, id_estudiante):
        return hash_estable(id_estudiante) % self.cantidad_de_shards

    def insertar(self, reserva):
        shard_id = self.shard_de(reserva.id_estudiante)
        self.shards[shard_id].append(reserva)
        
    def tamanos(self):
        contar = []
        
        for shard in self.shards:
            contar.append(len(shard))
            
        return contar

    def reservas_de_estudiante(self, id_estudiante):
        reservas_estudiante = []
        
        shard_id = self.shard_de(id_estudiante)
        for reserva in self.shards[shard_id]:
            if reserva.id_estudiante == id_estudiante:
                reservas_estudiante.append(reserva)
                
        return reservas_estudiante, 1
        
    def reservas_de_cancha(self, campus, cancha, fecha):
        reservas_encontradas = []

        for shard in self.shards:
            for reserva in shard:
                if reserva.campus == campus and reserva.cancha == cancha and reserva.fecha == fecha:
                    reservas_encontradas.append(reserva)
                
        return reservas_encontradas, self.cantidad_de_shards
    
def fraccion_que_cambia_de_shard(claves, shards_antes, shards_despues):
    if not claves:
        return 0.0
        
    cambian = 0 
    for clave in claves:
        if (hash_estable(clave) % shards_antes) != (hash_estable(clave) % shards_despues):
            cambian += 1 
            
    return cambian / len(claves)