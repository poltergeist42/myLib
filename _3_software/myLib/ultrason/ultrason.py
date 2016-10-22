#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Infos
=====

   :Nom du fichier:     ultrason.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20161022

####

   :Licence:            CC-BY-NC-SA
   :Liens:              https://creativecommons.org/licenses/by-nc-sa/4.0/

####

    :dev langage:       Python 3.4

####

lexique
=======

   :**v_**:                 variable
   :**l_**:                 list
   :**t_**:                 tuple
   :**d_**:                 dictionnaire
   :**f_**:                 fonction
   :**C_**:                 Class
   :**i_**:                 Instance
   :**m_**:                 matrice
   
####

Class C_ultrasonSensor
======================

"""

import sys
sys.path.insert(0,'../')

    # ajouter le repertoire precedent au path
    # (non definitif, supprimer du cache a la fin de l'execution)
    # pour pouvoir importer les modules et paquets parent

try :
    from devChk.devChk import C_DebugMsg
    v_dbgChk = True
    i_dbg = C_DebugMsg()
   
except ImportError :
    print( "module devChk non present" )
    v_dbgChk = False


try :
    import RPi.GPIO as GPIO
    
except ImportError :
    print("module 'RPi' non charge")
    
import time
import argparse

class C_ultrasonSensor(object) :
    """ **C_ultrasonSensor(object)**
    
        Class permettant d'utiliser le capteur ultra son 
    
        :Type de capteur:   HC-SR04
        
        **Trig**
            En Sortie (hautparleur)
                # 1 impulsion est egale a 10us (0.00001)
                        
        **Echo**
            En Entree (Micro)
                # Attention les entrees du RPi etant en 3.3v,
                il faut faire un pont diviseur entre la broche
                "Echo" et le GND pour pouvoir se brancher
                sur le RPi
                    
        **Vitesse du son**
            Le son se déplace à une vitesse d'environ 343 m/s
            soit 34300 cm / us (centimetre / micro seconde)
                                   
        **Distance**
            D = 17150 x time
                # 17150 correspond a la vitesse du son / 2 (34300/2).
                On divise par 2 car seule la distance en l'obstacle et le mur nous intéresse
                et non la distance total parcourue par l'onde radio.
                
        :source: https://www.youtube.com/watch?v=xACy8l3LsXI
        
    """
    
    def __init__(self) :
    
        """ 
            **__init()**
        
            Creation et initialisation des variables globales de cette Class
            
        """
                
        ## declaration des variables
        self.v_trig = 0
        self.v_echo = 0
        self.v_timeSpeed = 17150
        
    def __del__(self) :
        """
            **__del__()**
        
            Permet de terminer proprement l'instance de la Class courante
        
            il faut utilise : ::
            
                del [nom_de_l'_instance]
                
        """
        
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "__del__", self.__del__)
        
        ## Action
        self.f_gpioDestructor()
        v_className = self.__class__.__name__
        print("\n\t\tL'instance de la class {} est terminee".format(v_className))
        
    def f_gpioDestructor(self):
        """
            **f_gpioDestructor()**
        
            Methode permettant de fermer proprement la gestion des GPIO du Rpi
            
            Cette methode doit etre appellee a la fin de l'utilisation
            des broches GPIO (avant de quiter le programme).
            
        """
        
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_gpioDestructor", self.f_gpioDestructor)
        
        ## Action
        try :
            GPIO.cleanup()
            
        except NameError :
            print("GPIO error : f_gpioDestructor")

        
    def f_ultraInit(self, v_gpioTrig=7, v_gpioEcho=12) :
        """
            **f_ultraInit()**

            initialisation des broches GPIO en entree (Echo) et en sortie (Trig).
            Par défaut, le Trig et l'Echo sont affectés aux broches 
            7 et 12 du Raspberry Pi
            
            Echo est configure en entree avec la PULL_DOWN activee.
            
        """
        
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_ultraInit", self.f_ultraInit)
        
        ## Action
        GPIO.setmode(GPIO.BCM)
        
        self.v_trig = v_gpioTrig
        self.v_echo = v_gpioEcho
        
        GPIO.setup(self.v_echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.v_trig, GPIO.OUT)
        
        GPIO.output(self.v_trig, 0)
        
        time.sleep(0.1)

                
    def f_ultraMesure(self) :
        """
            **f_ultraMesure()**
            
            Renvoie la distance entre le capteur et l'obstacle.
            
            *N.B :* valeur en centimetre
            
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_ultraMesure", self.f_ultraMesure)
        
        ## Action
        ## Emission de l'onde radio
        
        GPIO.output(self.v_trig, 1)
        
        ## dbg
        f_dbg(v_dbg, "self.v_trig", self.v_trig)
        
        ## Action
        time.sleep(0.00001)
        GPIO.output(self.v_trig, 0)
        
        ## dbg
        f_dbg(v_dbg, "self.v_trig", self.v_trig)
        
        ## Action
        ## reception de l'echo radio
        while GPIO.input(self.v_echo) == 0 :
            pass
            
        v_start = time.time()
        
        ## dbg
        f_dbg(v_dbg, "v_start", v_start)
        
        ## Action
        while GPIO.input(self.v_echo) == 1 :
            pass
            
        v_stop = time.time()
        v_timeDiff = v_stop - v_start
        v_dist = (v_timeDiff * self.v_timeSpeed)
        
        # dbg
        f_dbg(v_dbg, "v_stop", v_stop)
        f_dbg(v_dbg, "v_timeDiff", v_timeDiff)
        f_dbg(v_dbg, "v_dist", v_dist)
        
        return v_dist
 
 
def f_dbg( v_bool, v_tittle, v_data ) :
    """ Fonction de traitemant du debug """
    if v_dbgChk :
        i_dbg.dbgPrint( v_bool, v_tittle, v_data )
 
def main() :
    """**Fonction main()**

        Cette Fonction affiche en permanence la distance entre le capteur et l'obstacle.
        Pour sortir de la boucle il faut faire une interruption (CTRL - c).
    """
    parser = argparse.ArgumentParser()
    parser.add_argument( "-d", "--debug", action='store_true', help="activation du mode debug")
                        
    args = parser.parse_args()
    
    if args.debug :
        if v_dbgChk :
            i_dbg.f_setAffichage( True )
            print( "Mode Debug activer" )
        else :
            print( "Le mode Debug ne peut pas etre active car le module n'est pas present")

        
    # Instance par defaut
    
    print("Instance par defaut")
    i_testClass = C_ultrasonSensor()
    i_testClass.f_ultraInit()
    
    v_boucle = True
    while v_boucle :
    
        try :
            time.sleep(0.1)
            print(i_testClass.f_ultraMesure())

        except KeyboardInterrupt :
            print("\nLa boucle a ete interrompue par l'utilisateur")
            v_boucle = False

    del i_testClass
  
if __name__ == '__main__':
    main()