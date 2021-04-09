import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from plotly.offline import plot
from utils import *

class Interactive_Visuals:
    """This class allows creating dynamic visualizations that match ggplot's format. Current options include the following:
        
        * Histogram 
        * Bar chart
        * Scatterplot
        * Line chart
        * Control chart
    """
    
    def __init__(self, df):
        self._df = df
    
    def histogram(self, x = "Predictor", y = None, is_horizontal = False, color = None, facet_col = None, facet_row = None, 
                  bins = 20, opacity = 1, marginal = None, template = "ggplot2", has_title = True, title = None):
        """Creates a Plotly histogram. Plotly histograms can work with both numeric and categorical data.
        
        :param Dataframe df: Required. A Pandas dataframe for plotting the data. 
        
        :param str x: Required. The name of a numeric variable in the data frame you want to be your predictor.
        
        :param str y: Optional, default None. **Using this may give weird and unexpected results, as Plotly tries to adapt to data fed in!**
        
        :param bool is_horizontal: Optional, default False. Will swap x and y values so that the plot appears horizontally.
        
        :param str color: Optional; default None. A factor variable that you want to visualize your histogram.
        
        :param str facet_col: Optional; default None. A factor variable you want to facet your histogram on vertically.
        
        :param str facet_row: Optional; default None. A factor variable you want to facet your histogram on horizontally.
        
        :param int bins: Optional; default 20. The number of bins you want your histogram to have.
        
        :param float opacity: Optional, default 1. The opacity of the bars in the histogram. Can be set between 0 and 1.
        
        :param str marginal: Optional; default None. Can set to "rug", "box", or "violin".
        
        :param str template: Optional, default ggplot2 (chosen to align with R visualizations). Changes template of plot from default Plotly to another format.
        
        :param bool has_title: Optional, default True. Determines if plot has a title or not. Default title is provided if True, but can be customized with title.
        
        :param str title: Optional, default None. Changes title of plot from the default.
        
        :returns: Plotly fig object
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

        if has_title:
            if not title:
                title = f"Histogram of {x_clean}"

        if is_horizontal:
            fig = px.histogram(df_clean, y=x_clean, x = y_clean, color=color_clean, title = title,
                            marginal = marginal, template = template, opacity = opacity, 
                            nbins=bins, facet_col = facet_col_clean, facet_row = facet_row_clean)
        else:
            fig = px.histogram(df_clean, x=x_clean, y = y_clean, color=color_clean, title = title,
                            marginal = marginal, template = template, opacity = opacity, 
                            nbins=bins, facet_col = facet_col_clean, facet_row = facet_row_clean)
        return fig
    
    def barplot(self, x = "Predictor", color = None, opacity = 1, template = "ggplot2", 
                has_title = True, barmode="stack", is_horizontal = False, title = None, is_percent = False,
                show_num = False):
        """Creates a Plotly bar plot. Bar plots work with categorical data. Function computes appropriate counts and percentages to create bar plots.
        
        :param Dataframe df: Required. A Pandas dataframe for plotting the data. 
        
        :param str x: Required. The name of a categorical variable in the data frame you want to be your predictor.
                        
        :param str color: Optional; default None. A factor variable that you want to visualize your bar plot.
        
        :param bool is_horizontal: Optional, default False. Will swap x and y values so that the plot appears horizontally.

        :param float opacity: Optional, default 1. The opacity of the bars in the histogram. Can be set between 0 and 1.
                
        :param str template: Optional, default ggplot2 (chosen to align with R visualizations). Changes template of plot from default Plotly to another format.
        
        :param str barmode: Optional, default "stack". Options: ['stack', 'group', 'overlay', 'relative']
        
        :param bool has_title: Optional, default True. Determines if plot has a title or not. Default title is provided if True, but can be customized with title.
        
        :param str title: Optional, default None. Changes title of plot from the default. 
        
        :param bool is_percent: Optional, default False. Set true to plot a percentage-based stacked bar plot.
        
        :param bool show_num: Optional, default False. Show percentages on stacked bar plot.
        
        :returns: Plotly fig object
        """
        if color: #Produce either a stacked or grouped bar plot
            df_stack = self._df.groupby([x,color]).size().reset_index()
            df_stack['Percentage'] = self._df.groupby([x, color]).size().groupby(level = 0).apply(lambda 
        x:100 * x/float(x.sum())).values
            df_stack.columns = [x, color, 'Count', 'Percentage']
            df_stack['Percentage'] = round(df_stack['Percentage'], 2)
            
            x_clean, df_clean = clean_varname(df_stack, var = x)
            color_clean, df_clean = clean_varname(df_clean, var = color)
            
            if has_title:
                if not title:
                    title = f"Bar Plot of {x_clean} and {color_clean}"
            else:
                title = None
             
                
            # 8 different variations for how this graph can appear:
            if is_horizontal:
                if is_percent:
                    if show_num: #Show percentages on stacked bar graph
                        fig = px.bar(df_clean, y = x_clean, x = 'Percentage', 
                                 color = color_clean, template = template, barmode=barmode, 
                             opacity = opacity, title = title, text = df_clean['Percentage'])
                    else:
                        fig = px.bar(df_clean, y = x_clean, x = 'Percentage', 
                                 color = color_clean, template = template, barmode=barmode, 
                             opacity = opacity, title = title)
                else:
                    if show_num: #Show counts on stacked bar graph:
                        fig = px.bar(df_clean, y = x_clean, x = 'Count', 
                             color = color_clean, template = template, barmode=barmode, 
                         opacity = opacity, title = title, text = df_clean['Count'])
                    else:
                        fig = px.bar(df_clean, y = x_clean, x = 'Count', 
                                 color = color_clean, template = template, barmode=barmode, 
                             opacity = opacity, title = title)
            else:
                if is_percent:
                    if show_num:
                        fig = px.bar(df_clean, x = x_clean, y = 'Percentage', 
                                color = color_clean, template = template, barmode=barmode, 
                             opacity = opacity, title = title, text = df_clean['Percentage'])
                    else:
                        fig = px.bar(df_clean, x = x_clean, y = 'Percentage', 
                                color = color_clean, template = template, barmode=barmode, 
                             opacity = opacity, title = title)
                else:
                    if show_num:
                        fig = px.bar(df_clean, x = x_clean, y = 'Count', 
                            color = color_clean, template = template, barmode=barmode, 
                         opacity = opacity, title = title, text = df_clean['Count'])
                    else:
                        fig = px.bar(df_clean, x = x_clean, y = 'Count', 
                                color = color_clean, template = template, barmode=barmode, 
                             opacity = opacity, title = title) 
            
            return fig
        
        else: #Create a basic bar plot
           df_stack = self._df.groupby([x]).size().reset_index()
           df_stack['Percentage'] = self._df.groupby([x]).size().groupby(level = 0).apply(lambda 
   x:100 * x/float(x.sum())).values
           df_stack.columns = [x, 'Count', 'Percentage']
           x_clean, df_clean = clean_varname(df_stack, var = x)
           
           if has_title:
               if not title:
                   title = f"Bar plot of {x_clean}"
           
           if is_horizontal:
               fig = px.bar(df_clean, y = x_clean, x = 'Count', 
                            template = template, title = title)
           else:
               fig = px.bar(df_clean, x = x_clean, y = 'Count', 
                            template = template, title = title)
           return fig 
        
    def scatterplot(self, x = "Predictor", y = "Response", color = None, jitter = False, jitter_sd = .1,
                marg_x = None, marg_y = None, trendline = None, opacity = 1, template = "ggplot2",
                has_title = True, title = None):
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
        
        :param bool has_title: Optional, default True. Determines if plot has a title or not. Default title is provided if True, but can be customized with title.
        
        :param str title: Optional, default None. Changes title of plot from the default. 
        
        :returns: Plotly fig object.
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

        if has_title:
            if not title:
                title = f"Scatter Plot of {x_clean} and {y_clean}"
                
        fig = px.scatter(df_clean, x=x_clean, y=y_clean, color=color_clean, title = title,
                        marginal_x = marg_x, marginal_y = marg_y, trendline = trendline, template = template, opacity = opacity)
        return fig
    
    def linechart(self, x = "Predictor", y = "Response", color = None, template = "ggplot2",
                  has_title = True, title = None):
        """Creates a Plotly line chart of a numeric and date variable
        
        :param Dataframe df: Required. A Pandas dataframe for plotting the data. 
        
        :param str x: Required. The name of a **date** variable in the data frame you want to be your predictor.
        
        :param str y: Required. The name of a **numeric** variable in the data frame you want to be your response.
        
        :param str color: Optional; default None. A variable that you want to visualize your scatterplot across. Can be numeric or factor.
        
        :param str template: Optional, default ggplot2 (chosen to align with R visualizations). Changes template of plot from default Plotly to another format.
        
        :param bool has_title: Optional, default True. Determines if plot has a title or not. Default title is provided if True, but can be customized with title.
        
        :param str title: Optional, default None. Changes title of plot from the default.
        
        :returns: Plotly fig object.
        """
        
        
        x_clean, df_clean = clean_varname(self._df, var = x)
        y_clean, df_clean = clean_varname(df_clean, var = y)

        if color:
            color_clean, df_clean = clean_varname(df_clean, var = color)
        else:
            color_clean = color

        if has_title:
            if not title:
                title = f"Time Series of {y_clean}"

        fig = px.line(df_clean, x=x_clean, y=y_clean, color = color_clean, template = template, title = title)

        return fig
    
    
    def forecast_CV_surge(self, title = "Cross-Validation", value_name = "Actuals",
                 upper_bound_name = "Worst-Case", lower_bound_name = "Best-Case",
                 upper_bound_color = "red", lower_bound_color = "blue", predicted_color = "orange",
                 fill_color_and_opacity = 'rgba(50, 50, 50, .2)', roll_avg = False, roll_avg_num = 7):
        """Creates a Plotly line chart of a metric alongside bounds and predicted values. Can be used for either cross-validation or forecasting.
        
        :param Dataframe df: Required. Data frame fed in should have these columns:
            
            * Date (as index)
            * Values (known, not forecasted)
            * Predicted (forecasted expected values)
            * UB (upper bound; ex: prediction interval 95%)
            * LB (lower bound)
            
        :param str title: A string that will define the title of your graph. Default is "Cross-Validation".
        
        :param str value_name: A string that represent the name of the values in the graph. Default is "Actuals".
        
        :param str upper_bound_name: A string that represents the name of the upper bound in the graph. Default is "Worst-Case".
        
        :param str lower_bound_name: A string that represents the name of the lower bound in the graph. Default is "Best-Case".
        
        :param str lower_bound_color: A string that represents the color of the lower bound in the graph. Default is "blue".
        
        :param str upper_bound_color: A string that represents the color of the upper bound in the graph. Default is "red".
        
        :param str predicted_color: A string that represents the color of the predicted linke in the graph. Default is "orange".
        
        :param str fill_color_and_opacity: A string that represents the color and opacity of the fill. Default is 'rgba(50,50,50.2)', which creates a light gray tint between the lower and upper bounds. To make opacity clear and have no shading appear, set the final value in rgba to be 0.
        
        :param bool roll_avg: Boolean to determine if need to apply rolling average to data.
        
        :param int roll_avg_num: Integer indicating frequency to apply rolling average on. Default is 7.
        
        :returns: Plotly fig object.
        """
        
        if roll_avg:
            self._df['Values'] = self._df['Values'].rolling(window=roll_avg_num, closed = 'left').mean()
            self._df['Predicted'] = self._df['Predicted'].rolling(window=roll_avg_num, closed = 'left').mean()
            self._df['UB'] = self._df['UB'].rolling(window=roll_avg_num, closed = 'left').mean()
            self._df['LB'] = self._df['LB'].rolling(window=roll_avg_num, closed = 'left').mean()
        
        fig = go.Figure(
            data = go.Scatter(
                name=value_name,
                mode="markers+lines", 
                x=self._df.index, 
                y=self._df["Values"],
                marker_symbol="circle", 
                marker_size = 6,
                line_color = "black"
            ),
            layout_title_text = title,
            layout_template = "ggplot2"
        )
        
        fig.add_trace(go.Scatter(
            name="Predicted",
            mode="lines", 
            x=self._df.index, 
            y=self._df["Predicted"], 
            line_color = predicted_color,
            line_width = 2
        ))
        
        fig.add_trace(go.Scatter(
            name=upper_bound_name,
            mode="lines", 
            x=self._df.index, 
            y=self._df["UB"], 
            line_color = upper_bound_color,
            line_width = 2
        ))
        
        fig.add_trace(go.Scatter(
            name=lower_bound_name,
            mode="lines", 
            x=self._df.index, 
            y=self._df["LB"], 
            line_color = lower_bound_color,
            fill = 'tonexty',
            fillcolor = fill_color_and_opacity,
            line_width = 2
        ))
        
        
        return fig
        
    
    def control_chart_ADTK(self, title = "Control Chart Example", value_name = "Actuals"):
        """Creates a Plotly control chart of a metric measured over time. 
        
        :param Dataframe df: Required. Data frame fed in should have these columns:
            
            * Date (as index)
            * Values
            * Median
            * UCL
            * LCL
            * Violation (value between 0 and 1 returning the probability of a point being an outlier)
            
        :param str title: A string that will define the title of your Control Chart. Default is "Control Chart Example".
        
        :param str value_name: A string that represent the name of the values in the control chart. Default is "Actuals".
        
        :returns: Plotly fig object.
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
                x=self._df.index, 
                y=self._df["Values"],
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
            x=self._df.index, 
            y=self._df["Median"], 
            line_color = "gray",
            line_width = 2
        ))

        fig.add_trace(go.Scatter(
            name="Control Limits",
            mode="lines", 
            x=self._df.index, 
            y=self._df["UCL"], 
            line_color = "black",
            line_dash = "dash",
            line_width = 2
        ))

        fig.add_trace(go.Scatter(
            name="LCL",
            mode="lines", 
            showlegend = False,
            x=self._df.index, 
            y=self._df["LCL"], 
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
    #iv = Interactive_Visuals(df)
    #plot(iv.scatterplot(x = "sepal_length", y = "sepal_width"))
    #plot(iv.histogram(x = "sepal_length", color = "species", facet_col = "species", marginal="box", bins = 10, title = "Sepal Length Faceted on Species"))
    # df = px.data.tips()
    # iv = Interactive_Visuals(df)
    # plot(iv.barplot(x = "sex", color = "smoker", is_horizontal = True, is_percent = True, show_num = True))
    # df = px.data.gapminder().query("country=='Canada'")
    # iv = Interactive_Visuals(df)
    # plot(iv.linechart(x = "year", y = "lifeExp"))
    # df = pd.DataFrame(dict(
    #     Date=["2020-01-10", "2020-02-10", "2020-03-10", "2020-04-10", "2020-05-10", "2020-06-10", "2020-07-10"],
    #     Values=[1,2,3,1, None, None, None],
    #     Predicted = [None,None,None,None,2,2,2],
    #     UB = [None,None,None,None,3,3,3],
    #     LB = [None,None,None,None,1,1,1]
    # ))
    # df = pd.DataFrame(dict(
    #     Date=["2020-01-10", "2020-02-10", "2020-03-10", "2020-04-10", "2020-05-10", "2020-06-10", "2020-07-10"],
    #     Values=[1,2,3,1,2,4, 5],
    #     Predicted = [2,2,2,2,2,2,2],
    #     UB = [3,3,3,3,3,3,3],
    #     LB = [1,1,1,1,1,1,1]))
    
    # #Pandas set date to index col (will be how ingested from ADTK)
    # df = df.set_index("Date")
    # iv = Interactive_Visuals(df)
    # plot(iv.surge_forecast_CV(title = "CV Test"))
    
    df = pd.read_csv("test.csv")
    df = df.set_index("Date")
    iv = Interactive_Visuals(df)
    plot(iv.surge_forecast_CV(title = "Forecast", dates_as_month = True))