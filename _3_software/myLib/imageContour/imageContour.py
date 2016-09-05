#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   :Nom du fichier:     imageContour.py
   :Autheur:            `Poltergeist42 <https://github.com/poltergeist42>`_
   :Version:            20160905

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

class C_ImageContour( object ) :
    """ **C_ImageContour( object )**
    
        Class permettant de detourer et d'isoler la forme exterieur d'un sujet pris sur
        fond unie.
    """
    def __init__( self ) :
        """ 
            **__init()**
        
            Creation et initialisation des variables globales de cette Class
        """
        
        ## Creation de l'instance pour les message de debug
        self.i_dbg = C_DebugMsg()
                
        ## declaration des variables
        self.i_img1     = False
        self.i_img2     = False
        self.i_BWMask   = False
        self.v_maskOn   = False
        
        self.npImg1     = False
        self.npImg2     = False
        Self.npBWMask   = False

###
        
    def __del__(self) :
        """
            **__del__()**
        
            Permet de terminer proprement l'instance de la Class courante
        
            il faut utilise : ::
            
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

    def imageOpen( self, v_img1, v_img2=False, v_maskOn=False ) :
        """ **imageOpen( str, str, bool )**
        
            Permet d'ouvrir les photos passees en arguments et de les convertir en Matrice.
            
            Le format des photos etant obligatoirement au format Jpeg, le nom des photos
            passees en arguments ne doivent pas comprtes l'extension '.jpeg' car elle sera 
            ajoute automatiquement.
            
            Seul 'v_img1' est obligatoire car au minimum, il n'y a qu'une seule phtoto a
            ouvrir (dans le cas d'un mask par exemple)
            
            Si l'une des 2 photos est un mask (en noir et blanc) la variable 'v_maskOn'
            doit etre mis a True et doit etre associer a 'v_img1'
            
            img1 est soit la photo vide, soit le mask en noir et blanc. C'est toujours 
            l'image a partir de laquelle nous ferons la soustrction (voir imageSubst).
            
            ex :
                imageResultat = imag1 - imag2
            
        """
        if v_img1 and not v_maskOn :
            self.i_img1 = v_img1 + ".jpg"
            self.npImg1 = np.array(Image.open(self.i_img1), dtype=i_np.uint8)
        
        if v_img2 :
            self.i_img2 = v_img2 + ".jpg"
            self.npImg2 = np.array(Image.open(self.i_img2), dtype=i_np.uint8)

        if v_maskOn and self.npImg2 :
            ## Creation d'une matrice de la taille de npImg2 et remplissage de cette matrice
            ## avec le contenu de npImg1
            Self.npBWMask = np.zeros(self.npImg2.shape, dtype=i_np.uint8)
            for rowIdx, row in enumerate( self.npImg1 ) :
                for colIdx, val in enumerate( row ) :
                    Self.npBWMask[rowIdx, colIdx] = self.npImg1[rowIdx, colIdx]

    def imageSubst( self, v_maskOn = False,  v_img1=False, v_img2=False) :
        """ **imageSubst( bool )**
        """
        ## soustraction de l'image vide (ou du mask Noir et Blanc) par le model
        self.npImg2 = i_np.clip(self.npImg2, 0, self.npImg1)
        npSubst = self.npImg1 - self.npImg2

        ## invertion des couleurs pour la remettre normal
        i_img = m_pilImg.fromarray(npSubst)
        v_outputFilename = "out_" + self.i_img2
        # i_img.save(v_outputFilename)
        
        i_invImgmage = ImageOps.invert(i_img)

        i_invImgmage.save(v_outputFilename)

            
