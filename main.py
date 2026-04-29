import streamlit as st
import numpy as np
import keras

# =========================
# Disease Remedy Dictionary
# =========================
disease_info = {

# ================= APPLE =================
'Apple___Apple_scab': {
    "Symptoms": "Olive-green spots on leaves and fruits.",
    "Chemical Control": "Spray Captan or Myclobutanil.",
    "Organic Control": "Use sulfur-based fungicides.",
    "Fertilizer": "Balanced NPK with compost.",
    "Prevention": "Remove fallen leaves, ensure airflow."
},

'Apple___Black_rot': {
    "Symptoms": "Brown lesions on leaves, black rotten fruits.",
    "Chemical Control": "Use Mancozeb or Thiophanate-methyl.",
    "Organic Control": "Copper fungicide sprays.",
    "Fertilizer": "Add potassium-rich fertilizer.",
    "Prevention": "Prune infected parts."
},

'Apple___Cedar_apple_rust': {
    "Symptoms": "Yellow-orange spots on leaves.",
    "Chemical Control": "Use Myclobutanil fungicide.",
    "Organic Control": "Neem oil spray.",
    "Fertilizer": "Balanced NPK.",
    "Prevention": "Remove nearby cedar trees."
},

'Apple___healthy': {
    "Symptoms": "No disease.",
    "Chemical Control": "Not required.",
    "Organic Control": "Maintain soil health.",
    "Fertilizer": "Compost + NPK (10-10-10).",
    "Prevention": "Regular monitoring."
},

# ================= BLUEBERRY =================
'Blueberry___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "Not required.",
    "Organic Control": "Maintain acidic soil (pH 4.5–5.5).",
    "Fertilizer": "Ammonium sulfate fertilizer.",
    "Prevention": "Proper irrigation."
},

# ================= CHERRY =================
'Cherry_(including_sour)___Powdery_mildew': {
    "Symptoms": "White powder on leaves.",
    "Chemical Control": "Use Sulfur or Potassium bicarbonate.",
    "Organic Control": "Neem oil spray.",
    "Fertilizer": "Balanced NPK.",
    "Prevention": "Improve airflow."
},

'Cherry_(including_sour)___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "Not required.",
    "Organic Control": "Proper pruning.",
    "Fertilizer": "Compost.",
    "Prevention": "Maintain spacing."
},

# ================= CORN =================
'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': {
    "Symptoms": "Gray rectangular lesions.",
    "Chemical Control": "Use Azoxystrobin or Mancozeb.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Nitrogen balanced.",
    "Prevention": "Crop rotation."
},

'Corn_(maize)___Common_rust_': {
    "Symptoms": "Reddish pustules.",
    "Chemical Control": "Propiconazole fungicide.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Avoid excess nitrogen.",
    "Prevention": "Resistant hybrids."
},

'Corn_(maize)___Northern_Leaf_Blight': {
    "Symptoms": "Long gray-green lesions.",
    "Chemical Control": "Mancozeb or Azoxystrobin.",
    "Organic Control": "Crop rotation.",
    "Fertilizer": "Balanced nutrients.",
    "Prevention": "Use resistant seeds."
},

'Corn_(maize)___healthy': {
    "Symptoms": "Healthy crop.",
    "Chemical Control": "None.",
    "Organic Control": "Maintain soil health.",
    "Fertilizer": "NPK fertilizer.",
    "Prevention": "Proper irrigation."
},

# ================= GRAPE =================
'Grape___Black_rot': {
    "Symptoms": "Black spots on leaves and fruits.",
    "Chemical Control": "Mancozeb or Myclobutanil.",
    "Organic Control": "Copper fungicide.",
    "Fertilizer": "Balanced nutrients.",
    "Prevention": "Remove infected fruits."
},

'Grape___Esca_(Black_Measles)': {
    "Symptoms": "Leaf discoloration and fruit spotting.",
    "Chemical Control": "No effective cure.",
    "Organic Control": "Remove infected vines.",
    "Fertilizer": "Balanced fertilizer.",
    "Prevention": "Avoid pruning wounds."
},

'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': {
    "Symptoms": "Brown spots on leaves.",
    "Chemical Control": "Mancozeb spray.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Balanced nutrients.",
    "Prevention": "Prune properly."
},

'Grape___healthy': {
    "Symptoms": "Healthy vine.",
    "Chemical Control": "None.",
    "Organic Control": "Maintain vineyard hygiene.",
    "Fertilizer": "NPK fertilizer.",
    "Prevention": "Proper pruning."
},

# ================= ORANGE =================
'Orange___Haunglongbing_(Citrus_greening)': {
    "Symptoms": "Yellow shoots, misshapen fruits.",
    "Chemical Control": "Control psyllids using Imidacloprid.",
    "Organic Control": "Neem oil for vector control.",
    "Fertilizer": "Micronutrients (Zn, Fe).",
    "Prevention": "Remove infected trees."
},

# ================= PEACH =================
'Peach___Bacterial_spot': {
    "Symptoms": "Dark lesions on leaves.",
    "Chemical Control": "Copper bactericides.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Potassium-rich fertilizer.",
    "Prevention": "Use resistant varieties."
},

'Peach___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "None.",
    "Organic Control": "Maintain orchard hygiene.",
    "Fertilizer": "Balanced NPK.",
    "Prevention": "Proper irrigation."
},

# ================= PEPPER =================
'Pepper,_bell___Bacterial_spot': {
    "Symptoms": "Small dark spots.",
    "Chemical Control": "Copper sprays.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Potassium-rich.",
    "Prevention": "Avoid overhead watering."
},

'Pepper,_bell___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "None.",
    "Organic Control": "Good soil care.",
    "Fertilizer": "NPK.",
    "Prevention": "Proper spacing."
},

# ================= POTATO =================
'Potato___Early_blight': {
    "Symptoms": "Dark concentric spots.",
    "Chemical Control": "Mancozeb.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Add phosphorus & potassium.",
    "Prevention": "Crop rotation."
},

'Potato___Late_blight': {
    "Symptoms": "Water-soaked lesions.",
    "Chemical Control": "Metalaxyl + Mancozeb.",
    "Organic Control": "Copper fungicide.",
    "Fertilizer": "Balanced nutrients.",
    "Prevention": "Destroy infected plants."
},

'Potato___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "None.",
    "Organic Control": "Soil health maintenance.",
    "Fertilizer": "NPK.",
    "Prevention": "Regular monitoring."
},

# ================= OTHER =================
'Raspberry___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "None.",
    "Organic Control": "Maintain pruning.",
    "Fertilizer": "Compost.",
    "Prevention": "Proper care."
},

'Soybean___healthy': {
    "Symptoms": "Healthy crop.",
    "Chemical Control": "None.",
    "Organic Control": "Soil fertility.",
    "Fertilizer": "Nitrogen fixation support.",
    "Prevention": "Crop rotation."
},

'Squash___Powdery_mildew': {
    "Symptoms": "White powdery coating.",
    "Chemical Control": "Sulfur fungicide.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Balanced nutrients.",
    "Prevention": "Air circulation."
},

'Strawberry___Leaf_scorch': {
    "Symptoms": "Red/purple leaf edges.",
    "Chemical Control": "Fungicide sprays.",
    "Organic Control": "Remove infected leaves.",
    "Fertilizer": "Balanced NPK.",
    "Prevention": "Avoid overcrowding."
},

'Strawberry___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "None.",
    "Organic Control": "Good irrigation.",
    "Fertilizer": "Compost.",
    "Prevention": "Regular care."
},

# ================= TOMATO =================
'Tomato___Bacterial_spot': {
    "Symptoms": "Dark leaf spots.",
    "Chemical Control": "Copper bactericide.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Potassium-rich.",
    "Prevention": "Avoid wet leaves."
},

'Tomato___Early_blight': {
    "Symptoms": "Brown rings on leaves.",
    "Chemical Control": "Mancozeb.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Add potassium.",
    "Prevention": "Crop rotation."
},

'Tomato___Late_blight': {
    "Symptoms": "Dark lesions.",
    "Chemical Control": "Metalaxyl.",
    "Organic Control": "Copper spray.",
    "Fertilizer": "Balanced nutrients.",
    "Prevention": "Remove infected plants."
},

'Tomato___Leaf_Mold': {
    "Symptoms": "Yellow spots, mold underside.",
    "Chemical Control": "Chlorothalonil.",
    "Organic Control": "Improve airflow.",
    "Fertilizer": "Balanced.",
    "Prevention": "Reduce humidity."
},

'Tomato___Septoria_leaf_spot': {
    "Symptoms": "Small circular spots.",
    "Chemical Control": "Mancozeb.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Balanced.",
    "Prevention": "Remove infected leaves."
},

'Tomato___Spider_mites Two-spotted_spider_mite': {
    "Symptoms": "Yellow specks, webbing.",
    "Chemical Control": "Abamectin.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Balanced.",
    "Prevention": "Maintain humidity."
},

'Tomato___Target_Spot': {
    "Symptoms": "Circular spots with rings.",
    "Chemical Control": "Chlorothalonil.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Balanced.",
    "Prevention": "Remove debris."
},

'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
    "Symptoms": "Yellow curled leaves.",
    "Chemical Control": "Control whiteflies (Imidacloprid).",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Micronutrients.",
    "Prevention": "Remove infected plants."
},

'Tomato___Tomato_mosaic_virus': {
    "Symptoms": "Mosaic leaf pattern.",
    "Chemical Control": "No cure.",
    "Organic Control": "Remove infected plants.",
    "Fertilizer": "Balanced.",
    "Prevention": "Sanitize tools."
},

'Tomato___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "None.",
    "Organic Control": "Maintain soil health.",
    "Fertilizer": "NPK (10-10-10).",
    "Prevention": "Regular monitoring."
}
}

# =========================
# Model Prediction Function
# =========================
def model_prediction(test_image):
    model = keras.models.load_model("fixed_plant_disease_model.keras")

    image = keras.preprocessing.image.load_img(test_image, target_size=(128,128))
    input_arr = keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])

    predictions = model.predict(input_arr)

    result_index = np.argmax(predictions)
    confidence = np.max(predictions) * 100

    return result_index, confidence


# =========================
# Sidebar
# =========================
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About", "Disease Recognition"])


# =========================
# Home Page
# =========================
if app_mode == "Home":
    st.header("PLANT DISEASE RECOGNITION SYSTEM")
    st.image("home_page.jpeg", use_container_width=True)

    st.markdown("""
    Welcome to the Plant Disease Recognition System!

    Upload a plant leaf image and get:
    - Disease detection
    - Confidence score
    - Preventive measures

    Go to **Disease Recognition** to begin.
    """)


# =========================
# About Page
# =========================
elif app_mode == "About":
    st.header("About")

    st.markdown("""
    Dataset contains ~87K images across 38 classes.

    Split:
    - Train: 70K+
    - Validation: 17K+
    - Test: 33 images

    Built using CNN for plant disease classification.
    """)


# =========================
# Disease Recognition Page
# =========================
elif app_mode == "Disease Recognition":
    st.header("Disease Recognition")

    test_image = st.file_uploader("Upload a plant leaf image")

    if test_image is not None:
        if st.button("Show Image"):
            st.image(test_image, use_container_width=True)

        if st.button("Predict"):
            st.snow()

            # Class labels
            class_name = [
                'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew',
                'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight',
                'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)',
                'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
                'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
                'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
                'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
                'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
                'Strawberry___Leaf_scorch', 'Strawberry___healthy',
                'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
                'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
                'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
                'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                'Tomato___healthy'
            ]

            # Prediction
            result_index, confidence = model_prediction(test_image)
            predicted_disease = class_name[result_index]

            # Clean display
            plant, disease = predicted_disease.split("___")

            st.success(f"Plant: {plant}")
            st.warning(f"Disease: {disease}")
            st.info(f"Confidence: {confidence:.2f}%")

            st.subheader("Preventive Measures / Cure")
            # Remedy
            remedy = disease_info.get(predicted_disease)

            if remedy:
                for key, value in remedy.items():
                    st.write(f"**{key}:** {value}")