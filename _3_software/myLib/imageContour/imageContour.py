#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   :Nom du fichier:     imageContour.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20160829

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
    print( "module non present" )
