#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""


Infos
=====

   :Nom du fichier:     libReplicator.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20160912

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
except ImportError :
    print("module 'devChk' non charge")
    
from distutils import dir_util
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
        
    def __init__(self) :
        """ Init variables """
        self.v_localDir = os.getcwd()
        self.v_workDir = "./myLib"
        self.l_listDir = os.listdir(self.v_workDir)
        self.l_subDirProjectList = []
        self.fichierTxt = "projectList.txt"
        self.d_fullFile = {}
        
        self.i_dbg = C_DebugMsg(False)
        
####
    
    def __del__(self) :
        """destructor
        
            il faut utilise : ::
            
                del [nom_de_l'_instance]
        """
        v_className = self.__class__.__name__
        print("\n\t\tL'instance de la class {} est terminee".format(v_className))

####
        
    def f_osIdentifier(self) :
        """ Permet d'identifier le type de systeme d'exploitation """
        v_dbg = True
        
        v_osType = sys.platform
        
        if v_osType == 'linux' :
            v_clear = "clear"
        elif  v_osType == "win32" :
            v_clear = "cls"
            
        system(v_clear)
        
        #### dbg
        self.i_dbg.dbgPrint(v_dbg, "v_osType", v_osType)

####

    def f_arboList(self) :
        """ parcourrir l'ensemble des sous dossier du dossier 'myLib'
            et copie l'ensemble dans le dictionnaire : d_fullFile
        """
        v_dbg = True
        
        #### dbg
        self.i_dbg.dbgPrint(v_dbg, "l_listDir", self.l_listDir)
        
        for i in self.l_listDir :
            if i == "__pycache__" or i == "__init__.py" :
                pass
            else :
                v_subDirLocal = self.v_workDir + "/" + i
                self.i_dbg.dbgPrint(v_dbg, "v_subDirLocal", v_subDirLocal)
                v_project = v_subDirLocal + "/" + self.fichierTxt
                self.l_subDirProjectList.append(v_project)
                
                #### dbg
                self.i_dbg.dbgPrint(v_dbg, "v_project", v_project)
                
                l_parcourProject = [1]
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

                self.d_fullFile[i] = l_parcourProject
                
                #### dbg
                self.i_dbg.dbgPrint(v_dbg, "self.l_subDirProjectList", self.l_subDirProjectList)
            
####

    def f_libVersionComparator(self, v_localLibFile, v_distLibFile) :
        """ Permet d'identifier si la version de la lib distante
            est differente de la lib local
        """
        v_dbg = True

        v_boucle = True
        v_copyLib = False
        v_local = self.f_libVersion(v_localLibFile)
        v_dist = self.f_libVersion(v_distLibFile)
        
        if v_local == v_dist :
            v_copyLib = False
            print("les deux version sont identiques")
        else :
            while v_boucle :
                print("\n\tversion locale : {} - version distante : {}\n".format(v_local, v_dist))
                v_question = input("Voulez-vous remplacer la lib distante par la lib locale (O/N) ? ").lower()
                
                if v_question == 'o' or v_question == 'y' or v_question == "oui" or v_question == "yes" :
                    v_copyLib = True
                    v_boucle = False
                    print("v_copyLib = ", v_copyLib)
                elif v_question == 'n' or v_question == "non" or v_question == "no" :
                    v_copyLib = False
                    v_boucle = False
                    #### dbg
                    self.i_dbg.dbgPrint(v_dbg, "v_copyLib", v_copyLib)
                else :
                    print("repondre par O ou N !")
                    
        return v_copyLib

####

    def f_libVersion(self, v_libFile) :
        """ renvoie la version contenu dans la lib qui est passe en argument """
        v_dbg = True

        v_chaine = ":Version:"
        v_compteur = 0
        v_chk = True
        v_vers = []
        
        try :
            v_localLib = open(v_libFile)
            
            for line in v_localLib : 
                if v_chaine in line :                   
                    for i in line :
                        if i == '2' :
                            v_vers = line[v_compteur:].replace("\n", "")
                            break

                        v_compteur += 1

        except FileNotFoundError :
            print("fichier non trouve")
            v_chk = False
            

        finally :
            if v_chk : v_localLib.close()
            
        return v_vers
        
####

    def f_copyAll(self) :
        """ Copie les différentes librairies dans les projet au quel elles appartiennent """
        v_dbg = True

        print("d_fullFile :\n", self.d_fullFile)
        
        for key in self.d_fullFile :
        
            #### dbg
            self.i_dbg.dbgPrint(v_dbg, "key", key)
            self.i_dbg.dbgPrint(v_dbg, "self.d_fullFile[key][0]", self.d_fullFile[key][0])
            
            v_src = self.v_workDir + "/" + key
            
            #### dbg
            self.i_dbg.dbgPrint(v_dbg, "type(v_src)", type(v_src))
            
            for i in range(self.d_fullFile[key][0]) :
            
                #### dbg
                self.i_dbg.dbgPrint(v_dbg, "i", i)
                self.i_dbg.dbgPrint(v_dbg, "self.d_fullFile[key][i]", self.d_fullFile[key][i])
                self.i_dbg.dbgPrint(v_dbg, "type(self.d_fullFile[key][i])", type(self.d_fullFile[key][i]))
                
                if i == 0 or self.d_fullFile[key][1] == False :
                        pass
                else :
                    v_dest = self.d_fullFile[key][i] + "/" + key
                    v_localLibFile = v_src + "/" + key + ".py"
                    v_distLibFile = v_dest + "/" + key + ".py"
                    if self.f_libVersionComparator(v_localLibFile, v_distLibFile):
                    
                        #### dbg
                        self.i_dbg.dbgPrint(v_dbg, "v_dest", v_dest)
                        dir_util.copy_tree(v_src, v_dest, preserve_mode=1, preserve_times=1, preserve_symlinks=0, update=0, verbose=0, dry_run=0)
                        
########
# Main #
########
                        
def main() :
    """ Fonction principale """
    print("\n\t\t## Creation de l'instance ##\n")
    i_replicator = C_bougeTonFile()
    print("\n\t\t## Debut de f_osIdentifier() ##\n")
    i_replicator.f_osIdentifier()
    i_git = C_GitChk()
    i_git.f_gitBranchChk()
    print("\n\t\t## Debut de f_arboList() ##\n")
    i_replicator.f_arboList()
    print("\n\t\t## Debut de f_copyAll() ##\n")
    i_replicator.f_copyAll()
    
    input("\n\n\t\t fin de la sequence ")
    

if __name__ == '__main__':
    main()
