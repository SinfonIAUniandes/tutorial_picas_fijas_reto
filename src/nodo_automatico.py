#!/usr/bin/env python3
import rospy
import random
import os
from std_msgs.msg import String
from picas_fijas_msgs.srv import Intento, IntentoResponse
from rospy import ServiceException

muerto = False

def generar_numero_secreto():
    digitos = list(range(10))
    random.shuffle(digitos)
    return ''.join(map(str, digitos[:4]))

def generar_intento_estrategico():
    # Placeholder para una estrategia más avanzada
    pass

# TODO: Mejorar estrategia de ataque
# Estrategia simple: generar intentos aleatorios
def generar_intento_aleatorio():
    return generar_numero_secreto()

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
    global muerto
    team_name = input("Ingrese nombre del equipo (sin espacios): ").strip().replace(" ", "_")
    rospy.init_node(team_name)
    secreto = generar_numero_secreto()
    rospy.loginfo(f"[{team_name}] Secreto: {secreto}")
    global_pub = rospy.Publisher('/topico_global', String, queue_size=10)

    def manejar_intento(req):
        global muerto
        intento = req.valor
        if len(intento) != 4 or not intento.isdigit():
            global_pub.publish(String(f"Intento invalido para {team_name}"))
            return IntentoResponse(exito=False)
        picas, fijas = calcular_picas_fijas(secreto, intento)
        if fijas == 4:
            global_pub.publish(String(f"{team_name} fue eliminado con el numero {intento}"))
            muerto = True
            return IntentoResponse(exito=True)
        else:
            global_pub.publish(String(f"Para {team_name} el numero {intento} tiene {picas} picas y {fijas} fijas."))
            return IntentoResponse(exito=False)




    service = rospy.Service(f'/{team_name}/guess_service', Intento, manejar_intento)
    rospy.loginfo(f"[{team_name}] Servicio /{team_name}/guess_service creado.")




    # Pedir primer objetivo
    current_target = None
    while not rospy.is_shutdown() and not muerto:
        if current_target is None:
            target_input = input("Ingrese el nombre del equipo a atacar (o vacío para esperar): ").strip().replace(" ", "_")
            if not target_input:
                rospy.loginfo("Esperando objetivo...")
                rospy.sleep(1)
                continue
            if target_input == team_name:
                print("No puede atacarse a sí mismo. Ingrese otro objetivo.")
                continue
            current_target = target_input
            rospy.loginfo(f"[{team_name}] Atacando a: {current_target}")

        # Intentos de ataque al objetivo actual
        try:
            proxy = rospy.ServiceProxy(f'/{current_target}/guess_service', Intento)
            # Llamar al servicio periódicamente con números aleatorios
            # TODO
            # intento = generar_intento_estrategico()  # Aquí se podría usar una estrategia más avanzada
            intento = generar_intento_aleatorio()
            rospy.loginfo(f"[{team_name}] Probando {intento} contra {current_target}")
            resp = proxy(intento)
            if resp.exito:
                rospy.loginfo(f"[{team_name}] Eliminó a {current_target} con {intento}")
                global_pub.publish(String(f"{team_name} elimino a {current_target} con {intento}"))
                # Pedir nuevo objetivo
                current_target = None
            else:
                # publicar intento fallido para visibilidad
                global_pub.publish(String(f"{team_name} intento {intento} contra {current_target} (falló)"))
           
            # PROHIBIDO MODIFICAR LOS SLEEPS
            rospy.sleep(1.0)
        except ServiceException as e:
            rospy.logwarn(f"[{team_name}] Servicio de {current_target} no disponible: {e}")
            # esperar y pedir nuevo objetivo
            current_target = None
            rospy.sleep(1.0)
        except rospy.ROSException as e:
            rospy.logwarn(f"[{team_name}] Error ROS al llamar a {current_target}: {e}")
            current_target = None
            rospy.sleep(1.0)
        except Exception as e:
            rospy.logwarn(f"[{team_name}] Excepción al atacar: {e}")
            current_target = None
            rospy.sleep(1.0)

    if muerto:
        rospy.loginfo(f"[{team_name}] Fue eliminado. Cerrando nodo...")
    else:
        rospy.loginfo(f"[{team_name}] Nodo detenido por ROS.")
    os._exit(0)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        os._exit(0)
# ...existing code...