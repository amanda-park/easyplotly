import plotly.express as px

def clean_varname(df, var):
    """Formats text of variables so that titles and axes on Plotly graphs look cleaner.
    :param Dataframe df: Required. A Pandas dataframe for plotting the data. 
    :param str var: Required. The name of a variable in the data frame you want to clean the name of.
    :returns: var_clean, df_clean
    """
    var_clean = var.replace("_", " ")
    var_clean = var_clean.title()
    df_clean = df.rename(columns={var : var_clean})
    return var_clean, df_clean

if __name__ == '__main__':    
    df = px.data.iris()
    #df = clean_varname(df, )
    
