#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Infos
=====

   :Nom du fichier:     fakeLib.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20161026

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
   :**m_**:                 Matrice
   
####

Liste des libs
==============

    - os
    - sys
    - devChk
    - argparse
    
####

"""

import os, sys
sys.path.insert(0,'..')        # ajouter le repertoire precedent au path (non definitif)
                                # pour pouvoir importer les modules et paquets parent
try :
    from devChk.devChk import C_DebugMsg
    v_dbgChk = True
    i_dbg = C_DebugMsg()
   
except ImportError :
    print( "module devChk non present" )
    v_dbgChk = False
    
import argparse
import time

####

class C_ProgressBar( object ) :
    """ Class permettant de créer une barre de progression """
    def __init__( self, v_etiquette = "Progression", v_char = '#', v_width = 100 ) :
        """ **__init__()**
        
            Creation et initialisation des variables globales de cette Class
        """
        
        # declaration des variables
        self.v_char             = v_char
        self.v_width            = v_width
        self.v_etiquette        = v_etiquette
        self.v_percent          = 0
        self.v_prevValue        = 0
        self.v_firstStep        = False

####
        
    def __del__( self ) :
        """ **__del__()**
        
            Permet de terminer proprement l'instance de la Class courante
        
            il faut utilise : ::
            
                del [nom_de_l'_instance]
                
            *N.B :* Si l'instance n'est plus utilisee, cette methode est appellee 
            automatiquement.
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "__del__", self.__del__)
        
        ## Action
        v_className = self.__class__.__name__
        print("\n\t\tL'instance de la class {} est terminee".format(v_className))
        
####

    def f_pbPercent(self, v_valueMax, v_value = 0):
        """ **f_progress( int )**
        
            Permet de déssiner la barre de progression et d'afficher
            le pourcentage d'avancement
        """
        
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_pbPercent", self.f_pbPercent)
        
        ## Action
        if not v_value :
            v_ratio = False
            
        else :
            if v_valueMax < self.v_width :
                v_valueMax = v_valueMax * self.v_width + self.v_width //2
                v_value = v_value * self.v_width + self.v_width + self.v_width //2
                    # Si la valeur Max est trop petite, on multiplie la valeur Max
                    # et la valeur à représenter par la longueur de la barre de progression
                    # puis on ajoute la moitier de cette longueur

            v_ratio = self.f_setRatio( v_valueMax, v_value)
            
        if not v_ratio and not self.v_firstStep :          
            spaces = ' ' * (self.v_width-1)
            backspace = '\b' * (self.v_width+4)
            print(' {} [{}] {:03}%{}'.format(self.v_etiquette, spaces, 0, backspace), end='')
            sys.stdout.flush()
            self.v_firstStep = True
            pass
            
        elif not v_ratio and self.v_firstStep :
            pass
            
        else :
            spaces = ' ' * (self.v_width - v_ratio )
            backspace = '\b' * ((self.v_width+6))
            time.sleep(0.05)
            
            if not v_ratio == self.v_width :
                print("{}{}] {:03}%{}".format(self.v_char * v_ratio, spaces, v_ratio+1, backspace), end='')
                sys.stdout.flush()
            else :
                print("{}{}] 100%".format(self.v_char * v_ratio, spaces), end='\n')
####

    def f_pbRatio(self, v_valueMax, v_value = 0):
        """ **f_progress( int )**
        
            Permet de déssiner la barre de progression et d'afficher
            l'avancement sous forme de rapport ::
            
                1/25
                2/25
                3/25
                etc ...
        """
        
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_pbRatio", self.f_pbRatio)
        
        ## Action
        v_valueMaxReal = v_valueMax
        v_vMaxLen = len( str(v_valueMaxReal))
        v_valueReal = v_value + 1
        v_valueLen = len( str(v_valueReal) )
        v_lenDiff = v_vMaxLen - v_valueLen
        
        if not v_value :
            v_ratio = False
            
        else :
            if v_valueMax < self.v_width :
                v_valueMax = v_valueMax * self.v_width + self.v_width //2
                v_value = v_value * self.v_width + self.v_width + self.v_width //2
                    # Si la valeur Max est trop petite, on multiplie la valeur Max
                    # et la valeur à représenter par la longueur de la barre de progression
                    # puis on ajoute la moitier de cette longueur

            v_ratio = self.f_setRatio( v_valueMax, v_value)
            
        if not v_ratio and not self.v_firstStep :          
            spaces = ' ' * (self.v_width-1)
            backspace = '\b' * (self.v_width+4)
            print(" {} [{}] {}/{}{}".format (
                                                self.v_etiquette,
                                                spaces,
                                                '0'* v_vMaxLen,
                                                v_valueMaxReal,
                                                backspace),
                                                end=''
                                            )
            sys.stdout.flush()
            self.v_firstStep = True
            pass
            
        elif not v_ratio and self.v_firstStep :
            pass
            
        else :
            spaces = ' ' * ( self.v_width - v_ratio )
            backspace = '\b' * ((self.v_width+1+v_valueMaxReal*2))
            time.sleep(0.05)
            
            if not v_ratio == self.v_width :
                print("{}{}] {}{}/{}{}".format  (   self.v_char * v_ratio,
                                                    spaces,
                                                    '0'* v_lenDiff, 
                                                    v_valueReal,
                                                    v_valueMaxReal,
                                                    backspace),
                                                    end=''
                                                )
                sys.stdout.flush()
            else :
                print("{}{}] {}/{}".format  (   self.v_char * v_ratio,
                                                spaces,
                                                v_valueMaxReal,
                                                v_valueMaxReal),
                                                end='\n'
                                            )
####

    def f_setRatio( self, v_valueMax, v_value ) :
        """ **f_setRatio( int, int )**
        
            Permet de créer un ratio entre la valeur max, la longueur de la barre de
            progression, et la valeur à atteindre
        """
        
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_setRatio", self.f_setRatio)
        
        ## Action
        return ((v_value * self.v_width) // v_valueMax)

####
        
def f_dbg( v_bool, v_tittle, v_data ) :
    """ Fonction de traitemant du debug """
    if v_dbgChk :
        i_dbg.dbgPrint( v_bool, v_tittle, v_data )
        
####

def main() :
    """ Fonction principale """
    
    parser = argparse.ArgumentParser()
    parser.add_argument( "-d", "--debug", action='store_true', help="activation du mode debug")
    parser.add_argument( "-p", "--progress", action='store_true', help="activation du mode debug")
                        
    args = parser.parse_args()
    
    if args.debug :
        if v_dbgChk :
            i_dbg.f_setAffichage( True )
            print( "Mode Debug activer" )
        else :
            print( "Le mode Debug ne peut pas etre active car le module n'est pas present")
            
    if args.progress :
        i_ist = C_ProgressBar(  )
        v_valueMax = 100
        for i in range( v_valueMax ) :
            i_ist.f_pbRatio( v_valueMax, i )

        
        del i_ist


    
if __name__ == '__main__':
    main()


