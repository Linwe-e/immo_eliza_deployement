# Import libraries
import numpy as np
import streamlit as st
import pandas as pd
from pycaret.regression import load_model, predict_model

# Loading the trained model
# Try except verification
try:
    loaded_model = load_model('model/pipeline_immo_eliza')
    # st.sidebar.success("Modèle PyCaret chargé avec succès !")
except Exception as e:
    st.error(f"Erreur lors du chargement du modèle PyCaret : {e}")
    st.stop() # Stop app if error


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

    st.subheader("Data send to the predict model :") # For debug
    # st.dataframe(df_input_data)

    print("Colonnes de df_input_data:", df_input_data.columns.tolist())
    print("Nombre de colonnes de df_input_data:", len(df_input_data.columns))
    print("Première ligne de df_input_data:\n", df_input_data.head())
    # Si possible, affiche aussi les types de données pour vérifier
    print("Types de données de df_input_data:\n", df_input_data.dtypes)


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

def main():
    # Use all the wide
    st.set_page_config(layout="centered")

    # Title
    st.title('Immo Eliza AI 🏡')

    # Image 
    image_url = "image/accueil_immo_eliza.webp"
    st.image(image_url, width=300)

    # Welcome text
    welcome_text = """ ### Welcome !
   
    Curious about housing prices in Belgium ? This tool helps you get an estimated value.

    Just provide a few details about a property, and let's find out what it might be worth !
    """

    st.markdown(welcome_text)
    

    # Input from the user
    st.sidebar.header('Enter property details :')

    # Numerical data
    bedroomCount = st.sidebar.slider('Bedroom Count', min_value=0, max_value=10, step=1)
    bathroomCount = st.sidebar.slider('Bathroom Count', min_value=0, max_value=10, step=1)
    postCode = st.sidebar.number_input('Post Code', min_value=1000, max_value=9999, value=1000, step=1)
    habitableSurface = st.sidebar.number_input('Habitable Surface',min_value=0, step=1)
    buildingConstructionYear = st.sidebar.number_input('Building Construction Year', min_value=1800, max_value=2025, step=1)
    facedeCount = st.sidebar.number_input('Facede Count', min_value=2, max_value = 4, step=1)
    toiletCount = st.sidebar.number_input('Toilet Count', min_value=1, step=1)
    landSurface = st.sidebar.number_input('Land Surface', min_value=0, step=1)
    gardenSurface = st.sidebar.number_input('Garden Surface', min_value=0, step=1)
    # building_floors = st.sidebar.number_input('Building Floors for a house', min_value=0, value=2, step=1)
    # apartment_floor = st.sidebar.number_input('Apartment Floor for an apartment', min_value=0, value=2, step=1)

    # Categorical data
    type = st.sidebar.selectbox('Type', ['House', 'Apartment'])
    if type == 'House':
        building_floors = st.sidebar.number_input('Building Floors', min_value=0, value=0, step=1)
        apartment_floor = 0
    else:
        apartment_floor =  apartment_floor = st.sidebar.number_input('Apartment Floor', min_value=0, value=0, step=1)
        building_floors = 0
    

    subtype_grouped = st.sidebar.selectbox('SubType', ['STANDARD_HOUSE', 'STANDARD_APARTMENT',
                                                       'LUXURY_PROPERTY', 'SPECIAL_APARTMENT',
                                                       'MIXED_USE', 'RURAL_HOUSE', 'OTHER'])




    buildingCondition = st.sidebar.selectbox('Building Condition', [
        'GOOD', 'AS_NEW', 'JUST_RENOVATED', 
        'TO_RENOVATE', 'UNKNOWN', 
        'TO_BE_DONE_UP', 'TO_RESTORE'
    ])

    floodZoneType = st.sidebar.selectbox('Flood Zone Type', [
        'NON_FLOOD_ZONE', 'RECOGNIZED_FLOOD_ZONE', 'POSSIBLE_FLOOD_ZONE',
        'POSSIBLE_N_CIRCUMSCRIBED_FLOOD_ZONE',
        'RECOGNIZED_N_CIRCUMSCRIBED_FLOOD_ZONE', 'CIRCUMSCRIBED_WATERSIDE_ZONE',
        'CIRCUMSCRIBED_FLOOD_ZONE', 'POSSIBLE_N_CIRCUMSCRIBED_WATERSIDE_ZONE',
        'RECOGNIZED_N_CIRCUMSCRIBED_WATERSIDE_FLOOD_ZONE'])

    heatingType = st.sidebar.selectbox('Heating Type', [
        'GAS', 'FUELOIL', 'ELECTRIC', 'WOOD', 'PELLET', 'SOLAR', 'CARBON'
    ])

    kitchenType = st.sidebar.selectbox('Kitchen Type', [
        'INSTALLED', 'HYPER_EQUIPPED', 'NOT_INSTALLED', 'USA_INSTALLED',
        'USA_UNINSTALLED', 'USA_HYPER_EQUIPPED', 'SEMI_EQUIPPED',
        'USA_SEMI_EQUIPPED'
    ])

    epcNumeric = st.sidebar.selectbox('EPC Score', [
        'B', 'A', 'C', 'F', 'D', 'E', 'G', 'A+', 'A++'
    ])

    locality = st.sidebar.text_input('Locality') # What happen if the name is wrong spelled ?

    province = st.sidebar.selectbox('Province', ['West Flanders',      
                                                'Antwerp',           
                                                'East Flanders',     
                                                'Flemish Brabant',   
                                                'Hainaut',           
                                                'Liège',            
                                                'Limburg',           
                                                'Luxembourg',      
                                                'Namur',             
                                                'Walloon Brabant',
                                                'Brussels'])
    
    region = st.sidebar.selectbox('Region',['Bruxelles', 'Wallonia', 'Flanders'])

      

    # Bolean data
    st.sidebar.write('Additionnal features')
    hasGarden = st.sidebar.checkbox('Garden', value=False)
    hasSwimmingPool = st.sidebar.checkbox('Swimming Pool', value=False)
    hasFireplace = st.sidebar.checkbox('Fireplace', value=False)
    hasTerrace = st.sidebar.checkbox('Terrace', value=False)

    
    # Creating a button for prediction
    if st.button('Predict Price'):
        list_input_data = [type, bedroomCount, bathroomCount, province, locality,
       postCode, habitableSurface, buildingCondition,
       buildingConstructionYear, facedeCount, floodZoneType,
       heatingType, kitchenType, landSurface, hasGarden,
       gardenSurface, toiletCount, hasSwimmingPool, hasFireplace,
       hasTerrace, subtype_grouped, building_floors,
       apartment_floor, region, epcNumeric]

        predicted_price_value = immo_prediction(list_input_data)

    
        if isinstance(predicted_price_value, (int, float)):
                st.success(f"The estimated price of the property is : **{predicted_price_value:,.2f} €**")
        else:
            # L'erreur aura déjà été affichée dans immo_prediction ou lors du chargement du modèle
            st.error("La prédiction n'a pas pu être effectuée. Vérifiez les messages d'erreur ci-dessus.")

if __name__ == '__main__':
    main()


 
    



