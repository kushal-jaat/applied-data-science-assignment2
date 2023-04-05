import pandas as pd
import matplotlib.pyplot as plt

def read_worldbank_data(file_path, skiprows):
    """
    Reads a CSV file containing electric power transmission and distribution loss data for different countries from the World Bank,
    cleans the data, and returns two dataframes: one with rows removed that contain missing values,
    and one with columns removed that contain missing values.

    Parameters:
    file_path (str): The file path of the CSV file.
    skiprows (list): The rows to be skipped when reading the CSV file.

    Returns:
    df_years_rows (pandas dataframe): A dataframe with rows removed that contain missing values.
    df_years_cols (pandas dataframe): A dataframe with columns removed that contain missing values.
    """
    # read the data into a pandas dataframe and skip the specified rows
    df = pd.read_csv(file_path, index_col='Country Name', skiprows=skiprows)

    # drop unnecessary columns
    df.drop(['Country Code', 'Indicator Name', 'Indicator Code'], axis=1, inplace=True)

    # select columns with years that are multiples of 5
    df = df.iloc[:,::5]

    # transpose the dataframe to have years as columns
    df_years = df.T
 
    # clean the transposed dataframe
    df_years.index.name = 'Year'
    df_years.columns.name = 'Country Name'
    df_years.index = pd.to_datetime(df_years.index, format='%Y').strftime('%Y')

    # create a copy of the original transposed dataframe to remove rows with NaN values
    df_years_rows = df_years.copy()
    df_years_rows.dropna(inplace=True)

    # create a copy of the original transposed dataframe to remove columns with NaN values
    df_years_cols = df_years.copy()
    df_years_cols = df_years_cols.loc[:, ~df_years_cols.isna().all()]

    return df_years_rows, df_years_cols


file_path = "C:/Users/kusha/OneDrive/Desktop/assignment/Electric power transmission and distribution losses.csv"
skiprows = [0,1,2,3]
df_rows, df_cols = read_worldbank_data(file_path, skiprows)

# create a pie chart to show the electricity loss in G7 countries
g7_countries = ['Canada', 'France', 'Germany', 'Italy', 'Japan', 'United Kingdom', 'United States']
df_g7 = df_cols[g7_countries].sum()
df_g7.name = 'Electricity Loss (%)'
df_g7.plot.pie(figsize=(10,10), autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})
plt.title('Electricity Loss in G7 Countries from 1960 to 2021')
plt.ylabel('')
plt.show()

# explore the statistical properties of the data for G7 countries
g7_data = df_cols[g7_countries]
g7_summary = g7_data.describe()

print("Summary statistics for G7 countries:\n")
print(g7_summary)
