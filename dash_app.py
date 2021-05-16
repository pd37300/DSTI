import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(r"df_dash.csv")


# def update_table(selectedData):


app.layout = html.Div([

    html.Div([
        html.H3(children='Data visualization for feature discovery'),
        html.Label([
            'x-axis:',
            dcc.Dropdown(
                id='dropdown-x-feature',
                options=[{'label':i, 'value':i} for i in df.columns],
                value='date',

            ),
        ]),
        html.Label([
            'y-axis:',
            dcc.Dropdown(
                id='dropdown-y-feature',
                options=[{'label':i, 'value':i} for i in df.columns],
                value='actual_productivity'
            ),
        ]),
        html.Label([
            'Color:',
            dcc.Dropdown(
                id='dropdown-color-feature',
                options=[{'label': i, 'value': i} for i in df.columns],
                value='department'
            ),
        ]),
        # html.Label([
        #     'Shape:',
        #     dcc.Dropdown(
        #         id='dropdown-shape-feature',
        #         options=[{'label': i, 'value': i} for i in df.columns],
        #         value=None
        #     ),
        # ]),
        html.Label([
            'Size:',
            dcc.Dropdown(
                id='dropdown-size-feature',
                options=[{'label': i, 'value': i} for i in df.columns],
                value='no_of_workers'
            ),
        ]),
        html.Label([
            'Facet x-axis',
            dcc.Dropdown(
                id='dropdown-facet-x-feature',
                options=[{'label': i, 'value': i} for i in df.columns],
                value=None
            ),
        ]),
        html.Label([
            'Facet y-axis',
            dcc.Dropdown(
                id='dropdown-facet-y-feature',
                options=[{'label': i, 'value': i} for i in df.columns],
                value=None
            )
        ])
    ],
    style={'width':'15%', 'display':'inline-block',
           'backgroundColor':'rgb(250,250,250)',
           'padding': '10px 10px',
           # 'borderBottom':'thin lightgrey solid'
    }),
    html.Div([
        dcc.Graph(
            id='graph-main'
        ),
    ],
    style={'width':'83%','height':'100%', 'display':'inline-block'}
    ),
    dash_table.DataTable(
        id='table-main',
        columns=[{'name':i, 'id':i, 'deletable':True, 'selectable':True} for i in df.columns],
        data=df.to_dict('records'),
        # editable=True,
        filter_action='native',
        sort_action='native',
        sort_mode='multi',
        # column_selectable='single',
        # row_selectable='multi',
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action='native',
        page_current=0,
        page_size=10,
        # style_cell={'height':'auto', 'lin}

    ),
    # html.Div(id='div-1'),
    # html.Div(id='test-output')
])
@app.callback(
    dash.dependencies.Output('graph-main','figure'),
    [
        dash.dependencies.Input('dropdown-x-feature', 'value'),
        dash.dependencies.Input('dropdown-y-feature', 'value'),
        dash.dependencies.Input('dropdown-color-feature', 'value'),
        # dash.dependencies.Input('dropdown-shape-feature', 'value'),
        dash.dependencies.Input('dropdown-size-feature', 'value'),
        dash.dependencies.Input('dropdown-facet-x-feature', 'value'),
        dash.dependencies.Input('dropdown-facet-y-feature', 'value'),
    ]
)
def graph_handling(
        dropdown_x_feature,
        dropdown_y_feature,
        dropdown_color_feature,
        # dropdown_shape_feature,
        dropdown_size_feature,
        dropdown_facet_x_feature,
        dropdown_facet_y_feature
):
    dfx = df.copy()
    fig = px.scatter(
        x=None if dropdown_x_feature is None else dfx[dropdown_x_feature],
        y=None if dropdown_y_feature is None else dfx[dropdown_y_feature],
        color=None if dropdown_color_feature is None else dfx[dropdown_color_feature],
        # marker_symbol=None if dropdown_shape_feature is None else dfx[dropdown_shape_feature],# shape
        size=None if dropdown_size_feature is None else dfx[dropdown_size_feature],
        facet_row=None if dropdown_facet_x_feature is None else dfx[dropdown_facet_x_feature],
        facet_col=None if dropdown_facet_y_feature is None else dfx[dropdown_facet_y_feature],
        template='plotly_white'

    )
    fig.update_xaxes(title=dropdown_x_feature)
    fig.update_yaxes(title=dropdown_y_feature)
    return fig

@app.callback(dash.dependencies.Output('table-main','data'),
              [dash.dependencies.Input('graph-main','selectedData')])
def datatable_handling(selectedData):
    # table_style_conditions = update_table(selectedData)
    selected_points = []
    for point in selectedData['points']:
        selected_points.append(point['pointIndex'])
    # df_ = df.sample(10)
    df_ = df.loc[selected_points,:]
    return df_.to_dict(orient='records')

# @app.callback(
#     dash.dependencies.Output('test-output','children'),
#     dash.dependencies.Input('graph-main','selectedData')
# )
# def test_output(input_value):
#     selected_points = []
#     for point in input_value['points']:
#         selected_points.append(point['pointIndex'])
#
#     return 'Output: {} \n\n XXXXXXXXXX: {}'.format(input_value, selected_points)
if __name__ == '__main__':
    app.run_server(debug=True)