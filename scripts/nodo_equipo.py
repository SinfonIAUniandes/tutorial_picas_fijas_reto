#!/usr/bin/env python3

import rospy
import random
from std_msgs.msg import String
from picas_fijas_msgs.srv import Intento, IntentoResponse

def generar_numero_secreto():
    digitos = list(range(10))
    random.shuffle(digitos)
    return ''.join(map(str, digitos[:4]))

def calcular_picas_fijas(secreto, intento):
    picas = 0
    fijas = 0
    for i in range(4):
        if intento[i] == secreto[i]:
            fijas += 1
        elif intento[i] in secreto:
            picas += 1
    return picas, fijas

def main():
    # Pedir nombre del equipo
    team_name = input("Ingrese nombre del equipo: ").strip().replace(" ", "_")  # Reemplazar espacios para nombre de nodo valido
    
    rospy.init_node(team_name)
    
    # Generar numero secreto
    secreto = generar_numero_secreto()
    rospy.loginfo(f"Secreto para {team_name}: {secreto}")
    
    # Publicadores
    reg_pub = rospy.Publisher('/topico_registro', String, queue_size=10)
    global_pub = rospy.Publisher('/topico_global', String, queue_size=10)
    
    # Registrarse con el nodo central
    reg_pub.publish(String(team_name))
    
    def manejar_intento(req):
        intento = req.valor
        
        if len(intento) != 4 or not intento.isdigit():
            global_pub.publish(String(f"Intento invalido para {team_name}"))
            return IntentoResponse(exito=False)
        
        picas, fijas = calcular_picas_fijas(secreto, intento)
        
        if fijas == 4:
            global_pub.publish(String(f"{team_name} fue eliminado con el numero {intento}"))
            return IntentoResponse(exito=True)
        else:
            global_pub.publish(String(f"Para {team_name} el numero {intento} tiene {picas} picas y {fijas} fijas."))
        
        return IntentoResponse(exito=False)
    
    service = rospy.Service(f'/{team_name}/guess_service', Intento, manejar_intento)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
