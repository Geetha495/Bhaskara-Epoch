import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Student Courses Review App"

 
courses_df = pd.read_csv('./courses_data.csv')

 
app.layout = dbc.Container([
    html.H1("Courses Review App", className="my-4 text-center"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Courses")),
                dbc.CardBody([
                    dcc.Graph(id='courses-graph'),
                ]),
            ]),
        ], lg=6),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Student Reviews")),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='course-review',
                        options=[{'label': course, 'value': course} for course in courses_df['Course']],
                        placeholder='Select an course to review'
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
    Output('courses-graph', 'figure'),
    Output('insights-graph', 'figure'),
    Output('course-review', 'value'),   
    Output('student-name', 'value'),   
    Output('student-rating', 'value'),   
    Output('student-comment', 'value'),   
    Output('validation-message', 'children'),   
    Input('submit-button', 'n_clicks'),
    State('course-review', 'value'),
    State('student-name', 'value'),
    State('student-rating', 'value'),
    State('student-comment', 'value')
)
def update_courses_and_insights(n_clicks, course_review, student_name, student_rating, student_comment):
    validation_message = ''   

    if n_clicks is None or n_clicks == 0:
        courses_fig = px.bar(courses_df, x='Course', y='Average Rating', title='Course Ratings')         
        insights_fig = px.pie(courses_df, names='Course', values='Average Rating', title='Course Ratings Distribution')
        return courses_fig, insights_fig
    
    if not course_review:
         
        validation_message = 'Please select a courses course.'
        return dash.no_update, dash.no_update, course_review, student_name, student_rating, student_comment, validation_message

    if not student_name:         
        validation_message = 'Please enter your name.'
        return dash.no_update, dash.no_update, course_review, student_name, student_rating, student_comment, validation_message

    if student_rating is None:         
        validation_message = 'Please enter a rating (1-5).'
        return dash.no_update, dash.no_update, course_review, student_name, student_rating, student_comment, validation_message

     
    if not (1 <= student_rating <= 5):
         
        validation_message = 'Rating must be between 1 and 5.'
        return dash.no_update, dash.no_update, course_review, student_name, student_rating, student_comment, validation_message

     
    course_index = courses_df.index[courses_df['Course'] == course_review].tolist()[0]
    courses_df.at[course_index, 'Average Rating'] = (courses_df.at[course_index, 'Average Rating'] + student_rating) / 2

    courses_df.to_csv('courses_data.csv', index=False)   

     
    course_review = ''
    student_name = ''
    student_rating = ''
    student_comment = ''

    courses_fig = px.bar(courses_df, x='Course', y='Average Rating', title='Course Ratings')
    
         
    insights_fig = px.pie(courses_df, names='Course', values='Average Rating', title='Course Ratings Distribution')

    return courses_fig, insights_fig, course_review, student_name, student_rating, student_comment, validation_message

 
if __name__ == '__main__':
    app.run_server(debug=True)
