#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   :Nom du fichier:     moteurPap.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20160731

####

   :Licence:            CC-BY-NC-SA
   :Liens:              https://creativecommons.org/licenses/by-nc-sa/4.0/

####

    :dev language:      Python 3.4
    
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
   :**m_**:                 Module

####

moteurPap
=========

    Ce module permet de creer et de manipuler l'objet 'C_MoteurPap'
    
    Une valeur positive fait tourner le moteur dans le sens horaire.
    Une valeur négative fait tourner le moteur
    dans le sens anti-horaire (si on ne s'est pas trompé dans le cablage)

    N.B : se PAP doit etre pilote par un driver comme le UNL2003

    *** Specification ***
    
        :reference du moteur Pas a Pas:             28BJY-48
        :angle par pas (moteur):                    5.625°
        :Nbe de pas / tours (moteur):               64 (360/5.625)
        :ratio (demultiplicateur):                  1/64
        :angle par pas (en sortie d'abre):          0.087890625°
        :Nbe de pas / tour (en sortie d'arbre):     4096 

   *** Correspondance entre le driver UNL2003 et les GPIO ***
   
       +------------+-------------------------+
       | BCM (GPIO) | Serigraphie sur UNL2003 |
       +============+=========================+
       |   v_gpioA  |           N1            |
       +------------+-------------------------+
       |   v_gpioB  |           N2            |
       +------------+-------------------------+
       |   v_gpioC  |           N3            |
       +------------+-------------------------+
       |   v_gpioD  |           N4            |
       +------------+-------------------------+

    *** t_phases ***
    
        +-----------------+---+---+---+---+---+---+---+---+
        |                 | --> CW Direction (1-2 phase ) |
        +=================+===+===+===+===+===+===+===+===+
        | lead Wire color | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
        +-----------------+---+---+---+---+---+---+---+---+
        |   4 orange      | x | x |   |   |   |   |   | x |
        +-----------------+---+---+---+---+---+---+---+---+
        |   3 yelow       |   | x | x | x |   |   |   |   |
        +-----------------+---+---+---+---+---+---+---+---+
        |   2 pink        |   |   |   | x | x | x |   |   |
        +-----------------+---+---+---+---+---+---+---+---+
        |   1 blue        |   |   |   |   |   | x | x | x |
        +-----------------+---+---+---+---+---+---+---+---+
           
        N.B : les 8 phases donnent 1 tour complet sur le moteur,
              soit 1/64 de tour en sortie d'arbre.
"""

import sys
sys.path.insert(0,'..')         # ajouter le repertoire precedent au path (non definitif)

try :                           # pour pouvoir importer les modules et paquets parent
    from devChk.devChk import C_DebugMsg
except ImportError :
    print( "module 'devChk' non charge")

try :
    import RPi.GPIO as GPIO
    
except ImportError :
    print("module 'RPi' non charge")
    
import time

from math import pi


class C_MoteurPap(object):
    """ Class permettant d'instancier un objet 'C_MoteurPap' """
    
    def __init__(self, v_rotationInit = "horaire", v_rayonInit = 1) :
        """
            Declaration et initialisation des variables
        """
        # Creation de l'instance pour les message de debug
        self.i_dbg = C_DebugMsg()
        
        # declaration des variables
        self.v_rotation = v_rotationInit.lower()
        self.v_dest = 1
        self.v_compteurDePas = 0
        self.v_tempDePause = 0.005
        self.v_nbPas = 0
        self.v_angle = 0
        self.v_refAngle = 0.087890625
        
        self.t_broches = [0, 0, 0, 0]
        
        self.v_rayon = v_rayonInit
        self.v_perimetre = 2 * pi * self.v_rayon

        # Séquense de sortie
        self.v_ndp = 8
        self.t_phase = list(range(self.v_ndp))
        self.t_phase[0] = [1,0,0,0]
        self.t_phase[1] = [1,1,0,0]
        self.t_phase[2] = [0,1,0,0]
        self.t_phase[3] = [0,1,1,0]
        self.t_phase[4] = [0,0,1,0]
        self.t_phase[5] = [0,0,1,1]
        self.t_phase[6] = [0,0,0,1]
        self.t_phase[7] = [1,0,0,1]
        
    def __del__(self) :
        """destructor
        
            il faut utilise : ::
            
                del [nom_de_l'_instance]
        """
        self.f_gpioDestructor()
        v_className = self.__class__.__name__
        print("\n\t\tL'instance de la class {} est terminee".format(v_className))
        
    def f_gpioInit(self, v_gpioA=17, v_gpioB=18, v_gpioC=27, v_gpioD=22):
        """
            Methode permettant de selectionner et d'activer les 4 ports du RPi
            necessaires au fonctionnement du moteur Pas a Pas.
            par défaut, les ports sont configures de la facon suivante : ::
            
                v_gpioA = GPIO17
                v_gpioB = GPIO18
                v_gpioC = GPIO27
                v_gpioD = GPIO22
                
            Ces ports doivent etre change si il y a plus d'un moteur sur le montage
            
            Cette methode est obligatoire est doit etre appellee lors de la creation
            de chaque nouvelle instance de l'objet.
        """
        # configuration du mode du GPIO
        try :
            GPIO.setmode(GPIO.BCM)

            # Déclaration des broches : GPIO17, GPIO18, GPIO27, GPIO22
            self.t_broches = [v_gpioA, v_gpioB, v_gpioC, v_gpioD]

            # Configuration des broches en sortie et initialisation à l'état bas
            for v_sortieInit in self.t_broches :
                GPIO.setup(v_sortieInit, GPIO.OUT)
                GPIO.output(v_sortieInit, False)
        except NameError :
            print("GPIO error : f_gpioInit")


    def f_gpioDestructor(self):
        """
            Methode permettant de fermer proprement la gestion des GPIO du Rpi
            
            Cette methode doit etre appellee a la fin de l'utilisation
            des broches GPIO (avant de quitter le programme).
        """
        try :
            GPIO.cleanup()
            
        except NameError :
            print("GPIO error : f_gpioDestructor")

    def f_moveDeg(self, v_deg):
        """
            Methode permettant d'effectuer une rotation egale 
            a la valeur fournie degres
        """
        v_dbg = True
        
        # Récupération d'une valeur donnée en degrés puis conversion
        # de cette valeur en nombre de pas en sortie d'arbre
        self.v_dest = self.f_convertDegToStep( v_deg )
        
        #dbg
        self.i_dbg.dbgPrint(v_dbg, "self.v_dest [ + ]", self.v_dest)
        
        self.f_sensDeRotation()
        self.f_move(self.v_dest, v_deg)

    def f_moveStep(self, v_step):
        """
            Methode permettant d'effectuer une rotation egale
            a la valeur fournie nombre de pas (en sortie d'arbre)
        """
        v_dbg = True
        
        # Recuperation d'une valeur donnee en nombre de pas en sortie d'arbre
        self.v_dest =  v_step
        
        #dbg
        self.i_dbg.dbgPrint(v_dbg, "self.v_dest [ + ]", self.v_dest)
        
        self.f_sensDeRotation()
        self.f_move(self.v_dest, v_step)

    def f_moveCm(self, v_cm) :
        """ effectue une rotation egale a une distance en centimetre """
        v_dbg = True
        
        self.v_dest = self.f_convertCmToStep(v_cm)
        self.f_sensDeRotation()
        self.f_move(self.v_dest, v_cm)
                       
    def f_move(self, v_destMove, v_step) :
        """ Factorisation de la sequence de mouvement des PAP """
        v_dbg = True
        
        if v_destMove > 0 :
            v_destMove+= 1
            v_step = 1
        else :
            v_destMove -=1
            v_step = -1
            
            #dbg
            self.i_dbg.dbgPrint(v_dbg, "self.v_dest [ - ]", self.v_dest)
        
        for v_pas in range(0, v_destMove, v_step):
        
            #dbg
            self.i_dbg.dbgPrint(v_dbg, "v_pas : ", v_pas)
            
            for v_sortie in range(4):
                v_sortieN = self.t_broches[v_sortie]
                
                try :
                    if self.t_phase[self.v_compteurDePas][v_sortie] !=0 :
                    
                        #dbg
                        self.i_dbg.dbgPrint(v_dbg, "t_phase", self.v_compteurDePas)
                        self.i_dbg.dbgPrint(v_dbg, "Activation v_sortie", v_sortieN)
                        
                        GPIO.output(v_sortieN, True)
                    else :
                        GPIO.output(v_sortieN, False)
                except NameError :
                    print("GPIO error : f_move\n")
                    
                    #dbg
                    self.i_dbg.dbgPrint(v_dbg, "t_phase", self.v_compteurDePas)
                    self.i_dbg.dbgPrint(v_dbg, "Activation v_sortie", v_sortieN)
                    
            time.sleep(self.v_tempDePause)
            if v_step == 1 : self.v_compteurDePas -= 1
            elif v_step == -1 : self.v_compteurDePas +=1
        
            if (self.v_compteurDePas == self.v_ndp) : self.v_compteurDePas = 0
            if (self.v_compteurDePas < 0) : self.v_compteurDePas = self.v_ndp-1       
                
    def f_convertDegToStep(self, v_degToStep):
        """
            Methode permettant de convertir en nombre de Pas
            une valeur entree en degres
        """
        return int( v_degToStep //self.v_refAngle)
        
    def f_convertStepToDeg(self, v_stepToDeg):
        """
            Methode permettant de convertir en degres
            une valeur entree nombre de Pas
        """
        return v_stepToDeg * self.v_refAngle
        
    def f_convertCmToDeg(self, v_cmToDeg) :
        """
            Methode permettant de convertir en centimetre
            une valeur donnee en degres
            
            :Rappel:
                Calcul du perimetre d'un cercle : ::
                    
                        2 x pi x R
                
                +-----------------+------------------+
                |     Degres      |   centimetres    |
                +=================+==================+
                |      360        |      2piR        |
                +-----------------+------------------+
                |     360/(2piR)  |        1         |
                +-----------------+------------------+
                | (x360) / (2piR) |        x         |
                +-----------------+------------------+
                |        1        | (2piR) / (x360)  |
                +-----------------+------------------+
                |        x        | (x2piR) / (x360) |
                +-----------------+------------------+
        """
        return (v_cmToDeg * 360) / self.v_perimetre
        
    def f_convertDegToCm(self, v_degToCm) :
        """
            Methode permettant de convertir en degres
            une valeur donnee en centimetre
            
            :Rappel:
                Calcul du perimetre d'un cercle : ::
                    
                        2 x pi x R
                
                +-----------------+------------------+
                |     Degres      |   centimetres    |
                +=================+==================+
                |      360        |      2piR        |
                +-----------------+------------------+
                |     360/(2piR)  |        1         |
                +-----------------+------------------+
                | (x360) / (2piR) |        x         |
                +-----------------+------------------+
                |        1        | (2piR) / (x360)  |
                +-----------------+------------------+
                |        x        | (x2piR) / (x360) |
                +-----------------+------------------+
        """
        return (v_degToCm * self.v_perimetre) / 360
    
    def f_convertCmToStep(self, v_cmToStep) :
        """ convertit une valeur en centimetre
            en l'equivalent en nombres de pas
        """
        return int((4096 * v_cmToStep) / self.v_perimetre)
        
    def f_convertStepToCm(self, v_stepToCm) :
        """ convertit un nombre de pas en une distance en centimetre """
        return (v_stepToCm * self.v_perimetre) / 4096
        
       
    def f_sensDeRotation(self) :
        """
            identifie le sens de rotation attendu par l'utilisateur
            et l'affecter au PAP
        """
        if self.v_rotation == "antihoraire" :
            self.v_dest *= -1


           
def main() :
    #######################
    # Instance par defaut #
    #######################
    print("Instance par defaut")
    i_testClass1 = C_MoteurPap()

    input("f_gpioInit : ")
    i_testClass1.f_gpioInit()
        
    input("f_moveDeg(30)")
    i_testClass1.f_moveDeg(30)
    
    input("f_moveStep(256)")
    i_testClass1.f_moveStep(256)
    
    input("fin de l'instance")
    del i_testClass1
    
    #########################
    # Instance Anti-horaire #
    #########################
    print("Instance Anti-horaire")
    i_testClass2 = C_MoteurPap(v_rotationInit = "antihoraire")
    
    input("f_gpioInit")
    i_testClass2.f_gpioInit()
        
    input("f_moveDeg(30)")
    i_testClass2.f_moveDeg(30)
    
    input("f_moveStep(256)")
    i_testClass2.f_moveStep(256)
    
    input("fin de l'instance")
    del i_testClass2
    
    ###############
    # Instance cm #
    ###############
    print("Instance Centimetre")
    i_testClass3 = C_MoteurPap(v_rayonInit = 3)
    
    input("f_gpioInit")
    i_testClass3.f_gpioInit()
    
    input("f_moveCm(4)")
    i_testClass3.f_moveCm(4)

    input("fin de l'instance")
    del i_testClass3
    
          
if __name__ == '__main__':
    main()