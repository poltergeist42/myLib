#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Infos
=====

   :Nom du fichier:     logIt.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20161011

####

   :Licence:            CC-BY-NC-SA
   :Liens:              https://creativecommons.org/licenses/by-nc-sa/4.0/

####

    :dev language:      Python 3.4
    
####

Class C_logIt
=============
    
"""
try :
    import os, sys
    sys.path.insert(0,'..')         # ajouter le repertoire precedent au path (non définitif)
                                    # pour pouvoir importer les modules et paquets parent
    from devChk.devChk import C_DebugMsg
   
except ImportError :
    print( "module non present" )
    

import argparse
from datetime import datetime
from copy import deepcopy

#####
class C_logIt( object ) :
    """ Classe permettant lister et de journaliser des evenement externe """
    def __init__( self ) :
       """ 
            **__init()**
        
            Creation et initialisation des variables globales de cette Class
        """
        
        ## Creation de l'instance pour les message de debug
        self.i_dbg = C_DebugMsg(v_debug)
                
        ## declaration des variables
        self.v_timeCode         = False
        self.v_shortTimeCode    = False
        self.v_msg              = False
        self.l_taskTitle        = []
        self.d_task             = {}
        
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

####

    def f_setTimeCode( self ) :
        """ **setTimeCode**()
        
            Permet de creer le timeCode qui sera ajouter devant chaque nouvelle entree du
            journal. Se Time code est sous la forme : ::
                '[ yyyyMMdd-hh.mm.ss ] : '
                
            avec :
                :yyyy:      l'annee (sur 4 digit)
                :MM:        le mois (sur 2 digit)
                :dd:        le jour (sur 2 digit)
                :hh:        l'heure (sur 2 digit)
                :mm:        les minutes (sur 2 digit)
                :ss:        Les secondes (sur 2 gigits)
                
            **N.B** : la version courte (v_shortTimeCode) et sous la forme : ::
                'yyyyMMdd-hh.mm'
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_setTimeCode", self.f_setTimeCode)
        
        ## Action
        v_date = datetime.now()
        
        self.v_timeCode = "[ {}{:02}{:02}-{:02}.{:02}.{:02} ] : ".format(   v_date.year,
                                                                            v_date.month,
                                                                            v_date.day,
                                                                            v_date.hour,
                                                                            v_date.minute,
                                                                            v_date.second
                                                                        )
                                                                        
        self.v_shortTimeCode = "{}{:02}{:02}-{:02}.{:02}".format(   v_date.year,
                                                                    v_date.month,
                                                                    v_date.day,
                                                                    v_date.hour,
                                                                    v_date.minute,
                                                                )
        ## dbg
        i_debug(v_dbg, "v_timeCode", self.v_timeCode)
        i_debug(v_dbg, "v_shortTimeCode", self.v_shortTimeCode)

####
                                                                        
    def f_setTaskTitle(self, v_taskTitle ) :
        """ **f_setTaskTitle**( self, str)
        
            Permet de recuperer le nom de la tache en cours et de l'ajouter
            a la liste 'l_setTaskTitle'.
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_setTaskTitle", self.f_setTaskTitle)
        
        ## Action
        if not v_taskTitle in self.l_taskTitle :
            self.l_taskTitle.append( v_taskTitle)
            
            ## dbg
            i_debug(v_dbg, "l_taskTitle", self.l_taskTitle)
            
####
            
    def f_setDTask(self, v_taskTitle, v_task, v_taskDetail = False ) :
        """ **f_setDTask**(str, str, str)
        
            Permet de creer un dictionnaire comportant les informations qui devrons etre
            journalisee.
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_setDTask", self.f_setDTask)
        
        ## Action
        if not v_taskTitle in self.d_task.keys() :
            l_taskList = []
            self.d_task[v_taskTitle] = deepcopy(l_taskList)
            self.d_task[v_taskTitle].append( deepcopy(l_taskList))
            
        if v_taskDetail :
            if not v_taskDetail in self.d_task[v_taskTitle] :
                self.d_task[v_taskTitle].append( v_taskDetail )
            
        if not v_task in self.d_task[v_taskTitle][0] :
            self.d_task[v_taskTitle][0].append( v_task )

        ## dbg
        i_debug(v_dbg, "d_task", self.d_task)
            
####

    def f_setMsg( self ) :
        """ **f_setMsg**()
        
            Permet de creer le message qui sera utilise par la methode 'makeLog'
        """
        for key in self.d_task.keys() :
            if not self.v_msg :
                self.v_msg = "{}\n{}\n\n".format( key, '=' * len( key ) )
            else :
                self.v_msg += "{}\n{}\n\n".format( key, '=' * len( key ) )
                
            
            if len( self.d_task[key] ) == 2 :
                self.v_msg += "{}\n\n".format( self.d_task[key][1] )
            
            for i in range( len( self.d_task[key][0] ) :
                self.v_msg += "{}{}\n".format( self.v_timeCode, self.d_task[key][0][i] )
                
            self.v_msg += "\n{}\n\n".format( '#' * 80 )
            
        ## dbg
        i_debug(v_dbg, "v_msg", self.v_msg)
        
####

    def f_wrLog( self ) :
        """ **f_makeLog**()
        
            Permet de creer le fichier journal. Le nom du fichier sera sous la forme : ::
                'shortTimeCode.log'.
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_wrLog", self.f_wrLog)
        
        ## Action
        v_logDest = "/log/{}.log".format( self.shortTimeCode)
        with open(v_logDest, 'a') as i_logFile :
            i_logFile.write( self.v_msg )
        
        
####

def main() :
    """ Fonction principale """
    
####ü

if __name__ == '__main__':
    main()