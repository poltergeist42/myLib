#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   :Nom du fichier:     imageContour.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20160908

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
            passees en arguments ne doivent pas compotes l'extension '.jpeg' car elle sera 
            ajoute automatiquement.
            
            Seul 'v_img1' est obligatoire car au minimum, il n'y a qu'une seule phtoto a
            ouvrir (dans le cas d'un mask par exemple)
            
            Si v_img1 est un mask (en noir et blanc) la variable 'v_maskOn'
            doit etre mis a True. l'argument a donner pour v_img1 doit normalement etre le
            contenu de 'i_BWMask'.
            
            v_img1 est soit la photo vide, soit le mask en noir et blanc. C'est toujours 
            l'image a partir de laquelle nous ferons la soustrction (voir imageSubst).
            
            ex :
                imagSubst = imag1 - imag2
            
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_openImage", self.f_openImage)
        
        ## Action
        if v_img1 and not v_maskOn :
            self.i_img1 = v_img1 + ".jpg"
            self.m_npImg1 = np.array(Image.open(self.i_img1), dtype = np.uint8)
        
        if v_img2 :
            self.i_img2 = v_img2 + ".jpg"
            self.m_npImg2 = np.array(Image.open(self.i_img2), dtype = np.uint8)

        if v_maskOn and not v_img2 :
            ## Creation d'une matrice de la taille de m_npImg2 et remplissage de cette matrice
            ## avec le contenu de m_npImg1
            self.i_img1 = v_img1 + ".jpg"
            self.m_npImg1 = np.array(Image.open(self.i_img1), dtype = np.uint8)
            self.m_npBWMask = np.zeros(self.m_npImg2.shape, dtype = np.uint8)
            for rowIdx, row in enumerate( self.m_npImg1 ) :
                for colIdx, val in enumerate( row ) :
                    self.m_npBWMask[rowIdx, colIdx] = self.m_npImg1[rowIdx, colIdx]
                    
            self.m_npImg1 = self.m_npBWMask

####

    def f_imageSubst( self) :
        """ **f_imageSubst(  )**
        
            Soustraction de l'image vide (ou du mask Noir et Blanc) par le model
            
            **N.B :** Pour ne pas avoir de valeur negative lors de la soustraction, les
            valeurs de la matrice m_npImg2 (la matrice du modele) sont contrainte entre
            m_npImg2 (lui meme) pour les valeurs hautes et m_npImg1 pour les valeur basses
            
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
        
            Permet de creer l'image finale (ou intermediaire si l'on ne souhaite pas creer
            le mask.
            
            Le nom l'image generee aura le prefix 'out_' suivie du nom du model (i_img2)
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
            
        self.i_imgSubst.save(self.v_outputFilename)
        
####

    def f_createMask( self, v_img1, v_show = False ) :
        """ **f_createMask( str, bool )**
        
            permet d'effectuer les traitemants de l'image intermediaire avec openCV.
            Ces traitemant convertissent l'image en Noir et blanc. La zone Noir correspond
            au fond de l'image alors que le blanc correspond a la forme du modele.
            
            c'est la valeur de la variable 'v_outputFilename' qui doit etre passe 
            en argument v_img1.
            
            Lorsque 'v_show' est vrai, l'image en cours de traitemant sera afficher 
            a l'ecran.
            
            L'image creer apres le traitemant se nomme 'cvOut.jpg' ce nom est sauvegarde
            dans la variable 'i_BWMask'
            
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_createMask", self.f_createMask)
        
        ## Action
        
        # charger l'image, la convertir en niveaux de gris, et la brouiller legerement
        i_image = cv2.imread(v_img1)
        i_gray = cv2.cvtColor(i_image, cv2.COLOR_BGR2GRAY)
        i_gray = cv2.GaussianBlur(i_gray, (5, 5), 0)


        # seuillage de l'image, avant d'effectuer une serie de traitemant pour eliminer
        # toutes zone de bruit sur l'image
        i_work = cv2.threshold(i_gray, 45, 255, cv2.THRESH_BINARY)[1]
        i_work = cv2.erode(i_work, None, iterations=2)
        i_work = cv2.dilate(i_work, None, iterations=2)
        if v_show : cv2.imshow("i_work", i_work)
        cv2.imwrite("cvOut.jpg", i_work)
        self.i_BWMask = "cvOut"
        
        self.f_setMask()

        
####

    def f_invert( self ) :
        """ **f_invert( )**
         
            invertion des couleurs pour remettre normal l'image avec la bonne apparence
        """
        ## dbg
        v_dbg = 1
        v_dbg2 = 1
        i_debug = self.i_dbg.dbgPrint
        i_debug(v_dbg2, "f_invert", self.f_invert)
        
        ## Action
        self.i_imgSubst = ImageOps.invert(self.i_imgSubst)
        
    def f_setMask( self ) :
        """ **f_setMask()**
        
            Inverse automatiquement la valeur de 'v_maskOn'
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
            
    def f_resetVar( self ) :
        """ **f_resetVar()**
        
            reinitialise toutes les variable de l'instance
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
       
#####

def main() :
    """ Fonction principale """
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
            l_lstArgsImage = []
            for i in args.images :
                l_lstArgsImage.append( i )
                
            v_maskPrim, v_modelPrim = l_lstArgsImage
            if args.number :
                for n in range( args.number ) :
                    v_mask = v_maskPrim + "_{:03}".format(n)
                    v_model = v_modelPrim + "_{:03}".format(n)
                    
                    i_ic.f_openImage( v_mask, v_img2=v_model )
                    i_ic.f_imageSubst()
                    i_ic.f_createImage()
                    
                    # input( "\nappuyez sur entree pour continuer\n" )
                    
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
                
                # input( "\nappuyez sur entree pour continuer\n" )
                
                i_ic.f_createMask( i_ic.v_outputFilename )
                i_ic.f_openImage( i_ic.i_BWMask, v_maskOn=True )
                i_ic.f_imageSubst()
                i_ic.f_createImage()
            
            
    
if __name__ == '__main__':
    main()