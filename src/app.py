'''
 # @ Create Time: 2024-02-12 21:51:43.021711
'''

from student_loan_functions import calculate_paid_off_year_and_total_paid_array_across_initial_debt_and_salary, plot_interactive_line_graph_of_total_paid_array_against_overpayment_and_initial_debt

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
from meteorological import plt_meteorological_contour_averaged_month_and_longitude_app, plt_meteorological_against_latitude_for_varying_altitude_app, int_to_month

overpayment_factor_array = np.arange(0, 10, 0.1)

app = Dash(__name__, title="MyDashApp")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = dbc.Container([
    html.H1("Contrail Persistence Viewer", className='mb-2', style={'textAlign': 'left',"font-weight":"bold","font-family":"arial"}),
    html.H4("David Barton, 2024 - Optimised for Mobile Viewing", className='mb-2', style={'textAlign': 'left',"font-family":"arial"}),
    html.H5("The aim of this tool is to indicate the altitudes where cruising\naircraft would not produce long-lasting contrails, which are one\nof the leading causes of aviation's climate impact. The approach\nused to develop these plots is detailed in the associated paper\n(doi.org/10.3390/aerospace10080688) to which this work contributed.",
        className='mb-2', style={'textAlign': 'start', 'white-space': 'pre', "font-family": "arial"}),

    html.H5("Contrails persist in regions where the air is 'ice super-saturated',\ni.e. sufficiently cold and wet that any excess moisture condenses\nout as water droplets that freeze into ice crystals, forming\ncontrails. The plots below user weather data from the European\nCentre for Medium-Range Weather-Forecasting to estimate the altitudes\nand latitudes where ice super-saturation typically occurs.\n\nUse the sliders at the bottom to see the results for a range of months and years.\n\n➤  The first plot shows the frequency at which the historic weather\ndata indicated ice super-saturated (ISSR) conditions, as a percentage\n(ISSR Frequency). The trends depended much less significantly on\nlongitude than latitude, so all data has been averaged across longitude\nto eliminate longitude as a parameter.\n\n➤  The second plot looks at three specific altitudes along the\nsame latitude range (x-axis). It shows the extent to which ISSR\nFrequency (and hence probability of long-lived contrails) can be\nreduced by operating higher in non-equatorial latitudes and\nlower in equatorial latitudes.", className='mb-2', style={'textAlign': 'start','white-space':'pre',"font-family":"arial"}),
    dbc.Row([
        dbc.Col([
            html.Img(id='bar-graph-matplotlib')
        ])
    ],justify="start"),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Slider(2015,2020,1,
                        marks={
                        2015: {'label':'2015', 'style': {'fontSize': '12px',"font-family":"arial"}},
                        2016: {'label':'2016', 'style': {'fontSize': '12px',"font-family":"arial"}},
                        2017: {'label':'2017', 'style': {'fontSize': '12px',"font-family":"arial"}},
                        2018: {'label':'2018', 'style': {'fontSize': '12px',"font-family":"arial"}},
                        2019: {'label':'2019', 'style': {'fontSize': '12px',"font-family":"arial"}},
                        2020: {'label':'2020', 'style': {'fontSize': '12px',"font-family":"arial"}},
                        },
                        id='year',
                        value=2017,
                       tooltip={"placement": "top", "always_visible": True,"template":" Year: {value}",
                                "style": {"white-space":'pre',"fontSize": "18px","font-family":"arial"},},
                       )
        ], width=2),
        dbc.Col([
        ], width=2),
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Slider(0, 12, 1,
                       marks={
                           0: {'label': 'Average', 'style': {'fontSize': '12px',"font-family":"arial"}},
                           3: {'label': 'March', 'style': {'fontSize': '12px',"font-family":"arial"}},
                           6: {'label': 'June', 'style': {'fontSize': '12px',"font-family":"arial"}},
                           9: {'label': 'September', 'style': {'fontSize': '12px',"font-family":"arial"}},
                           12: {'label': 'December', 'style': {'fontSize': '12px',"font-family":"arial"}}
                       },
                       id="month",
                       value=0,
                       tooltip={"placement": "top", "always_visible": True, "transform": "intToMonth",
                                "style": {"white-space": 'pre', "fontSize": "18px","font-family":"arial"}, },
                       )
        ], width=2),
        html.Br(),
        html.Br(),
        dbc.Col([html.Div(
            "➤ The slider below may be used to vary the relative humidity threshold at which\nair is deemed to be ice super-saturated (ISSR). Strictly, the condition for ice\nsuper-saturation is that the relative humidity with respect to ice exceeds 100%.\nHowever, some studies (see ref 16 in the associated paper) indicated that\nbetter matching to empirical contrail measurements are achieved when a\nlower threshold (~90%) is applied. One explanation for this phenomenon\nis proposed in the associated paper.\n\n")],
            width=2, style={"white-space": 'pre', 'fontSize': 14,"font-family":"arial"})
    ]),
    html.Br(),
dbc.Row([
        dbc.Col([
            dcc.Slider(80,100,5,
                        marks={
                        80: {'label':'80%', 'style': {'fontSize': '12px',"font-family":"arial"}},
                        85: {'label':'85%', 'style': {'fontSize': '12px',"font-family":"arial"}},
                        90: {'label':'90%', 'style': {'fontSize': '12px',"font-family":"arial"}},
                        95: {'label':'95%', 'style': {'fontSize': '12px',"font-family":"arial"}},
                        100: {'label':'100%', 'style': {'fontSize': '12px',"font-family":"arial"}}
                        },
                        id = "issr_limit",
                        value=90,
                        tooltip={"placement": "top", "always_visible": True,"template":" ISSR Limit: {value}%",
                                "style": {"white-space":'pre',"fontSize": "18px","font-family":"arial"},},
                       )
        ], width=2),
    ]),
    html.Br(),
    dbc.Row([dbc.Col([html.Div(
            "\n\n\nPLANNED FEATURES:\n\n➤ It will be possible to vary the high non-equatorial altitude (blue)\nand low equatorial altitude (red) which are used to generate the\nsecond figure. This would enable users to observe the potential\ncontrail reduction achieved by different altitude changes.\n\n➤ The ability to plot reduction in ISSR achieved by changing altitude\nagainst the magnitude of the change in altitude (increase and decrease)\nfor the equatorial and non-equatorial regions. This would give a clear\noverview of the benefits of altering flight altitude.")],
                width=2,style={"white-space": 'pre', 'fontSize':14,"font-family":"arial"}),
    ]),
])

# Create interactivity between dropdown component and graph
@app.callback(
    Output(component_id='bar-graph-matplotlib', component_property='src'),
    Input('year', 'value'),
    Input('issr_limit', 'value'),
    Input('month', 'value')
)

def plot_data(year,issr_limit,month):
    print(month)
    month = int_to_month(month)
    # Build the matplotlib figure
    fig, (axis1,axis2) = plt.subplots(2,1,figsize=(6,8),dpi=85,constrained_layout=True)

    if(month=="Averaged across all Months"):
        # Averaged Across All Months
        issr_freq_percentage = np.load("data/meteorological/issr_freq_{}%_monthly_total_{}_full.npy".format(issr_limit, year))
    else:
        # An Individual Month
        issr_freq_percentage = np.load("data/meteorological/issr_freq_{}%_monthly_total_{}_{}.npy".format(issr_limit, year, month))
    levels = range(0, 80, 2)

    plt_meteorological_contour_averaged_month_and_longitude_app(issr_freq_percentage, "ISSR Frequency",
                                                            title="Frequency of Contrail Persistence Regions (RH Ice > {}%)".format(
                                                                issr_limit),axis=axis1,fig=fig, unit=" [%]", levels=levels,issr_limit=issr_limit)
    plt_meteorological_against_latitude_for_varying_altitude_app(issr_freq_percentage, "ISSR Frequency",
                                                             plot_only_operating_altitudes=True,
                                                             title="Frequency of Contrail Persistence Regions (RH Ice > {}%)".format(
                                                                 issr_limit), axis=axis2,fig=fig,unit=" [%]", alt_plotting=True)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    fig_bar_matplotlib = f'data:image/png;base64,{fig_data}'

    return fig_bar_matplotlib

if __name__ == '__main__':
    app.run_server(debug=True)
