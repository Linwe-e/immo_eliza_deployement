# Import libraries
import numpy as np
import streamlit as st
import pandas as pd
from pycaret.regression import load_model, predict_model
from local_storage import LocalStorageWrapper
from traduction_fr import fr_to_en, en_to_fr, translate_with_prefix
from feedback_form import display_feedback_section


 # Use all the wide
st.set_page_config(layout="centered")

# Loading the trained model
# Try except verification
try:
    loaded_model = load_model('model/pipeline_immo_eliza')
    # st.sidebar.success("Modèle PyCaret chargé avec succès !")  # Check
except Exception as e:
    st.error(f"Erreur lors du chargement du modèle PyCaret : {e}")
    st.stop() # Stop app if error

# Import class LocalStorageWrapper

load_cache = LocalStorageWrapper()
load_cache.initialize_state()
session_values = load_cache.get_all_items( )

for key_from_defaults, default_val_from_wrapper in load_cache.default_session_values.items():
    # On récupère la valeur ACTUELLE du local storage (qui a pu être initialisée par initialize_state)
    value_currently_in_storage = load_cache.get(key_from_defaults)

    # Si la clé n'est PAS ENCORE dans st.session_state, on l'ajoute.
    if key_from_defaults not in st.session_state:
        target_value = None
        if value_currently_in_storage is not None:
            # Si on a une valeur du storage, on l'utilise
            target_value = value_currently_in_storage
        else:
            # Sinon, on utilise la valeur par défaut
            target_value = default_val_from_wrapper
        st.session_state[key_from_defaults] = target_value

# # Pour déboguer, juste avant de créer le slider :
# st.sidebar.subheader("Debug Info (Session State)")
# st.sidebar.write(f"Initial bedroomCount_key in session_state: {st.session_state.get('bedroomCount_key')}")
# st.sidebar.write(f"Initial Type: {type(st.session_state.get('bedroomCount_key'))}")
# st.sidebar.write(st.session_state)

# Data feedback
# Au début de ton application
if 'all_feedback' not in st.session_state:
    st.session_state.all_feedback = []

if 'feedback_submitted' not in st.session_state:
    st.session_state.feedback_submitted = False


EXPECTED_COLUMNS_ORDER = [
    'type', 'bedroomCount', 'bathroomCount', 'province', 'locality',
       'postCode', 'habitableSurface', 'buildingCondition',
       'buildingConstructionYear', 'facedeCount', 'floodZoneType',
       'heatingType', 'kitchenType', 'landSurface', 'hasGarden',
       'gardenSurface', 'toiletCount', 'hasSwimmingPool', 'hasFireplace',
       'hasTerrace', 'subtype_grouped', 'building_floors',
       'apartment_floor', 'region', 'epcNumeric']

# Creating a function for Prediction

def immo_prediction(list_input_data):
    global loaded_model
    global EXPECTED_COLUMNS_ORDER

    if len(list_input_data) != len(EXPECTED_COLUMNS_ORDER):
        st.error(f"Incohérence de données : {len(list_input_data)} valeurs reçues, {len(EXPECTED_COLUMNS_ORDER)} attendues.")
        return "Erreur de prédiction (taille des données)"
    
    # Changin the data into a Dataframe
    df_input_data = pd.DataFrame([list_input_data], columns=EXPECTED_COLUMNS_ORDER)

    # add region information
    def get_region(zip_code):
        # On tente de convertir en int
        try:
            z = int(zip_code)
        except (ValueError, TypeError):
            return pd.NA    

        if 1000 <= z <= 1299:
            return "Bruxelles"
        elif 1300 <= z <= 1499 or 4000 <= z <= 7999:
            return "Wallonia"
        else:
            return "Flanders"

    df_input_data['region'] = df_input_data['postCode'].apply(get_region)

    # add and convert epc score
    def epcToNumeric(row):
        region = row['region']
        epc_score = row['epcNumeric']
        
        epc_mapping = {
            'Flanders': {
                'A++': 0,
                'A+': 0,
                'A': 100,
                'B': 200,
                'C': 300,
                'D': 400,
                'E': 500,
                'F': 600,
                'G': 700
            },
            'Wallonia': {
                'A++': 0,
                'A+': 50,
                'A': 90,
                'B': 170,
                'C': 250,
                'D': 330,
                'E': 420,
                'F': 510,
                'G': 600
            },
            'Bruxelles': {
                'A++': 0,
                'A+': 0,
                'A': 45,
                'B': 95,
                'C': 145,
                'D': 210,
                'E': 275,
                'F': 345,
                'G': 450
            }
        }
        
        return epc_mapping.get(region, {}).get(epc_score, None)
    
    df_input_data['epcNumeric'] = df_input_data.apply(epcToNumeric, axis=1)

    # st.subheader("Data envoyé au modèle prédictif :") # For debug

    print("Colonnes de df_input_data:", df_input_data.columns.tolist())
    print("Nombre de colonnes de df_input_data:", len(df_input_data.columns))
    print("Première ligne de df_input_data:\n", df_input_data.head())
    # Si possible, affiche aussi les types de données pour vérifier
    # print("Types de données de df_input_data:\n", df_input_data.dtypes)


    try:
        # Utiliser predict_model de PyCaret
        predictions_df = predict_model(estimator=loaded_model, data=df_input_data)
        
        # Extraire la valeur prédite (souvent dans 'prediction_label' ou 'Label')
        # Vérifie le nom exact de la colonne de prédiction retournée par ton modèle PyCaret
        if 'prediction_label' in predictions_df.columns:
            predicted_value = predictions_df['prediction_label'].iloc[0]
        elif 'Label' in predictions_df.columns: # Ancien nom ou pour d'autres types de tâches
            predicted_value = predictions_df['Label'].iloc[0]
        else:
            st.error(f"Colonne de prédiction ('prediction_label' ou 'Label') non trouvée dans le résultat : {predictions_df.columns.tolist()}")
            return "Erreur de prédiction (colonne résultat)"
            
        return predicted_value

    except Exception as e:
        st.error(f"Erreur lors de la prédiction par le modèle : {e}")
        st.exception(e) # Affiche la trace complète de l'erreur pour le débogage
        return "Erreur de prédiction (exception)"
    

# Callback function to update local storage when a session_state item changes
def update_local_storage_callback(item_key):
    if item_key in st.session_state:
        # print(f"Callback: Updating local storage for {item_key} with value {st.session_state[item_key]}") # Debug
        load_cache.set(item_key, st.session_state[item_key])

    

def main():
    # Title
    st.title('Immo Eliza AI 🏡')

    # Image 
    image_url = "image/accueil_immo_eliza.webp"
    st.image(image_url, width=300)

    # Welcome text
    welcome_text = """ ### Bienvenue !
    
    Curieux de connaître les prix de l'immobilier en Belgique ? Cet outil vous permet d'obtenir une estimation.
    
    Il vous suffit de fournir quelques informations sur un bien immobilier, et nous découvrirons ce qu'il pourrait valoir !
    """

    st.markdown(welcome_text)
    

    # --- SIDEBAR ---
    st.sidebar.header('🔍 Caractéristiques du Bien')

    # Expander 1
    with st.sidebar.expander("🏡 Infos Générales & Structure", expanded=False):

        type_options = translate_with_prefix('HOUSE', 'APARTMENT')
        type = st.selectbox('Type de bien', type_options,
                                key='type_key', format_func=lambda en: en_to_fr[en],
                                on_change=update_local_storage_callback, args=('type_key',))
        #Conditional inputs for building_floors and apartment_floor
        # Initialize to 0 if not the selected type, to avoid issues with the model later
        building_floors_val = st.session_state.get('building_floors_key', 0)
        apartment_floor_val = st.session_state.get('apartment_floor_key', 0)

        if type == 'HOUSE':
            building_floors = st.number_input("Nombre d'étages", min_value=0, step=1, 
                                                    key='building_floors_key',
                                                    on_change=update_local_storage_callback, args=('building_floors_key',))
            # When type is HOUSE, apartment_floor should conceptually be 0 or NA for the model.
            # We ensure session_state reflects this if it changes.
            if st.session_state.apartment_floor_key != 0: # Check if it needs update
                st.session_state.apartment_floor_key = 0
                update_local_storage_callback('apartment_floor_key') # Persist this change
            apartment_floor = 0 # For the list_input_data
        elif type == 'APARTMENT':
            apartment_floor =  st.number_input("Etage de l'appartement", min_value=0, step=1, 
                                                    key='apartment_floor_key',
                                                    on_change=update_local_storage_callback, args=('apartment_floor_key',))
            if st.session_state.building_floors_key != 0: # Check if it needs update
                st.session_state.building_floors_key = 0
                update_local_storage_callback('building_floors_key') # Persist this change
            building_floors = 0 # For the list_input_data
        else: # '--- Choisissez un type ---' or other
            # Default to 0 if no type is selected or if values are not set.
            building_floors = building_floors_val 
            apartment_floor = apartment_floor_val
            
        subtype_options = translate_with_prefix('STANDARD_HOUSE', 'STANDARD_APARTMENT', 'LUXURY_PROPERTY', 'SPECIAL_APARTMENT', 'MIXED_USE', 'RURAL_HOUSE', 'OTHER')
        subtype_grouped = st.selectbox('Sous-type', subtype_options,
                                           key='subtype_grouped_key', format_func=lambda en: en_to_fr[en],
                                           on_change=update_local_storage_callback, args=('subtype_grouped_key',))

        habitableSurface = st.number_input('Surface habitable',min_value=0, step=1, 
                                               key='habitableSurface_key',
                                               on_change=update_local_storage_callback, args=('habitableSurface_key',))
        
        buildingCondition_options = translate_with_prefix('GOOD', 'AS_NEW', 'JUST_RENOVATED', 'TO_RENOVATE', 'UNKNOWN', 'TO_BE_DONE_UP', 'TO_RESTORE')
        buildingCondition = st.selectbox('Etat du bâtiment',
                                                 buildingCondition_options,
                                                 key='buildingCondition_key', 
                                                 format_func=lambda en: en_to_fr[en],
                                                 on_change=update_local_storage_callback, args=('buildingCondition_key',))

        buildingConstructionYear = st.number_input('Année de construction', min_value=1800, max_value=2025, step=1, 
                                                       key='buildingConstructionYear_key',
                                                       on_change=update_local_storage_callback, 
                                                       args=('buildingConstructionYear_key',))

        facedeCount = st.number_input('Nombre de façades', min_value=0, max_value = 4, step=1,  # min_value can be 0, 1, 2, 3, 4
                                          key='facedeCount_key',
                                          on_change=update_local_storage_callback, 
                                          args=('facedeCount_key',))
        

    # Expander 2
    with st.sidebar.expander("📍 Localisation"):

        province_options = translate_with_prefix('West Flanders', 'Antwerp', 'East Flanders', 
                            'Flemish Brabant', 'Hainaut', 'Liège', 'Limburg', 
                            'Luxembourg', 'Namur', 'Walloon Brabant', 'Brussels')
        province = st.selectbox('Province', province_options,
                                     key='province_key',
                                     format_func=lambda en: en_to_fr[en],
                                     on_change=update_local_storage_callback, 
                                     args=('province_key',))
        
        region_options = translate_with_prefix('Wallonia', 'Flanders', 'Bruxelles')
        region = st.selectbox('Région',region_options,
                                  key='region_key', 
                                  format_func=lambda en: en_to_fr[en],
                                  on_change=update_local_storage_callback, 
                                  args=('region_key',))
        
        locality = st.text_input('Localité', 
                                     key='locality_key',
                                     on_change=update_local_storage_callback, 
                                     args=('locality_key',)) # What happen if the name is wrong spelled ?


        postCode = st.number_input('Code postal', min_value=1000, max_value=9999, step=1, 
                                       key='postCode_key',
                                       on_change=update_local_storage_callback, 
                                       args=('postCode_key',)) # Removed default value=1000 to rely on session_state
       
        floodZoneType_options = translate_with_prefix('NON_FLOOD_ZONE', 'RECOGNIZED_FLOOD_ZONE', 
                                 'POSSIBLE_FLOOD_ZONE', 'POSSIBLE_N_CIRCUMSCRIBED_FLOOD_ZONE', 
                                 'RECOGNIZED_N_CIRCUMSCRIBED_FLOOD_ZONE', 'CIRCUMSCRIBED_WATERSIDE_ZONE', 
                                 'CIRCUMSCRIBED_FLOOD_ZONE', 'POSSIBLE_N_CIRCUMSCRIBED_WATERSIDE_ZONE', 
                                 'RECOGNIZED_N_CIRCUMSCRIBED_WATERSIDE_FLOOD_ZONE')
        floodZoneType = st.selectbox('Type de zone inondable', floodZoneType_options,
                                             key='floodZoneType_key', 
                                             format_func=lambda en: en_to_fr[en],
                                             on_change=update_local_storage_callback, args=('floodZoneType_key',))
        
    # Expander 3: Agencement Intérieur et Confort
    with st.sidebar.expander("🛋️ Agencement Intérieur & Confort"):

        bedroomCount = st.slider('Nombre de chambres', min_value=0, max_value=10, step=1, 
                                     key='bedroomCount_key', 
                                     on_change=update_local_storage_callback, 
                                     args=('bedroomCount_key',))
        
        bathroomCount = st.slider('Nombre de salles de bain', min_value=0, max_value=10, step=1, 
                                      key='bathroomCount_key',
                                      on_change=update_local_storage_callback,
                                      args=('bathroomCount_key',))
        
        toiletCount = st.number_input('Nombre de toilettes', min_value=0, step=1, 
                                          key='toiletCount_key',
                                          on_change=update_local_storage_callback, 
                                          args=('toiletCount_key',))
        
        kitchenType_options = translate_with_prefix('INSTALLED', 'HYPER_EQUIPPED', 'NOT_INSTALLED', 'USA_INSTALLED', 
                               'USA_UNINSTALLED', 'USA_HYPER_EQUIPPED', 'SEMI_EQUIPPED', 
                               'USA_SEMI_EQUIPPED')
        kitchenType = st.selectbox('Type de cuisine', kitchenType_options,
                                           key='kitchenType_key',
                                           format_func=lambda en: en_to_fr[en],
                                           on_change=update_local_storage_callback, 
                                           args=('kitchenType_key',))
        
        heatingType_options = translate_with_prefix('GAS', 'FUELOIL', 'ELECTRIC', 'WOOD', 'PELLET', 'SOLAR', 
                               'CARBON')
        heatingType = st.selectbox('Type de chauffage', heatingType_options,
                                           key='heatingType_key',
                                           format_func=lambda en: en_to_fr[en],
                                           on_change=update_local_storage_callback, 
                                           args=('heatingType_key',))
        
       
        epcNumeric_options = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'A+', 'A++']
        epcNumeric = st.selectbox('PEB', epcNumeric_options,
                                          key='epcNumeric_key',
                                          on_change=update_local_storage_callback, 
                                          args=('epcNumeric_key',))
        
        hasFireplace = st.checkbox('Cheminée', 
                                    key='hasFireplace_key',
                                    on_change=update_local_storage_callback, 
                                    args=('hasFireplace_key',))
        
    # Expander 4 
    with st.sidebar.expander("🌳 Extérieur & Annexes"):

        landSurface = st.number_input('Surface du terrain', min_value=0, step=1, 
                                          key='landSurface_key',
                                          on_change=update_local_storage_callback, 
                                          args=('landSurface_key',))
        
        hasGarden = st.checkbox('Jardin', 
                                    key='hasGarden_key',
                                    on_change=update_local_storage_callback, 
                                    args=('hasGarden_key',))
        if st.session_state.hasGarden_key == True:
            gardenSurface = st.number_input('Garden Surface', min_value=0, step=1, 
                                            key='gardenSurface_key',
                                            on_change=update_local_storage_callback, 
                                            args=('gardenSurface_key',))
        else:
            gardenSurface = 0
            st.session_state['gardenSurface'] = gardenSurface 

        hasTerrace = st.checkbox('Terrasse', 
                                         key='hasTerrace_key',
                                         on_change=update_local_storage_callback, 
                                         args=('hasTerrace_key',))
        
        hasSwimmingPool = st.checkbox('Piscine', 
                                          key='hasSwimmingPool_key',
                                          on_change=update_local_storage_callback, 
                                          args=('hasSwimmingPool_key',))

    
    # Creating a button for prediction
    if st.button("Prédire le prix", type="primary"):
        # Ensure building_floors and apartment_floor are correctly sourced from session_state for prediction
        # as their direct widget variables might be conditionally defined
        list_input_data = ([type, 
                            bedroomCount, bathroomCount, province, locality, 
                            postCode, habitableSurface, buildingCondition,
                            buildingConstructionYear, facedeCount, floodZoneType,
                            heatingType, kitchenType, landSurface, hasGarden,
                            gardenSurface, toiletCount, hasSwimmingPool, hasFireplace,
                            hasTerrace, subtype_grouped, building_floors,
                            apartment_floor, region, epcNumeric])

        predicted_price_value = immo_prediction(list_input_data)

        # Afficher les résultats avec un effet visuel
        with st.spinner("Analyse en cours..."):
            import time
            time.sleep(1)

        if isinstance(predicted_price_value, (int, float)):
            # STOCKER la prédiction dans session_state
            st.session_state.last_prediction = predicted_price_value
            
            # --- Mise en forme prix estimé ---
            wch_colour_box_rgb = "0,204,102"  # Vert 
            wch_colour_font_rgb = "0,0,0"    # Noir 
            fontsize = "18px"
            
            texte_prix = "Le prix du bien est estimé à : "
            prix_formate = f"{int(predicted_price_value):,.2f} €"
            message_principal = f"{texte_prix}<strong>{prix_formate}</strong>"

            iconname = "fas fa-check-circle" # Ou un icône de succès
    
            # Lien Font Awesome
            lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'

            htmlstr = f"""
                <div style="
                    background-color: rgba({wch_colour_box_rgb}, 0.75);
                    color: rgb({wch_colour_font_rgb});
                    font-size: {fontsize};
                    border-radius: 7px;
                    padding: 18px 12px;
                    line-height: 1.6;
                    margin-bottom: 10px; /* Ajoute un peu d'espace en dessous */
                ">
                    <i class='{iconname} fa-fw'></i> {message_principal}
                    
             
            """
            st.markdown(lnk + htmlstr, unsafe_allow_html=True)
        
        else:
            st.error("La prédiction n'a pas pu être effectuée. Vérifiez les messages d'erreur ci-dessus.")
            st.session_state.last_prediction = None

   
    # Section feedback - toujours visible après une prédiction
    if 'last_prediction' in st.session_state and st.session_state.last_prediction is not None:
        display_feedback_section(st.session_state.last_prediction)


    # --- DEBUG ---
    # Afficher le contenu de session state 
    # if st.sidebar.checkbox("Voir session state"):
    #     st.sidebar.write(st.session_state)

    # voir les feedbacks actuels
    # if st.checkbox("🔧 Mode debug"):
    #     if 'all_feedback' in st.session_state:
    #         st.write("Feedbacks stockés:", st.session_state.all_feedback)
    #     else:
    #         st.write("Aucun feedback trouvé")

        

if __name__ == '__main__':
    main()


 
    # Pied de page
st.markdown("---")
st.caption("_Immo Eliza AI - Développé dans le cadre d'un projet de formation IA chez BeCode_")
