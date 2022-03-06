from turtle import width
import plotly.express as px
import pandas as pd

def get_map_graph(selection_map):

    selection_map = selection_map.rename({selection_map.index[0]: str(selection_map['DPA_DESCAN'].values[0])}, axis='index')

    fig = px.choropleth(geojson=selection_map.geometry, locations=selection_map.index, 
                        color_discrete_sequence=px.colors.qualitative.Pastel2)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    return fig

def get_pie_chart(df_selected):
    data_pie = pd.pivot_table(df_selected, index=['cobertura'],values=['km2_1'],aggfunc='sum')
    data_pie = data_pie['km2_1'].sort_values(ascending=False)

    suma = data_pie.iloc[9:].sum()
    out = data_pie.iloc[:9]
    row = pd.Series({'OTROS':suma})
    out = out.append(row)

    fig = px.pie(out, values= out.values, names=out.index, color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_traces(textposition='inside', textinfo='percent')
    fig.update_layout(
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
    )
    return fig

def get_line_chart(vab_selected):
    fig = px.line(vab_selected, x=vab_selected['Anio'], y=vab_selected['Valor'], 
                markers=True, labels=None,color_discrete_sequence=px.colors.qualitative.Dark2,
                text=vab_selected['Valor'])
    fig.update_traces(textposition="top right")
    fig.update_xaxes(showgrid=True, gridwidth=0.05, gridcolor='rgba(230, 230, 230, 0.8)')
    fig.update_yaxes(showgrid=True, gridwidth=0.01, gridcolor='rgba(230, 230, 230, 0.8)')
    fig.update_layout(yaxis_title=None, xaxis_title=None,paper_bgcolor= 'rgba(0, 0, 0, 0)',
                      plot_bgcolor= 'rgba(0, 0, 0, 0)', margin=dict(l=10, r=10, t=10, b=0),autosize=True,height=300)

    return fig

def get_bar_chart(df_vab_2020):
    fig = px.bar(df_vab_2020, x=df_vab_2020.index, y='Valor',color=df_vab_2020.index,
                color_discrete_sequence=px.colors.qualitative.Dark2)
    fig.update_xaxes(showgrid=True, gridwidth=0.05, gridcolor='rgba(230, 230, 230, 0.8)')
    fig.update_yaxes(showgrid=True, gridwidth=0.01, gridcolor='rgba(230, 230, 230, 0.8)')
    fig.update_layout(yaxis_title=None, xaxis_title=None,paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    plot_bgcolor= 'rgba(0, 0, 0, 0)', 
                    margin=dict(l=10, r=10, t=10, b=0),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ),
                    autosize=True,height=300)

    fig.update_xaxes(visible=False)
    return fig

########    TABLES   #########
def get_stats_people(selection):
    base_stats = []
    rows_name = ["% Hombres","% Mujeres","% Población Rural","% Población Urbana","% Población Provincial", "PEA"]
    total = selection['Poblacion Hombres 2022'].values[0] + selection['Poblacion Mujeres 2022'].values[0]
    base_stats.append(str(round(((selection['Poblacion Hombres 2022'].values[0]/total)*100), 2))+"%")
    base_stats.append(str(round(((selection['Poblacion Mujeres 2022'].values[0]/total)*100), 2))+"%")
    base_stats.append(str(round(selection['% Poblacion Rural'].values[0], 2))+"%")
    base_stats.append(str(round(100-selection['% Poblacion Rural'].values[0], 2))+"%")
    base_stats.append("Pendiente")
    base_stats.append(str(round(selection['PEA'].values[0], 2))+"%")
    df_stats_people = pd.DataFrame({'Indicador': rows_name,'%': base_stats})
    
    return df_stats_people

def get_vab_values(df_2017,df_2018,df_2019,df_2020,selection):
    rows_name = ['2017','2018','2019','2020']
    vab_value = [
        (df_2017.loc[df_2017['CÓDIGO CANTÓN'] == selection['DPA_CANTON'].values[0]])['ECONOMÍA TOTAL'].values[0],
        (df_2018.loc[df_2018['CÓDIGO CANTÓN'] == selection['DPA_CANTON'].values[0]])['ECONOMÍA TOTAL'].values[0],
        (df_2019.loc[df_2019['CÓDIGO CANTÓN'] == selection['DPA_CANTON'].values[0]])['ECONOMÍA TOTAL'].values[0],
        (df_2020.loc[df_2020['CÓDIGO CANTÓN'] == selection['DPA_CANTON'].values[0]])['ECONOMÍA TOTAL'].values[0]
    ]
    vab_selected = pd.DataFrame({'Anio': rows_name,'Valor': vab_value})
    return vab_selected

def get_vab_sector_values(df_2020,selection):
    f_20 = (df_2020.loc[df_2020['CÓDIGO CANTÓN'] == selection['DPA_CANTON'].values[0]])
    f_20 = f_20.drop(columns=['PROVINCIA', 'CÓDIGO PROVINCIA','CANTÓN','CÓDIGO CANTÓN','ECONOMÍA TOTAL'])
    df_vab_2020 = f_20.rename({f_20.index[0]: 'Valor'}, axis='index').T
    df_vab_2020 = df_vab_2020.sort_values(by="Valor", ascending=False).iloc[:3]
    df_vab_2020.index.name = 'Actividad'
    return df_vab_2020

def get_index_prosperity(selection):
    base_stats = []
    rows_name = ["Tasa de Alfabetismo","Ingreso Medio de Hogares USD (Mensual)",
                 "Población en asentamientos Precarios","Población Afectada por eventos naturales (cada mil personas)"]
    base_stats.append(str(round(selection['Tasa de Alfabetismo'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Ingreso Medio Hogares  USD (Mensual)'].values[0], 2)))
    base_stats.append(str(round(selection['Poblacion en asentamientos precarios'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Poblacion afectada por eventos naturales'].values[0], 2))+"%")
    df_stats_people = pd.DataFrame({'Indicador': rows_name,'%': base_stats})
    return df_stats_people

def get_service_access(selection):
    base_stats = []
    rows_name = ["Acceso a Agua Mejorada (% Población)","Acceso a Saneamiento Adecuado (%Población)","Acceso a Electricidad (% Población)",
                 "Acceso a Internet (Usuarios de internet por cada 100 habitantes)", "Acceso Computadores (% Hogares)"]
    #column_name = ['Indicador','%']
    base_stats.append(str(round(selection['Acceso a Agua Mejorada'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Acceso a Saneamiento Adecuado'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Acceso a Electricidad'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Acceso a Internet'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Acceso Computadores (% Hogares)'].values[0], 2))+"%")
    df_stats_people = pd.DataFrame({'Indicador': rows_name,'%': base_stats})
    return df_stats_people

def get_health_infrastructure(selection):
    base_stats = []
    rows_name = ["Centro de Salud Tipo A","Centro de Salud Tipo B","Centro de Salud Tipo C - Maternidad e Infantil",
                 "Centros Especializados","Hospital Básico","Hospital de Especialidades","Hospital General","Puesto de Salud"]
    base_stats.append(str(round(selection['Centro de Salud Tipo A'].values[0])))
    base_stats.append(str(round(selection['Centro de Salud Tipo B'].values[0])))
    base_stats.append(str(round(selection['Centro de Salud Tipo C'].values[0])))
    base_stats.append(str(round(selection['Centros especializados'].values[0])))
    base_stats.append(str(round(selection['Hospital Basico'].values[0])))
    base_stats.append(str(round(selection['Hospital de especialidades'].values[0])))
    base_stats.append(str(round(selection['Hospital General'].values[0])))
    base_stats.append(str(round(selection['Puesto de Salud'].values[0])))
    df_stats_people = pd.DataFrame({'Indicador': rows_name,'%': base_stats})
    return df_stats_people