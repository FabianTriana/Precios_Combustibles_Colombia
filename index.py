import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import principal


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Principal', href='/apps/principal', className = 'index_item'),
        #dcc.Link('Mercado', href='/apps/mercado', className = 'index_item'),
        #dcc.Link('Detalle', href='/apps/detalle', className = 'index_item')
    ], className = 'index_menu'),
    html.Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"),
	html.Div(
		[
		html.Div(html.Img(src = app.get_asset_url("fuel_logo.png"), id = 'logo_image'), id = 'logo_section'),
		html.Div(html.Div('Precios Combustibles - Colombia', id = 'title'), id = 'title_section'),
		html.Div(
			[
			html.Div(html.A(href="https://www.linkedin.com/in/fabiantriana/", className="fa fa-linkedin"), className = 'contact_item_container'),
			html.Div(html.A(href= 'https://github.com/FabianTriana/', className = 'fa fa-github'), className = 'contact_item_container'),
			html.Div(html.A(href='mailto:fatrianaa1@gmail.com', className = 'fa fa-envelope'), className = 'contact_item_container')
			], id = 'contact_section')
		], id = 'header'),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/principal':
        return principal.layout
    else:
        return principal.layout


if __name__ == '__main__':
    app.run_server(debug=True)
