#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   :Nom du fichier:     objJson.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20160731

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

import os, sys
sys.path.insert(0,'..')         # ajouter le repertoire precedent au path (non definitif)
                                # pour pouvoir importer les modules et paquets parent
from devChk.devChk import C_DebugMsg

import json, copy

class C_ObjJson (object):
    """ La class permet de manipuler des objet formater en Json depuis et vers des 
        dictionnaires.
    """

    def __init__(self) :
        """ 
            **__init()**
        
            Creation et initialisation des variables globales de cette class
        """
        
        ## Creation de l'instance pour les message de debug
        self.i_dbg = C_DebugMsg()
                
        ## declaration des variables
        self.d_dicoToStuff = {}
        self.d_dicoFunc = {}
        self.d_dicoWorkSpace = {}
        d_dicoLocalWorkSpace = {}
        
        self.v_nomPlusChemin = ""
        self.i_monFichier = ""
        
###
        
    def __del__(self) :
        """
            **__del__()**
        
            Permet de terminer proprement l'instance de la class courante
        
            il faut utilise ::
            
                del [nom_de_l'_instance]
                
            *N.B :* Si l'instance n'est plus utilisee, cette methode est appellee 
            automatiquement.
        """
        v_dbg = 1
        v_dbg2 = 0
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "__del__", self.__del__)
        
        v_className = self.__class__.__name__
        print("\n\t\tL'instance de la class {} est terminee".format(v_className))    
    
###
    
    def f_setFileName(  self,
                        v_nomDuFichier = "fichierJson.json", 
                        v_cheminDuFichier = "./" ) :
        """ **f_setFileName( str, str )**
        
            Permet de renseigner le chemin et le nom du fichier.
        """
        v_dbg = 1
        v_dbg2 = 0
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_setFileName", self.f_setFileName)
        
        os.makedirs(os.path.normpath(v_cheminDuFichier), mode=0o777, exist_ok=True)
        self.v_nomPlusChemin = str( v_cheminDuFichier ) + str( v_nomDuFichier )
        ## dbg
        i_debug(v_dbg, "v_nomPlusChemin", self.v_nomPlusChemin)

###
        
    def f_setDicoToStuff( self, v_dicoSource ) :
        """ **f_setDicoToStuff( dict )**
        
            Permet de remplir le dictionnaire d_dicoToStuff avec le contenue d'un autre
            dictionnaire passé en argument.
        """
        v_dbg = 1
        v_dbg2 = 0
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_setDicoToStuff", self.f_setDicoToStuff)
        
        self.d_dicoToStuff = copy.deepcopy( v_dicoSource )
        ## dbg
        i_debug(v_dbg, "d_dicoToStuff", self.d_dicoToStuff)

###
        
    def f_setDicoFunc( self, v_dicoSource ) :
        """ **f_setDicoToStuff( dict )**
        
            Permet de remplir le dictionnaire d_dicoFunc avec le contenue d'un autre
            dictionnaire passé en argument.
        """
        v_dbg = 1
        v_dbg2 = 0
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_setDicoFunc", self.f_setDicoFunc)
        
        self.d_dicoFunc = copy.deepcopy( v_dicoSource )
        ## dbg
        i_debug(v_dbg, "d_dicoFunc", self.d_dicoFunc)

        
###
        
    def f_openRWFile( self, v_mode = 'r' ) :
        """ **f_openRWFile( str, str )**
        
            Permet d'ouvrir un fichier en mode 'Lecture' : 'r' (valeur par défaut)
            ou en mode 'ecriture' : 'w'
            
            Les nom et chemin pour acceder / creer le fichier est donne par
            v_nomPlusChemin qui prend les valeurs par defaut de 'f_setFileName()' si aucun
            parametre n'est donne.
            
            *N.B :* L'instance du fichier devra etre fermee avec '.close()' depuis
            l'endroit de l'appel de 'f_openRWFile()'
        """
        v_dbg = 1
        v_dbg2 = 0
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_openRWFile", self.f_openRWFile)
        

        v_nomPlusChemin = self.v_nomPlusChemin
            
        try :
            self.i_monFichier = open( v_nomPlusChemin, v_mode, encoding='utf-8' )
        
        except :
            print( "Le chemin ou le nom demander n'a pas été trouvé" )
                        
###
    
    def f_dicoFuncRun( self, v_dicoValueRead ) :
        """ **f_dicoFuncRun( dict.value )**
        
            Cette methode execute une fonction en interpretant la valeur passer en
            argument. Cet argument placer en index dans le dictionnaire 'd_dicoFunc'.
            c'est donc la clef. Pour chaque clef est assocé une valeur qui correspond
            a une fonction. Seule le nom de la fonction doit etre precisee, les
            parentheses ne doivent etres specifees.
            
            *N.B :* La fonction doit etre declaree avant.
            *N.B 2 :* Il faut aussi remplir le dictionnaire avant d'appeler cette
            fonction.
            
            ex ::

                def maFonction () :
                    print( "Vous etes dans 'maFonction'" )
                
                d_dicoFunc = { "maClef" : maFonction }
                
                dicoFuncRun( "maClef" )
                
                >>> Vous etes dans 'maFonction'
        """
        v_dbg = 1
        v_dbg2 = 0
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_dicoFuncRun", self.f_dicoFuncRun)
        
        try :
            self.d_dicoFunc[v_dicoValueRead] ()
            ## dbg
            i_debug(v_dbg, "d_dicoFunc[v_dicoValueRead]", self.d_dicoFunc[v_dicoValueRead])
        except NameError :
            print( "{} n'est pas definie\n".format( self.d_dicoFunc[v_dicoValueRead] ))
        
###
        
    def f_dicoSort( self ) :
        """ **f_dicoSort( dict )**
        
            Renvoie une list des enssemble 'clefs : valeurs', sous la forme de tupple
            tries par ordre alphabetique
        """
        v_dbg = 1
        v_dbg2 = 0
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_dicoSort", self.f_dicoSort)
        
        d_dicoWorkSpace = self.d_dicoWorkSpace
        l_listSortedWorkSpace = []
        
        for clef in sorted(d_dicoWorkSpace.keys()) :
            l_listSortedWorkSpace.append( (clef, d_dicoWorkSpace[clef]) )
            
        #dbg
        i_debug(v_dbg, "l_listSortedWorkSpace", l_listSortedWorkSpace)
        
        return l_listSortedWorkSpace
        
###
        
    def f_dumpJsonFile( self ) :
        """ **f_dumpJsonFile( <str>, <str> )**
            
            Cette fonction permet de creer un fichier texte et d'y ajouter le contenu du
            dictionnaire 'd_dicoToStuff' formater en json.
            
            Par defaut le nom du fichier est : 'fichierJson.json' 
            Le chemin par defaut quant à lui se trouve dans le dossier local
        """
        v_dbg = 1
        v_dbg2 = 0
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_dumpJsonFile", self.f_dumpJsonFile)
        
        self.f_openRWFile(v_mode = 'w')
        json.dump(self.d_dicoToStuff, self.i_monFichier, indent=4)
        self.i_monFichier.close()
        
    def f_dumpLocalJson( self, v_dicoSource ) :
        """ **f_dumpLocalJson( <str>/<dict> )**
            
            Cette fonction permet de faire un dump dans une variable / dictionnaire
            local, le tous formater en json.
            
        """
        v_dbg = 1
        v_dbg2 = 0
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_dumpLocalJson", self.f_dumpLocalJson)
        
        self.d_dicoLocalWorkSpace = json.dumps(v_dicoSource, indent=4)
        ## dbg
        i_debug(v_dbg, "d_dicoWorkSpace", self.d_dicoLocalWorkSpace)
        
###
        
    def f_loadJson( self ) :
        """ **f_loadJson( <str>, <str> )**
        
            Permet de lire un fichier en considerant que toutes les donnee sont de 
            type : <str>. C'est donnee sont ajouter au dictionnaire 'd_dicoWorkSpace'
        """

        v_dbg = 1
        v_dbg2 = 0
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_loadJson", self.f_loadJson)
        
        self.f_openRWFile(v_mode = 'r')
        self.d_dicoWorkSpace = json.load( self.i_monFichier )
        self.i_monFichier.close()
        ## dbg
        i_debug(v_dbg, "d_dicoWorkSpace", self.d_dicoWorkSpace)

###
        
    def f_loadLocalJson( self, v_dicoSource ) :
        """ **f_loadJson( [Data in Json format] )**
        
            Permet de lire et de formater directement les donnees transmisent au 
            format Json et de renvoyer une variables aux format Json
        """
        v_dbg = 1
        v_dbg2 = 0
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_loadLocalJson", self.f_loadLocalJson)
        
        v_localJson = json.loads( v_dicoSource )
        
        ## dbg
        i_debug(v_dbg, "v_localJson", v_localJson)
        return v_localJson
        
    
def main() :
    ##################################
    # Creation des fonctions de test #
    ##################################
    def f_avance() : print( "Fonction Avance" )
    def f_recul() : print( "Fonction Recul" )
    def f_droite() : print( "Fonction Droite" )
    def f_gauche() : print( "Fonction Gauche" )
    
    ######################################
    # Creation des dictionnaires de test #
    ######################################
    
    d_dicoFuncTest =    {   "f_avance" : f_avance,
                            "f_recul" : f_recul, 
                            "f_droite" : f_droite,
                            "f_gauche" : f_gauche
                        }
                        
    d_dicoToStuffTest = {   "0000" : "f_avance",
                            "0002" : "f_droite",
                            "0001" : "f_gauche",
                            "0003" : 3,
                            "0004" : "f_recul"
                        }
    
    ##################################################################
    # Creation de l'instance + mise en place de la structure de test #
    ##################################################################
    
    ################################################
    # Instance et test avec les valeurs par defaut #
    ################################################
    i_testObjJson = C_ObjJson()
    
    ## Remplissage des dictionnaires de l'instance :
    i_testObjJson.f_setDicoFunc( d_dicoFuncTest )
    i_testObjJson.f_setDicoToStuff( d_dicoToStuffTest )
        
    ## test des fonctions :
    i_testObjJson.f_setFileName()
    i_testObjJson.f_dumpJsonFile()
    i_testObjJson.f_loadJson()
    i_testObjJson.f_dumpLocalJson( i_testObjJson.d_dicoToStuff )
    i_testObjJson.f_loadLocalJson( i_testObjJson.d_dicoLocalWorkSpace )
    l_list = i_testObjJson.f_dicoSort()
    
    for i in range( len(l_list) ) :
        if type( l_list[i][1] ) == type( "str" ) :
            i_testObjJson.f_dicoFuncRun( l_list[i][1] )
            
    del( i_testObjJson )
            
    ###############################################
    # Instance et test avec les valeurs miodifies #
    ###############################################
    i_testObjJson = C_ObjJson()
    
    ## Remplissage des dictionnaires de l'instance :
    i_testObjJson.f_setDicoFunc( d_dicoFuncTest )
    i_testObjJson.f_setDicoToStuff( d_dicoToStuffTest )
        
    ## test des fonctions :
    i_testObjJson.f_setFileName (
                                v_nomDuFichier = "fichierJson2.json", 
                                v_cheminDuFichier = "./testJson/" 
                                )
    i_testObjJson.f_dumpJsonFile()
    i_testObjJson.f_loadJson()
    i_testObjJson.f_dumpLocalJson( i_testObjJson.d_dicoToStuff )
    i_testObjJson.f_loadLocalJson( i_testObjJson.d_dicoLocalWorkSpace )
    l_list = i_testObjJson.f_dicoSort()
    
    for i in range( len(l_list) ) :
        if type( l_list[i][1] ) == type( "str" ) :
            i_testObjJson.f_dicoFuncRun( l_list[i][1] )
            
    del( i_testObjJson )
            
            
        
    # v_Un = 33
    # v_stringFormat = "{:04}".format(v_Un,)
    # print("{} - {} \n\n".format(v_stringFormat, type(v_stringFormat)))
    # print("{} - {} \n\n".format("f_avance", type(f_avance)))
    
    # print(json.dumps(d_dicoTest, indent=4))
    
if __name__ == '__main__':
    main()