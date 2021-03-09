import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from plotly.offline import plot
from utils import *

class Interactive_Visuals:
    """This class allows creating dynamic visualizations that match ggplot's format.
    """
    
    def __init__(self, df):
        self._df = df
    
    def histogram(self, x = "Predictor", y = None, color = None, facet_col = None, facet_row = None, 
                  bins = 20, opacity = 1, marginal = None, template = "ggplot2"):
        """Creates a Plotly histogram. Plotly histograms can work with both numeric and categorical data.
        :param Dataframe df: Required. A Pandas dataframe for plotting the data. 
        :param str x: Required. The name of a **numeric** variable in the data frame you want to be your predictor.
        :param str y: Optional, default None.
        :param str color: Optional; default None. A factor variable that you want to visualize your histogram.
        :param str facet_col: Optional; default None. A factor variable you want to facet your histogram on vertically.
        :param str facet_row: Optional; default None. A factor variable you want to facet your histogram on horizontally.
        :param int bins: Optional; default 20. The number of bins you want your histogram to have.
        :param float opacity: Optional, default 1. The opacity of the bars in the histogram. Can be set between 0 and 1.
        :param str marginal: Optional; default None. Can set to "rug", "box", or "violin".
        :param str template: Optional, default ggplot2 (chosen to align with R visualizations). Changes template of plot from default Plotly to another format.
        """
        x_clean, df_clean = clean_varname(self._df, var = x)

        #These can probably be converted into Lambda functions... but for now, this works.
        if color:
            color_clean, df_clean = clean_varname(df_clean, var = color)
        else:
            color_clean = color
        if y:
            y_clean, df_clean = clean_varname(df_clean, var = y)
        else:
            y_clean = y
        if facet_col:
            facet_col_clean, df_clean = clean_varname(df_clean, var = facet_col)
        else:
            facet_col_clean = facet_col
        if facet_row:
            facet_row_clean, df_clean = clean_varname(df_clean, var = facet_row)
        else:
            facet_row_clean = facet_row

        fig = px.histogram(df_clean, x=x_clean, y = y_clean, color=color_clean, title = "Histogram of %s"%(x_clean),
                        marginal = marginal, template = template, opacity = opacity, nbins=bins, facet_col = facet_col_clean,
                          facet_row = facet_row_clean)
        return fig
    
    def scatterplot(self, x = "Predictor", y = "Response", color = None, jitter = False, jitter_sd = .1,
                marg_x = None, marg_y = None, trendline = None, opacity = 1, template = "ggplot2"):
        """Creates a Plotly scatter plot of two numeric variables.
        :param Dataframe df: Required. A Pandas dataframe for plotting the data. 
        :param str x: Required. The name of a **numeric** variable in the data frame you want to be your predictor.
        :param str y: Required. The name of a **numeric** variable in the data frame you want to be your response.
        :param bool jitter: Optional; default False. Setting to true adds noise to data to stop points from overlapping on each other.
        :param float jitter_sd: Optional; default .1. Determines the variability of random noise applied to your data.
        :param str color: Optional; default None. A variable that you want to visualize your scatterplot across. Can be numeric or factor.
        :param str marg_x: Optional; default None. Set to either "histogram", "box", "rug", or "violin" to visualize distribution of x variable.
        :param str marg_y: Optional; default None. Set to either "histogram", "box", "rug", or "violin" to visualize distribution of y variable.
        :param float opacity: Optional, default 1. The opacity of the bars in the histogram. Can be set between 0 and 1.
        :param str trendline: Optional, default None. Sets a trendline for scatterplot if "ols" is chosen. If categorical color chosen, will fit OLS to each factor of color.
        :param str template: Optional, default ggplot2 (chosen to align with R visualizations). Changes template of plot from default Plotly to another format.
        """
        x_clean, df_clean = clean_varname(self._df, var = x)
        y_clean, df_clean = clean_varname(df_clean, var = y)

        if jitter:
            df_clean[x_clean] = df_clean[x_clean] + np.random.normal(0, jitter_sd, size=len(df))
            df_clean[y_clean] = df_clean[y_clean] + np.random.normal(0, jitter_sd, size=len(df))

        if color:
            color_clean, df_clean = clean_varname(df_clean, var = color)
        else:
            color_clean = color 

        fig = px.scatter(df_clean, x=x_clean, y=y_clean, color=color_clean, title = "Scatter Plot of %s and %s"%(x_clean, y_clean),
                        marginal_x = marg_x, marginal_y = marg_y, trendline = trendline, template = template, opacity = opacity)
        return fig
    
    def linechart(self, x = "Predictor", y = "Response", color = None, template = "ggplot2"):
        """Creates a Plotly line chart of a numeric and date variable
        :param Dataframe df: Required. A Pandas dataframe for plotting the data. 
        :param str x: Required. The name of a **date** variable in the data frame you want to be your predictor.
        :param str y: Required. The name of a **numeric** variable in the data frame you want to be your response.
        :param str color: Optional; default None. A variable that you want to visualize your scatterplot across. Can be numeric or factor.
        :param str template: Optional, default ggplot2 (chosen to align with R visualizations). Changes template of plot from default Plotly to another format.
        """
        x_clean, df_clean = clean_varname(self._df, var = x)
        y_clean, df_clean = clean_varname(df_clean, var = y)

        if color:
            color_clean, df_clean = clean_varname(df_clean, var = color)
        else:
            color_clean = color

        fig = px.line(df_clean, x=x_clean, y=y_clean, color = color_clean, template = template, title = "Time Series of %s"%(y_clean))

        return fig
    
    def control_chart_ADTK(self, title = "Control Chart Example", value_name = "Actuals"):
        """Creates a Plotly control chart of a metric measured over time. 
        :param Dataframe df: Required. Data frame fed in should have these columns:
            * date (as index)
            * value
            * median
            * UCL
            * LCL
            * is_violation (binary 0/1 that represents if a point violates expectations according to SPC/Anomaly detection principles)
            * violation_prob (value between 0 and 1 returning the probability of a point being an outlier)
        """

        #Create violation criteria
        df_viol = self._df[self._df["Violation"] > 0]
        df_viol_low = df_viol[df_viol["Violation"] <= .33]
        df_viol_med = df_viol[df_viol["Violation"] <= .67]
        df_viol_med = df_viol_med[df_viol_med["Violation"] > .33]
        df_viol_high = df_viol[df_viol["Violation"] > .67]

        fig = go.Figure(
            data = go.Scatter(
                name=value_name,
                mode="markers+lines", 
                x=df.index, 
                y=df["Values"],
                marker_symbol="circle", 
                marker_size = 6,
                line_color = "blue"
            ),
            layout_title_text = title,
            layout_template = "ggplot2"
        )

        fig.add_trace(go.Scatter(
            name="Median",
            mode="lines", 
            x=df.index, 
            y=df["Median"], 
            line_color = "gray",
            line_width = 2
        ))

        fig.add_trace(go.Scatter(
            name="Control Limits",
            mode="lines", 
            x=df.index, 
            y=df["UCL"], 
            line_color = "black",
            line_dash = "dash",
            line_width = 2
        ))

        fig.add_trace(go.Scatter(
            name="LCL",
            mode="lines", 
            showlegend = False,
            x=df.index, 
            y=df["LCL"], 
            line_color = "black",
            line_dash = "dash",
            line_width = 2
        ))

        fig.add_trace(go.Scatter(
            name = "Violation",
            mode = "markers", 
            x = df_viol.index,
            y = df_viol["Values"],
            marker_color = "red",
            marker_size = 12,
            marker_symbol = "circle-open",
            marker_opacity = .8

        ))

        fig.add_trace(go.Scatter(
            name = "Low Probability of Violation",
            mode = "markers", 
            x = df_viol_low.index,
            y = df_viol["Values"],
            marker_color = "yellow",
            marker_size = 10,
            marker_opacity = .5

        ))

        fig.add_trace(go.Scatter(
            name = "Medium Probability of Violation",
            mode = "markers", 
            x = df_viol_med.index,
            y = df_viol_med["Values"],
            marker_color = "orange",
            marker_size = 10,
            marker_opacity = .5

        ))

        fig.add_trace(go.Scatter(
            name = "High Probability of Violation",
            mode = "markers", 
            x = df_viol_high.index,
            y = df_viol_high["Values"],
            marker_color = "red",
            marker_size = 10,
            marker_opacity = .5

        ))

        return fig

if __name__ == '__main__':    
    #df = px.data.iris()
    #Test to see if Plotly SPC Chart works
    df = pd.DataFrame(dict(
        Date=["2020-01-10", "2020-02-10", "2020-03-10", "2020-04-10", "2020-05-10", "2020-06-10", "2020-07-10"],
        Values=[1,2,3,1,2,4, 5],
        Median = [2,2,2,2,2,2,2],
        UCL = [3,3,3,3,3,3,3],
        LCL = [1,1,1,1,1,1,1],
        Violation = [0,0,0,0,0,.5, .9]
    ))

    #Pandas set date to index col (will be how ingested from ADTK)
    df = df.set_index("Date")
    plt = Interactive_Visuals(df)
    plot(plt.control_chart_ADTK(title = "Anomaly Detection Graph"))

