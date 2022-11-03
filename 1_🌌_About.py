import streamlit as st
import pandas as pd

st.set_page_config(page_title="Booster Landing Prediction App", page_icon="icon/rocket.png")

st.title('🚀 Booster Landing Prediction App')

st.sidebar.subheader("Hoşgeldiniz! 🎉")
st.sidebar.info("Uygulamada gezinmek için yukarıdaki alandan bir sayfa seçebilirsiniz 👆")
st.sidebar.success("Proje Hakkında Bilgi Sahibi Olmak İçin: https://lnkd.in/dXvjMSSg")
st.sidebar.markdown("### İletişim")
st.sidebar.info("E-Posta: hakan-aydogmus@hotmail.com | "
                "[LinkedIn](https://www.linkedin.com/in/hakanaydogmus/) | "
                "[GitHub](https://github.com/hakanaydgmstr/boosterLandingPredictionApp)")

st.write("IBM Data Science Professional Certificate programının bitirme projesine hoş geldiniz! 🎉")

st.write("Bu projede Falcon 9'un ilk aşamasının başarılı bir şekilde inip inmeyeceğini tahmin edeceğiz. "
         "Diğer roket firmaları 165 milyon dolardan fazla maliyet belirlemesine rağmen; SpaceX, web sitesinde 62 "
         "milyon dolarlık bir maliyetle Falcon 9 roket fırlatmalarının reklamını yapıyor. "
         "Tasarrufların çoğu SpaceX'in ilk aşamayı yeniden kullanabilmesiyle ortaya çıkmaktadır. "
         "Dolayısıyla ilk etabın inip inmeyeceğini belirleyebilirsek, bir fırlatmanın maliyetini de belirleyebiliriz. "
         "Alternatif bir şirket, bir uçuş için SpaceX'e karşı teklif vermek isterse bu bilgi kullanılabilir.")

img_url = "https://www.spaceflightinsider.com/wp-content/uploads/hangar/header/falcon-9.jpg"
st.image(img_url)

st.markdown('#')

col1, col2 = st.columns(2)

col1.image("profile_pic.jpeg", width=200)
col2.write("Merhabalar, ben Hakan. 2022 yılının Ocak ayından itibaren düzenli olarak veri bilimi ve makine öğrenmesi "
           "alanlarında çalışmalar yapıyorum. Kendimi geliştirmek için bu alanda çeşitli kurslara ve bootcamplere "
           "katıldım ve katılmaya devam ediyorum. Bu proje de dahil olmak üzere diğer çalışmalarıma GitHub hesabımdan "
           "ulaşabilirsiniz. İletişim bilgilerime ve projenin Coursera'daki sayfasına sidebar üzerinden "
           "ulaşabilirsiniz ✨")
