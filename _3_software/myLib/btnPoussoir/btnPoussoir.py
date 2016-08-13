#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   :Nom du fichier:     btnPoussoir.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20160814

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
    sys.path.insert(0,'..')         # ajouter le repertoire precedent au path (non definitif)
                                    # pour pouvoir importer les modules et paquets parent
    from devChk.devChk import C_DebugMsg
   
except ImportError :
    print( "module devChk non present" )
    
try :
    import RPi.GPIO as GPIO
    
except ImportError :
    print("module 'RPi' non charge")
    
import time

class C_BtnPoussoir( object ) :
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
        self.v_prevTime = 0.0
        
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
        
        self.f_gpioDestructor()
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
        i_debug( v_dbg, "v_pudStatus", self.v_pudStatus )
        i_debug( v_dbg, "v_pudState", self.v_pudState )
        i_debug( v_dbg, "v_broche", self.v_broche )

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
                print(  "Atention ! La resistance de tirage interne n'est pas activee.\n",
                        "Pensez a mettre une resistance de tirage externe.\n\n",
                        "Rappel : les entree du Raspberry Pi sont en 3.3v\n" )
                GPIO.setup(v_broche, GPIO.IN)

        except NameError :
            print("GPIO error : f_gpioInit")

####

    def f_gpioDestructor(self):
        """
            Methode permettant de fermer proprement la gestion des GPIO du Rpi
            
            Cette methode doit etre appellee a la fin de l'utilisation
            des broches GPIO (avant de quitter le programme).
        """
        try :
            GPIO.remove_event_detect(self.v_broche)
            GPIO.cleanup()
            
        except NameError :
            print("GPIO error : f_gpioDestructor")
            
####

    def f_btnWaitForEvent( self, v_fnToExecute, v_front = "FALLING", v_timeout = 1 ) :
        """ **f_btnWaitForEvent(
                                [nom_de_la_fonction_a_executer -- Type 'function'],
                                [Etat_attendu_pour_le_declenchement_de_l'evenement -- Type 'str'],
                                [temps_du_time_Out_en_milisecondes -- Type 'int']
                                )**
        
            Cette methode attend un chagemant d'etat de la broche (front montant,
            front descandant, ou les deux) puis execute la fonction passee en parametre.
            
            les modes disponibles sont : 
            
                * 'RISING' : Front Montant
                * 'FALLING' : Front Descendant
                * 'BOTH' : Front Montant + Front Descendant
                
            Il est possible de definir un delais d'expiration qui lorsqu'il est atteind
            annule l'attente d'une action.
                
            Si tous les parametres sont laisser par Defaut, le chagemant d'etat se fait
            sur le front Descendant car la resistance de tirrage est en Pull-UP.
            
            ** Attention : ** Cettte fonction est une fonction bloquante
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
        i_debug( v_dbg, "v_fnToExecute", v_fnToExecute )
        i_debug( v_dbg, "v_rfb", v_rfb )
        i_debug( v_dbg, "v_timeout", v_timeout )
        
        GPIO.wait_for_edge(v_broche, v_rfb, v_timeout)
        
        return v_fnToExecute()
        
####
        
    def f_btnEvent_detect   (    self,
                                v_fnToExecute,
                                v_front = "FALLING",
                                v_bouncetime=200
                            ) :
        """ **f_btnEvent_detect(
                                [nom_de_la_fonction_a_executer -- Type 'function'],
                                [Etat_attendu_pour_le_declenchement_de_l'evenement -- Type 'str'],
                                [Duree_de_l'anti-rebond_(en milisecondes) -- Type 'int']
                                )**
        
            Cette methode s'execute lors d'un chagemant d'etat de la broche (front montant,
            front descandant, ou les deux) puis execute la fonction passee en parametre.
            C'est le callback.
            
            les modes disponibles sont : 
            
                * 'RISING' : Front Montant
                * 'FALLING' : Front Descendant
                * 'BOTH' : Front Montant + Front Descendant
                
            Il est possible de definir le delais durant lequel la fonction ne sera pas
            reexecute. on parles d'anti-rebond.
                
            Si tous les parametres sont laisser par Defaut, le chagemant d'etat se fait
            sur le front Descendant car la resistance de tirrage est en Pull-UP.
            
            *N.B :* Il s'agit ici d'une interpretation de : ::
                
                GPIO.add_event_detect()
                
            et non de : ::
            
                GPIO.event_detected()
        """
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug( v_dbg2, "f_btnEvent_detect", self.f_btnEvent_detect )
        
        ## raccourcis
        v_broche        = self.v_broche
        f_myCallBack    = self.f_myCallBack

        ## Selection du front
        if v_front      == "RISING"     : v_rfb = GPIO.RISING
        elif v_front    == "FALLING"    : v_rfb = GPIO.FALLING
        elif v_front    == "BOTH"       : v_rfb = GPIO.BOTH
               
        ## dbg
        i_debug( v_dbg, "v_fnToExecute", v_fnToExecute )
        i_debug( v_dbg, "v_rfb", v_rfb )
        i_debug( v_dbg, "v_bouncetime", v_bouncetime )
        
        ## Event detect
        GPIO.add_event_detect(  v_broche, v_rfb, bouncetime = v_bouncetime )
        if isinstance( v_fnToExecute, list ) :
        
            ## dbg
            i_debug( v_dbg, "Type de l'argument ", type(v_fnToExecute) )
            
            for i in range( len(v_fnToExecute) ) :
                GPIO.add_event_callback( v_broche, v_fnToExecute[i] )
        else :
            ## dbg
            i_debug( v_dbg, "Type de l'argument ", type(v_fnToExecute) )

            GPIO.add_event_callback( v_broche, callback = f_myCallBack(v_fnToExecute) )
           
       
####

    def f_btnEvent_detected(    self,
                                v_fnToExecute,
                                v_front = "FALLING",
                                v_howManyHit = 1,
                                v_bouncetime = 250
                            ) :
        """ **f_btnEvent_detected(
                                [nom_de_la_fonction_a_executer -- Type 'function'],
                                [Etat_attendu_pour_le_declenchement_de_l'evenement -- Type 'str'],
                                [nombre_d'impulsions_attendues -- Type 'int'],
                                [Duree_de_l'anti-rebond_(en_milisecondes) -- Type 'int']
                                )**
        
            Cette methode s'execute lors d'un chagemant d'etat de la broche (front montant,
            front descandant, ou les deux) puis execute la fonction passee en parametre.
            C'est le callback.
            
            les modes disponibles sont : 
            
                * 'RISING' : Front Montant
                * 'FALLING' : Front Descendant
                * 'BOTH' : Front Montant + Front Descendant
                
            La valeur de 'v_howManyHit' permet de d'attendre que l'utilisateur appuie un
            nombre de fois egal a cette valeur avant d'effectuer l'action passer par
            'v_fnToExecute'
                
            Si tous les parametres sont laisse par Defaut, le chagemant d'etat se fait
            sur le front Descendant car la resistance de tirrage est en Pull-UP.
            
            *N.B :* Il s'agit ici d'une interpretation de : ::
                
                
                GPIO.event_detected()
                
            et non de : ::
            
                GPIO.add_event_detect()
        """
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug( v_dbg2, "f_btnEvent_detected", self.f_btnEvent_detected )
        
        ## variables
        v_broche    = self.v_broche
        v_prev      = self.v_prevTime
        v_dBounce   = v_bouncetime / 1000
        v_timeStart = 0.0
        v_timeOut   = (v_howManyHit * v_dBounce) * 2
        v_hit       = 0

        ## Selection du front
        if v_front      == "RISING"     : v_rfb = GPIO.RISING
        elif v_front    == "FALLING"    : v_rfb = GPIO.FALLING
        elif v_front    == "BOTH"       : v_rfb = GPIO.BOTH
               
        ## dbg
        i_debug( v_dbg, "v_fnToExecute", v_fnToExecute )
        i_debug( v_dbg, "v_rfb", v_rfb )
        i_debug( v_dbg, "v_howManyHit", v_howManyHit )
        
        ## Event detected
        if GPIO.event_detected(v_broche):
            v_timeNow = time.time()
            if not v_prev : v_timeStart = v_prev = v_timeNow
            if (v_timeNow - v_timeStart) <= v_timeOut :
                if (v_timeNow - v_prev) >= v_dBounce :
                    v_hit += 1
                    if v_hit == v_howManyHit :
                        print( "TimeOut !" )
                        v_prev = v_timeNow
                        v_hit = 0
                        v_fnToExecute()
            else :
                v_hit = 0
                v_timeStart = v_prev = 0.0
        
    def f_myCallBack( self, v_broche = self.v_broche, v_fnToExecute ) :
        """
        """
        return v_fnToExecute()
        
####
        
def main() :
    """ Fonction pricipale """
    ##################################
    # Creation des fonctions de test #
    ##################################
    def f_fnTest1(var) : 
        print( "{} - {}".format(var, type(var)) )
        input( "Execution de Fonction fnTest1" )
        
    def f_fnTest2() : input( "Execution de Fonction fnTest2" )
    def f_fnTest3() : input( "Execution de Fonction fnTest3" )
    def f_fnTest4() : input( "Execution de Fonction fnTest4" )
    
    ##################################################################
    # Creation de l'instance + mise en place de la structure de test #
    ##################################################################
    
    ################################################
    # Instance et test avec les valeurs par defaut #
    ################################################
    
    ## f_gpioInit : valeurs par defaut
    input( "f_gpioInit : valeurs par defaut" )
    i_testBtn = C_BtnPoussoir()
    ## test des fonctions :
    i_testBtn.f_gpioInit()
    ## destructor
    del( i_testBtn )
    
    ## f_btnWaitForEvent : valeurs par defaut"
    # input( "f_btnWaitForEvent : valeurs par defaut" )
    # i_testBtn = C_BtnPoussoir()
    ## test des fonctions :
    # i_testBtn.f_gpioInit()
    # i_testBtn.f_btnWaitForEvent( f_fnTest1 )
    ## destructor
    # del( i_testBtn )

    ## f_btnEvent_detect : valeurs par defaut
    input( "f_btnEvent_detect : valeurs par defaut" )
    i_testBtn = C_BtnPoussoir()
    print( "j'attend" )
    ## test des fonctions :
    i_testBtn.f_gpioInit()
    i_testBtn.f_btnEvent_detect( f_fnTest2 )
    try: 
        while True :
            print( "j'attend !" )
            time.sleep(0.25)
            
    except KeyboardInterrupt :
            print( "Interrompu par l'utilisateur" )

    ## destructor
    del( i_testBtn )

    ## f_btnEvent_detected : valeurs par defaut
    # input( "f_btnEvent_detected : valeurs par defaut" )
    # i_testBtn = C_BtnPoussoir()
    ## test des fonctions :
    # i_testBtn.f_gpioInit()
    # try :
        # while True :
            # i_testBtn.f_btnEvent_detected( f_fnTest1 )
            # print( "j'attend !" )
    # except KeyboardInterrupt :
        # print( "inerrompu par l'utilisateur" )
    ## destructor
    # del( i_testBtn )

    
if __name__ == '__main__':
    main()

    