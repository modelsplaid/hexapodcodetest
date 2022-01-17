import dash
import dash_core_components as dcc
import dash_html_components as html



app = dash.Dash(__name__,              
                update_title='Loading...'
                )

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Plotly Dash', className="app-header--title")
        ]
    ),
    
    html.Div(
        children=html.Div([
            
            html.H1('Overview'),        
            html.Div('''
                This is an example of a simple Dash app with
                local, customized CSS.
            ''')
        ])   
    )
    
])

if __name__ == '__main__':
    app.run_server(debug=True)