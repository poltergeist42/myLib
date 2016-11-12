#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""


Infos
=====

   :Nom du fichier:     libReplicator.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20161112

####

   :Licence:            CC-BY-NC-SA
   :Liens:              https://creativecommons.org/licenses/by-nc-sa/4.0/

####

   :Licence:            CC-BY-NC-SA
   :Liens:              https://creativecommons.org/licenses/by-nc-sa/4.0/

####

    :dev langage:       Python 3.4

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

Class C_bougeTonFile
====================
   
"""

from __future__ import absolute_import  # Permet d'importer en chemin abslolu ou relatif
                                        # doit etre importer en premier

import os, sys
sys.path.insert(0,'..')                 # ajouter le repertoire precedent au path (non définitif)
                                        # pour pouvoir importer les modules et paquets parent
import argparse
import shutil

from os import system

try :
    from myLib.devChk.devChk import C_DebugMsg
    
    from myLib.devChk.devChk import C_GitChk
                                            # Arboressence de l'import :
                                            # _3_software           <-- origin du projet
                                            #  |
                                            #  +- myLib             <-- paquet
                                            #  |  |
                                            #  |  +- devChk         <-- sous-paquet
                                            #  |  |  |
                                            #  |  |  +- devChk.py   <-- librairie
                                            #  |  |  |  |
                                            #  |  |  |  +- C_GitChk <-- class 
                                            #                           de la lib devChk.py   
    v_dbgChk = True
    i_dbg = C_DebugMsg()

except ImportError :
    print("module 'devChk' non charge")
    v_dbgChk = True

try : 
    from myLib.logIt.logIt import C_logIt
    
except ImportError :
    print("module 'logIt' non charge")
    
from distutils import dir_util
import argparse

"""
    :liens web sbutil:
        https://docs.python.org/3.4/library/shutil.html
    :liens web dir_util:
        https://docs.python.org/3.4/distutils/apiref.html#module-distutils.dir_util
"""
class C_bougeTonFile(object) :
    """ **C_bougeTonFile(object)**
    
        Class permettant de copier et de mettre a jours les diférentes librairies dans
        l'ensemble des projet auquel elles sont utiles
    """
        
    def __init__( self) :
        """ 
            **__init()**
        
            Creation et initialisation des variables globales de cette Class
        """
        
        ## Creation des instances de debug et de log
        self.i_log = C_logIt()
                
        ## declaration des variables
        self.v_localDir             = os.getcwd()
        self.v_workDir              = "./myLib"
        self.v_docDir               = "../_1_userDoc"
        self.l_listDir              = os.listdir(self.v_workDir)
        self.l_docListDir           = os.listdir(self.v_docDir)
        self.l_subDirProjectList    = []
        self.t_distDirPath          = ("_1_userDoc", "_3_software")
        self.fichierTxt             = "projectList.txt"
        self.d_fullFile             = {}
        self.d_docPath              = {}
        self.v_testMode             = False
        self.v_versDist             = False
        self.v_yesToAll             = False
        self.v_curKey               = False
        
####
    
    def __del__(self) :
        """destructor
        
            il faut utilise : ::
            
                del [nom_de_l'_instance]
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

    def f_arboList(self) :
        """ parcourrir l'ensemble des sous dossier du dossier 'myLib'
            et copie l'ensemble dans le dictionnaire : d_fullFile
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_arboList", self.f_arboList)
        f_dbg(v_dbg, "l_listDir", self.l_listDir)
        
        ## Action
        if not self.v_testMode :
            for i in self.l_listDir :
                if i == "__pycache__" or i == "__init__.py" :
                    pass
                else :
                    self.f_subProcessArboList( i )
        else :
            for i in self.l_listDir :
                if i != "fakeLib" :
                    pass
                else :
                    self.f_subProcessArboList( i )
####

    def f_subProcessArboList( self, v_boucleIteration ) :
        """ Sous processus de la methode 'f_arboList'.
        
            Permet d'effectuer la routine de traitemant
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_subProcessArboList", self.f_subProcessArboList)
        
        ## Action
        v_subDirLocal = self.v_workDir + "/" + v_boucleIteration
        v_project = v_subDirLocal + "/" + self.fichierTxt
        self.l_subDirProjectList.append(v_project)
        l_parcourProject = [1]
                    # On initialise la list 'l_parcourProject[0]' a 1
                    # L'index [0] est incremente de 1 a chaque nouvelle entree.
                    # se conteur permet de servir de reference pour la boucle
                    # de copie.
        v_chk = True
        
        try :
            v_projectTxt = open(v_project,'r')
            
            for line in v_projectTxt :
                l_parcourProject[0] += 1
                l_parcourProject.append(line.replace("\n", ""))

        except FileNotFoundError :
            print("fichier non trouve")
            v_chk = False

        finally :
            if v_chk : v_projectTxt.close()

        self.d_fullFile[v_boucleIteration] = l_parcourProject
        self.d_docPath[v_boucleIteration] = "docLib_" + v_boucleIteration
                    # remplissage des dictionnaires en fonction du contenu
                    # du fichier 'projectList.txt' de chacun des dossier examines
        
        ## dbg
        f_dbg(v_dbg, "v_subDirLocal", v_subDirLocal)
        f_dbg(v_dbg, "v_project", v_project)
        f_dbg(v_dbg, "l_subDirProjectList", self.l_subDirProjectList)
        f_dbg(v_dbg, "d_docPath", self.d_docPath)

            
####

    def f_libVersionComparator(self, v_localLibFile, v_distLibFile, v_key) :
        """ Permet d'identifier si la version de la lib distante
            est differente de la lib local
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_libVersionComparator", self.f_libVersionComparator)
        
        ## log
        i_logSetD = self.i_log.f_setDTask
        
        ## Action
        v_boucle = True
        v_copyLib = False
        v_local = self.f_libVersion(v_localLibFile)
        v_dist = self.f_libVersion(v_distLibFile)
        self.v_versDist = v_dist
        
        if v_local == v_dist :
            v_copyLib = False
            print("les deux versions de la lib {} sont identiques".format(v_key))
            
            ## log
            i_logSetD("f_libVersionComparator", "{} : vers dist = vers loc pour la dest : {}".format(self.v_curKey, v_distLibFile))

        elif v_dist == "fix" :
            v_copyLib = False
            
            v_msg = """
                La version de la lib : {}
            
                est figee dans la destination suivante :
                {}
                """.format( v_key, v_distLibFile )
            print( v_msg )
            
            ## log
            i_logSetD("f_libVersionComparator", "{} : vers dist figee : {}".format(self.v_curKey, v_distLibFile))

        else :
            while v_boucle :
                if not self.v_yesToAll :
                    ## dbg
                    f_dbg(v_dbg, "v_yesToAll", self.v_yesToAll)
                    
                    ## Action
                    print("\n\tversion locale : {} - version distante : {}\n".format(v_local, v_dist))
                    v_question = input("Voulez-vous remplacer la version distante de {} par la version locale (O/N), oui pour toutes (A) ? ".format(v_key)).lower()
                    
                    if v_question == 'a' or v_question == 'A' :
                        self.v_yesToAll = True
                        v_copyLib = True
                        v_boucle = False
                    
                        ## dbg
                        f_dbg(v_dbg, "v_copyLib", v_copyLib)
                        
                    elif v_question == 'o' or v_question == 'y' or v_question == "oui" or v_question == "yes" :
                        v_copyLib = True
                        v_boucle = False
                        
                        ## dbg
                        f_dbg(v_dbg, "v_copyLib", v_copyLib)
                        
                    elif v_question == 'n' or v_question == "non" or v_question == "no" :
                        v_copyLib = False
                        v_boucle = False
                        
                        ## dbg
                        f_dbg(v_dbg, "v_copyLib", v_copyLib)
                        
                    ## Action    
                    else :
                        print("repondre par O ou N ! ('A' pour : oui pour toutes)")
                        
                else :
                    v_copyLib = True
                    v_boucle = False
                    
                    ## dbg
                    f_dbg(v_dbg, "v_yesToAll", self.v_yesToAll)
                    
        return v_copyLib

####

    def f_libVersion(self, v_libFile) :
        """ renvoie la version contenu dans la lib qui est passe en argument """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_libVersion", self.f_libVersion)

        
        ## Action
        v_chaine = ":Version:"
        v_compteur = 0
        v_chk = True
        v_vers = []
        
        try :
            v_localLib = open(v_libFile)
            
            for line in v_localLib : 
                if v_chaine in line :                   
                    for i in line :
                        if (i == 'f') or (i == 'F') :
                            v_vers = "fix"
                            break

                        if i == '2' :
                            v_vers = line[v_compteur:].replace("\n", "")
                            break

                        v_compteur += 1

        except FileNotFoundError :
            print("fichier non trouve")
            v_chk = False
            v_vers = "empty"
            

        finally :
            if v_chk : v_localLib.close()
            
        ## dbg
        f_dbg(v_dbg, "v_vers", v_vers)
        
        ## Action
        return v_vers
        
####

    def f_copyAll(self) :
        """ Copie les differentes librairies dans les projet aux quels elles appartiennent """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_copyAll", self.f_copyAll)
        f_dbg(v_dbg, "d_fullFile", self.d_fullFile)
        
        ## log
        i_logSetD = self.i_log.f_setDTask
        
        ## Action
        for key in self.d_fullFile :
            self.v_curKey = key
            v_src = self.v_workDir + "/" + key
            v_docSrc = "../"+ self.t_distDirPath[0] + "/" + self.d_docPath[key]
            
            ## dbg
            f_dbg(v_dbg, "key", key)
            f_dbg(v_dbg, "self.d_fullFile[key][0]", self.d_fullFile[key][0])
            # f_dbg(v_dbg, "type(v_src)", type(v_src))           
            f_dbg(v_dbg, "v_docSrc", v_docSrc)           
            
            ## Action
            for i in range(self.d_fullFile[key][0]) :
            
                ## dbg
                f_dbg(v_dbg, "i", i)
                f_dbg(v_dbg, "self.d_fullFile[key][i]", self.d_fullFile[key][i])
                # f_dbg(v_dbg, "type(self.d_fullFile[key][i])", type(self.d_fullFile[key][i]))
                
                ## Action
                if i == 0 or self.d_fullFile[key][1] == False :
                    pass
                else :
                    v_dest =    (   self.d_fullFile[key][i]+ "/" +
                                    self.t_distDirPath[1] + "/" + key
                                )
                    v_docDest = (   self.d_fullFile[key][i] + "/" +
                                    self.t_distDirPath[0] + "/" +
                                    self.d_docPath[key]
                                )

                    v_localLibFile = v_src + "/" + key + ".py"
                    v_distLibFile = v_dest + "/" + key + ".py"
                    
                    ## dbg
                    f_dbg(v_dbg, "v_localLibFile", v_localLibFile)
                    f_dbg(v_dbg, "v_distLibFile", v_distLibFile)
                    
                    ## Action
                    if self.f_libVersionComparator(v_localLibFile, v_distLibFile, key):
                        if self.v_versDist == "empty" :
                            pass
                            
                        else :
                            v_destOld = (   self.d_fullFile[key][i]+ "/" +
                                            self.t_distDirPath[1] +
                                            "/oldLibVers/" + self.v_versDist + "_" + key
                                        )
                            if os.path.isdir(v_dest) :
                                # os.path.isdir(path) renvoie 'True' si le dossier existe
                                v_msg = """ 
                                            le dossier :
                                            {}
                                            
                                            vas etre deplace vers :
                                            {}
                                        """.format( v_dest, v_destOld )
                                        
                                print( v_msg )
                                shutil.move(v_dest, v_destOld)
                    
                        
                        ## dbg
                        f_dbg(v_dbg, "v_dest", v_dest)
                        f_dbg(v_dbg, "v_docDest", v_docDest)
                        
                        ## Action
                        dir_util.copy_tree  (   v_src, 
                                                v_dest, preserve_mode=1, 
                                                preserve_times=1, 
                                                preserve_symlinks=0, 
                                                update=0, 
                                                verbose=0, 
                                                dry_run=0
                                            )
                                            
                        dir_util.copy_tree  (   v_docSrc, 
                                                v_docDest, preserve_mode=1, 
                                                preserve_times=1, 
                                                preserve_symlinks=0, 
                                                update=0, 
                                                verbose=0, 
                                                dry_run=0
                                            )
                                            
                        ## log
                        i_logSetD("Copie de Lib", v_dest, v_taskDetail = "copie de la lib : {}".format(self.v_curKey))
                        i_logSetD("Copie de Lib", v_docDest, v_taskDetail = "copie de la lib : {}".format(self.v_curKey))
        # ## log
        # i_logWr()

####

    def f_setTestOn( self ) :
        """ active le mode Test.
        
            Lorsque se mode est active, seul le travail sur 'fakeLib' sera effectue
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        f_dbg(v_dbg2, "f_setTestOn", self.f_setTestOn)
        
        ## Action
        self.v_testMode = True
        print( "Vous etes maintenant en mode Test" )
                                            
####

def f_osIdentifier() :
    """ Permet d'identifier le type de systeme d'exploitation """
    
    v_osType = sys.platform
    
    if v_osType == 'linux' :
        v_clear = "clear"
    elif  v_osType == "win32" :
        v_clear = "cls"
        
    system(v_clear)

####

def f_dbg( v_bool, v_data, v_tittle = False  ) :
    """ Fonction de traitemant du debug """
    if v_dbgChk and v_tittle :
        i_dbg.dbgPrint( v_bool, v_tittle, v_data )
        
    elif v_dbgChk and not v_tittle :
        i_dbg.dbgDel( v_bool, v_data)
        
########
# Main #
########
                        
def main() :
    """ Fonction principale """
    parser = argparse.ArgumentParser()
    parser.add_argument( "-d", "--debug", action='store_true', help="activation du mode debug")
    parser.add_argument( "-t", "--test", action='store_true', help="activation du mode Test")
                        
    args = parser.parse_args()
    
    f_osIdentifier()
    
    if args.debug :
        print( "Mode Debug active" )
        i_dbg.f_setAffichage( True )
    
    i_replicator = C_bougeTonFile()
        
    if args.test : i_replicator.f_setTestOn()

    i_git = C_GitChk()
    i_git.f_gitBranchChk()
    i_replicator.f_arboList()
    i_replicator.f_copyAll()
    i_replicator.i_log.f_wrLog()
    
    print("\n\n\t\t fin de la sequence ")
    

if __name__ == '__main__':
    main()
