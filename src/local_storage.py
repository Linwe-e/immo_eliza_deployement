from streamlit_local_storage import LocalStorage
import os

class LocalStorageWrapper:

    def __init__(self):
        self.localS = LocalStorage()

        self.prefix = 'immo_eliza_'
        self.default_session_values = {
            'type_key': '--- Choisissez un type ---',
            'bedroomCount_key': 1,
            'bathroomCount_key': 1,
            'postCode_key': 1000,
            'habitableSurface_key': 1,
            'buildingCondition_key': 'GOOD',
            'buildingConstructionYear_key': 1900,
            'facedeCount_key': 2,
            'toiletCount_key': 1,
            'landSurface_key': 1,
            'hasGarden_key': False,
            'gardenSurface_key': 1,
            'hasSwimmingPool_key': False,
            'hasFireplace_key': False,
            'hasTerrace_key': False,
            'subtype_grouped_key': 'STANDARD_HOUSE',
            'floodZoneType_key': 'NON_FLOOD_ZONE',
            'heatingType_key': 'GAS',
            'kitchenType_key': 'INSTALLED',
            'building_floors_key': 1,
            'apartment_floor_key': 1,
            'region_key': "Wallonia",
            'epcNumeric_key': 'A',
            'province_key': 'Brussels',
            'locality_key': None
    }
        
        # print("LocalStorageWrapper: Initialized") # --> Debug

    def _get_prefixed_key(self, key_suffix):
        ''' 
        Add prefix to key to avoid collisions with other keys
        '''
        return f"{self.prefix}{key_suffix}"
    
    def get(self, key_suffix):
        ''' 
        Get local storage value by key with prefix
        '''
        prefixed_item_key = self._get_prefixed_key(key_suffix)
        value = self.localS.getItem(prefixed_item_key)
        # print(f"LocalStorageWrapper: GET {prefixed_item_key} = {value}") # --> Debug
        return value
    
    def set(self, key_suffix, value):
        ''' 
        Set local storage value by key with prefix
        '''
        prefixed_item_key = self._get_prefixed_key(key_suffix)
        unique_key = f"set_{prefixed_item_key}"
        self.localS.setItem(prefixed_item_key, value, key=unique_key)
        # print(f"LocalStorageWrapper: SET {prefixed_item_key} = {value}") # --> Debug
   
    

    def initialize_state(self):
        '''
        Initialize local storage with default values if not already set
        '''
        # print("LocalStorageWrapper: initialize_state...") # --> Debug

        for key_suffix, default_value in self.default_session_values.items():
            current_value = self.get(key_suffix)
            if current_value is None:
                #print(f"LocalStorageWrapper: Initializing {key_suffix} with {default_value}") # --> Debug
                self.set(key_suffix, default_value)
            #else:
                #print(f"LocalStorageWrapper: {key_suffix} already exist to {current_value}") # --> Debug

    
    def get_all_items(self):
         '''
         Get all local storage values
         '''
         stored_values = {}
         for key_suffix in self.default_session_values.keys():
             stored_values[key_suffix] = self.get(key_suffix) # Utilise la méthode get existante
         
         #print(f"LocalStorageWrapper: All items retrieved: {stored_values}") # --> Debug
         
         return stored_values


