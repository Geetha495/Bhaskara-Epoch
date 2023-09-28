import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Student Menu Review App"

 
menu_df = pd.read_csv('menu_data.csv')

 
app.layout = dbc.Container([
    html.H1("Menu Review App", className="my-4 text-center"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Menu")),
                dbc.CardBody([
                    dcc.Graph(id='menu-graph'),
                ]),
            ]),
        ], lg=6),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Student Reviews")),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='item-review',
                        options=[{'label': item, 'value': item} for item in menu_df['Item']],
                        placeholder='Select an item to review'
                    ),
                    dbc.Input(id='student-name', type='text', placeholder='Your Name', className="my-2"),
                    dbc.Input(id='student-rating', type='number', placeholder='Rating (1-5)', className="my-2"),
                    dbc.Textarea(id='student-comment', placeholder='Review Comment', className="my-2"),
                    dbc.Button('Submit', id='submit-button', n_clicks=0, color="primary", className="my-2"),
                    html.Div(id='validation-message', className="text-danger"),   
                ]),
            ]),
        ], lg=6),
    ]),

    dbc.Card([
        dbc.CardHeader(html.H4("Insights")),
        dbc.CardBody([
            dcc.Graph(id='insights-graph'),
        ]),
    ], className="my-4"),

], fluid=True)

 
@app.callback(
    Output('menu-graph', 'figure'),
    Output('insights-graph', 'figure'),
    Output('item-review', 'value'),   
    Output('student-name', 'value'),   
    Output('student-rating', 'value'),   
    Output('student-comment', 'value'),   
    Output('validation-message', 'children'),   
    Input('submit-button', 'n_clicks'),
    State('item-review', 'value'),
    State('student-name', 'value'),
    State('student-rating', 'value'),
    State('student-comment', 'value')
)
def update_menu_and_insights(n_clicks, item_review, student_name, student_rating, student_comment):
    validation_message = ''   

    if n_clicks is None or n_clicks == 0:
        return dash.no_update, dash.no_update, item_review, student_name, student_rating, student_comment, validation_message

    if not item_review:
         
        validation_message = 'Please select a menu item.'
        return dash.no_update, dash.no_update, item_review, student_name, student_rating, student_comment, validation_message

    if not student_name:
         
        validation_message = 'Please enter your name.'
        return dash.no_update, dash.no_update, item_review, student_name, student_rating, student_comment, validation_message

    if student_rating is None:
         
        validation_message = 'Please enter a rating (1-5).'
        return dash.no_update, dash.no_update, item_review, student_name, student_rating, student_comment, validation_message

     
    if not (1 <= student_rating <= 5):
         
        validation_message = 'Rating must be between 1 and 5.'
        return dash.no_update, dash.no_update, item_review, student_name, student_rating, student_comment, validation_message

     
    item_index = menu_df.index[menu_df['Item'] == item_review].tolist()[0]
    menu_df.at[item_index, 'Average Rating'] = (menu_df.at[item_index, 'Average Rating'] + student_rating) / 2

    menu_df.to_csv('menu_data.csv', index=False)   

     
    item_review = ''
    student_name = ''
    student_rating = ''
    student_comment = ''

    menu_fig = px.bar(menu_df, x='Item', y='Average Rating', title='Menu Item Ratings')
    
     
         
    insights_fig = px.pie(menu_df, names='Item', values='Average Rating', title='Menu Item Ratings Distribution')

    return menu_fig, insights_fig, item_review, student_name, student_rating, student_comment, validation_message

 
if __name__ == '__main__':
    app.run_server(debug=True)
