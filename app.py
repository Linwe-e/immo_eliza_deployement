# Import libraries
import numpy as np
import streamlit as st
import pandas as pd
from pycaret.regression import load_model, predict_model

# Loading the trained model
# Try except verification
try:
    loaded_model = load_model('Light Gradient Boosting Machine')
    # st.sidebar.success("Modèle PyCaret chargé avec succès !")
except Exception as e:
    st.error(f"Erreur lors du chargement du modèle PyCaret : {e}")
    st.stop() # Stop app if error


EXPECTED_COLUMNS_ORDER = [
    'type', 'subtype', 'bedroomCount', 'bathroomCount', 'locality',
    'postCode', 'habitableSurface', 'buildingCondition',
    'buildingConstructionYear', 'facedeCount', 'floodZoneType',
    'heatingType', 'kitchenType', 'hasGarden_1', 'toiletCount',
    'hasSwimmingPool_True', 'hasFireplace_True', 'hasTerrace_True',
    'epcScore']



# Creating a function for Prediction

def immo_prediction(list_input_data):
    global loaded_model
    global EXPECTED_COLUMNS_ORDER

    if len(list_input_data) != len(EXPECTED_COLUMNS_ORDER):
        st.error(f"Incohérence de données : {len(list_input_data)} valeurs reçues, {len(EXPECTED_COLUMNS_ORDER)} attendues.")
        return "Erreur de prédiction (taille des données)"

    #  # Changing the data into a NumPy array
    # input_data_as_nparray = np.asarray(input_data)

    # Reshaping the data since there is only one instance
    # input_data_reshaped = input_data_as_nparray.reshape(1, -1)
    
    # Changin the data into a Dataframe
    df_input_data = pd.DataFrame([list_input_data], columns=EXPECTED_COLUMNS_ORDER)

    st.subheader("Data send to the predict model :") # For debug
    # st.dataframe(df_input_data)

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
    st.set_page_config(layout="wide")

    # Title
    st.title('Immo Eliza AI 🏡')

    # Image 
    image_url = 'https://plus.unsplash.com/premium_photo-1661427080615-a954867eaeca?q=80&w=1032&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    st.image(image_url, use_container_width=True)

    # Welcome text
    welcome_text = """ ### Welcome !
   
    Curious about housing prices in Belgium ? This tool helps you get an estimated value.

    Just provide a few details about a property, and let's find out what it might be worth !
    """

    st.markdown(welcome_text)
    

    # Input from the user
    st.sidebar.header('Enter property details :')

    # Numerical data
    bedroomCount = st.sidebar.number_input('Bedroom Count', min_value=0, value=2, step=1)
    bathroomCount = st.sidebar.number_input('Bathroom Count', min_value=0, value=1, step=1)
    postCode = st.sidebar.number_input('Post Code', min_value=1000, max_value=9999, value=1000, step=1)
    habitableSurface = st.sidebar.slider('Habitable Surface',min_value=0, max_value=1000, value=100, step=1)
    buildingConstructionYear = st.sidebar.slider('Building Construction Year', min_value=1800, max_value=2025, value=1990, step=1)
    facedeCount = st.sidebar.number_input('Facede Count', min_value=0, value=2, step=1)
    toiletCount = st.sidebar.number_input('Toilet Count', min_value=0, value=1, step=1)

    # Categorical data
    type = st.sidebar.selectbox('Type', ['House', 'Appartment']) 

    subtype = st.sidebar.selectbox('SubType', [
        'EXCEPTIONAL_PROPERTY', 'VILLA', 'HOUSE', 'MANSION', 'MIXED_USE_BUILDING', 
        'PENTHOUSE', 'APARTMENT', 'DUPLEX', 'GROUND_FLOOR', 'CASTLE',
        'COUNTRY_COTTAGE', 'MANOR_HOUSE', 'FARMHOUSE', 'TOWN_HOUSE', 'LOFT', 'TRIPLEX',
        'OTHER_PROPERTY', 'BUNGALOW', 'KOT', 'SERVICE_FLAT', 'FLAT_STUDIO', 'CHALET',
        'PAVILION'
    ])

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

    epcScore = st.sidebar.selectbox('EPC Score', [
        'B', 'A', 'C', 'F', 'D', 'E', 'G', 'A+', 'A++'
    ])

    locality = st.sidebar.text_input('Locality') # What happen if the name is wrong spelled ?

    # Bolean data
    st.sidebar.write('Additionnal features')
    hasGarden_1 = st.sidebar.checkbox('Garden', value=False)
    hasSwimmingPool_True = st.sidebar.checkbox('Swimming Pool', value=False)
    hasFireplace_True = st.sidebar.checkbox('Fireplace', value=False)
    hasTerrace_True = st.sidebar.checkbox('Terrace', value=False)

    # Code for prediction
    price_prediction = ''
    
    # Creating a button for prediction
    if st.button('Predict Price'):
        list_input_data = [type, subtype, bedroomCount, bathroomCount, locality,
        postCode, habitableSurface, buildingCondition,
        buildingConstructionYear, facedeCount, floodZoneType,
        heatingType, kitchenType, hasGarden_1, toiletCount,
        hasSwimmingPool_True, hasFireplace_True, hasTerrace_True,
        epcScore]

        predicted_price_value = immo_prediction(list_input_data)

    
        if isinstance(predicted_price_value, (int, float)):
                st.success(f"The estimated price of the property is : **{predicted_price_value:,.2f} €**")
        else:
            # L'erreur aura déjà été affichée dans immo_prediction ou lors du chargement du modèle
            st.error("La prédiction n'a pas pu être effectuée. Vérifiez les messages d'erreur ci-dessus.")

if __name__ == '__main__':
    main()


 
    



