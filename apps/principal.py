import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from urllib.request import urlopen
import json

from app import app


import pandas as pd

# Fuel Data:
df = pd.read_csv("https://gist.githubusercontent.com/FabianTriana/ed6969797aa0f69fcd41f34e670eafed/raw/colombia_fuel_prices_2022_2q.csv", delimiter= ",")
departments = sorted(list(df['department'].str.title().unique())+['Todos'])
cities_dict = {}
for city in df['municipality'].unique():
	cities_dict[city.title()] = city
cities = sorted(list(df['municipality'].str.title().unique())+['Todas'])
brands = sorted(list(df['brand'].str.title().unique())+['Todas'])
products = sorted(list(df['product'].str.title().unique())+['Todos'])

# Geographic Data:
with urlopen('https://gist.githubusercontent.com/FabianTriana/ddcce8b1991536826cd8ef1126c28e7a/raw/077e1b21767f9e29bcf36fc8be35bd40b1659b53/colombia_municipalities_assigned_code.json') as response:
	geo = json.load(response)

layout = html.Div(
	[
	html.Div(
		[
		html.Div([html.Div('Departamento', className = 'filter_title'), dcc.Dropdown(options=[{"label": i, "value": i} for i in departments], value = ['Todos'], multi = True, id = 'department_dropdown')], className = 'filter'), 
		html.Div([html.Div('Ciudad', className = 'filter_title'), dcc.Dropdown(options=[{"label": i, "value": i} for i in cities], value = ['Sopo'], multi = True, id = 'city_dropdown')], className = 'filter'), 
		html.Div([html.Div('Marca', className = 'filter_title'), dcc.Dropdown(options=[{"label": i, "value": i} for i in brands], value = ['Todas'], multi = True, id = 'brand_dropdown')], className = 'filter'), 
		html.Div([html.Div('Producto', className = 'filter_title'), dcc.Dropdown(options=[{"label": i, "value": i} for i in products], value = ['Gasolina Corriente'], multi = True, id = 'product_dropdown')], className = 'filter')
		], id = 'filter_section'), 
	html.Div(
		[
		html.Div([dcc.Graph(id = 'the_map')], id = 'map_section'), 
		html.Div(['This is the statistics section'], id = 'statistics_section')
		], id = 'main_section'), 
	html.Div(
		[
		html.Div('This is the disclaimer section')
		], id = 'disclaimer_section')
	])


# Callbacks:
@app.callback([Output('the_map', 'figure')], 
	[Input('city_dropdown', 'value')])
def update_map(selected_cities):
	list_selected_cities = []
	for city in selected_cities:
		list_selected_cities.append(cities_dict[city])
	df_selected = df[df['municipality'].isin(list_selected_cities)]
	fig = px.choropleth_mapbox(df, 
		geojson=geo, locations='assigned_code', 
		color='price', 
		featureidkey = 'properties.assigned_code',
		color_continuous_scale="RdYlGn",
		range_color=(7000, 25000),
		mapbox_style="carto-positron",
		zoom=3,
		opacity=0.5,
		labels={'price':'price'})
	fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
	return [fig]