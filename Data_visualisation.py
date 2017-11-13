import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sb
import numpy as np
import pandas as pd

import cufflinks as cf

import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

from plotly.graph_objs import *

class DataVis:

    def __init__(self, username, api_key):
        tls.set_credentials_file(username=username, api_key=api_key)

    def pie_chart(self,data,labels, title = None, filename = None):

        if title is None: title =  'Simple Pie Chart'
        fig = {'data': [{'labels': labels, 'values': data, 'type': 'pie'}],'layout': {'title': title}}
        if filename is None :
            if title is None : filename='default-pie-chart'
            else: filename = title
        py.iplot(fig, filename=filename)

    def pie_chart_data(self,data,labels):
        return {'labels': labels, 'values': data, 'type': 'pie'}

    def time_series_graph_data(self,DF_dictionary):
        data = []
        #for category in DF_dictionary:
           # data.append(go.Scatter(x = DF_dictionary[category].keys(),y= DF_dictionary[category].values,mode='lines+markers'))
            #data.append({'x':DF_dictionary[category].keys(),'y':DF_dictionary[category].values,'mode':'lines=markers','name':category})
        return go.Scatter(x = DF_dictionary['Tube'].keys(),y= DF_dictionary['Tube'].values,mode='lines+markers')
        #return data

    def time_series_graph(self,DF_dictionary,title=None, filename= None):
        data = []
        for category in DF_dictionary:
            data.append({'x':DF_dictionary[category].keys(),'y':DF_dictionary[category].values,'mode':'lines=markers','name':category})

        if title is None: title = 'Time Series Graph'
        fig = {'data': data
             , 'layout': {'xaxis': {'title': ''}, 'yaxis': {'title': 'Expenditure (GBP)'},'title': title}}
        if filename is None:
            if title is None:
                filename = 'Time_Series_Graph'
            else:
                filename = title
        py.iplot(fig, filename=filename)

    def graph_all (self,pie_data,pie_labels,scatter_DF_dictionary):
        pie_data = self.pie_chart_data(pie_data,pie_labels)
        scatter_data = self.time_series_graph_data(scatter_DF_dictionary)
        data = Data([ pie_data,scatter_data])
        layout = {
            "plot_bgcolor": 'black',
            "paper_bgcolor": 'black',
            "titlefont": {
                "size": 20,
                "family": "Raleway"
            },
            "font": {
                "color": 'white'
            },
            "dragmode": "zoom",
            "margin": {
                "r": 10,
                "t": 25,
                "b": 40,
                "l": 60
            },
            "showlegend": False,
            "title": "<br>Volcano Database",
            "xaxis": {
                "anchor": "y",
                "domain": [0, 0]
            },
            "yaxis": {
                "anchor": "x",
                "domain": [0, 0],
                "showgrid": False
            },
            "xaxis2": {
                "anchor": "y",
                "domain": [5, 5]
            },
            "yaxis2": {
                "anchor": "x",
                "domain": [5, 5],
                "showgrid": False
            }
        }
        fig = Figure(data=data,layout = layout)
        py.iplot(fig, filename="Mixed Subplots bank data")
        fig2 = Figure(data=data)
        py.iplot(fig2, filename="Mixed Subplots bank data 2")
        py.iplot(fig2, filename="Mixed Subplots bank data 3", subplots = True)


    def bar_chart(self,x_data,y_data, title = None, filename = None):
        data = [go.Bar(x= x_data, y= y_data)]
        if title is None: title =  'Simple Bar Chart'

        layout = go.Layout(title=title)
        fig = go.Figure(data=data, layout=layout)
        if filename is None :
            if title is None : filename='default-bar-chart'
            else: filename = title
        py.iplot(fig, filename=filename)

    def test_line_chart(self):
        a = np.linspace(start=0, stop=36, num=36)

        np.random.seed(25)
        b = np.random.uniform(low=0.0, high=1.0, size=36)

        trace = go.Scatter(x=a, y=b)

        data = [trace]

        py.iplot(data, filename='basic-line-chart')