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
df['brand'] = df['brand'].str.strip()
departments = sorted(list(df['department'].str.title().unique())+['Todos'])
cities = sorted(list(df['municipality'].str.title().unique())+['Todas'])
brands = sorted(list(df['brand'].str.title().unique())+['Todas'])
products = sorted(list(df['product'].str.title().unique())+['Todos'])

# Dictionary for value shown to user and value used internally:
cities_dict = {'Todas': 'Todas'}
for city in df['municipality'].unique():
	cities_dict[city.title()] = city

departments_dict = {'Todos': 'Todos'}
for department in df['department'].unique():
	departments_dict[department.title()] = department

products_dict = {'Todos': 'Todos'}
for product in df['product'].unique():
	products_dict[product.title()] = product

# Geographic Data:
with urlopen('https://gist.githubusercontent.com/FabianTriana/ddcce8b1991536826cd8ef1126c28e7a/raw/077e1b21767f9e29bcf36fc8be35bd40b1659b53/colombia_municipalities_assigned_code.json') as response:
	geo = json.load(response)


# Dictionary for logos:
logos = {'BIOMAX': 'logo_biomax.png', 'BRIO': 'logo_brio.png', 
'ECOS': 'logo_ecos.png', 'ESSO': 'logo_esso.png', 
'MOBIL': 'logo_mobil.png', 'OCTANO': 'logo_octano.png', 
'PETROBRAS': 'logo_petrobras.png', 'PETROMIL': 'logo_petromil.png', 
'PLUS MAS': 'logo_plusmas.png', 'PUMA': 'logo_puma.png', 
'TERPEL': 'logo_terpel.png', 'TEXACO': 'logo_texaco.png', 
'ZEUSS': 'logo_zeuss.png'}


# App Layout:
layout = html.Div(
	[
	html.Div(
		[
		html.Div([html.Div('Departamento', className = 'filter_title'), dcc.Dropdown(options=[{"label": i, "value": departments_dict[i]} for i in departments], value = ['CUNDINAMARCA'], multi = True, id = 'department_dropdown')], className = 'filter'), 
		html.Div([html.Div('Ciudad', className = 'filter_title'), dcc.Dropdown(options=[{"label": i, "value": cities_dict[i]} for i in cities], value = ['Todas'], multi = True, id = 'city_dropdown')], className = 'filter'), 
		html.Div([html.Div('Marca', className = 'filter_title'), dcc.Dropdown(options=[{"label": i, "value": i} for i in brands], value = ['Todas'], multi = True, id = 'brand_dropdown')], className = 'filter'), 
		html.Div([html.Div('Producto', className = 'filter_title'), dcc.Dropdown(options=[{"label": i, "value": products_dict[i]} for i in products], value = ['GASOLINA CORRIENTE'], multi = True, id = 'product_dropdown')], className = 'filter')
		], id = 'filter_section'), 
	html.Div(
		[
		html.Div([dcc.Graph(id = 'the_map')], id = 'map_section'), 
		html.Div(
			[
			html.Div(
				[
				html.Div(
					[
					html.Div('Máximo', className = 'statistics_indicator_name'), 
					html.Div(id = 'max_price', className = 'price_text'), 
					html.Div(id = 'max_trade_name')
					], className = 'statistics_indicator_info'), 
				html.Div(html.Img(id = 'max_logo', className = 'logo'))
				], className = 'statistics_indicator_container'), 
			html.Div(
				[html.Div(
					[html.Div('Mínimo', className = 'statistics_indicator_name'), 
					html.Div(id = 'min_price', className = 'price_text'), 
					html.Div(id = 'min_trade_name')
					], className = 'statistics_indicator_info'), 
				html.Div(html.Img(id = 'min_logo', className = 'logo'))
				], className = 'statistics_indicator_container'), 
			html.Div(
				[html.Div(
					[html.Div('Mediana', className = 'statistics_indicator_name'), 
					html.Div(id = 'median_price', className = 'price_text'), 
					html.Div(id = 'median_trade_name')
					], className = 'statistics_indicator_info'), 
				html.Div(html.Img(id = 'median_logo', className = 'logo'))
				], className = 'statistics_indicator_container'), 
			html.Div(
				[html.Div(
					[html.Div('Promedio', className = 'statistics_indicator_name'), 
					html.Div(id = 'mean_price', className = 'price_text')
					], className = 'statistics_indicator_info'), 
				html.Div(html.Img(src = app.get_asset_url('fuel_black_logo.png'), className = 'logo'))
				], className = 'statistics_indicator_container')
			], id = 'statistics_section')
		], id = 'main_section'), 
	html.Div(
		[
		html.Div('This is the disclaimer section')
		], id = 'disclaimer_section')
	])


# Callbacks:
@app.callback([Output('the_map', 'figure'), 
	Output('max_price', 'children'), 
	Output('max_trade_name', 'children'), 
	Output('max_logo', 'src'), 
	Output('min_price', 'children'), 
	Output('min_trade_name', 'children'), 
	Output('min_logo', 'src'), 
	Output('median_price', 'children'), 
	Output('median_trade_name', 'children'), 
	Output('median_logo', 'src'), 
	Output('mean_price', 'children')], 
	[Input('department_dropdown', 'value'),
	Input('city_dropdown', 'value'), 
	Input('product_dropdown', 'value')])
def update_map(selected_departments, selected_cities, selected_products):
	# Department Selection:
	if 'Todos' in selected_departments:
		selected_departments = list(df['department'].unique())
	else:
		selected_departments = selected_departments

	# City Selection:
	if 'Todas' in selected_cities:
		selected_cities = list(df['municipality'].unique())
	else:
		selected_cities = selected_cities
	
	# Product Selection:
	if 'Todos' in selected_products:
		selected_products = list(df['product'].unique())
	else:
		selected_products = selected_products
	
	# Conditions to filter Dataframe:
	city_filter = df['municipality'].isin(selected_cities)
	department_filter = df['department'].isin(selected_departments)
	product_filter = df['product'].isin(selected_products)

	# Dataframe:
	df_selected = df[(city_filter) & (department_filter) & (product_filter)]
	
	# Price Range:
	max_price = df_selected['price'].max()
	min_price = df_selected['price'].min()
	median_price = df_selected['price'].median()
	mean_price = df_selected['price'].mean()

	# Trade name:
	max_trade_name = list(df_selected[df_selected['price'] == max_price]['trade_name'].unique())[0]
	min_trade_name = list(df_selected[df_selected['price'] == min_price]['trade_name'].unique())[0]
	median_trade_name = list(df_selected[df_selected['price'] == median_price]['trade_name'].unique()[0])

	# Logos:
	max_brand = list(df_selected[df_selected['price'] == max_price]['brand'].unique())[0]
	if max_brand in logos.keys():
		max_logo = app.get_asset_url(logos[max_brand])
	else:
		max_logo = app.get_asset_url('fuel_black_logo.png')
	
	min_brand = list(df_selected[df_selected['price'] == min_price]['brand'].unique())[0]
	if min_brand in logos.keys():
		min_logo = app.get_asset_url(logos[min_brand])
	else:
		min_logo = app.get_asset_url('fuel_black_logo.png')

	median_brand = list(df_selected[df_selected['price'] == median_price]['brand'].unique())[0]
	if median_brand in logos.keys():
		median_logo = app.get_asset_url(logos[median_brand])
	else:
		median_logo = app.get_asset_url('fuel_black_logo.png')

	# Figure:
	fig = px.choropleth_mapbox(df_selected, 
		geojson=geo, locations='assigned_code', 
		color='price', 
		featureidkey = 'properties.assigned_code',
		color_continuous_scale="RdYlGn_r",
		range_color=(min_price, max_price),
		mapbox_style="carto-positron",
		zoom=7,
		opacity=0.5,
		center = {'lat': 4.62, 'lon': -74.06},
		labels={'price':'price'})
	fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
	return [fig, '$'+str(int(max_price)), max_trade_name, max_logo, '$'+str(int(min_price)), min_trade_name, min_logo, '$'+str(int(median_price)), median_trade_name, median_logo, '$'+str(int(mean_price))]