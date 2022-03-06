from dash import dcc, html
from utils import Header, make_dash_table
import dataservice
import graphs

# get relative data folder

df = dataservice.get_selected_dataframe('CANTON','1FvE33JAUWO8mgzcoaZF7H1iYCEYm6da06rmEX8lGJaM')
df_suelo = dataservice.get_selected_dataframe('Uso_S_Manabi','1LgCKDvc1JFc_F0pAzmHUNE0QeNHPc9VoU_NOton1tw0')
geo = dataservice.get_geojson()
df_2017 = dataservice.get_selected_dataframe('2017','1EOEmsm1R8ubMSXEcPBKbLF5dAOqVM5tTUIy702WSJmM')
df_2018 = dataservice.get_selected_dataframe('2018','1EOEmsm1R8ubMSXEcPBKbLF5dAOqVM5tTUIy702WSJmM')
df_2019 = dataservice.get_selected_dataframe('2019','1EOEmsm1R8ubMSXEcPBKbLF5dAOqVM5tTUIy702WSJmM')
df_2020 = dataservice.get_selected_dataframe('2020','1EOEmsm1R8ubMSXEcPBKbLF5dAOqVM5tTUIy702WSJmM')

def create_layout(app,value):
    selection = df.loc[df['CANTON'] == value]
    selection_map = geo.loc[geo['DPA_CANTON'] == str(selection['DPA_CANTON'].values[0])]
    df_selected = df_suelo.loc[df_suelo['DPA_CANTON'] == selection['DPA_CANTON'].values[0]]
    vab_selected = graphs.get_vab_values(df_2017,df_2018,df_2019,df_2020,selection)
    df_vab_2020 = graphs.get_vab_sector_values(df_2020,selection)
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app,value)]),
            # page 1
            html.Div(
                [
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Información"),
                                    html.Br([]),
                                    html.H6("Extensión Territorial",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                    html.H6("Habitantes",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Mapa",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=graphs.get_map_graph(selection_map)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Uso de Suelo",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=graphs.get_pie_chart(df_selected)),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Características Población"], className="subtitle padded"
                                    ),
                                    html.Table(make_dash_table(graphs.get_stats_people(selection))),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Evolución VAB 2017-2020",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=graphs.get_line_chart(vab_selected)),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Índice de Prosperidad Territorial 2021",
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_dash_table(graphs.get_index_prosperity(selection))),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Price & Performance (%)",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=graphs.get_bar_chart(df_vab_2020)),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),
                    # Row 6
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Acceso a Servicios",
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_dash_table(graphs.get_service_access(selection))),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Infraestructura de Salud",
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_dash_table(graphs.get_health_infrastructure(selection))),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )

