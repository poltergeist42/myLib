#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Infos
=====

   :Nom du fichier:     fakeLib.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20161023

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
    def __init__( self, v_char = '#', v_width = 100 ) :
        """ **__init__()**
        
            Creation et initialisation des variables globales de cette Class
        """
        
        # declaration des variables
        self.v_char = v_char
        self.v_width = v_width

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

    def f_progressPercent(self, v_valueMax, v_value = 0):
        """ **f_progress( int )**
        
            Permet de déssiner la barre de progression
        """
        
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_progress", self.f_progress)
        
        ## Action
        spaces = ' ' * (self.v_width-1)
        backspace = '\b' * (self.v_width+4)
        v_percent = 0
        print('Starting [{}] {:03}%{}'.format(spaces, v_percent, backspace), end='')
        sys.stdout.flush()
        steps = v_valueMax / self.v_width
        for i in range(v_valueMax):
            v_percent+=1
            spaces = ' ' * (self.v_width - i )
            backspace = '\b' * ((self.v_width+6)-i)
            time.sleep(0.1)
            if i % steps == 0:
                if not v_percent == self.v_width :
                    print("{}{}] {:03}%{}".format(self.v_char, spaces, v_percent, backspace), end='')
                    sys.stdout.flush()
                else :
                    print("{}{}] {:03}%".format(self.v_char, spaces, v_percent), end='\n')
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
        i_ist = C_ProgressBar()
        i_ist.f_progressPercent( 150 )

        
        del i_ist


    
if __name__ == '__main__':
    main()


