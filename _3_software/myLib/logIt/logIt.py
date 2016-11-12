#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Infos
=====

   :Nom du fichier:     logIt.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20161112

####

   :Licence:            CC-BY-NC-SA
   :Liens:              https://creativecommons.org/licenses/by-nc-sa/4.0/

####

    :dev langage:       Python 3.4

####

List des Libs
=============

    * os
    * sys
    * devChk
    * datetime
    * copy
    
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

Class C_logIt
=============

"""

# from __future__ import absolute_import  # Permet d'importer en chemin abslolu ou relatif
                                        # # doit etre importer en premier

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
    
from datetime import datetime
from copy import deepcopy

#####

class C_logIt( object ) :
    """ Classe permettant lister et de journaliser des evenement externe """
    
    def __init__( self ) :
        """ **__init()**
        
            Creation et initialisation des variables globales de cette Class
        """
        
        ## declaration des variables
        self.v_timeCode         = False
        self.v_shortTimeCode    = False
        self.v_msg              = False
        self.l_taskTitle        = []
        self.d_task             = {}
        
####
        
    def __del__(self) :
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

        ## dbg
        f_dbg( v_dbg, v_className, v_tittle = False  )

####

    def f_setTimeCode( self ) :
        """ **setTimeCode()**
        
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
                
            La version courte (v_shortTimeCode) et sous la forme : ::
            
                'yyyyMMdd-hh.mm'
                
        """
        
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_setTimeCode", self.f_setTimeCode)
        
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
        f_dbg(v_dbg, "v_timeCode", self.v_timeCode)
        f_dbg(v_dbg, "v_shortTimeCode", self.v_shortTimeCode)

####
                                                                        
    def f_setTaskTitle(self, v_taskTitle ) :
        """ **f_setTaskTitle( self, str)**
        
            Permet de recuperer le nom de la tache en cours et de l'ajouter
            a la liste 'l_setTaskTitle'.
        """
        
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_setTaskTitle", self.f_setTaskTitle)
        
        ## Action
        if not v_taskTitle in self.l_taskTitle :
            self.l_taskTitle.append( v_taskTitle)
            
            ## dbg
            f_dbg(v_dbg, "l_taskTitle", self.l_taskTitle)
            
####
            
    def f_setDTask(self, v_taskTitle, v_task, v_taskDetail = False ) :
        """ **f_setDTask(str, str, str)**
        
            Permet de creer un dictionnaire comportant les informations qui devrons etres
            journalisee.
        """
        
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_setDTask", self.f_setDTask)
        
        ## Action
        if not v_taskTitle in self.d_task.keys() :
            l_taskList = []
            self.d_task[v_taskTitle] = deepcopy(l_taskList)
            self.d_task[v_taskTitle].append( deepcopy(l_taskList))
            self.f_setTimeCode()
            self.d_task[v_taskTitle].append( self.v_timeCode )

        if v_taskDetail :
            if not v_taskDetail in self.d_task[v_taskTitle] :
                if len( self.d_task[v_taskTitle] ) == 3 :
                    self.d_task[v_taskTitle][2] = v_taskDetail
                else :
                    self.d_task[v_taskTitle].append( v_taskDetail )

        if not v_task in self.d_task[v_taskTitle][0] :
            self.d_task[v_taskTitle][0].append( v_task )

        ## dbg
        f_dbg(v_dbg, "d_task", self.d_task)
            
####

    def f_setMsg( self ) :
        """ **f_setMsg()**
        
            Permet de creer le message qui sera utilise par la methode 'makeLog'
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_setMsg", self.f_setMsg)
        
        ## Action
        for key in self.d_task.keys() :
            if not self.v_msg :
                self.v_msg = "{}\n{}\n\n".format( key, '=' * len( key ) )
            else :
                self.v_msg += "{}\n{}\n\n".format( key, '=' * len( key ) )
                
            
            if len( self.d_task[key] ) == 3 :
                self.v_msg += "{}\n\n".format( self.d_task[key][2] )
            
            for i in range( len( self.d_task[key][0] )) :
                self.v_msg += "{}{}\n".format( self.d_task[key][1], self.d_task[key][0][i] )
                
            self.v_msg += "\n{}\n\n".format( '#' * 80 )
            
        ## dbg
        f_dbg(v_dbg, "v_msg", self.v_msg)
        
####

    def f_wrLog( self ) :
        """ **f_wrLog()**
        
            Permet de creer le fichier journal. Le nom du fichier sera sous la forme : ::
            
                'shortTimeCode.log'.
        """
        
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_wrLog", self.f_wrLog)
        
        ## Action
        self.f_setMsg()
        self.f_makeDir()
        v_logDest = "./log/{}.log".format( self.v_shortTimeCode)
        with open(v_logDest, 'a') as i_logFile :
            i_logFile.write( self.v_msg )
            
####

    def f_makeDir( self ) :
        """ **f_makeDir()**
        
            Permet de creer le dossier 'log' si il n'existe pas
        """
    l_listDir = os.listdir()
    if not 'log' in l_listDir :
        os.makedirs(os.path.normpath('./log'), mode=0o777, exist_ok=True)
               
####

def f_dbg( v_bool, v_data, v_tittle = False  ) :
    """ Fonction de traitemant du debug """
    if v_dbgChk and v_tittle :
        i_dbg.dbgPrint( v_bool, v_tittle, v_data )
        
    elif v_dbgChk and not v_tittle :
        i_dbg.dbgDel( v_bool, v_data)
        
####

def main() :
    """ Fonction principale """
    if v_dbgChk :
        i_dbg.f_setAffichage( True )
    
####

if __name__ == '__main__':
    main()