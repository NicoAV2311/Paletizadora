#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.button import Button
from time import sleep

# Inicializar los motores
motor_vinilo = LargeMotor(OUTPUT_A)  # Motor que mueve el vinilo
motor_base = LargeMotor(OUTPUT_B)  # Motor de la base giratoria

# Inicializar los sensores
sensor_presion = TouchSensor(INPUT_1)  # Sensor de presión en la parte inferior de la banda

# Inicializar los botones
btn = Button()

# Definir la función para mover el motor del vinilo
def mover_vinilo(velocidad):
    motor_vinilo.on(velocidad)

# Definir la función para detener el motor del vinilo
def detener_vinilo():
    motor_vinilo.stop()

# Pedir al usuario la velocidad de la base giratoria
def seleccionar_velocidad_base():
    print("Seleccione la velocidad de la base giratoria:")
    print("Boton izquierdo para 25, boton derecho para 50.")
    
    velocidad = 0

    while True:
        if btn.left:
            velocidad = 25
            print("Velocidad seleccionada: 25")
            break
        elif btn.right:
            velocidad = 50
            print("Velocidad seleccionada: 50")
            break
        sleep(0.1)
    
    return velocidad

# Pedir al usuario la altura del objeto a paletizar
def seleccionar_altura_objeto():
    print("Seleccione la altura del objeto a paletizar:")
    print("Boton Abajo: Altura Baja")
    print("Boton Central: Altura Media")
    print("Boton Arriba: Altura Alta")

    altura = 0

    while True:
        if btn.down:
            altura = 0.3  # Rotaciones para altura baja
            print("Altura seleccionada: Altura Baja")
            break
        elif btn.enter:
            altura = 0.6  # Rotaciones para altura media
            print("Altura seleccionada: Altura Media")
            break
        elif btn.up:
            altura = 0.9  # Rotaciones para altura alta
            print("Altura seleccionada: Altura Alta")
            break
        sleep(0.1)

    return altura

# Realizar el loop de funciones
while True:
    try:
        # Seleccionar velocidad de la base giratoria
        velocidad_base = seleccionar_velocidad_base()

        # Separar claramente la selección de la altura
        altura = seleccionar_altura_objeto()

        # Verificar que el motor esté en la posición más baja usando el sensor de presión
        print("Bajando el motor del vinilo para verificar la posicion...")
        mover_vinilo(15)  # Mover hacia abajo

        while not sensor_presion.is_pressed:  # Esperar hasta que se active el sensor de presión
            sleep(0.1)

        detener_vinilo()  # Detener el motor cuando el sensor se activa
        print("El motor del vinilo esta en la posicion mas baja.")

        # Iniciar la base giratoria
        motor_base.on(velocidad_base)

        print("Comenzando el ciclo de 6 repeticiones de subir y bajar el vinilo...")

        for _ in range(6):  # Subir y bajar 6 veces
            motor_vinilo.on_for_rotations(-15, altura)  # Subir
            sleep(0.5)  # Esperar 0.5 segundos
            detener_vinilo()
            sleep(0.5)  # Pausa antes de bajar
            motor_vinilo.on_for_rotations(15, altura)  # Bajar
            sleep(0.5)  # Esperar 0.5 segundos
            detener_vinilo()

        print("Proceso completado.")
        motor_base.stop()  # Detener la base giratoria al finalizar

    except Exception as e:
        print("Error: {}".format(e))
        detener_vinilo()
        motor_base.stop()  # Asegurarse de detener la base giratoria
        break
