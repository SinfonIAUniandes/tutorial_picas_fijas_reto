#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from rospy import ServiceException
import os

def main():
    rospy.init_node('nodo_central')
    publicador = rospy.Publisher('/topico_global', String, queue_size=10)
    rospy.loginfo("Publicador global creado.")
    
    # Conjunto para controlar los equipos registrados
    equipos_registrados = set()
    
    def manejar_registro(datos):
        nombre_equipo = datos.data
        if nombre_equipo not in equipos_registrados:
            equipos_registrados.add(nombre_equipo)
            mensaje_de_registro = String()
            mensaje_de_registro.data = f"{nombre_equipo}, registrado"
            publicador.publish(mensaje_de_registro)
            rospy.loginfo(f"Registrado: {nombre_equipo}")
        else:
            rospy.loginfo(f"Equipo {nombre_equipo} ya registrado.")
    
    suscriptor = rospy.Subscriber('/topico_registro', String, manejar_registro)
    rospy.loginfo("Suscriptor de registro creado.")
    
    rospy.spin()

if __name__ == '__main__':
    try:
        print("Iniciando nodo central...")
        main()
        print("Nodo central finalizado.")
    except rospy.ROSInterruptException:
        os.exit(0)
