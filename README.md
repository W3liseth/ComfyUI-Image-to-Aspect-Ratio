# Image to aspect ratio

Redémarrer ComfyUI puis recharger la page. Ajouter **Image to aspect ratio**, catégorie **latent**.

## Installation

Depuis le dossier `ComfyUI/custom_nodes`, cloner ce dépôt puis redémarrer ComfyUI. Aucune dépendance supplémentaire à installer.

- `image` est facultative : son ratio exact et son orientation sont utilisés lorsqu'elle est connectée. Les pixels ne sont pas encodés.
- Sans image, choisir `aspect_ratio`. Pour un ratio libre, sélectionner `Custom` et renseigner `custom_ratio` dans les paramètres avancés (`5:7`, `1.85:1`, etc.).
- `megapixels` définit la surface cible ; 1 MP correspond à 1024 × 1024 pixels, comme dans les captures de référence.
- `multiple` définit la grille d'arrondi. Les dimensions respectent également le multiple de 8 requis par le latent standard (par exemple, un multiple de 10 donne une grille de 40).
- L'arrondi peut modifier légèrement le ratio et la surface. Avec `4:3`, `1.0` MP et un multiple de `32`, la sortie fait **1184 × 896**.
- Sorties : `latent`, `width`, `height`. La résolution réelle s'affiche sur le nœud après exécution. `batch_size` est disponible dans les paramètres avancés.

Le latent utilise le nœud natif Empty Latent Image : 4 canaux, réduction spatiale de 8, pour les modèles tels que SD 1.x et SDXL. Les modèles nécessitant un autre format latent ne sont pas pris en charge par cette sortie.

Aucune dépendance supplémentaire.
