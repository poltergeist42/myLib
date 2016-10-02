#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Infos
=====

   :Nom du fichier:     fakeLib.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20161002

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
   
objectif
========

Cette Librairie ne fait rien. Elle n'existe que pour pouvoir tester certain
elements des autres lib en cours de developpement.

La class est fictive, mais elle doit tout de meme etre commenter pour pourvoir generer la
documentation de facon automatique avec Sphinx et et ainsi pouvoir tester des elements de
traitemant de la documentation.
    
    
"""

try :
    import os, sys
    sys.path.insert(0,'..')         # ajouter le repertoire precedent au path (non définitif)
                                    # pour pouvoir importer les modules et paquets parent
    from devChk.devChk import C_DebugMsg
   
except ImportError :
    print( "module non present" )
    
import argparse

class C_FakeLib( object ) :
    """ Class fictive permettant de faire des teste pour les autres lib
        en cours de developement.
    """
    def __init__( self, v_debug=False ) :
        """ 
            **__init()**
        
            Creation et initialisation des variables globales de cette Class
        """
        
        ## Creation de l'instance pour les message de debug
        self.i_dbg = C_DebugMsg(v_debug)
        
####
        
    def __del__(self) :
        """
            **__del__()**
        
            Permet de terminer proprement l'instance de la Class courante
        
            il faut utilise : ::
            
                del [nom_de_l'_instance]
                
            *N.B :* Si l'instance n'est plus utilisee, cette methode est appellee 
            automatiquement.
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "__del__", self.__del__)
        
        ## Action
        v_className = self.__class__.__name__
        print("\n\t\tL'instance de la class {} est terminee".format(v_className))
        
    def f_doNothing( self ) :
        """ Cette fonction ne fait rien d'autre que de retourner 'True" """
        return True
        
def main() :
    """ Fonction principale """
    parser = argparse.ArgumentParser()
    parser.add_argument( "-d", "--debug", action='store_true', help="activation du mode debug")
                        
    args = parser.parse_args()
    if args.debug :
        print( "Mode Debug activer" )
        i_ist = C_FakeLib( True )
    else :
        i_ist = C_FakeLib( False )
    
    i_ist.f_doNothing()
        