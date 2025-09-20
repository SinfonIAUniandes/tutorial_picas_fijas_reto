#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from rospy import ServiceException

def main():
    rospy.init_node('nodo_central')
    pub = rospy.Publisher('/topico_global', String, queue_size=10)
    
    # Conjunto para controlar los equipos registrados
    equipos_registrados = set()
    
    def manejar_registro(datos):
        nombre_equipo = datos.data
        if nombre_equipo not in equipos_registrados:
            equipos_registrados.add(nombre_equipo)
            pub.publish(String(f"{nombre_equipo}, registrado"))
            rospy.loginfo(f"Registrado: {nombre_equipo}")
    
    sub = rospy.Subscriber('/topico_registro', String, manejar_registro)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
