fine_tune_rcnn.py: Tränar nätverket.

detect_all_pools.py: Itererar över alla bilder och och sparar bounding boxes för de pooler den hittar.

pool_coordinates.py: Omvandlar bounding boxes till världskoordinater och kopplar de till närmsta adress. 
Är adressen inte en villa eller om det är för långt avstånd mellan poolen och adressen så tas den bort.