import pandas as pd
import matplotlib.pyplot as plt

def worldbank(filepath, skiprows):
    """
    Reads a CSV file containing forest land area data for different countries from the World Bank,
    cleans the data, and returns two dataframes: one with rows removed that contain missing values,
    and one with columns removed that contain missing values.

    Parameters:
    filepath (str): The file path of the CSV file.
    skiprows (list): The rows to be skipped when reading the CSV file.

    Returns:
    dfyear_row (pandas dataframe): A dataframe with rows removed that contain missing values.
    dfyear_colm (pandas dataframe): A dataframe with columns removed that contain missing values.
    """
    # reading the data into a pandas dataframe and skip the specified rows
    df = pd.read_csv(filepath, index_col='Country Name', skiprows=skiprows)

    # droping unnecessary columns
    df.drop(['Country Code', 'Indicator Name', 'Indicator Code'], axis=1, inplace=True)

    # selecting columns with years that are multiples of 5
    df = df.iloc[:,::5]

    # transposing the dataframe to have years as columns
    dfyears = df.T

    # cleaning the transposed dataframe
    dfyears.index.name = 'Year'
    dfyears.columns.name = 'Country Name'
    dfyears.index = pd.to_datetime(dfyears.index, format='%Y').strftime('%Y')

    # creating a copy of the original transposed dataframe to remove rows with NaN values
    dfyear_row = dfyears.copy()
    dfyear_row.dropna(inplace=True)

    # creating a copy of the original transposed dataframe to remove columns with NaN values
    dfyear_colm = dfyears.copy()
    dfyear_colm = dfyear_colm.loc[:, ~dfyear_colm.isna().all()]

    return dfyear_row, dfyear_colm


filepath = "C:/Users/kusha/OneDrive/Desktop/assignment/New folder/forest land.csv"
skiprows = [0,1,2,3]
df_rows, df_cols = worldbank(filepath, skiprows)

# creating a bar chart to show the forest land area in G7 countries over time
g7countries = ['Canada', 'France', 'Germany', 'Italy', 'Japan', 'United Kingdom', 'United States']
dfg7 = df_cols[g7countries]
dfg7.plot(kind='bar', figsize=(10,10))
plt.title('Forest Land Area in G7 Countries from 1960 to 2021 (Median: {:.2f})'.format(dfg7.median().median()))
plt.xlabel('Year')
plt.ylabel('Forest Land Area (% of land area)')
plt.ylim(0, 100)
plt.show()
 