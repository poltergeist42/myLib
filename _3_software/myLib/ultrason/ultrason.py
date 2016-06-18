#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   :Nom du fichier:     ultrason.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20160614

----

   :Licence:            CC-BY-NC-SA
   :Liens:              https://creativecommons.org/licenses/by-nc-sa/4.0/

----


lexique
-------

   :v_:                 variable
   :l_:                 list
   :t_:                 tuple
   :d_:                 dictionnaire
   :f_:                 fonction
   :C_:                 Class
   :i_:                 Instance
   :m_:                 Module
"""
#################### Taille maximum des commentaires (80 caracteres)######################

import RPi.GPIO as GPIO
import time

class C_ultrasonSensor(object) :
    """ Class permettant d'utiliser le capteur ultra son 
    
    :Type de capteur: HC-SR04
    
    Trig
        En Sortie (hautparleur)
            # 1 impulsion est egale a 10us (0.00001)
                    
    Echo
        En Entree (Micro)
        
            # Attention les entrees du RPi etant en 3.3v,
            il faut faire un pont diviseur entre la broche
            "Echo" et le GND pour pouvoir se brancher
            sur le RPi
                
    Vitesse du son
        Le son se déplace à une vitesse d'environ 340 m/s
            
            
                
    Distance
        D = 170 x time
            # 170 correspond a la vitesse du son / 2 (340/2).
            On divise par 2 car seule la distance en l'obstacle et le mur nous intéresse
            et non la distance total parcourue par l'onde radio.
    - source : https://www.youtube.com/watch?v=xACy8l3LsXI
    """
    def init(self) :
        """ variables globales """
        self.v_trig = 0
        self.v_echo = 0
        self.v_timeSpeed = 170
        
    def __del__(self) :
        """destructor
        
            il faut utilise :
            ::
            
                del [nom_de_l'_instance]
        """
        self.f_gpioDestructor()
        v_className = self.__class__.__name__
        print("\n\t\tL'instance de la class {} est terminee".format(v_className))
        
    def f_gpioDestructor(self):
        """
            Methode permettant de fermer proprement la gestion des GPIO du Rpi
            
            Cette methode doit etre appellee a la fin de l'utilisation
            des broches GPIO (avant de quiter le programe).
        """
        try :
            GPIO.cleanup()
            
        except NameError :
            print("GPIO error : f_gpioDestructor")

        
    def f_ultraInit(self, v_gpioTrig = 7, v_gpioEcho = 12) :
        """ initialisation des broches GPIO en entree (Echo) et en sortie (Trig) """
        GPIO.setmode(GPIO.BCM)
        self.v_trig = v_gpioTrig
        self.v_echo = v_gpioEcho
        
        GPIO.setup(self.v_echo, GPIO.IN)
        GPIO.setup(self.v_trig, GPIO.OUT)
        
    def f_ultraMesure(self) :
        """ mersure de la distance entre le capteur et l'obstacle """
        
        # Emission de l'onde radio
        time.sleep(0.1)
        GPIO.output(self.v_trig, 1)
        time.sleep(0.00001)
        GPIO.output(self.v_trig, 1)
        
        # reception de l'echo radio
        while GPIO.input(self.v_echo == 0) :
            pass
            
        v_start = timte.time()
        
        while GPIO.input(self.v_echo == 1)
            pass
            
        v_stop = time.time()
        
        return (stop - start) * self.v_timeSpeed
 
 def main() :
    """ Fonction principal """
    #######################
    # Instance par defaut #
    #######################
    print("Instance par defaut")
    i_testClass = C_ultrasonSensor
    
    input("f_ultraInit : ")
    i_testClass.f_ultraInit()
    
    input("f_ultraMesure : )
    i_testClass.f_ultraMesure()
    
    del i_testClass
 
 if __name__ == '__main__':
    main()