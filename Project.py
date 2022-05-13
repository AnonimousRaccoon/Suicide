import pandas as pd
import streamlit as st
import numpy as np
import plotly_express as px
import base64
import altair as alt
from io import StringIO, BytesIO


def read_file():
    data_url = "suicide.csv"
    return pd.read_csv(data_url)
####DOWNLOAD EXCEL AND PLOT FUNCTIONS
### Adapted FROM: (https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5)
def generate_excel_download_link(df):
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File of the first graph</a>'
    return st.markdown(href, unsafe_allow_html=True)
### END FROM
### Adapted FROM: (https://discuss.streamlit.io/t/download-plotly-plot-as-html/4426/2)
def generate_html_download_link(fig):
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot of the first graph</a>'
    return st.markdown(href, unsafe_allow_html=True)
### END FROM
####END DOWNLOAD

df = read_file()
st.set_page_config(page_title='Suicide country info data visualization')
st.title('Suicide country info data visualization')
st.write(df)

df_year_coun = df.groupby(by = ['country', 'year'], as_index=False)['suicides_no'].sum()
countries = list(df_year_coun['country'].unique())
"""
Here tablet with different countries and years
"""
st.write(df_year_coun)
print("hello world")


##FIRST GRAPH
groupby_column = st.selectbox(
    'Please, choose the category about which you will get analysis',
    ('sex', 'age', 'generation', 'country')
)

# GROUP DATAFRAME 1
output_columns = ['suicides_no', 'suicides/100k pop']
df_grouped = df.groupby(by=[groupby_column], as_index = False)[output_columns].sum()
df_sum_pop = df.groupby(by=[groupby_column], as_index = False)['population'].sum()

st.dataframe(df_grouped)
st.dataframe(df_sum_pop)
print(df.columns)
df_grouped['suicides/100k pop'] = df_grouped['suicides_no']/df_sum_pop['population']*100000

st.dataframe(df_grouped)
#PLOT DATAFRAME 1
fig = px.bar(
    df_grouped,
    x=groupby_column,
    y="suicides_no",
    color='suicides/100k pop',
    color_continuous_scale=['green','yellow','red'],
    template='presentation',
    title=f'<b> Suicides number by {groupby_column}</b>'
)
st.plotly_chart(fig)
"""
You can download these graphs and excel tablets on the bottom of the website.
"""
##END FIRST GRAPH
"""
GDP GRAPH
"""
##SECOND GDP GRAPH
df_gdp = df.groupby(by=['country'], as_index = False)['suicides/100k pop'].mean()
df_sum_gdp = df.groupby(by=['country'], as_index = False)['gdp_per_capita ($)'].mean()
df_gdp['gdp_per_capita ($)']=df_sum_gdp['gdp_per_capita ($)']
"""correl = df_gdp.drop(['country'], axis = 1).corr(method='pearson', min_periods=1)['gdp_per_capita ($)','suicides/100k pop']
print(correl)"""
st.dataframe(df_gdp)

#PLOT
c = alt.Chart(df_gdp, title='Scattered map of suicide rate and GDP').mark_circle().encode(
    x='gdp_per_capita ($)',
    y='suicides/100k pop',
    tooltip=['gdp_per_capita ($)', 'suicides/100k pop', 'country'],
    color="country"
).properties(title='quantitative')
line = (
    alt.Chart(
        df_gdp
    )
    .transform_loess('gdp_per_capita ($)', 'suicides/100k pop')
    .mark_line()
    .encode(x=alt.X('gdp_per_capita ($)'), y=alt.Y('suicides/100k pop'))
)
st.altair_chart(c+line, use_container_width=True)
##END SECOND GRAPH



##THIRD GRAPH
#CHOSE OF COUNTRY FOR 3 GRAPH
groupby_column1 = st.selectbox('Select country for analysis',
    countries, index = 75
)
df_year_coun_ch=df_year_coun[df_year_coun['country']==groupby_column1]
st.write(df_year_coun_ch)
"""
THIRD GRAPH
"""
#PLOT
fig_product_sales = px.bar(
    df_year_coun_ch,
    x="year",
    y="suicides_no",
    orientation="v",
    title=f'<b>Suicides in {groupby_column1} </b>',
    color='year',
    template="plotly_white",
    facet_row_spacing=0.06,
    width = 800
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=True))
)
st.plotly_chart(fig_product_sales)
## STOP
"""
FOURTH GRAPH
"""
##TOP 15 COUNTRIES FOURTH GRAPH
df_sum = df.groupby(by=["country"], as_index = False)["suicides_no"].sum()
df_sum = df_sum.sort_values(by='suicides_no', ascending=False)[:15]
st.write(df_sum)
#PLOT
chart = (
    alt.Chart(
        df_sum,
        title="Static site generators popularity",
    )
    .mark_bar()
    .encode(
        x=alt.X("suicides_no", title="Suicides in 15 top countries"),
        y=alt.Y(
            "country",
            sort=alt.EncodingSortField(field="suicides_no", order="descending"),
            title="",
        ),
        color='country',
        tooltip=["country", "suicides_no"],
    )
)
st.altair_chart(chart, use_container_width=True)
##STOP

print("END")
#BOTTOM

st.subheader('Downloads:')
generate_excel_download_link(df_grouped)
generate_html_download_link(fig)













