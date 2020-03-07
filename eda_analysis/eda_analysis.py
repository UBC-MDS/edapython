
"""Perform EDA analysis of the given DataFrame"""
import pandas as pd
import numpy as np
import altair as alt

def generate_report(dataframe,cat_vars,num_vars):
    """
    This function generates an EDA report by plotting graphs and tables for the 
    numeric variables, categorical variables, NA values and correlation in a dataframe
    
    Parameters:
    -----------
    dataframe: pandas.DataFrame
        The dataframe whose EDA analysis is to be performed
    cat_vars: list
        A list containing names of categorical variables
    num_vars: list
        A list containing names of numerical variable
        
    Returns:
    --------
    boolean
        It returns True on successful execution else returns False
        
    Examples:
    ---------
    >>> X= pandas.DataFrame({
    'type':['Car','Bus','Car']
    'height':[10,20,30]
    })
    >>>cat_vars = ['type']
    >>>num_vars = ['height']
    >>> describe_cat_variable(X,cat_vars,num_vars)
    
    """
    
    
def describe_na_values(dataframe):
    '''
    describes the na_values in an input pandas dataframe as a 2d array of 1's and 0's.

    Parameters
    ----------
    dataframe: Pandas.DataFrame
        the input pd.DataFrame object.

    Returns
    -------
    numpy.ndarray
        A 2d Numpy Array of 1's and 0's, corresponding to the value of each entry in the dataframe.
        0 represents an NA value, 1 represents a non-NA value.
    '''
    pass    

  
def describe_cat_var(dataframe,cat_vars, n_cols = 3):
    """
    This function will take dataframe and categorical variable names and will 
    plot the histogram of each categorical variable.
    
    Parameters:
    -----------
    dataframe: pandas.DataFrame
        The dataframe whose EDA analysis is to be performed
    cat_vars: list
        A list containing names of categorical variables
    n_cols: int (default: 3)
        A number indicating how many plots should be displayed in a row
    
    Returns:
    --------
    altair
        a grid of altair plot containing all histograms
    
    Examples:
    ---------
    >>> X= pandas.DataFrame({
    'type':['Car','Bus','Car']
    'height':[10,20,30]
    })
    >>> cat_vars = ['type']
    >>> describe_cat_variable(X,cat_vars)
       
    """
    
    #Checking for valid inputs
    if not isinstance(dataframe, pd.DataFrame):
        raise Exception("The value of the argument 'dataframe' must be of type 'pandas.DataFrame'")
    
    if not isinstance(cat_vars,list) or not all(isinstance(x, str) for x in cat_vars):
        raise Exception("The value of the argument 'cat_vars' must be a list of strings")
        
    if not isinstance(n_cols,int) or n_cols<=0:
        raise Exception("The value of the argument 'n_cols' must be a positive non zero integer")
    
    col_set = set(dataframe.columns)
    col_subset = set(cat_vars)
    if not col_subset.issubset(col_set):
        raise Exception("The input categorical column names must belong to the dataframe")
    
    dataframe=dataframe.dropna()
    data = dataframe[col_subset]
    n = len(cat_vars)
    n_cols = n_cols
    n_rows = int(np.ceil(n/n_cols))
    z = 0
    
    # Plotting the histograms in loop
    for i in range(n_rows):
        for j in range(n_cols):
            if z < n :
                cols = cat_vars[z]
            else:
                break
            hist = alt.Chart(data).mark_bar(width = 40).encode(
                x = alt.X(cols+':O'),
                y = 'count()'
            ).properties(height = 200, width = 300, title = 'Histogram of '+cat_vars[z])
            z = z + 1
            if j == 0:
                row_plot = hist
            else:
                row_plot = alt.hconcat(row_plot,hist)
        if i == 0:
            plot = row_plot
        else:
            plot = alt.vconcat(plot,row_plot)
            
    return plot

    
def describe_num_var(dataframe, num_vars):
    """ 
    This function takes dataframe and numeric variable names and provides 
    statistical summary of the numeric variables for a dataframe.
    Also, the function plots the histogram of each numeric variable.

    Parameters:
    -----------
    dataframe: pandas.DataFrame
        The dataframe to be inspected.
    num_vars: list
        A list of unique character strings of the names of the numeric variables.
    
    Returns:
    --------
    tuple(pandas.DataFrame, altair)
        pandas.DataFrame
            statistical summary of the numeric variables
        altair
            a grid of altair plot containing all histograms
    
    Examples:
    ---------
    >>> X= pandas.DataFrame({
    'type':['Car', 'Bus', 'Car']
    'height':[10, 20, 30]
    'width':[12, 15, 11]
    })
    >>> num_vars = ['height', 'width']
    >>> summary, plot = describe_num_var(X, num_vars)
    >>> summary
    >>> plot
      
    """
    # Check the dataframe input
    if not isinstance(dataframe, pd.DataFrame):
        raise Exception("The value of the argument 'dataframe' should be of type pandas dataframe.")
    
    # Check the num_vars input should be a list of strings
    if not (all(isinstance(item, str) for item in num_vars) & isinstance(num_vars, list)):
        raise Exception("The value of the argument 'num_vars' should be a list of strings.")
    
    # Check if the elements in the num_vars input are unique
    if len(num_vars) != len(set(num_vars)):
        raise Exception("The elements in the argument 'num_vars' should be unique.")

    # Check if the num_vars input contains only the column names
    if not all(item in dataframe.columns for item in num_vars):
        raise Exception("The argument 'num_vars' should be a subset of the column names from the dataframe.")
    
    # Subset and transpose the dataframe for later use 
    df = pd.DataFrame(dataframe[num_vars]).T
    
    # Check if only the numeric columns are selected
    if not np.issubdtype(df.to_numpy().dtype, np.number):
        raise Exception("Only numeric columns expected, please check the input.")

    # Calculate the statistical summaries
    stat_funs = [np.nanmin, np.nanmax, np.nanmedian, np.nanmean, np.nanstd]
    temp = []
    for fun in stat_funs:
        data_stat = df.apply(fun, axis=1)
        temp.append(data_stat)

    temp_df = pd.DataFrame(temp)
    quantiles_df = pd.DataFrame([np.nanquantile(df, 0.25, axis = 1), 
                                 np.nanquantile(df, 0.75, axis = 1)])
    quantiles_df.columns = num_vars

    summary = pd.concat([quantiles_df, temp_df])
    
    # Change the index more readable
    summary.index = ["25%", "75%", "min", "max", "median", "mean", "sd"]
    
    # Make the histogram
    df_to_plot = df.T.melt().dropna()
    plot = alt.Chart(df_to_plot).mark_bar().encode(
        alt.X("value:Q", bin=alt.Bin(maxbins=30), title = "Value"),
        y='count()'
    ).properties(
        width=300,
        height=300,
        title='Histogram of Numeric Variables'
    ).facet(
        facet='variable:N',
        columns=3
        )
    
    return summary, plot


def calc_cor(dataframe, num_vars):
    """
    This function evaluates the correlation between the numeric 
    variables of a given dataframe.


	Parameters:
    -----------
    dataframe: pandas.DataFrame
        The data frame whose EDA analysis is to be performed.
    num_vars: list
        A list of strings of column names containing numeric variables.

    Returns:
    --------
    altair
        A correlogram plot labelled with the correlation coefficients 
        of -1 to 1 between each numeric column and other numeric variables
        in the dataframe.

    Examples:
    ---------
    >>> X= pandas.DataFrame({
    'type':['Car','Bus','Car']
    'width':[40, 10, 5]
    'height':[10,20,30]
    })
    >>>num_var = ['height', 'width']
    >>> calc_cor(X, num_vars)    
    """
    # Code
