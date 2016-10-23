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
   
objectif
========

    Cette Librairie ne fait rien. Elle n'existe que pour pouvoir tester certains
    elements des autres lib en cours de developpement.

    La class est fictive, mais elle doit tout de meme etre commenter pour pourvoir generer
    la documentation de facon automatique avec Sphinx et ainsi pouvoir tester des elements
    de traitemant de la documentation.
    
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
                        
    args = parser.parse_args()
    
    if args.debug :
        if v_dbgChk :
            i_dbg.f_setAffichage( True )
            print( "Mode Debug activer" )
        else :
            print( "Le mode Debug ne peut pas etre active car le module n'est pas present")


    
if __name__ == '__main__':
    main()


