from streamlit_local_storage import LocalStorage

class local_storage:

    def __init__(self):
        self.localS = LocalStorage()

    default_session_values = {
        'type_key': '--- Choisissez un type ---',
        'bedroomCount_key': 0,
        'bathroomCount_key': 0,
        'postCode_key': 1000,
        'habitableSurface_key': 0,
        'buildingCondition_key': 'GOOD',
        'buildingConstructionYear_key': 1900,
        'facedeCount_key': 2,
        'toiletCount_key': 1,
        'landSurface_key': 0,
        'hasGarden_key': False,
        'gardenSurface_key': 0,
        'hasSwimmingPool_key': False,
        'hasFireplace_key': False,
        'hasTerrace_key': False,
        'subtype_grouped_key': 'STANDARD_HOUSE',
        'floodZoneType_key': 'NON_FLOOD_ZONE',
        'heatingType_key': 'GAS',
        'kitchenType_key': 'INSTALLED',
        'building_floors_key': 0,
        'apartment_floor_key': 0,
        'region_key': "Wallonia",
        'epcNumeric_key': 'A',
        'province_key': 'Brussels',
        'locality_key': None
    }

    def initialize_state(self):
        '''
        Initialize local storage with default values if not already set
        '''
        for key, value in self.default_session_values.items():
            if self.get(key) is None:
                self.set(key, value)
                
    
    def get(self, key):
        ''' 
        Get local storage value by key
        '''

        return self.localS.get(key)

    def set(self, key, value):
        ''' 
        Set local storage value by key
        '''

        self.localS.set(key, value)
