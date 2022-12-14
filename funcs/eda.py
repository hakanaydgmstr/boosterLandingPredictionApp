import numpy as np
import pandas as pd

#from statsmodels.stats.proportion import proportions_ztest

#pd.set_option("display.max_columns", None)
#pd.set_option("display.max_rows", None)
#pd.set_option("display.float_format", lambda x: '%.3f' % x)
#pd.set_option("display.width", 500)


def outlier_thresholds(dataframe, num_col, q1=0.25, q3=0.75):
    quartile1 = dataframe[num_col].quantile(q1)
    quartile3 = dataframe[num_col].quantile(q3)
    iqr = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * iqr
    low_limit = quartile1 - 1.5 * iqr

    # outliers = [dataframe[(dataframe[num_col] < low) | (dataframe[num_col] > up)]]
    return low_limit, up_limit


def check_outlier(dataframe, num_col, q1=0.25, q3=0.75):
    low_limit, up_limit = outlier_thresholds(dataframe, num_col, q1, q3)

    if dataframe[(dataframe[num_col] < low_limit) | (dataframe[num_col] > up_limit)].any(axis=None):
        return True
    else:
        return False


def reach_outliers(dataframe, num_col, q1, q3, index=False):
    low_limit, up_limit = outlier_thresholds(dataframe, num_col, q1, q3)

    if len(dataframe[(dataframe[num_col] < low_limit) | (dataframe[num_col] > up_limit)]) > 10:
        print(dataframe[(dataframe[num_col] < low_limit) | (dataframe[num_col] > up_limit)].head())
    else:
        print(dataframe[(dataframe[num_col] < low_limit) | (dataframe[num_col] > up_limit)])

    if index:
        return dataframe[(dataframe[num_col] < low_limit) | (dataframe[num_col] > up_limit)].index


def remove_outliers(dataframe, num_col):
    low_limit, up_limit = outlier_thresholds(dataframe, num_col)
    df_without_outliers = dataframe[~((dataframe[num_col] < low_limit) | (dataframe[num_col] > up_limit))]

    return df_without_outliers


def replace_with_thresholds(dataframe, num_col, q1=0.25, q3=0.75):
    low_limit, up_limit = outlier_thresholds(dataframe, num_col, q1, q3)

    dataframe.loc[(dataframe[num_col] < low_limit), num_col] = low_limit
    dataframe.loc[(dataframe[num_col] > up_limit), num_col] = up_limit


def missing_values_table(dataframe, na_name=False):
    # eksik veri bulunduran de??i??kenlerin se??ilmesi
    na_columns = [col for col in dataframe.columns if dataframe[col].isnull().sum() > 0]

    # de??i??kenlerdeki eksik de??er miktar??
    n_miss = dataframe[na_columns].isnull().sum().sort_values(ascending=False)
    # de??i??kenlerdeki eksik de??er oran??
    ratio = (dataframe[na_columns].isnull().sum() / len(dataframe) * 100).sort_values(ascending=False)

    # yukardaki hesaplad??????m??z miktar ve oran bilgilerini i??eren bir df olu??turulmas??
    missing_df = pd.concat([n_miss, np.round(ratio, 2)], axis=1, keys=['n_miss', 'ratio'])

    print(missing_df, end='\n')

    if na_name:
        return na_columns


def missing_vs_target(dataframe, target, na_columns):
    temp_df = dataframe.copy()  # dataframe'in kopyas??n?? olu??turduk. Bunun ??zerinden i??lem yapaca????z.

    for col in na_columns:  # daha ??nceden belirledi??imiz na i??eren de??i??kenlerin bulundu??u listede gez
        # bu de??i??kenler i??erisinde na ifade bulunan sat??ra 1 di??erlerine 0 yaz, bu de??i??kenleri de ismine na_flag ifadesini ekleyerek al
        temp_df[col + '_NA_FLAG'] = np.where(temp_df[col].isnull(), 1, 0)

    # temp_df i??erisinde '_NA_' stringini i??eren de??i??kenleri al, na_flags'e ata.
    na_flags = temp_df.loc[:, temp_df.columns.str.contains('_NA_')].columns

    for col in na_flags:  # na_flags i??erisinde gez
        print(pd.DataFrame({"TARGET_MEAN": temp_df.groupby(col)[target].mean(),
                            "Count": temp_df.groupby(col)[target].count()}), end="\n\n\n")
        # na i??eren de??i??kenlerin k??r??l??m??nda ba????ml?? de??i??kenin (target'in) ortalamas??n?? ve toplam??n?? i??eren bir df olu??tur


def label_encoder(dataframe, binary_col):
    labelencoder = LabelEncoder()
    dataframe[binary_col] = labelencoder.fit_transform(dataframe[binary_col])
    return dataframe


def one_hot_encoder(dataframe, categorical_cols, drop_first=True):
    # fonksiyona girilen dataframe i??erisinden kategorik de??i??kenleri one hot encoding i??lemine sokuyoruz
    # sonras??nda ana dataframe'e bunu kaydederek fonksiyon sonunda bu df'i d??nd??r??yoruz.
    dataframe = pd.get_dummies(dataframe, columns=categorical_cols, drop_first=drop_first)
    return dataframe


def rare_analyser(dataframe, target, cat_cols):
    import pandas as pd
    
    for col in cat_cols:
        print(col, ":", len(dataframe[col].value_counts()))  # de??i??kenin i??erisinde ka?? tane s??n??f var?

        # de??i??kendeki s??n??flar??n toplamlar??, oranlar?? ve target de??i??kenine g??re oranlar??n?? veren dataframe
        print(pd.DataFrame({"COUNT": dataframe[col].value_counts(),
                            "RATIO": dataframe[col].value_counts() / len(dataframe),
                            "TARGET_MEAN": dataframe.groupby(col)[target].mean()}), end="\n\n\n")


def rare_encoder(dataframe, rare_perc):
    # dataframe'in kopyas??n?? ald??k
    temp_df = dataframe.copy()

    # e??er de??i??ken kategorikse ve i??erisindeki s??n??flardan herhangi birisinin oran?? rare_perc'de verilen orandan az ise
    # bu de??i??keni rare_columns'a ata
    rare_columns = [col for col in temp_df.columns if temp_df[col].dtypes == 'O' and
                    (temp_df[col].value_counts() / len(temp_df) < rare_perc).any(axis=None)]

    for var in rare_columns:  # se??ilen rare de??i??kenler i??erisinde gez
        tmp = temp_df[var].value_counts() / len(temp_df)  # temp_df de var de??i??keninin oran??n?? al
        rare_labels = tmp[tmp < rare_perc].index  # e??er al??nan oran rare_perc'den k??????kse bunun label'??n?? al
        temp_df[var] = np.where(temp_df[var].isin(rare_labels), "Rare", temp_df[var])  # bu label yerine 'Rare' yazd??r

    return temp_df


