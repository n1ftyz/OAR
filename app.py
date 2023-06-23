from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go



df = pd.read_csv('1C_Developer.csv')

df_cities = pd.read_csv('cities_russia.csv')

#external_stylesheets = [dmc.theme.DEFAULT_COLORS]
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
all_cont = df['name'].unique()







SIDESTYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#ffdfde",
    "text-color": "#000000"
}


CONTSTYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div([    
        html.H2("Раздел", className="display-4", style={'color': 'black'}),
            html.Hr(style={'color': 'black'}),
            dbc.Nav([
                    dbc.NavLink("Общие показатели", href="/page1", active="exact"),
                    dbc.NavLink("Карта", href="/page2", active="exact"),
                ],
                vertical=True,pills=True),
        ],
        style=SIDESTYLE,
    ),
    html.Div(id="page-content", children=[], style=CONTSTYLE)
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])







#app.layout = dmc.Container([ 



def pagecontent(pathname):
    if pathname == "/page1":
        return dmc.Container([
        html.Div([
            html.H1("Информация о профессии Программист 1С"),
            html.P(
                "Анализ профессии на сайте hh.ru. "
                "Используйте фильтры, чтобы увидеть результат."
                )
            ], style={
                'backgroundColor': 'rgb(255, 223, 222)',
                'padding': '50px 25px',
                'text-align' : 'center'
            }),      
        html.Div([
                html.Div([
                    html.Label('Профессии'),
                    dcc.Dropdown(
                        id ='name',
                        options=[{'label': i, 'value': i} for i in all_cont],
                        value=['Администратор 1С', 'Аналитик 1С', 'Архитектор 1С', 'Программист 1С', 'Программист-разработчик 1С', 'Разработчик 1С', 'Специалист 1С'],
                        multi=True
                    )
                ], 
                style={'width': '100%', 'display': 'inline-block'}),
                html.Div(
                    dcc.Graph(id='pie'),
                    style={'display': 'inline-block'}),
                html.Div(
                    dcc.Graph(id='scatter'),
                    style={'display': 'inline-block'}),
                html.Div([
                    html.Label('Города'),
                    dcc.Dropdown(
                        id ='area_name',
                        options=[{'label': i, 'value': i} for i in df['area_name'].unique()],
                        value=['Москва','Санкт-Петербург'],
                        multi=True
                    )
                ], 
                style={'width': '100%', 'display': 'inline-block'}),
                html.Div(
                    dcc.Graph(id='pie2'),
                    style={'width': '100%', 'display': 'inline-block'}),
                html.Div(
                    dcc.Graph(id='bar'),
                    style={'width': '100%', 'display': 'inline-block'}),
                 html.Div(
                    dcc.Graph(id='mapbox'),
                    style={'width': '100%', 'display': 'inline-block'}),
                ])
        ], fluid=True) #РАСТЯГИВАНИЕ НА ВЕСЬ ЭКРАН

    elif pathname == "/page2":
        return dmc.Container([
            html.Div([
                html.Div([
                    html.H1("Вакансии дизайнеров"),
                    html.P(
                        "Данные о вакансиях дизайн-индустрии."
                        " Используйте фильтры, чтобы увидеть результат."
                    )
                ], style={
                    'backgroundColor': 'rgb(255, 223, 222)',
                    'padding': '10px 5px'
                }),
                    html.Div([
                    html.Label('Профессии'),
                    dcc.Dropdown(
                        id ='name',
                        options=[{'label': i, 'value': i} for i in all_cont],
                        value=['Администратор 1С', 'Аналитик 1С', 'Архитектор 1С', 'Программист 1С', 'Программист-разработчик 1С', 'Разработчик 1С', 'Специалист 1С'],
                        multi=True
                    )
                ]),
                    html.Div(
                        dcc.Graph(id='mapbox'),
                        style={'width': '100%', 'display': 'inline-block'}),
                ])
        ], fluid=True)


@callback(
    Output('pie', 'figure'),
    Input('name', 'value'),
)
def update_pie(name):
    filtered_data = df[(df['name'].isin(name))]
    fig = px.pie(filtered_data, values=filtered_data.groupby('name')['name'].count(), names=filtered_data['name'].unique(), hole=.0, color_discrete_sequence=px.colors.sequential.Burg, title="Количество вакансий по названиям")
    return fig


@callback(
    Output('pie2', 'figure'),
    Input('area_name', 'value'),
)
def update_pie2(name):
    filtered_data = df[(df['area_name'].isin(name))]
    fig = px.pie(filtered_data, values=filtered_data.groupby('area_name')['area_name'].count(), names=filtered_data['area_name'].unique(), hole=.0, color_discrete_sequence=px.colors.sequential.Burg, title="Количество вакансий по выбранной профессии")
    return fig


@callback(
    Output('scatter', 'figure'),
    Input('name', 'value'),
)
def update_scatter(name):
    filtered_data = df[(df['name'].isin(name))]
    fig = px.bar(filtered_data,
            y=(((filtered_data.groupby('name')['salary_to'].sum()+filtered_data.groupby('name')['salary_from'].sum())/2)/filtered_data.groupby('name')['name'].count()),
            x=filtered_data['name'].unique(),
            labels = {'x': 'Вакансия','y': 'Средняя зарплата'}, color_discrete_sequence=px.colors.sequential.Burg, title="Средняя зарплата по вакансиям")
    return fig


@callback(
    Output('bar', 'figure'),
    Input('name', 'value'),
)
def update_bar(name):
    fig = px.bar(df,
            x=df['employer_name'].unique(),
            y=df.groupby('employer_name')['employer_name'].count(), labels = {'x': 'Компания','y': 'Кол-во вакансий'}, color_discrete_sequence=px.colors.sequential.Burg, title="Компании с количеством выбранных вакансий")
    return fig

@callback(
Output('mapbox','figure'),
Input ('name','value'),
)
def update_map(name):
    df_fil = pd.merge(df, df_cities, left_on=['area_name'], right_on=['Город'], how='inner')
    fig = px.scatter_mapbox(df_fil, lat=df_fil['Широта'].unique(), lon=df_fil['Долгота'].unique(), hover_name=df_fil['area_name'].unique())
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)