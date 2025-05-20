# dictionnaire pour FR --> EN 
fr_to_en = {
    "Maison": "HOUSE",
    "Appartement": "APARTMENT",
    "Maison standard": "STANDARD_HOUSE",
    "Appartement standard": "STANDARD_APARTMENT",
    "Propriété de luxe": "LUXURY_PROPERTY",
    "Appartement spécial": "SPECIAL_APARTMENT",
    "Usage mixte": "MIXED_USE",
    "Maison rurale": "RURAL_HOUSE",
    "Autre": "OTHER",
    "Bon": "GOOD",
    "Comme neuf": "AS_NEW",
    "Juste rénové": "JUST_RENOVATED",
    "À rénover": "TO_RENOVATE",
    "Inconnu": "UNKNOWN",
    "À rafraîchir": "TO_BE_DONE_UP",
    "À restaurer": "TO_RESTORE",
    "Gaz": "GAS",
    "Mazout": "FUELOIL",
    "Électrique": "ELECTRIC",
    "Bois": "WOOD",
    "Pellets": "PELLET",
    "Solaire": "SOLAR",
    "Charbon": "CARBON",
    "Installée": "INSTALLED",
    "Hyper équipée": "HYPER_EQUIPPED",
    "Non installée": "NOT_INSTALLED",
    "USA installée": "USA_INSTALLED",
    "USA non installée": "USA_UNINSTALLED",
    "USA hyper équipée": "USA_HYPER_EQUIPPED",
    "Semi équipée": "SEMI_EQUIPPED",
    "USA semi équipée": "USA_SEMI_EQUIPPED",
    "Zone non inondable": "NON_FLOOD_ZONE",
    "Zone inondable reconnue": "RECOGNIZED_FLOOD_ZONE",
    "Zone inondable possible": "POSSIBLE_FLOOD_ZONE",
    "Possible zone inondable non circonscrite": "POSSIBLE_N_CIRCUMSCRIBED_FLOOD_ZONE",
    "Zone inondable reconnue non circonscrite": "RECOGNIZED_N_CIRCUMSCRIBED_FLOOD_ZONE",
    # province
    'Flandre occidentale': 'West Flanders', 
    'Anvers':'Antwerp', 
    'Flandre occidentale': 'East Flanders', 
    'Brabant Flamand':'Flemish Brabant',
    'Hainaut' : 'Hainaut', 
    'Liège' : 'Liège', 
    'Limbourg':'Limburg',
    'Luxembourg' : 'Luxembourg', 
    'Namur' : 'Namur',  
    'Brabant wallon':'Walloon Brabant', 
    'Bruxelles':'Brussels',
    # region
    'Flandre' : 'Flanders',
    'Wallonie' : 'Wallonia',
    'Bruxelles' : 'Bruxelles'
}

# Inversion pour EN --> FR
en_to_fr = {en: fr for fr, en in fr_to_en.items()}

def translate_with_prefix (*prefixes):
    """
    Retourne la liste des clés EN qui commencent par un des préfixes.
    Utile pour filtrer par catégorie.
    """
    return [en for en in en_to_fr if any(en.startswith(p) for p in prefixes)]



