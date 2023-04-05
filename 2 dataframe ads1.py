import pandas as pd
import matplotlib.pyplot as plt

def worldbank(filename):
    """
    Reading World Bank data from a CSV file and processing it into a clean pandas dataframe.

    Args:
        filename (str): The path to the CSV file containing the World Bank data.

    Returns:
        df_years_rows (pandas.DataFrame): A cleaned pandas dataframe with rows containing NaN values removed.
        df_years_cols (pandas.DataFrame): A cleaned pandas dataframe with columns containing NaN values removed.
    """

    # reading the data into a pandas dataframe
    df = pd.read_csv(filename, index_col='Country Name')

    # droping unnecessary columns 
    df.drop(['Country Code', 'Indicator Name',
            'Indicator Code'], axis=1, inplace=True)

    # filtering the years between 1960 and 2021
    df = df.loc[:, '1960':'2021']

    # transposing the dataframe to have years as columns
    df_years = df.T

    # clean the transposed dataframe
    df_years.index.name = 'Years'
    df_years.columns.name = 'Country'
    df_years.index = pd.to_datetime(df_years.index, format='%Y')

    # create a copy of the original transposed dataframe to remove rows with NaN values
    df_years_rows = df_years.copy()
    df_years_rows.dropna(inplace=True)

    # create a copy of the original transposed dataframe to remove columns with NaN values
    df_years_cols = df_years.copy()
    df_years_cols = df_years_cols.loc[:, ~df_years_cols.isna().all()]

    return df_years_rows, df_years_cols


def barchart(df, countries):
    """
    Create a bar chart of electricity consumption per capita for selected countries.

    Args:
        df (pandas.DataFrame): The pandas dataframe containing the electricity consumption data.
        countries (list): A list of countries to include in the bar chart.

    Returns:
        None
    """

    filtered = df[countries].dropna()

    # Resampling the dataframe with a 4 year frequency
    filtered = filtered.resample('4Y').mean()

    # Make sure to convert the index back to a string representation of the year
    filtered.index = filtered.index.year

    filtered.plot(kind='bar', figsize=(16, 7))
    plt.title('G7 Countries')
    plt.xlabel('Years')
    plt.ylabel('electricity comsuption per capita')
    plt.legend(loc='upper left' , fancybox=True)
    plt.show()


filename = "C:/Users/kusha/OneDrive/Desktop/assignment/electricity power consuption/API_EG.USE.ELEC.KH.PC_DS2_en_csv_v2_4902453.csv"
rows, cols = worldbank(filename)

g7_countries = ['Canada', 'France', 'Germany', 'Italy',
                'Japan', 'United Kingdom', 'United States']

# Display dataframes with floating point numbers
with pd.option_context('display.float_format', '{:.4f}'.format):
    print("Dataframe with rows containing NaN values removed:\n")
    print(rows)

    print("\nDataframe with columns containing NaN values removed:\n")
    print(cols)

# Plot bar chart for G7 countries
barchart(cols, g7_countries)
