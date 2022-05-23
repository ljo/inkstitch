---
title: "Gestion des couleurs de fil"
permalink: /fr/docs/thread-color/
excerpt: ""
last_modified_at: 2022-04-03
toc: true
---
## Importer une liste de fils

Ink/Stitch peut appliquer des listes de fil personnalisées à une broderie. Ceci est particulièrement utile si vous souhaitez utiliser un fichier de broderie qui ne comporte pas d'information de couleur (par exemple DST).

Ce peut être aussi utile si vous souhaitez essayer différents réglages de couleurs. Vous pouvez exporter et importer ces listes de fils à votre convenance, mais faites attention à ne changer ni le nombre ni l'ordre des couleurs. Si vous souhaitez les changer, faites le dans une copie du fichier svg.

## Importation

Exécutez `Extensions > Ink/Stitch > Importer liste de fils ...` pour appliquer une liste de fils exportée par  Ink/Stitch.

Si vous souhaitez importer une autre liste de fils en provenance d'un fichier txt, choisissez l'option "importer une autre liste de fils ", et choisissez une liste de fil à partir du menu déroulant avant de cliquer sur "Appliquer"


**Astuce:** Installez des  Add-Ons pour Ink/Stitch pour avoir plus de listes de fils disponibles.
{: .notice--info }

## Exportation

Les listes de fils ne peuvent être exportées qu'en enregistrant une copie du fichier au format "Ink/Stitch: ZIP exporter plusieurs formats (.zip)" , puis après avoir cliqué sur "Enregistrer" selectionnez le format ".TXT: liste de fils".

[Lire plus à propos de cette fonction](/fr/docs/threadlist/)

## Installer une Palette personnalisée 

Si vous disposez d'un fichier `.gpl` qui contient la liste des fils que vous utilisez, vous pouvez la rendre disponible dans Ink/Stitch via cette extension: `Extensions > Ink/Stitch > Gestion des couleurs de fil > Installer une palette personnalisée...`. Vous devrez ensuite redémarrer Inkscape.

Les fichiers `.gpl` de palettes peuvent être générés par GIMP.

## Installer des Palettes de couleurs de fils à broder pour Inkscape

Ink/Stitch est fourni avec de nombreuses palettes de fils de fabricants qui peuvent être installées dans Inkscape. Ceci permet de construire des broderies avec les bonnes couleurs à l'esprit.
Les couleurs apparaîtront dans la sortie pdf et seront aussi incluses dans votre fichier de broderie si son format le permet.

**Installer**
* Allez à `Extensions > Ink/Stitch  > Gestion des couleurs de fil > Installer des palettes de couleurs de fils à broder pour Inkscape`
* Cliquez sur `Installer`
* Redémarrez Inkscape

## Utiliser les Palettes de couleurs du fabricant de fils

Une fois installées, les palettes Inkscape se trouvent dans la partie inférieure droite des nuanciers.

![Inkscape Color Palettes](/assets/images/docs/palettes-location.png)

Cliquez sur la petite flèche pour ouvrir une liste des palettes installées et choisissez la palette de couleurs du fabricant en fonction du fil que vous souhaitez utiliser.

Le choix s'appliquera également aux noms de fil à afficher dans l'aperçu avant impression.

## Generer une palette de couleur

{% include upcoming_release.html %}


Inkscape permet de générer des fichiers `.gpl`  de palette de couleurs. Mais il ne permet pas d'ordonner correctement les échantillons de couleur.

Cette extension exportera les couleur d'éléments textuels tout en utilisant le texte pour le noms et numéros des couleurs.

1. Importez une image avec les couleurs de fils que vous voulez utilisez pour la palette de couleurs. 
2. Activezl'outil texte et copier/collet les noms de couleurs (si vous les avez) ou saisissez les.
   Utilisez une ligne par couleur.
   Si un nom de couleur se termine par un nombre, ce nombre sera utilisé pour cette couleur dans le catalogue.
3. Utilisez `Extensions > Ink/Stitch > Gestion des couleurs de fils > Generer une palette de couleurs > Diviser le texte` pour diviser un bloc de texte avec plusieurs lignes en plusieurs éléments textuels séparés. 
4. Activez l'outil pipette (D) et colorez les éléments textuels, en utilisant les tabulation pour passer de l'un à l'autre.
5. Selectionnez les éléments textuels et  `Extensions > Ink/Stitch > Gestion des couleurs de fil > Generer une palette de couleurs > Generer une palette de couleurs...`
6. Specifiez le nom de votre palette de couleurs et cliquez sur Appliquer

{% include video id="4bcRVoKvzAw" provider="youtube" %}

## Palette to Text

{% include upcoming_release.html %}

Existing palettes can be edited with Ink/Stitch as text.

* Import colors and color names with `Extensions > Ink/Stitch > Thread Color Management > Palette to Text`
* Change colors, update color names or catalog numbers or add more colors.
* Export your palette with `Extensions > Ink/Stitch > Thread Color Management > Generate Palette > Generate Color Palette ...`
* Restart Inkscape