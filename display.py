import functions
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.Header(id='title', children="Procrastinate Smart!"),
    html.Header(id='header1', children='Please input youtube lecture video urls separated by spaces'),
    dcc.Textarea(
        id='inputVideos',
        placeholder='enter urls',
        style={'width': '100%'},
        rows=7,
        cols=30
    ),

    html.Button(id='submit-videos', n_clicks=0, children='Submit'),
    html.Header(id='header2', children='', style={'display': 'none', 'width': '100%'}),
    html.Header(id='header3', children='', style={'display': 'none'}),
    dcc.Textarea(
        id='inputSearch',
        placeholder='Search Term',
        style={'width': '30%'},
        rows=1
    ),
    html.Button(id='submit-search', n_clicks=0, children='Search', style={'display': 'none'}),
    html.Header(id='header4', children='', style={'display': 'none'}),

    html.Hr(id='bar2', style={'display': 'none'}),
    html.Div(id='output'),
    html.Div(id='videoArray', style={'display': 'none'}),
    html.Div(id='resultArray', children="", style={'display': 'none'})
])


@app.callback(Output('videoArray', 'children'),
              [Input('submit-videos', 'n_clicks')],
              [State('inputVideos', 'value')])
def update_videos(n_clicks, input):
    links = input.split()
    links = functions.parseLinks(links)
    return links


@app.callback(Output('header2', 'children'),
              [Input('submit-videos', 'n_clicks')],
              [State('inputVideos', 'value')])
def update_videos(n_clicks, input):
    return str(input.count(' ') + 1) + ' videos successfully uploaded! '


@app.callback(Output('header3', 'children'),
              [Input('submit-videos', 'n_clicks')],
              [State('inputVideos', 'value')])
def update_header3(n_clicks, input):
    return " What do you want to learn?"


@app.callback(Output('header3', 'style'),
              [Input('submit-videos', 'n_clicks')],
              [State('inputVideos', 'value')])
def show_header3(n_clicks, input):
    if n_clicks > 0:
        return {'display': 'block'}
    return {'display': 'none'}


@app.callback(Output('header4', 'children'),
              [Input('resultArray', 'children')],
              [State('resultArray', 'children')])
def update_header4(n_clicks, input):
    return str(int(len(input)/2)) + " results found!"


@app.callback(Output('header4', 'style'),
              [Input('resultArray', 'children')],
              [State('inputVideos', 'value')])
def show_header4(n_clicks, input):
    if len(input) > 0:
        return {'display': 'block'}
    return {'display': 'none'}


@app.callback(Output('header2', 'style'),
              [Input('submit-videos', 'n_clicks')],
              [State('inputVideos', 'value')])
def show_header2(n_clicks, input):
    if n_clicks > 0:
        return {'display': 'block'}
    return {'display': 'none'}


@app.callback(Output('inputSearch', 'style'),
              [Input('submit-videos', 'n_clicks')],
              [State('inputVideos', 'value')])
def show_input_search(n_clicks, input):
    if n_clicks > 0:
        return {'width': '100%', 'display': 'inline-block'}
    return {'width': '100%', 'display': 'none'}


@app.callback(Output('submit-search', 'style'),
              [Input('submit-videos', 'n_clicks')],
              [State('inputVideos', 'value')])
def show_submit_search(n_clicks, input):
    if n_clicks > 0:
        return {'display': 'inline-block'}
    return {'display': 'none'}


@app.callback(Output('bar2', 'style'),
              [Input('submit-videos', 'n_clicks')],
              [State('inputVideos', 'value')])
def show_bar2(n_clicks, input):
    if n_clicks > 0:
        return {'display': 'inline-block'}
    return {'display': 'none'}


@app.callback(Output('resultArray', 'children'),
              [Input('submit-search', 'n_clicks')],
              [State('videoArray', 'children'),
               State('inputSearch', 'value')])
def update_output(n_clicks, videoArray, inputSearch):

    links = videoArray
    xmlDicts = []
    for link in links:
        xmlDicts.append(functions.xmlToDict(link))
    timeDicts = []
    for xmlDict in xmlDicts:
        timeDicts.append(functions.buildProperDict(xmlDict))
    links2, descriptions = functions.searchAndDisplay(links, xmlDicts, timeDicts, inputSearch)
    return links2 + descriptions


@app.callback(Output('output', 'children'),
              [Input('resultArray', 'children')],
              [State('resultArray', 'children')])
def result_data(children1, children2):
    dict = []
    for i in range(0, int(len(children1)/2)):
        # https://www.youtube.com/watch?v=SXR9CDof7qw&feature=youtu.be&t=2860
        # https://www.youtube.com/watch?v=tBiPumGnVT4&t=16
        # http://video.google.com/timedtext?lang=en&v=SXR9CDof7qw&t=2372.51
        link = children1[i]
        print(link)
        index = link.index('v=') + 2
        extension = link[index:]
        link = 'https://www.youtube.com/watch?v=' + extension
        try:
            index2 = link.index('.', link.index('t=') + 2)
        except ValueError:
            index2 = -1

        if index2 != -1:
            link = link[:index2]
        dict.append({'props': {'children': '"' + children1[i + int((len(children1)/2))] + '"',
                               'href': link, 'target': '_blank'}, 'type': 'A', 'namespace': 'dash_html_components'})
    return dict


if __name__ == '__main__':
    app.run_server(debug=True)
