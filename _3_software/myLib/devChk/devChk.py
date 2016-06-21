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

class C_DebugMsg(object) :
    """ class permettant d'intercepter et d'afficher les message de debug """
    
    def __init__(self) :
        """ Init variables """
        self.affichage = True
        
    def __del__(self) :
        """destructor
        
            il faut utilise :
            ::
            
                del [nom_de_l'_instance]
        """
        v_className = self.__class__.__name__
        print("\n\t\tL'instance de la class {} est terminee".format(v_className))
        
####
        
class C_GitChk(object) :
    def __init__(self) :
        """ Init variables """
        self.affichage = True
        
    def __del__(self) :
        """destructor
        
            il faut utilise :
            ::
            
                del [nom_de_l'_instance]
        """
        v_className = self.__class__.__name__
        print("\n\t\tL'instance de la class {} est terminee".format(v_className))