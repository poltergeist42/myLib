=====
myLib
=====

   :Autheur:          `Poltergeist42 <https://github.com/poltergeist42>`_
   :Projet:           myLib
   :Licence:          CC BY-NC-SA 4.0
   :Liens:            https://creativecommons.org/licenses/by-nc-sa/4.0/ 

------------------------------------------------------------------------------------------

Description
===========

 MyLib est le dépot dans lequel toutes les bibliothèques et module que je vais écrire seront
 centralisés.
 
 Depuis se dépot, si il est local, toutes les bibliothèques pourrons êtres redistribuées
 à l'ensemble des projet qui utilisent ses bibliothèques.
 
Liste des bibliothèques
=======================

:devChk:
    Librairie servant a l'assistance au developpement.
    
    Deux Class la composent :
    
        **C_DebugMsg**
            Pour afficher les messages debug en cours de devellopement.
        
        **C_GitChk**
            Pour tester la branch (git) sur la quelle on se trouve, a fin d'eviter
            les operations malheureuses.
            
:btnPoussoir:
    Librairie permettant d'utiliser des boutons poussoirs avec le Raspberry Pi.
    
    Liste des fonctionnalités :
    
        * Déclaration des GPIO en entrée
        * Gestion du mode Pull-UP / Pull-DOWN en interne et possibilité de la gérer en
          dehors du Pi.
        * Gestion des interruptions (action bloquante ou thread parallèle)
        
:fakeLib:
    Cette Librairie ne fait rien. Elle n'existe que pour pouvoir tester certain
    elements des autres lib en cours de developpement.

    La class est fictive, mais elle doit tout de meme etre commenter pour pourvoir generer
    la documentation de facon automatique avec Sphinx et ainsi pouvoir tester des elements
    de traitemant de la documentation.

:imageContour:
    Permet de détourer proprement une image (ou une série) pour ne laisser que le sujet de
    l'image. Cette bibliothèques sert notamenant pour l'amélioration des clichés pour la
    reconstitution d'image en 3D.

:libReplicator:
    Permet de copier et de mettre a jours les diferentes librairies dans
    l'ensemble des projet aux quels elles sont utiles.
    
:logIt:
    Permet de creer un fichier journal. Ce journal ce presente sous la forme suivante : ::
    
        'Titre de l'action'
         =================
    
        Descriptif
        
        [ TimeCode ] : action effectuee
        
        ################################################################################
        
    **N.B** : La library 'logging' fait déjà tous ça bien mieu.

:moteurPap:
    moteurPap est une bibliothèque permettant de manipuler un moteur Pas à Pas de type :
        * 28BJY-48
    
    au traver du driver :
        * UNL2003
        
:objJson:
    objJson est une librairie servant à manipuler des objets formater en Json depuis 
    et vers des dictionnaires.
    
:ultrason:
   ultrason est une bibliothèque permettant de manipuler un capteur ultrason de type :
        * HC-SR04
        