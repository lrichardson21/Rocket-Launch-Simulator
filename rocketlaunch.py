#rocketlaunch.py
#This is a model rocket flight simulator programmed in python
#import necesary libraries
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import keyboard
import pygame
from pygame import mixer 
#import audio for error message
pygame.mixer.init() 
mixer.music.load("huston.mp3")
mixer.music.set_volume(0.5)

def main():
    #introduction to user
    print()
    typetext("Welcome to the python model rocket launch simulator. ", 0.08)
    typetext("This program is compatible for model rockets using AreoTech, Apogee, and Estes motors", 0.07)
    typetext("Assume all masses are in grams, thrust and impulse are in Newtons, time is in seconds, area is in meters^2 and any distance is in meters.", 0.05)
    typetext("Do not include units when you input your information.", 0.06)
    typetext("Starting simulation...............", 0.1)
    print()

    #get rocket information from user
    target_height = input("Does your rocket need to reach a specific apogee? (type 'yes' or 'no') >> ")
    if target_height[0] == 'y':
        height = float(input("What is the target apogee of your rocket? >> "))
        var = 1
    cross_sectional_area = float(input("Enter the rockets cross sectional area: >> "))
    mass = float(input("Enter mass of rocket (no motor) >> "))
    ejection_delay = float(input("How many seconds is the motor's ejection delay? >> "))

   #assign values based on motor type and models
    motorman = input("Enter motor manufacturer (AreoTech, Apogee, or Estes) >> ")
    while motorman[:2] != "Ar" and motorman[:2] != "Ap" and motorman[0] != "E":
        mixer.music.play()
        print("\nHuston we have a problem!")
        typetext("Your information could not be calculated.", 0.1)
        typetext("Please re-enter", 0.1)
        print()
        motorman = input("Enter motor manufacturer (AreoTech, Apogee, or Estes) >> ")
    while motorman[:2] == "Ar" or motorman[:2] == "Ap" or motorman[0] == "E":
        if motorman[:2] == "Ar": #AreoTech Motors
            motorman = "AreoTech"
            motormodel = input("Is your AreoTech motor model C3.4, D10, or D13 >> ")
            if motormodel == "C3.4":
                motormass = 23.9 / 1000
                propellant_mass = 5.2 / 1000
                burntime = 2.86
                thrust = 3.006
                impulse = 8.5972
                break
            elif motormodel == "D10":
                motormass = 25.9 / 1000
                propellant_mass = 9.8 / 1000
                burntime = 1.39
                thrust = 13.4
                impulse = 18.8
                break
            elif motormodel == "D13":
                motormass = 33.0 / 1000
                propellant_mass = 9.8 / 1000
                burntime = 1.7
                thrust = 12.7
                impulse = 19.3
                break
        elif motorman[0:2] == "Ap": #for apogee motors
            motorman = "Apogee"
            motormodel = input("Is your Apogee motor model E6 or F10 >> ")
            if motormodel == "E6":
                motormass = 46.3 / 1000
                propellant_mass = 21.5 / 1000
                burntime = 6.06
                thrust = 6.5
                impulse = 37.8
                break
            if motormodel == "F10":
                motormass = 84.1 / 1000
                propellant_mass = 40.7 / 1000
                burntime = 7.13
                thrust = 10.6
                impulse = 74.3
                break
        elif motorman[0] == "E": #for esstees motors
            motorman = "Estes"
            motormodel = input("Is your Estes motor model C5 or C6? >> ")
            if motormodel == "C5":
                motormass = 23.8 / 1000
                propellant_mass = 11.0 /1000
                burntime = 1.99
                thrust = 3.9
                impulse = 7.8
                break
            if motormodel == "C6":
                motormass = 23.1 / 1000
                propellant_mass = 10.8 /1000
                burntime = 1.86
                thrust = 4.7
                impulse = 8.8
                break

    #assign drag coefficient values to differnt nose cones
    nosecone = input("Is the nosecone type conical, parabolic, or neither? >> ")
    while nosecone[0] != "c" and nosecone[0] != "p" and nosecone[0] != 'n':
        mixer.music.play()
        print("\nHuston we have a problem!")
        typetext("Your information could not be calculated.", 0.1)
        typetext("Please re-enter", 0.1)
        print()
        nosecone = input("Is the nosecone type conical, parabolic, or neither? >> ")
    while nosecone[0] == "c" or nosecone[0] == "p" or nosecone[0] == 'n':
        if nosecone[0] == "c":
            Cd = 0.508609
            break
        elif nosecone[0] == "p":
            Cd = 0.39384
            break
        elif nosecone[0] == "n": #normal drag coefficinet
            Cd = 0.75
            break
    
    #variables for calculations
    g = 9.81 #acceleratioin due to gravity m/s^2
    e = 2.71828
    m =  mass / 1000
    # mass during coast is mr + me - mp
    mcoast = (m + motormass) - propellant_mass
    # average mass during boost is mr + me - mp/2
    mboost = (m + motormass) - (propellant_mass/2)
    t = burntime
    T = thrust
    I = impulse
    A = cross_sectional_area
    k = (1/2)*(1.2)*(Cd)*(A)
    w= (T-(mboost*g))/k
    q = math.sqrt(w)
    x = (2*k*q)/mboost

    #max velocity at burnout 
    v = q*((1-e**(-x*t))/(1+e**(-x*t)))
    v = round(v, 3)

    #Altitude at the end of boost
    y1 = (-mboost/(2*k))* math.log( (T-(mboost*g)-(k*v**2))/(T-mboost*(g))) 
    y1 = round(y1, 3)

    #coasting distance
    yc = (m/(2*k)) * math.log((mcoast*g + k*v**2) / (mcoast*g)) 
    yc = round(yc, 3)

    #apogee
    apogee = y1 + yc
    apogee = round(apogee, 3)
    
    #take to graphs
    typetext("\nInformation Processing......\nPress <enter> to view analysis.", 0.1)
    enter = input()
    if enter == "":

        #critical values and summary
        print()
        typetext("Here are the critical values for your model rocket: ", .08)
        print("----------------------------------------------------")
        print()
        typetext(("Your ", motorman, " ", motormodel, " motor will burn for ", burntime, " seconds", " and generate ", thrust, " Newtons of thrust."), .06)
        print()
        typetext(("The maximum altitude of your rocket is: ", apogee, " meters."), .06)
        print()
        typetext(("The altitude at the end of the motors initial thrust is ", y1, " meters."), .06 )
        print()
        typetext(("The maximum velocity at burnout is: ", v, " meters/second."), .06)
        print()
    
        #Print if rocket was above or below apogee based off the users answer to the first question
        if var == 1:
            height_left = str(apogee - height)
            if height_left[0] == '-':
                below = abs(float(height_left))
                print("Your rocket was ", round(below, 3), " meters below apogee.")
                print()
            else:
                height_left = float(height_left)
                print('Your rocket was ', round(height_left, 3), " meters above apogee.")
                print()
        
        #altitude bar graph
        altitudes = [y1, yc, apogee]
        altitude_types = ['End of Boost', 'Coasting Distance', 'Apogee']
        plt.bar(altitude_types, altitudes)
        plt.title('Key Altitudes Of Rocket')
        plt.ylabel('Meters')
        plt.show(block=True)


#function to make text in terminal appear like a typewriter
def typetext(text, delay=0.1):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

if __name__ == "__main__":
    main()
