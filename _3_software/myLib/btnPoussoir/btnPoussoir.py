#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   :Nom du fichier:     btnPoussoir.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20160808

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

"""
try :
    import os, sys
    sys.path.insert(0,'..')         # ajouter le repertoire precedent au path (non définitif)
                                    # pour pouvoir importer les modules et paquets parent
    from devChk.devChk import C_DebugMsg
   
except ImportError :
    print( "module devChk non present" )
    
try :
    import RPi.GPIO as GPIO
    
except ImportError :
    print("module 'RPi' non charge")
    
import time

class C_BtnPoussoir( object )
    """ **btnPoussoir()**
    
        Class permettant de gerer les boutons poussoirs
    """
    def __init__( self ) :
        """ **__init()**
        
            Creation et initialisation des variables globales de cette Class
        """
        
        ## Creation de l'instance pour les message de debug
        self.i_dbg = C_DebugMsg()
                
        ## declaration des variables
        self.v_broche = 0
        self.v_pudStatus = ""
        self.v_pudState = True
        
####
        
    def __del__( self ) :
        """ **__del__()**
        
            Permet de terminer proprement l'instance de la Class courante
        
            il faut utilise : ::
            
                del [nom_de_l'_instance]
                
            *N.B :* Si l'instance n'est plus utilisee, cette methode est appellee 
            automatiquement.
        """
        v_dbg = 1
        v_dbg2 = 0
        i_debug = self.i_dbg.dbgPrint
        i_debug( v_dbg2, "__del__", self.__del__ )
        
        v_className = self.__class__.__name__
        print( "\n\t\tL'instance de la class {} est terminee".format(v_className) )    

####
        
    def f_gpioInit(self, v_gpio = 21, v_pullUpDown = True, v_pullToUpOrDown = "UP"):
        """ **f_gpioInit( GPIO_Channel, Boolean, str )
            
            Methode permettant d'initialiser le bouton poussoir en entree sur une broche
            du raspberry pi. par defaut, le bouton est initialiser sur le GPIO 21 avec
            la resistance de tirage interne activee en mode pull-up. Les choix pour la
            gestion de la resistance de tirage sont : ::
            
                v_pullUpDown = True / False
                    # True siginifie 'activee' alors que False signifie 'desactive'
                    
                v_pullToUpOrDown = 'UP' / 'DOWN'
                    # 'UP' signifie PULL-UP et 'DOWN' signifie PULL-DOWN
            
            *N.B :* Pour une configuration en pull-up, le bouton poussoir devra etre
            connecte entre le broche d'entree et le GND. Pour une configuration en
            pull-down, le bouton poussoir devra etre connecte entre la broche et
            le VCC +3.3v.
            
            Cette methode est obligatoire est doit etre appellee lors de la creation
            de chaque nouvelle instance de l'objet.
        """
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug( v_dbg2, "f_gpioInit", self.f_gpioInit )

        
        self.v_pudStatus = v_pullToUpOrDown
        self.v_pudState = v_pullUpDown
        self.v_broche = v_gpio
        
        ## raccourcis
        v_broche = self.v_broche

        
        ## dbg
        i_debug( v_dbg1, "v_pudStatus", self.v_pudStatus )
        i_debug( v_dbg1, "v_pudState", self.v_pudState )
        i_debug( v_dbg1, "v_broche", self.v_broche )

        # configuration du mode du GPIO
        try :
            GPIO.setmode( GPIO.BCM )

            # Configuration de la broche
            if v_pullUpDown :
                if v_pullToUpOrDown == "UP" :
                    GPIO.setup(v_broche, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                    
                elif v_pullToUpOrDown == "DOWN" :
                    GPIO.setup(v_broche, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                    
            else :
                GPIO.setup(v_broche, GPIO.IN)

        except NameError :
            print("GPIO error : f_gpioInit")

####

    def f_btnWaitForEvent( self, v_fnToExecute, v_front = "FALLING", v_timeout = None ) :
        """ **f_btnWaitForEvent(
                                [nom_de_la_fonction_a_executer -- Type <function>],
                                [Etat attendu pour le declenchement de l'evenement -- Type <str>],
                                [temps du time Out en milisecondes -- Type <int>
                                )
        
            Cette methode attend un chagemant d'etat de la broche (front montant, front
            front descandant, ou les deux) puis execute la fonction passee en parametre.
            
            les modes disponibles sont : 
            
                * "RISING" : Front Montant
                * "FALLING" : Front Descendant
                * "BOTH" : Front Montant + Front Descendant
                
            Il est possible de définir un délais d'expiration qui lorsqu'il est atteind
            annule l'attente d'une action.
                
            Si tous les parametres sont laisser par Defaut, le chagemant d'etat se fait
            sur le front Descendant car la résistance de tirrage est en Pull-UP.
            
            **Attention :** Cettte fonction est une fonction bloquante
        """
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug( v_dbg2, "f_btnWaitForEvent", self.f_btnWaitForEvent )
        
        ## raccourcis
        v_broche = self.v_broche

        ## Selection du front
        if v_front      == "RISING"     : v_rfb = GPIO.RISING
        elif v_front    == "FALLING"    : v_rfb = GPIO.FALLING
        elif v_front    == "BOTH"       : v_rfb = GPIO.BOTH
               
        ## dbg
        i_debug( v_dbg1, "v_rfb", v_rfb )
        i_debug( v_dbg1, "v_fnToExecute", v_fnToExecute )
        
        GPIO.wait_for_edge(v_broche, v_rfb, v_timeout)
        
        return v_fnToExecute()
        
        
        
def main() :
    """ Fonction pricipale """
    ##################################
    # Creation des fonctions de test #
    ##################################
    def f_fnTest1() : print( "Fonction fnTest1" )
    def f_fnTest2() : print( "Fonction fnTest2" )
    def f_fnTest3() : print( "Fonction fnTest3" )
    def f_fnTest4() : print( "Fonction fnTest4" )
    
    ##################################################################
    # Creation de l'instance + mise en place de la structure de test #
    ##################################################################
    
    ################################################
    # Instance et test avec les valeurs par defaut #
    ################################################
    i_testBtn = C_BtnPoussoir()
    
    ## test des fonctions :
    i_testBtn.f_gpioInit()
    i_testBtn.f_btnWaitForEvent( f_fnTest1 )
    
    del( i_testBtn )

    
if __name__ == '__main__':
    main()

    