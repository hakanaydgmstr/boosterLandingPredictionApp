import numpy as np
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from funcs.data_prep import *
from funcs.eda import *
import pickle

st.set_page_config(layout="wide", page_title="Roket Uçuralım", page_icon="icon/rocket.png")

st.title("Roket Uçuralım 🚀")
st.sidebar.markdown("## Roket Uçuralım 🚀")


def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.unsplash.com/photo-1517976487492-5750f3195933?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8cm9ja2V0fGVufDB8fDB8fA%3D%3D&w=1000&q=80");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )


#add_bg_from_url()

df = pd.read_csv("app_data.csv")

st.write("Bu sayfada XGBoost algoritması ile oluşturulmuş olan model kullanılarak, özellikleri girilen roketin ilk "
         "aşamasının kurtarılıp kurtarılamayacağının tahminini gerçekleştireceğiz. Aşağıdaki seçenekler ile roketinizi "
         "inşa etmeye başlayabilirsiniz. Daha sonrasında sidebar üzerinden uçuşa hazır kutucuğunu işaretleyerek roketi "
         "ateşleyebilirsiniz 🔥")

st.markdown("#")

col1, col2 = st.columns(2)
with col1:
    # Block
    block_str = st.radio(
        "Görevde kullanılacak olan Falcon 9 modelini seçiniz.",
        ["Block 1", "Block 2", "Block 3", "Block 4", "Block 5"]
    )

with col2:
    if block_str == "Block 1":
        st.image("rocket_photos/block_1_new.png", width=400)
        block = 1
    elif block_str == "Block 2":
        st.image("rocket_photos/block_2.png", width=400)
        block = 2
    elif block_str == "Block 3":
        st.image("rocket_photos/block_3.png", width=400)
        block = 3
    elif block_str == "Block 4":
        st.image("rocket_photos/block_4.png", width=400)
        block = 4
    else:
        st.image("rocket_photos/block_5.png", width=400)
        block = 5

col1, col2 = st.columns(2)

with col1:
    # GridFins
    grid_fins_bool = st.radio(
        '1. aşamada kanatçık olacak mı?',
        ["Evet", "Hayır"],
        horizontal=True
    )

    if grid_fins_bool == "Evet":
        grid_fins = 1
    else:
        grid_fins = 0

with col2:
    # Legs
    legs_bool = st.radio(
        '1. aşamada ayaklar olacak mı?',
        ["Evet", "Hayır"],
        horizontal=True
    )

    if legs_bool == "Evet":
        legs = 1
    else:
        legs = 0

st.markdown('#')

# PayloadMass
payload_mass = st.slider(
    'Yük ağırlığı ne kadar?',
    0, int(df["PayloadMass"].max()),
    step=100
)

col1, col2 = st.columns(2)

with col1:
    # Reused
    reused_bool = st.radio(
        'Roketin 1. aşaması daha önce kullanıldı mı?',
        ["Evet", "Hayır"],
        horizontal=True
    )

    if reused_bool == "Evet":
        reused = 1
    else:
        reused = 0

with col2:
    # ReusedCount
    reused_count = st.number_input('1. aşama daha önce kullanıldıysa kaç kere kullanıldı? (İlk uçuşsa 0 giriniz.)',
                                   min_value=0,
                                   step=1)

# Flights
st.write(f"Yukarıdaki bilgilere göre bu uçuş, 1. aşamanın {reused_count+1}. uçuşu olacak.")
flights = reused_count + 1

# Orbit
orbit = st.selectbox(
    'Gidilecek yörüngeyi seçin',
    df["Orbit"].unique()
)

# LaunchSite
site = st.selectbox(
    'Fırlatılışın yapılacağı üssü seçin',
    df["LaunchSite"].unique()
)

if site == "CCAFS SLC 40":
    st.markdown("### Cape Canaveral Space Launch Complex 40")
    map_dict = {"lat": [28.5618571],
                "lon": [-80.577366]}
    map_df = pd.DataFrame(map_dict)
    st.map(data=map_df)
elif site == "VAFB SLC 4E":
    st.markdown("### Vandenberg Space Launch Complex 4")
    map_dict = {"lat": [34.632093],
                "lon": [-120.610829]}
    map_df = pd.DataFrame(map_dict)
    st.map(data=map_df)
else:
    st.markdown("### Kennedy Space Center Launch Complex 39")
    map_dict = {"lat": [28.6080585],
                "lon": [-80.6039558]}
    map_df = pd.DataFrame(map_dict)
    st.map(data=map_df)

st.markdown('#')

# LandingPad
landing_pad_bool = st.radio(
    "İniş pad'i kullanılacak mı?",
    ["Evet", "Hayır"],
    horizontal=True
)

if landing_pad_bool == "Evet":
    landing_pad = 1
else:
    landing_pad = 0

user_dict = {"PayloadMass": payload_mass,
             "Orbit": orbit,
             "LaunchSite": site,
             "Flights": flights,
             "GridFins": grid_fins,
             "Reused": reused,
             "Legs": legs,
             "Block": block,
             "ReusedCount": reused_count,
             "UsedLandingPad": landing_pad}

user_df = pd.DataFrame(user_dict, index=[0])

st.write("Girmiş olduğunuz seçeneklere göre roketin özellikleri:")
st.write(user_df)

# main df
data_df = df.drop(["Date", "Serial", "Class"], axis=1)
data_encode = one_hot_encoder(data_df, ["Orbit", "LaunchSite"], drop_first=False)

# user df
X = user_df
cat_cols = ["Orbit", "LaunchSite"]
X_encode = one_hot_encoder(user_df, cat_cols, drop_first=False)

# now we have to add user selections into the encoded main df as a new row and filling NaN values as 0
# then we are going to select the last row for the model
new_df = pd.concat([data_encode, X_encode], axis=0, ignore_index=True)
final_df = new_df.iloc[-1:,:]
final_df = final_df.fillna(0)

# loading model
model = pickle.load(open("xgb_model_v3.pkl", "rb"))

st.sidebar.write("Roketin özelliklerini girdikten ve aşağıdaki 'Ready to Launch!' kutucuğunu işaretledikten sonra"
                 "'Launch!' butonuna tıklayarak roketi fırlatabilirsiniz :)")

if st.sidebar.checkbox('Ready to Launch!'):
    # making prediction
    if st.sidebar.button("Launch!"):
        y_pred = model.predict(final_df.values)
        if y_pred == 1:
            st.success("""
            ### Tebrikler, görev başarılı! İlk aşama kurtarıldı.
            """)
            st.markdown(
                "![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/lab_v2/images/landing\_1.gif)")
        else:
            st.error("""
            ### Görev başarısız! İlk aşama kurtarılamadı.
            """)
            st.markdown(
                "![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/lab_v2/images/crash.gif)")
    else:
        st.write("Waiting for a launch...")


