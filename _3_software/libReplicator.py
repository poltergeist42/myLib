#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   :Nom du fichier:     libReplicator.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20160621

----

   :Licence:            CC-BY-NC-SA
   :Liens:              https://creativecommons.org/licenses/by-nc-sa/4.0/

----


lexique
-------

   :v_:                 variable
   :l_:                 list
   :t_:                 tuple
   :d_:                 dictionnaire
   :f_:                 fonction
   :C_:                 Class
   :i_:                 Instance
   :m_:                 Module
"""
#################### Taille maximum des commentaires (90 caracteres)######################


from __future__ import absolute_import  # Permet d'importer en chemin abslolu ou relatif
                                        # doit etre importer en premier

import os, sys, shutil
from os import system
from distutils import dir_util
"""
    :liens web sbutil:
        https://docs.python.org/3.4/library/shutil.html
    :liens web dir_util:
        https://docs.python.org/3.4/distutils/apiref.html#module-distutils.dir_util
"""
class C_bougeTonFile(object) :
    """ Class permettant de copier les diférentes librairies
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
    
    def __del__(self) :
        """destructor
        
            il faut utilise :
            ::
            
                del [nom_de_l'_instance]
        """
        v_className = self.__class__.__name__
        print("\n\t\tL'instance de la class {} est terminee".format(v_className))

    def f_osIdentifier(self) :
        """ Permet d'identifier le type de systeme d'exploitation """
        v_osType = sys.platform
        
        if v_osType == 'linux' :
            v_clear = "clear"
        elif  v_osType == "win32" :
            v_clear = "cls"
            
        system(v_clear)
        # print( "v_osType = ", v_osType)

    def f_arboList(self) :
        """ parcourrir l'ensemble des sous dossier du dossier 'myLib'
            et copie l'ensemble dans le dictionnaire : d_fullFile
        """
        # print("l_listDir = ", self.l_listDir)

        for i in self.l_listDir :
            if i == "__pycache__" or i == "__init__.py" :
                pass
            else :
                v_subDirLocal = self.v_workDir + "/" + i
                # print("v_subDirLocal : ", v_subDirLocal)
                v_project = v_subDirLocal + "/" + self.fichierTxt
                self.l_subDirProjectList.append(v_project)
                # print("v_project - ", v_project)
                l_parcourProject = [1]

                try :
                    v_projectTxt = open(v_project,'r')
                    # print("v_projectTxtSize = ", len(v_projectTxt))
                    for line in v_projectTxt :
                        l_parcourProject[0] += 1
                        l_parcourProject.append(line.replace("\n", ""))
                        
                except :
                    l_parcourProject[0] += 1
                    l_parcourProject.append( False )
                    print("v_projectTxt - fichier non trouve")
                    
                finally :
                    v_projectTxt.close()

                self.d_fullFile[i] = l_parcourProject
                # print("l_subDirProjectList - {}\n".format(self.l_subDirProjectList))
            
    def f_libVersionComparator(self, v_localLibFile, v_distLibFile) :
        """ Permet d'identifier si la version de la lib distante
            est differente de la lib local
        """
        v_local = self.f_libVersion(v_localLibFile)
        v_dist = self.f_libVersion(v_distLibFile)
        print("L : {} - D : {}".format(v_local, v_dist))
        
        
    def f_libVersion(self, v_libFile) :
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
        
    def f_copyAll(self) :
        """ Copie les différentes librairies dans les projet au quel elles appartiennent """
        # print("d_fullFile :\n", self.d_fullFile)
        
        for key in self.d_fullFile :
            # print("key - ", key)
            # print("d_fullFile[key][0] - {}".format(self.d_fullFile[key][0]))
            v_src = self.v_workDir + "/" + key
            # print("v_src : {} - Type : {}".format(v_src, type(v_src)))
            
            for i in range(self.d_fullFile[key][0]) :
                # print("i : {} - self.d_fullFile[key][i] : {} - type : {}".format(i, self.d_fullFile[key][i], type(self.d_fullFile[key][i])))
                if i == 0 : 
                    pass
                else :
                    if self.d_fullFile[key][1] == False :
                        pass
                    else :
                        v_dest = self.d_fullFile[key][i] + key
                        v_localLibFile = v_src + "/" + key + ".py"
                        v_distLibFile = v_dest + "/" + key + ".py"
                        self.f_libVersionComparator(v_localLibFile, v_distLibFile)
                        # print("v_dest = ", v_dest)
                        dir_util.copy_tree(v_src, v_dest, preserve_mode=1, preserve_times=1, preserve_symlinks=0, update=0, verbose=0, dry_run=0)
                        
                        
def main() :
    """ Fonction principale """
    print("\n\t\t## Creation de l'instance ##\n")
    i_replicator = C_bougeTonFile()
    print("\n\t\t## Debut de f_osIdentifier() ##\n")
    i_replicator.f_osIdentifier()
    print("\n\t\t## Debut de f_arboList() ##\n")
    i_replicator.f_arboList()
    print("\n\t\t## Debut de f_libVersion() ##\n")
    print("\n\t\t## Debut de f_copyAll() ##\n")
    i_replicator.f_copyAll()
    
    input("\n\n\t\t fin de la sequence ")
    

if __name__ == '__main__':
    main()
