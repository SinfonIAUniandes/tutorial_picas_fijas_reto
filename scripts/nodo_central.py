#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from rospy import ServiceException
import os

def main():
    rospy.init_node('nodo_central')
    publicador = rospy.Publisher('/topico_global', String, queue_size=10)
    rospy.loginfo("Publicador global creado.")
    
    rospy.spin()

if __name__ == '__main__':
    try:
        print("Iniciando nodo central...")
        main()
        print("Nodo central finalizado.")
    except rospy.ROSInterruptException:
        os.exit(0)
