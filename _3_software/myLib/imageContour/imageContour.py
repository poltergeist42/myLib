#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Infos
=====

   :Nom du fichier:     imageContour.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20161001

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
   :**m_**:                 Matrice
   
####
   
Librairie necessaire
====================

Les lib suivantes doivent etre installees dans votre environement Python :

    - Numpy
    - Pillow
    - Matplot lib
    - OpenCV
    
####

Class C_ImageContour
====================
    
"""
try :
    import os, sys
    sys.path.insert(0,'..')         # ajouter le repertoire precedent au path (non définitif)
                                    # pour pouvoir importer les modules et paquets parent
    from devChk.devChk import C_DebugMsg
   
except ImportError :
    print( "module non present" )
    
from PIL import Image     # PIL.Image is a module not a class...
from PIL import ImageOps
import numpy as np
import cv2
import argparse

#####

class C_ImageContour( object ) :
    """ **C_ImageContour( object )**
    
        Class permettant de detourer et d'isoler la forme exterieur d'un sujet pris sur
        fond unie.
    """
    def __init__( self, v_debug=False ) :
        """ 
            **__init()**
        
            Creation et initialisation des variables globales de cette Class
        """
        
        ## Creation de l'instance pour les message de debug
        self.i_dbg = C_DebugMsg(v_debug)
                
        ## declaration des variables
        self.i_img1             = False
        self.i_img2             = False
        self.i_BWMask           = False
        self.i_imgSubst         = False
        
        self.v_maskOn           = False
        self.v_outputFilename   = False
        self.v_imgSrc           = False
        self.v_outContour       = False
        self.v_outSubstract     = False
        self.v_numberOfImgSrc   = False
        
        self.m_npImg1           = False
        self.m_npImg2           = False
        self.m_npBWMask         = False
        self.m_npSubst          = False

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

    def f_openImage( self, v_img1, v_img2=False, v_maskOn=False ) :
        """ **f_openImage( str, str, bool )**
        
            Permet d'ouvrir les photos passees en arguments et de les convertir en Matrice.
            
            Le format des photos etant obligatoirement au format Jpeg, le nom des photos
            passees en arguments ne doit pas comporter l'extension '.jpeg' car elle sera 
            ajoute automatiquement.
            
            Seul 'v_img1' est obligatoire car au minimum, il n'y a qu'une seule photo a
            ouvrir (dans le cas d'un mask par exemple)
            
            Si v_img1 est un mask (en noir et blanc) la variable 'v_maskOn'
            doit etre mis a True. l'argument a donner pour v_img1 doit normalement etre le
            contenu de 'i_BWMask'.
            
            v_img1 est soit la photo vide, soit le mask en noir et blanc.
            v_img2 est le modele (elle n'est declarer qu'une fois).
            
            Cette methode doit etre appellee 2 fois. Une premiere fois en declarant
            l'image vide et le modele. Une seconde fois en declarant simplement le mask.

            'i_BWMask' doit etre passee en argument à 'f_openImage' lors de son second appel            
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_openImage", self.f_openImage)
        
        ## Action
        v_workDir = self.v_imgSrc
        if v_img1 and not v_maskOn :
            self.i_img1 = v_img1 + ".jpg"
            
            self.m_npImg1 = np.array(Image.open(v_workDir + self.i_img1), dtype = np.uint8)
        
        if v_img2 :
            self.i_img2 = v_img2 + ".jpg"
            self.m_npImg2 = np.array(Image.open(v_workDir + self.i_img2), dtype = np.uint8)

        if v_maskOn and not v_img2 :
            ## Creation d'une matrice de la taille de m_npImg2 et remplissage de cette matrice
            ## avec le contenu de m_npImg1
            v_workDir = self.v_outSubstract
            self.i_img1 = v_img1 + ".jpg"
            self.m_npImg1 = np.array(Image.open(v_workDir + self.i_img1), dtype = np.uint8)
            self.m_npBWMask = np.zeros(self.m_npImg2.shape, dtype = np.uint8)
            for rowIdx, row in enumerate( self.m_npImg1 ) :
                for colIdx, val in enumerate( row ) :
                    self.m_npBWMask[rowIdx, colIdx] = self.m_npImg1[rowIdx, colIdx]
                    
            self.m_npImg1 = self.m_npBWMask

####

    def f_imageSubst( self) :
        """ **f_imageSubst(  )**
        
            Soustraction de l'image vide (ou du mask Noir et Blanc) par le model
            
            **Dans une soustrataction photoVide / photoModele**
            
            Pour ne pas avoir de valeur negative lors de la soustraction (pixel parasites),
            les valeurs de la matrice m_npImg1 (photoVide) sont contraintes
            entre m_npImg1 (lui meme) pour les valeurs hautes et m_npImg2 (photoModele)
            pour les valeurs basses. La soustraction sera : ::
            
                m_npSubst = m_npImg2 - m_npImg1
                
            **Dans une soustrataction photoMask / photoModele**
            
            Les valeurs de la matrice m_npImg2 (la matrice du modele) sont contraintes
            entre m_npImg2 (lui meme) pour les valeurs hautes et m_npImg1 (photoMask) pour
            les valeurs basses. La soustraction sera : ::
            
                m_npSubst = m_npImg1 - m_npImg2
            
            Pour rappel :
                * Blanc = 255
                * Noir = 0

        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_openImage", self.f_openImage)
        
        ## Action
        if not self.v_maskOn :
            self.m_npImg1 = np.clip(self.m_npImg1, 0, self.m_npImg2)
            self.m_npSubst = self.m_npImg2 - self.m_npImg1
            
        if self.v_maskOn :
            self.m_npImg2 = np.clip(self.m_npImg2, 0, self.m_npImg1)
            self.m_npSubst = self.m_npImg1 - self.m_npImg2
            



        
####

    def f_createImage( self ) :
        """ **f_createImage()**
        
            Permet de creer l'image intermediaire si la variable de l'instance 'v_maskOn'
            est 'False' et si l'image finale si la variable de l'instance 'v_maskOn'
            est 'True'
            
            Le nom l'image generee aura le prefix 'out_' suivie du nom du model (i_img2)
            et l'extension 'jpg'
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_createImage", self.f_createImage)
        
        ## Action
        self.v_outputFilename = "out_" + str(self.i_img2)
        
        self.i_imgSubst = Image.fromarray(self.m_npSubst) 
        if self.v_maskOn :
            self.f_invert()
            self.f_setMask()
            v_workDir = self.v_outContour
        else :
            v_workDir = self.v_outSubstract
            
        self.i_imgSubst.save(v_workDir + self.v_outputFilename)
        
####

    def f_createMask( self, v_img1) :
        """ **f_createMask( str )**
        
            permet d'effectuer les traitemants de l'image intermediaire avec openCV.
            Ces traitemant convertissent l'image en Noir et blanc. La zone Noir correspond
            au fond de l'image alors que le blanc correspond a la forme du modele.
            
            c'est la valeur de la variable 'v_outputFilename' qui doit etre passe 
            en argument dans v_img1.
            
            L'image creer apres le traitemant se nomme 'cvOut.jpg' ce nom est sauvegarde
            dans la variable 'i_BWMask'
            
            'i_BWMask' doit etre passee en argument à 'f_openImage' lors de son second appel            
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_createMask", self.f_createMask)
        
        ## Action
        v_workDir = self.v_outSubstract
        
        # charger l'image, la convertir en niveaux de gris, et la brouiller legerement
        i_image = cv2.imread(v_workDir + v_img1)
        i_gray = cv2.cvtColor(i_image, cv2.COLOR_BGR2GRAY)
        i_gray = cv2.GaussianBlur(i_gray, (5, 5), 0)


        # seuillage de l'image, avant d'effectuer une serie de traitemant pour eliminer
        # toutes zone de bruit sur l'image
        i_work = cv2.threshold(i_gray, 45, 255, cv2.THRESH_BINARY)[1]
        i_work = cv2.erode(i_work, None, iterations=2)
        i_work = cv2.dilate(i_work, None, iterations=2)
        cv2.imwrite(v_workDir + "cvOut.jpg", i_work)
        self.i_BWMask = "cvOut"
        
        self.f_setMask()

        
####

    def f_invert( self ) :
        """ **f_invert( )**
         
            inverce les couleurs de l'image 'i_imgSubst'
            
            Cette methode est appellee par 'f_createImage' lors de la creation 
            de l'image finale 
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_invert", self.f_invert)
        
        ## Action
        self.i_imgSubst = ImageOps.invert(self.i_imgSubst)
        
####
        
    def f_setMask( self ) :
        """ **f_setMask()**
        
            Inverse automatiquement la valeur de 'v_maskOn'
            
            Cette methode est appellee par 'f_createMask' et 'f_createMask'
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_setMask", self.f_setMask)
        
        ## Action
        if self.v_maskOn :
            self.v_maskOn = False
            i_debug(v_dbg, "v_maskOn", self.v_maskOn)
            
        if not self.v_maskOn :
            self.v_maskOn = True
            i_debug(v_dbg, "v_maskOn", self.v_maskOn)
            
####
            
    def f_resetVar( self ) :
        """ **f_resetVar()**
        
            Reinitialise toutes les variables de l'instance
            
            Lors du traitemant d'une serie de photos, il faut reinitialiser toutes les
            variables entre chaque iteration.
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_resetVar", self.f_resetVar)
        
        ## Action
        self.i_img1             = False
        self.i_img2             = False
        self.i_BWMask           = False
        self.i_imgSubst         = False
        
        self.v_maskOn           = False
        self.v_outputFilename   = False
        
        self.m_npImg1           = False
        self.m_npImg2           = False
        self.m_npBWMask         = False
        self.m_npSubst          = False
       
####

    def f_setWorkDir(   self,
                        v_imgSrc = "./imgSrc", 
                        v_outSubstract = "./outSubstract",
                        v_outContour = "./outContour"
                    ) :
        """ **f_setWorkDir( string, string, string)**
        
            Permet de choisir le chemin des dossier de travail.
            Les dossiers de travail sont :
            
            - "imgSrc" : C'est le dossier source dans lequel doivent etre placer les
              photos (le mask + le sujet) qui seront traitee.
              
            - "outSubstract" : C'est le dossier dans lequel vont etre generees les photos
              de la soustraction simple. C'est photos serviront pour la soustraction
              detourage de contour.
              
            - "outContour" : C'est le dossier dans lequel vont etre generee les photos de
              la soustraction avec detection de contour.
              
            Si le dossier n'existe pas, il sera automatiquement creer. Si il existe deja,
            aucune action ne sera execute et les donnees presentes dans le dossier ne
            seront pas ecrasee.
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_setWorkDir", self.f_setWorkDir)
        
        ## Action
        self.v_imgSrc = v_imgSrc + "/"
        self.v_outSubstract = v_outSubstract + "/"
        self.v_outContour = v_outContour + "/"
                
        ## dbg
        i_debug(v_dbg2, "v_imgSrc", self.v_imgSrc)
        i_debug(v_dbg2, "v_outSubstract", self.v_outSubstract)
        i_debug(v_dbg2, "v_outContour", self.v_outContour)
        
        ## Action
        os.makedirs(os.path.normpath(self.v_imgSrc), mode=0o777, exist_ok=True)
        os.makedirs(os.path.normpath(self.v_outSubstract), mode=0o777, exist_ok=True)
        os.makedirs(os.path.normpath(self.v_outContour), mode=0o777, exist_ok=True)
                # os.makedirs() : Permet de creer le repertoire. Si les 
                # repertoires parents n'existent pas, os.makedirs
                # les creera automatiquement
                #
                # os.path.normpath() permet de normaliser la syntaxe du
                # chemin indiquer par v_target.
                # N.B : pour windows, les "\\" et '/' seront remplacer
                # par '\'
        
####

    def f_SetNumberOfImgSrc( self, v_setNumber = False ) :
        """ **f_SetNumberOfImgSrc( int )**
        
            Permet de determiner le nombre d'image de la sequence.
            Si la valeur n'est pas fixee de facon arbitraire (v_setNumber), Le nombre
            d'image du dossier 'imgSrc' est divise par 2 car il y a une paritee entre les
            images "sujet" et les images 'vide'.
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_SetNumberOfImgSrc", self.f_SetNumberOfImgSrc)
        
        ## Action
        if not v_setNumber :
            v_setNumber = ( len( os.listdir( self.v_imgSrc ) ))
            if v_setNumber < 2 :
                v_msg = "Vous devez mettre au moins 2 photos dans le dossier 'imgSrc' !\n" \
                        "Ce dossier en comporte actuellement {}".format( v_setNumber )
                raise ValueError(v_msg)
                
            self.v_numberOfImgSrc  = v_setNumber // 2
            
            ## dbg
            i_debug(v_dbg2, "v_setNumber", v_setNumber)
            i_debug(v_dbg2, "v_numberOfImgSrc", self.v_numberOfImgSrc)
            
        ## Action
        else :
            if  not isinstance(v_setNumber, "int" ) : int( v_setNumber )
            if v_setNumber < 1 :
                v_msg = "Vous devez mettre une valeur au moin egale a '1' !"
                raise ValueError(v_msg)
                
            self.v_numberOfImgSrc = v_setNumber
            
            ## dbg
            i_debug(v_dbg2, "v_setNumber", v_setNumber)
            i_debug(v_dbg2, "v_numberOfImgSrc", self.v_numberOfImgSrc)            
####
            
    def f_runSequence( self, v_maskPrim, v_modelPrim ) :
        """ **f_runSequence( str, str )**
        
            Permet de lancer la sequence complete depuis un autre programme
            
            - v_maskPrim : c'est le mask (l'image vide)
            - v_modelPrim : c'est le model
            
            *N.B1* : les noms doivent etre saisie sans le numero car il sera ajouter dans
                   le traitemant pendant la boucle.
                  
            *N.B2* : La numerotation etant arbitraire, elle doit etre adaptee 
                   a vos besoin
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_runSequence", self.f_runSequence)
        
        ## Action        
        self.f_setWorkDir()
        self.f_SetNumberOfImgSrc()
            
        for n in range( self.v_numberOfImgSrc ) :
            print( "traitement d'image {} / {}".format( n+1, self.v_numberOfImgSrc ))
            
            v_mask = v_maskPrim + "_{:03}".format(n)
            v_model = v_modelPrim + "_{:03}".format(n)
            
            self.f_openImage( v_mask, v_img2 = v_model )
            self.f_imageSubst()
            self.f_createImage()
                               
            self.f_createMask( self.v_outputFilename )
            self.f_openImage( self.i_BWMask, v_maskOn = True )
            self.f_imageSubst()
            self.f_createImage()
            
            self.f_resetVar()

       
#####

def main() :
    """ Fonction principale

        Cette fonction permet d'utiliser se script de facon autonaume.
        
        Differentes options sont disponibles : 
        
            :'--help' ou '-h':      Permet d'obtenir l'aide sur les differentes options
                                    de se script.
                                    
            :'--images' ou '-i':    Permet de donnee le nom des 2 photos (ou des 2 series)
                                    qui devrons etre traitee par le script.
                                    Les 2 parametres, de type string, sont :
                                    
                                    1. Le nom de l'image vide (sans extension)
                                    2. Le nom du model (sans extension)
                                    
            :'--debug' ou '-d':     Permet d'afficher les differentes informations des
                                    methodes utilisees
                                    
            :'--number' ou '-n':    Permet de specifier le nombre d'iteration sur la serie.
                                    Le parametres est un entier.
                                    
                                    **N.B** : l'iteration formate les noms passee avec '_000'
                                     ( ou 000 est incremente a chaque iterration).
                                     Ce formatage est arbitraire et ne correspond peut
                                     etre pas au votre. Il est donc a adaptee en fonction
                                     de vos besions.
                                     
        Attention, les options 'debug' et 'number' ne sont pas active sans l'option 'images'
    """
    parser = argparse.ArgumentParser()
    parser.add_argument( "-i", "--images", nargs = "+",
                        help = "[nom_premiere_image_(mask)] [nom_seconde_image_(model)]")
    parser.add_argument( "-n", "--number", type=int, help="nombre d'image dans la serie")
    parser.add_argument( "-d", "--debug", action='store_true', help="activation du mode debug")
                        
    args = parser.parse_args()
    if args.images :
        if args.debug :
            print( "Mode Debug activer" )
            i_ic = C_ImageContour( True )
        else :
            i_ic = C_ImageContour( False )
        
        if (len(args.images) < 2) or (len(args.images) > 2) :
            print(  "\nvous devez entrer que 2 nom :\n",
                    "\tle 1er\t: Le nom de l'image servant de mask\n",
                    "\tle 2eme\t: le nom de l'image servant de modele" )
        else :
            i_ic.f_setWorkDir()
            l_lstArgsImage = []
            for i in args.images :
                l_lstArgsImage.append( i )
                
            v_maskPrim, v_modelPrim = l_lstArgsImage
            if args.number :
                for n in range( args.number ) :
                    print( "traitement d'image {} / {}".format( n+1, args.number ))
                    
                    v_mask = v_maskPrim + "_{:03}".format(n)
                    v_model = v_modelPrim + "_{:03}".format(n)
                    
                    i_ic.f_openImage( v_mask, v_img2=v_model )
                    i_ic.f_imageSubst()
                    i_ic.f_createImage()
                                       
                    i_ic.f_createMask( i_ic.v_outputFilename )
                    i_ic.f_openImage( i_ic.i_BWMask, v_maskOn=True )
                    i_ic.f_imageSubst()
                    i_ic.f_createImage()
                    
                    i_ic.f_resetVar()
                    
            
            else :
                v_mask = v_maskPrim
                v_model = v_modelPrim
                i_ic.f_openImage( v_mask, v_img2=v_model )
                i_ic.f_imageSubst()
                i_ic.f_createImage()
                                
                i_ic.f_createMask( i_ic.v_outputFilename )
                i_ic.f_openImage( i_ic.i_BWMask, v_maskOn=True )
                i_ic.f_imageSubst()
                i_ic.f_createImage()
            
            
    
if __name__ == '__main__':
    main()