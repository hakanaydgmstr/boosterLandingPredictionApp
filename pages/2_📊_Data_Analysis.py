import streamlit as st
import pandas as pd
from funcs.data_prep import *
from funcs.eda import *
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

pd.set_option("display.max_column", None)
pd.set_option("display.width", 500)


st.set_page_config(layout="wide", page_title="Veri Analizi", page_icon="icon/rocket.png")

st.title("Veri Analizi 📊")

st.write("Bu sayfada, model için kullanılan veri setini ve veri setindeki değişkenler içi yapılan analizleri "
         "inceleyebilirsiniz. Ek olarak aşağıda bazı önemli değişkenler için çeşitli grafikler de bulunmaktadır.")

df = pd.read_csv("app_data.csv")
df["Block"] = df["Block"].astype("int64")
cat_cols, num_cols, cat_but_car = grab_col_names(df)

st.subheader("Veri Seti Bilgileri")
col1, col2 = st.columns(2)
col1.metric(label="Gözlem Sayısı", value=df.shape[0])
col1.metric(label="Kategorik Değişken Sayısı", value=len(cat_cols))
col2.metric(label="Değişken Sayısı", value=df.shape[1])
col2.metric(label="Nümerik Değişken Sayısı", value=len(num_cols))

if st.checkbox('Veri Setini Göster'):
    st.write(df)

st.subheader("Değişken Analizi")

col1, col2 = st.columns(2)

with col1:
    st.write("Kategorik Değişkenler")
    cat_feature = st.selectbox(
                "Bir kategorik değişken seçin:",
                cat_cols
            )

    @st.cache
    def get_cat_graphs(cat_feature):
        cat_fig = px.histogram(df,
                               x=cat_feature,
                               color=cat_feature,
                               width=450, height=450,
                               pattern_shape="Class",
                               color_discrete_sequence=px.colors.sequential.RdBu)
        return cat_fig

    cat_fig = get_cat_graphs(cat_feature)
    st.plotly_chart(cat_fig)

with col2:
    st.write("Nümerik Değişkenler")
    cat_feature = st.selectbox(
        "Bir nümerik değişken seçin:",
        ["PayloadMass"]
    )
    num_fig = px.histogram(df,
                           x=cat_feature,
                           color="Class",
                           color_discrete_sequence={1: "royalblue",
                                                    0: "lightblue"},
                           width=450, height=450)
    st.plotly_chart(num_fig)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs(["Orbit",
                                                                              "LaunchSite",
                                                                              "Flights",
                                                                              "GridFins",
                                                                              "Reused",
                                                                              "Legs",
                                                                              "Block",
                                                                              "ReusedCount",
                                                                              "Class",
                                                                              "UsedLandingPad",
                                                                              "PayloadMass"])

tab1.markdown("*Orbit* değişkeni, uçuşların hangi yörüngeye yapıldığını belirtir. Yapılan uçuşların en çok GTO "
              "yörüngesine yapıldığını görüyoruz. Bu yörüngeye yapılan uçuşların hemen hemen yarısı başarılı bir "
              "şekilde iniş yapmış. VLEO'ya yapılan uçuşlar ise en yüksek başarı oranına sahip.")
tab2.markdown("*LaunchSite* değişkeni, uçuşların hangi üslerden yapıldığının bilgisini tutuyor. Grafiğe göre en "
              "fazla uçuş yapılan üs CCAFS SLC 40 üssü. Bu üsten yapılan uçuşların yarısından fazlası başarılı bir "
              "şekilde iniş yapmıştır.")
tab3.markdown("*Flights*, kullanılacak olan roketin kaçıncı uçuşu olduğunu ifade eder. Grafiğe göre en çok uçuş "
              "yapan roketler ilk defa kullanılan roketlerdir.")
tab4.markdown("*GridFins*, 1. Aşamada kanatçık kullanılıp kullanılmadığını belirtir. Grafik incelendiği zaman "
              "çoğu uçuşta kanatçık kullanılmış ve yine en çok başarı kanatçıklar kullanıldığı zaman elde edilmiştir.")
tab5.markdown("*Reused*, roketin ilk defa mı yoksa tekrar mı kullanıldığını belirtir. Grafiğe göre ilk kez uçuş "
              "yapan roketlerin sayısı daha fazla. Bunun yanında tekrar uçuş yapan roketlerin başarı oranı daha "
              "fazladır.")
tab6.markdown("*Legs*, 1. Aşamada ayakların kullanılıp kullanılmadığını belirtir. Grafikten görüleceği üzere "
              "yapılan uçuşların neredeyse 4te 3ünde ayaklar kullanılmış ve en fazla başarı ayaklar olduğunda elde "
              "edilmiştir.")
tab7.markdown("*Block*, roketin versiyonunu temsil eder. Veri setinde 5 tane versiyon bulunmakta. Grafik "
              "incelendiğinde yapılan uçuşların çoğu Block 5 ile yapılmış ve yine en fazla başarı bu versiyon ile "
              "elde edilmiştir.")
tab8.markdown("*ReusedCount*, roket tekrar kullanılmışsa daha önce kaç kere kullanıldığının bilgisini tutar. Burada "
              "ilk kez uçan roketler 0 olarak girilmiştir.")
tab9.markdown("*Class*, veri setimizdeki bağımlı değişkenimizdir. Roketin başarılı bir şekilde iniş yapıp "
              "yapmadığının bilgisini tutar.")
tab10.markdown("*UsedLandingPad*, görevde iniş pad’inin kullanılıp kullanılmadığını belirtir. Grafiğe göre iniş "
               "pad’inin olduğu uçuşlarda başarı oranı çok yüksektir.")
tab11.markdown("*PayloadMass*, veri setindeki tek nümerik değişkendir. Roketteki yükün ağırlığını belirtir. Grafiğe "
               "göre uçuşların çoğunda roketler 2000-4000 kg arasında yük bulundurmaktadır. Ayrıca 10000-12000 kg "
               "arasında hiç yük yoktur.")

st.markdown('#')

st.markdown("### Fırlatış Sahasına Göre Başarı Oranları")

col1, col2 = st.columns([2, 1])

with col1:

    pie_option = st.radio(
        "Üs Seçiniz",
        ["Hepsi", "CCAFS SLC 40", "KSC LC 39A", "VAFB SLC 4E"],
        horizontal=True
    )

    @st.cache
    def get_pie_chart(pie_option):
        if pie_option == "Hepsi":
            fig = px.pie(df,
                         values="Class",
                         names="LaunchSite",
                         color="LaunchSite",
                         color_discrete_map={'CCAFS SLC 40': 'darkblue',
                                             'VAFB SLC 4E': 'lightblue',
                                             'KSC LC 39A': 'royalblue'},
                         width=500, height=500
                         )
            fig.update_traces(
                title_font=dict(size=25, family='Verdana',
                                color='darkred'),
                textposition='inside', textinfo='percent+label',
                hoverinfo='label+percent',
                #textinfo='percent',
                textfont_size=10)
        else:
            filtered_df = df[df["LaunchSite"] == pie_option]
            if pie_option=="CCAFS SLC 40":
                title = "Cape Canaveral Space Launch Complex 40"
            elif pie_option=="VAFB SLC 4E":
                title = "Vandenberg Air Force Base Space Launch Complex 4E"
            else:
                title = "Kennedy Space Center Launch Complex 39A"
            fig = px.pie(filtered_df,
                         values="PayloadMass",
                         names="Class",
                         color="Class",
                         color_discrete_map={0: 'royalblue',
                                             1: 'darkblue'},
                         title=title,
                         width=500, height=500
                         )
            fig.update_traces(
                title_font=dict(size=25, family='Verdana',
                                color='darkred'),
                hoverinfo='label+percent',
                textinfo='percent', textfont_size=20)
        return fig

    fig2 = get_pie_chart(pie_option)
    st.plotly_chart(fig2)

with col2:
    st.markdown("#")
    st.markdown("#")
    st.markdown("#")
    st.markdown("#")
    st.markdown("#")
    st.markdown("#")

    if pie_option == "Hepsi":
        st.metric("Toplam Uçuş Sayısı", len(df))
        st.metric("Toplam Başarılı İniş Sayısı", len(df[df["Class"] == 1]))
    else:
        filtered_df = df[df["LaunchSite"] == pie_option]
        st.metric(f"{pie_option} Üssünden Yapılan Uçuş Sayısı", len(filtered_df))
        st.metric(f"{pie_option} Üssüne Başarılı İniş Sayısı", len(filtered_df[filtered_df["Class"] == 1]))

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    st.markdown("### Falcon 9 Versiyonlarının Başarı Oranları")


    @st.cache
    def get_donut_chart():
        fig = px.pie(df,
                     values="Class",
                     names="Block",
                     color="Block",
                     hole=0.5,
                     width=500, height=500,
                     color_discrete_sequence=px.colors.sequential.RdBu,
                     title="Toplam Başarılı İnişlerin Versiyonlara Göre Oranları"
                     )
        fig.update_traces(
            title_font=dict(size=25, family='Verdana',
                            color='darkred'),
            hoverinfo='label+percent',
            textinfo='percent', textfont_size=20)

        return fig


    donut_fig = get_donut_chart()
    st.plotly_chart(donut_fig)

with col2:
    st.markdown('#')
    st.markdown('#')
    st.markdown('#')

    st.metric("Block 1'in Uçuşu ve İnişi", len(df[df["Block"] == 1]),
              delta=len(df[(df["Block"] == 1) & (df["Class"] == 1)]))
    st.metric("Block 2'nin Uçuşu ve İnişi", len(df[df["Block"] == 2]),
              delta=len(df[(df["Block"] == 2) & (df["Class"] == 1)]))
    st.metric("Block 3'ün Uçuşu ve İnişi", len(df[df["Block"] == 3]),
              delta=len(df[(df["Block"] == 3) & (df["Class"] == 1)]))
    st.metric("Block 4'ün Uçuşu ve İnişi", len(df[df["Block"] == 4]),
              delta=len(df[(df["Block"] == 4) & (df["Class"] == 1)]))
    st.metric("Block 5'in Uçuşu ve İnişi", len(df[df["Block"] == 5]),
              delta=len(df[(df["Block"] == 5) & (df["Class"] == 1)]))

with col3:
    st.markdown('#')
    st.markdown('#')
    st.markdown('#')

    block_1 = (len(df[(df["Block"] == 1) & (df["Class"] == 1)]) / len(df[df["Block"] == 1])) * 100
    block_2 = (len(df[(df["Block"] == 2) & (df["Class"] == 1)]) / len(df[df["Block"] == 2])) * 100
    block_3 = (len(df[(df["Block"] == 3) & (df["Class"] == 1)]) / len(df[df["Block"] == 3])) * 100
    block_4 = (len(df[(df["Block"] == 4) & (df["Class"] == 1)]) / len(df[df["Block"] == 4])) * 100
    block_5 = (len(df[(df["Block"] == 5) & (df["Class"] == 1)]) / len(df[df["Block"] == 5])) * 100

    st.metric("Block 1'in Başarı Oranı (%)", "{:.2f}".format(block_1))
    st.metric("Block 2'nin Başarı Oranı (%)", "{:.2f}".format(block_2))
    st.metric("Block 3'ün Başarı Oranı (%)", "{:.2f}".format(block_3))
    st.metric("Block 4'ün Başarı Oranı (%)", "{:.2f}".format(block_4))
    st.metric("Block 5'in Başarı Oranı (%)", "{:.2f}".format(block_5))

st.markdown('#')
st.subheader("İtici Versiyonlarının Yük Ağırlık Miktarına Göre Sonuçları")

slide_option = st.slider(
    'Yük aralığını giriniz',
    0, int(df["PayloadMass"].max()), (0, int(df["PayloadMass"].max())), step=1000
)

def get_scatter_chart(slide_option):
    filtered_df = df.copy()
    payload_range = filtered_df[(filtered_df["PayloadMass"] >= slide_option[0]) & (
                filtered_df["PayloadMass"] <= slide_option[1])]
    fig = px.scatter(payload_range,
                     x="PayloadMass",
                     y="Class",
                     color="Block",
                     title="Yük Miktarı ve Başarı Korelasyonu")
    return fig

st.plotly_chart(get_scatter_chart(slide_option))

st.write("Yukarıdaki grafik incelendiğinde en çok başarılı uçuşun Block 5 ile yapıldığı, en çok başarısız olanların "
         "da Block 1 ile yapıldığı gözlemlenmektedir. 10.000 kg ve üstü yüklerde sadece Block 5 ile başarı sağlanmış, "
         "15.000 kg üzerinde yapılan 4 uçuştan 2’si başarılı bir şekilde iniş yapmıştır. 5.000-10.000 kg arasındaki "
         "yüklerde de yine aynı şekilde en iyi sonuç Block 5 ile alınmıştır.")

st.markdown('#')

st.subheader("Yıllara Göre Ortalama Başarı Grafiği")

line_chart_df = df.groupby(pd.DatetimeIndex(df["Date"]).year).agg({"Class": "mean"}).reset_index()
year_fig = px.line(line_chart_df, x="Date", y="Class")
st.plotly_chart(year_fig)

year_info_df = df.groupby(pd.DatetimeIndex(df["Date"]).year).agg({"Class": "count"})
year_info_df.columns = ["Toplam Yapılan Uçuşlar"]
st.table(year_info_df.T)