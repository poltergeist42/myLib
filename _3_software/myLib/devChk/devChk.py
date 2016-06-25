#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   :Nom du fichier:     devChk.py
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

""" Ensemble de class permettant le control et le debug """

from os import system

class C_DebugMsg(object) :
    """ class permettant d'intercepter et d'afficher les message de debug """
    
    def __init__(self, v_affichage = True) :
        """ Init variables """
        self.affichage = v_affichage
        self.debugNumber = 0
        
    def __del__(self) :
        """destructor
        
            il faut utilise :
            ::
            
                del [nom_de_l'_instance]
        """
        v_className = self.__class__.__name__
        print("\n\t\tL'instance de la class {} est terminee".format(v_className))
        
    def dbgPrint(self, v_chk, v_varName, v_varValue) :
        """ intercept les messages pour les formater de facon homogene """
        if v_chk and self.affichage :
            self.debugNumber += 1
            print("dbgMsg[{}] : {} - {}".format(self.debugNumber, v_varName, v_varValue))
        
####
        
class C_GitChk(object) :
    def __init__(self, control = True) :
        """ Init variables """
        self.controlActif = control
        
    def __del__(self) :
        """destructor
        
            il faut utilise :
            ::
            
                del [nom_de_l'_instance]
        """
        v_className = self.__class__.__name__
        print("\n\t\tL'instance de la class {} est terminee".format(v_className))
        
    def f_gitBranchChk(self):
        """ identifie la branch courante et emet une alerte
        si elle est differente de '* master" """
        if self.controlActif :
            system("git branch > chkBranch")
            v_chaine = "* master"
            v_chk = True
            v_chaineIsTrue = True
            
            try :
                v_localLib = open("./chkBranch")
                
                for line in v_localLib : 
                    if not v_chaine in line : 
                        v_chaineIsTrue = False
                    else :
                        v_chaineIsTrue = True
                        break

            except FileNotFoundError :
                print("fichier non trouve")
                v_chk = False
                
            finally :
                if v_chk : v_localLib.close()
                
            if not v_chaineIsTrue :
                print   (" #################################################\n",
                         "#                                               #\n",
                         "# Attention, vous n'êtes sur la branch 'master' #\n",
                         "#                                               #\n",
                         "#################################################\n"
                        )

        else :
            print(" le control de branch est desactive")
    
 ####

def main():
    """ Fonction principale """
    system("cls")
    i_git = C_GitChk(False)
    i_git.f_gitBranchChk()
    
if __name__ == '__main__':
    main()
