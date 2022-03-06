# -*- coding: utf-8 -*-
from dash import Dash, dcc, html, Input, Output
from plotly.express import data
import dataservice
import utils

df =  dataservice.get_selected_dataframe('CANTON','1FvE33JAUWO8mgzcoaZF7H1iYCEYm6da06rmEX8lGJaM')


from pages import (
    overview,
    pricePerformance,
    portfolioManagement,
    feesMins,
    distributions,
    newsReviews,
    error
)

app = Dash(
    __name__, 
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']
)
app.title = "Reportes Financieros"
server = app.server
app.config.suppress_callback_exceptions=True


# Describe the layout/ UI of the app
app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            ["Cantón"], className="subtitle padded"
                        ),
                        dcc.Dropdown(options = df['CANTON'],
                                     id='pandas-dropdown-2',
                                     placeholder = "Seleccione Cantón"
                                     ),
                        html.Div(id='pandas-output-container-2')
                    ],
                    #className="six columns",
                ),
            ],
            className='dropdown'
        ),

        
    ]
)

# Update page
@app.callback(
    Output("page-content", "children"), 
    [Input("url", "pathname"),Input('pandas-dropdown-2', 'value')]
)
def display_page(pathname,value):
    if pathname == "/dash-financial-report/price-performance":
        return pricePerformance.create_layout(app,value)
    elif pathname == "/dash-financial-report/portfolio-management":
        return portfolioManagement.create_layout(app,value)
    elif pathname == "/dash-financial-report/fees":
        return feesMins.create_layout(app,value)
    elif pathname == "/dash-financial-report/distributions":
        return distributions.create_layout(app,value)
    elif pathname == "/dash-financial-report/news-and-reviews":
        return newsReviews.create_layout(app,value)
    elif pathname == "/dash-financial-report/full-view":
        return (
            overview.create_layout(app,value),
            pricePerformance.create_layout(app,value),
            portfolioManagement.create_layout(app,value),
            feesMins.create_layout(app,value),
            distributions.create_layout(app,value),
            newsReviews.create_layout(app,value),
        )
    else:
        return overview.create_layout(app,value)


# Error page

@app.callback(
    Output('pandas-output-container-2', 'children'),
    Input('pandas-dropdown-2', 'value')
)
def update_output(value):
    if(value):
        return dcc.Location(id="url", refresh=False), html.Div(id="page-content")
    else:
        return html.Div(
            [
                # page 1
                html.Br([]),
                html.Div(
                    [
                        html.H2("Seleccione un Cantón o Parroquia")
                    ]
                )
            ],
            className="page",
        )

    
if __name__ == "__main__":
    app.run_server(debug=True)
