#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 

infos
=====
    
    :Nom du fichier:     btnPoussoir.py
    :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
    :Version:            20161022

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
    :**m_**:                 matrice
    
####

Class C_BtnPoussoir
===================
    
"""
import os, sys
sys.path.insert(0,'..')         # ajouter le repertoire precedent au path (non definitif)
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

try :    
    import time, argparse
    from os import system
    
except ImportError :
    print("module non charge")

####

class C_BtnPoussoir( object ) :
    """ **C_BtnPoussoir()**
    
        Class permettant de gerer les boutons poussoirs
    """
    def __init__( self) :
        """ ::
        
                __init()
        
            Creation et initialisation des variables globales de cette Class
        """
        
        ## declaration des variables
        self.v_broche = False
        self.v_pudStatus = ""
        self.v_pudState = True
        self.v_prev = False
        self.v_timeStart = False
        self.v_bouncetime = False
        self.v_hit = False
        
####
        
    def __del__( self ) :
        """ ::
        
                __del__()
        
            Permet de terminer proprement l'instance de la Class courante
        
            il faut utilise : ::
            
                del [nom_de_l'_instance]
                
            *N.B :* Si l'instance n'est plus utilisee, cette methode est appellee 
            automatiquement.
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 0
        f_dbg( v_dbg2, "__del__", self.__del__ )
        
        ## Action
        self.f_gpioDestructor()
        v_className = self.__class__.__name__
        
        ## dbg
        f_dbg( v_dbg, v_className, v_tittle = False  )
####
        
    def f_gpioInit(self, v_gpio = 21, v_pullUpDown = True, v_pullToUpOrDown = "UP"):
        """ ::
        
                f_gpioInit( GPIO_Channel, Boolean, str )
            
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
        f_dbg( v_dbg2, "f_gpioInit", self.f_gpioInit )

        
        self.v_pudStatus = v_pullToUpOrDown
        self.v_pudState = v_pullUpDown
        self.v_broche = v_gpio
        
        ## raccourcis
        v_broche = self.v_broche

        
        ## dbg
        f_dbg( v_dbg, "v_pudStatus", self.v_pudStatus )
        f_dbg( v_dbg, "v_pudState", self.v_pudState )
        f_dbg( v_dbg, "v_broche", self.v_broche )

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
        """ ::
        
                f_gpioDestructor()
        
            Methode permettant de fermer proprement la gestion des GPIO du Rpi
            
            Cette methode doit etre appellee a la fin de l'utilisation
            des broches GPIO (avant de quitter le programme).
        """
        try :
            GPIO.remove_event_detect(self.v_broche)
            GPIO.cleanup(self.v_broche)
            
        except NameError :
            print("GPIO error : f_gpioDestructor")
            
####

    def f_setFront( self, v_front ) :
        """ ::
        
                f_setFront( [Etat_attendu_pour_le_declenchement_de_l'evenement -- Type 'str'])
        
            Cette methode permet de configurer le changement d'etat attendue pour
            l'execution de l'action.
            
            les modes disponibles sont : 
            
                * 'RISING' : Front Montant
                * 'FALLING' : Front Descendant
                * 'BOTH' : Front Montant + Front Descendant
                
            Si 'v_front == False' alors 'v_rfb = GPIO.FALLING'

        """
        if v_front      == "RISING"     : v_rfb = GPIO.RISING
        elif v_front    == "FALLING"    : v_rfb = GPIO.FALLING
        elif not v_front                : v_rfb = GPIO.FALLING
        elif v_front    == "BOTH"       : v_rfb = GPIO.BOTH
        
        return v_rfb

####

    def f_waitForEvent( self, v_fnToExecute, v_front = "FALLING", v_timeout = 1 ) :
        """ ::
        
                f_waitForEvent  (
                                    [nom_de_la_fonction_a_executer -- Type 'function'],
                                    [Etat_attendu_pour_le_declenchement_de_l'evenement -- Type 'str'],
                                    [temps_du_time_Out_en_milisecondes -- Type 'int']
                                )
        
            Cette methode attend un chagemant d'etat de la broche (front montant,
            front descandant, ou les deux) puis execute la fonction passee en parametre.
            
                
            Il est possible de definir un delais d'expiration qui lorsqu'il est atteind
            annule l'attente d'une action.
                
            Si tous les parametres sont laisses par Defaut, le chagemant d'etat se fait
            sur le front Descendant car la resistance de tirrage est en Pull-UP.
            
            ** Attention :** Cettte fonction est une fonction bloquante
        """
        
        v_dbg = 1
        v_dbg2 = 1
        f_dbg( v_dbg2, "f_waitForEvent", self.f_waitForEvent )
        
        ## raccourcis
        v_broche = self.v_broche

        ## Selection du front
        v_rfb = self.f_setFront( v_front )

               
        ## dbg
        f_dbg( v_dbg, "v_fnToExecute", v_fnToExecute )
        f_dbg( v_dbg, "v_rfb", v_rfb )
        f_dbg( v_dbg, "v_timeout", v_timeout )
        
        GPIO.wait_for_edge(v_broche, v_rfb, v_timeout)
        
        return v_fnToExecute()
        
####

    def f_addEventDetect    (   self,
                                v_front = "FALLING",
                                v_callBack = False,
                                v_bouncetime = 250
                            ) :
        """ ::
        
                f_addEventDetect    (
                                        [Etat_attendu_pour_le_declenchement_de_l'evenement -- Type 'str'],
                                        [allback -- Type 'bool' ou 'function.__name__'],
                                        [Duree_de_l'anti-rebond_(en milisecondes) -- Type 'int']
                                    )
                                    
            Cette methode permet d'initaliser le 'event_detect'. 
            
            Cette methode est appelee par 'f_onEventDetect' et doit etre appelee 
            specifiquement avant l'utilisation de 'f_ifDetected'

        """
        v_dbg = 1
        v_dbg2 = 1
        f_dbg( v_dbg2, "f_addEventDetect", self.f_addEventDetect )
        
        ## variables
        v_broche    = self.v_broche
        self.v_bouncetime = v_bouncetime


        ## Selection du front
        v_rfb = self.f_setFront( v_front )
               
        ## dbg
        f_dbg( v_dbg, "v_rfb", v_rfb )
        
        ## init Event detect
        if not v_callBack :
            return GPIO.add_event_detect    (   v_broche,
                                                v_rfb,
                                                bouncetime = v_bouncetime
                                            )
        else :
            # GPIO.add_event_callback
            return GPIO.add_event_detect    (   v_broche,
                                                v_rfb,
                                                callback = v_callBack,
                                                bouncetime = v_bouncetime
                                            )

####
        
    def f_onEventDetect( self, v_fnToExecute, v_front = "FALLING" ) :
        """ ::
            
                f_onEventDetect(
                                    [nom_de_la_fonction_a_executer -- Type 'function'],
                                    [Etat_attendu_pour_le_declenchement_de_l'evenement -- Type 'str'],
                                    [Duree_de_l'anti-rebond_(en milisecondes) -- Type 'int']
                                )
        
            Cette methode s'execute lors d'un chagemant d'etat de la broche (front montant,
            front descandant, ou les deux) puis execute la fonction passee en parametre.
            C'est le callback.
            
            Le front ecoute est renvoyer par 'f_setFront'
                
            Le delais durant lequel la fonction ne sera pas
            reexecute (l'anti-rebond), se configure lors de l'appel 
            de la fonction 'f_addEventDetect'.
                
            Si tous les parametres sont laisser par Defaut, le chagemant d'etat se fait
            sur le front Descendant car la resistance de tirrage est en Pull-UP.
            
        """
        v_dbg = 1
        v_dbg2 = 1
        f_dbg( v_dbg2, "f_onEventDetect", self.f_onEventDetect )
        
        ## raccourcis
        v_broche        = self.v_broche
        
        ## Selection du front
        v_rfb = self.f_setFront( v_front )

        ## dbg
        f_dbg( v_dbg, "v_fnToExecute", v_fnToExecute )
        f_dbg( v_dbg, "v_rfb", v_rfb )
                
######
        
        def f_myCallBack( channel ) :
            """ ::
            
                    f_myCallBack(   GPIO_Channel -- Type 'int',
                                    [nom_de_la_fonction_a_executer -- Type 'function'] )
                                
                Cette methode permet de ne renvoyer que la fonction passee en argument sans y
                ajouter le numero de broche en argument 'cache'
                
                'channel' et affectee directement par la lib 'RPi.GPIO'. cette affectation
                correspond au numero de la broche.
            """
            ##dbg
            f_dbg( v_dbg2, "f_myCallBack", f_myCallBack )
            f_dbg( v_dbg, "v_fnToExecute", v_fnToExecute )
            f_dbg( v_dbg, "channel", channel )
            
            f_dbg( v_dbg, "avant la fonction ...",  v_fnToExecute.__name__)
            
            v_fnToExecute()
            
            f_dbg( v_dbg, "... apres la fonction",  v_fnToExecute.__name__)
    
######
        
        ## Event detect

        if isinstance( v_fnToExecute, list ) :
        
            # ## dbg
            # f_dbg( v_dbg, "Type de l'argument ", type(v_fnToExecute) )
            # self.f_addEventDetect( v_broche )
            
            # for i in range( len(v_fnToExecute) ) :
                # GPIO.add_event_callback( v_broche, v_callBack = v_fnToExecute[i] )
                
            print( "\nLe mode multi-Callback ne fonctionne pas pour l'instant\n" )

        else :
            ## dbg
            f_dbg( v_dbg, "Type de l'argument ", type(v_fnToExecute) )

            self.f_addEventDetect( v_callBack = f_myCallBack )

####
        
    def f_ifDetected(    self,
                                v_fnToExecute,
                                v_howManyHit = 2,
                                v_timeOut = 3
                            ) :
        """ ::
        
                f_ifDetected(
                                [nom_de_la_fonction_a_executer -- Type 'function'],
                                [nombre_d'impulsions_attendues -- Type 'int'],
                                [Duree_du_time_Out_(en_secondes) -- Type 'int']
                            )
        
            Cette methode permet de l'ancer une action apres un certain nombre d'appuis
            sur le bouton pousoir.
                
            La valeur de 'v_howManyHit' permet de d'attendre que l'utilisateur appuie un
            nombre de fois egal a cette valeur avant d'effectuer l'action passer par
            'v_fnToExecute'
            
            Le timOut permet de determiner le temps maximum pour effectuer l'ensemble des
            impulsions
                
            Si tous les parametres sont laisses par Defaut :
            
            * le chagemant d'etat se fait sur le front Descendant car la resistance
              de tirrage est en Pull-UP.
              
            * Le nombre d'impulsion attendu est de 2
            
            * Le le timeOut est de 3 secondes
            
            Cette methode peut etre placer dans une boucle
            
            **N.B :** il faut utiliser 'f_addEventDetect' avant la boucle pour pouvoir
            utiliser cette methode
        """
        v_dbg = 0
        v_dbg2 = 0
        v_dbg3 = 0
        f_dbg( v_dbg2, "f_ifDetected", self.f_ifDetected )
        
        ## variables
        v_dBounce   = self.v_bouncetime / 1000
            
        ## dbg
        f_dbg( v_dbg, "v_fnToExecute", v_fnToExecute )
        f_dbg( v_dbg, "v_howManyHit", v_howManyHit )
        
        ## Event detected
        if GPIO.event_detected( self.v_broche ) :
            v_timeNow = time.time()
            self.v_hit += 1
            f_dbg( v_dbg3, "self.v_hit", self.v_hit )
            f_dbg( v_dbg3, "v_timeNow", v_timeNow )

            if not self.v_prev :
                self.v_timeStart = self.v_prev = v_timeNow
                f_dbg( v_dbg3, "not v_prev - v_timeStart : ", self.v_timeStart )

            v_timeDiff = v_timeNow - self.v_prev
            f_dbg( v_dbg3, "v_timeDiff", v_timeDiff )

            if (v_timeDiff >= v_dBounce) :
                if (v_timeDiff <= v_timeOut) :
                                    
                    ##dbg
                    f_dbg( v_dbg3, "v_dBounce", v_dBounce )
                    f_dbg( v_dbg3, "v_timeDiff", v_timeDiff )
                    f_dbg( v_dbg3, "v_timeOut", v_timeOut )

                    self.v_prev = v_timeNow

                    if self.v_hit == v_howManyHit :
                        self.v_prev = self.v_timeStart = False
                        self.v_hit = False
                        v_fnToExecute()
                        
                else :
                    print( "\nTimeOut ! Reinitialisation du compteur\n" )
                    self.v_prev = self.v_timeStart = False
                    self.v_hit = False

####

def f_dbg( v_bool, v_data, v_tittle = False  ) :
    """ Fonction de traitemant du debug """
    if v_dbgChk and v_tittle :
        i_dbg.dbgPrint( v_bool, v_tittle, v_data )
        
    elif v_dbgChk and not v_tittle :
        i_dbg.dbgDel( v_bool, v_data)
        
####
        
def main() :
    """ Fonction pricipale

        Ici vont etre tester toutes les methodes de la classe.
        
        **Attention !** La fonction de test 'f_fnTest1' executant un 'input()', il ne faut
        pas oubliez d'appuyer sur la touche 'entree' lors des appel a cette fonction.
        
        Chaque fonction testee, attend un appuie sur la touche 'entree' avant de lancer
        la sequense.
        
        Le script utilise de options :
        
        :'--help' ou '-h':
            Affiche l'aide pour les options
            
        :'--debug' ou '-d':
            Active le mode debug sur l'instance
            
        :'--number' ou '-n':
            Prend un entier en argument.
            Permet d'executer la fonction correspondant au numero de l'argument
    """
    parser = argparse.ArgumentParser()
    parser.add_argument( "-n", "--number", help="numero de la fonction a executer")
    parser.add_argument( "-d", "--debug", action='store_true', help="activation du mode debug")
                        
    args = parser.parse_args()
    
    def f_startInstance() :
        if args.debug :
            if v_dbgChk :
                i_dbg.f_setAffichage( True )
                print( "Mode Debug activer" )
            else :
                print( "Le mode Debug ne peut pas etre active car le module n'est pas present")

            i_testBtn = C_BtnPoussoir()
                
            return i_testBtn
            
    system( "clear" )
    
    ##################################
    # Creation des fonctions de test #
    ##################################
    def f_fnTest1() :
        print( "\nAppuyer sur la touche 'Entree' pour sortir de la fonction 'f_fnTest1'\n" )
        input( "Execution de Fonction fnTest1\n" )
        
    def f_fnTest2() : print( "\nExecution de Fonction fnTest2\n" )
    def f_fnTest3() : print( "\nExecution de Fonction fnTest3\n" )
    def f_fnTest4() : print( "\nExecution de Fonction fnTest4\n" )
    
    ##################################################################
    # Creation de l'instance + mise en place de la structure de test #
    ##################################################################

    ################################################
    # Instance et test avec les valeurs par defaut #
    ################################################

    def f_defautFN1() :
        ## f_gpioInit : valeurs par defaut
        input( "f_gpioInit : valeurs par defaut" )
        i_testBtn = f_startInstance()
        # test des fonctions :
        i_testBtn.f_gpioInit()
        # destructor
        del( i_testBtn )
    
####
    
    def f_defautFN2() :
        ## f_waitForEvent : valeurs par defaut"
        input( "f_waitForEvent : valeurs par defaut" )
        i_testBtn = f_startInstance()
        # test des fonctions :
        i_testBtn.f_gpioInit()
        print( "\nIl ne se passe rien tan que l'on appuis pas sur le bouton\n" )
        i_testBtn.f_waitForEvent( f_fnTest1 )
        # destructor
        del( i_testBtn )

####
    
    def f_defautFN3() :
        ## f_onEventDetect : valeurs par defaut
        input( "f_onEventDetect : valeurs par defaut" )
        i_testBtn = f_startInstance()
        # test des fonctions :
        i_testBtn.f_gpioInit()
        i_testBtn.f_onEventDetect( f_fnTest2 )
        try: 
            while True :
                print( "j'attend !" )
                time.sleep(0.25)
                
        except KeyboardInterrupt :
                print( "\nInterrompu par l'utilisateur" )
                pass

        # destructor
        del( i_testBtn )

####

    def f_defautFN4() :
        ## f_ifDetected : valeurs par defaut
        input( "f_ifDetected : valeurs par defaut" )
        i_testBtn = f_startInstance()
        # test des fonctions :
        i_testBtn.f_gpioInit()
        i_testBtn.f_addEventDetect()
        try :
            while True :
                i_testBtn.f_ifDetected( f_fnTest2 )
                print( "J'attend !" )
                time.sleep(0.25)

        except KeyboardInterrupt :
            print( "inerrompu par l'utilisateur" )
            pass
        # destructor
        del( i_testBtn )

####
    
    ###############################################
    # Instance et test avec les valeurs modifiees #
    ###############################################
    
    # def f_modifieesFN5() :
        # ## f_onEventDetect : valeurs modifiees
        # input( "f_onEventDetect : valeurs modifiees" )
        # i_testBtn = f_startInstance()
        # # test des fonctions :
        # l_lstFnTest = [ f_fnTest2, f_fnTest3, f_fnTest4 ]
        # i_testBtn.f_gpioInit()
        # i_testBtn.f_onEventDetect( l_lstFnTest )
        # try: 
            # while True :
                # print( "j'attend !" )
                # time.sleep(0.25)
                
        # except KeyboardInterrupt :
                # print( "\nInterrompu par l'utilisateur" )
                # pass

        # # destructor
        # del( i_testBtn )
    
    d_args = {  '1':f_defautFN1, '2':f_defautFN2, '3':f_defautFN3,
                '4':f_defautFN4 }

    d_args[args.number]()
    
if __name__ == '__main__':
    main()

    