#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   :Nom du fichier:     libReplicator.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20160614

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
#################### Taille maximum des commentaires (80 caracteres)######################

import os, sys, shutil
from os import system
"""
    :liens web sbutil:
        https://docs.python.org/3.4/library/shutil.html
"""
class C_bougeTonFile(object) :
    """ Class permettant de copier les diférentes librairies
        l'ensemble des projet auquel elles sont utiles
    """
        
    def __init__(self) :
        """ Init variables """
        self.localDir = "./myLib"
        self.l_listDir = os.listdir(self.localDir)
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
        print( "v_osType = ", v_osType)
        
        if v_osType == 'linux' :
            v_clear = "clear"
        elif  v_osType == "win32" :
            v_clear = "cls"
            
        system(v_clear)
        print( "v_osType = ", v_osType)

    def f_arboList(self) :
        """ parcourrir l'ensemble des sous dossier du dossier 'myLib'
            et copie l'ensemble dans le dictionnaire : d_fullFile
        """
        print("l_listDir = ", self.l_listDir)

        for i in self.l_listDir :
            v_subDirLocal = self.localDir + "/" + i
            print("v_subDirLocal : ", v_subDirLocal)
            v_project = v_subDirLocal + "/" + self.fichierTxt
            self.l_subDirProjectList.append(v_project)
            print("v_project - ", v_project)
            l_parcourProject = []
            
            try :
                v_projectTxt = open(v_project,'r')
                for line in v_projectTxt :
                    l_parcourProject.append(line.replace("\n", ""))
                    
            except :
                print("v_projectTxt - fichier non trouve")
                
            finally :
                v_projectTxt.close()

            l_subDirList = os.listdir(v_subDirLocal)
            print("l_subDirList - ", l_subDirList)
            self.d_fullFile[i] = l_parcourProject
            self.d_fullFile[i].append(l_subDirList)
            print("l_subDirProjectList - ", self.l_subDirProjectList)
            
    def f_libVersion(self) :
        """ Permet d'identifier si la version de la lib distante
            est differente de la lib local
        """

        
    def f_copyAll(self) :
        """ Copie les différentes librairies dans les projet au quel elles appartiennent """
        for key in self.d_fullFile :
            print(key)
            x= len(self.d_fullFile[key]) - 1
            print("{} - {}".format(len(self.d_fullFile[key]), x))
            for i in range(len(self.d_fullFile[key][x])) :
                y = str(key) + ".py"
                z = self.d_fullFile[key][x][i]
                if y == z :
                    print("y - {}".format(y))
                    print("z - ", self.d_fullFile[key][x][i])
                else :
                    print("y ne correspond pas à z")
        
def main() :
    """ Fonction principale """
    print("\n\t\t## Creation de l'instance ##\n")
    i_replicator = C_bougeTonFile()
    print("\n\t\t## Debut de f_osIdentifier() ##\n")
    i_replicator.f_osIdentifier()
    print("\n\t\t## Debut de f_arboList() ##\n")
    i_replicator.f_arboList()
    print("\n\t\t## Debut de f_copyAll() ##\n")
    i_replicator.f_copyAll()
    
    input("\n\n\t\t fin de la sequence ")
    

if __name__ == '__main__':
    main()
