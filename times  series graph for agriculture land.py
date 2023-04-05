import pandas as pd
import matplotlib.pyplot as plt

def read_worldbank_data(file_path, skiprows):
    """
    Reads in data from a specified file path, skips the specified rows, drops unnecessary columns,
    selects only the G7 countries of interest, transposes the data, and converts the index to a
    DatetimeIndex object.
    
    Args:
        file_path (str): The path to the data file.
        skiprows (list): A list of row indices to skip when reading the data file.
        
    Returns:
        df_g7 (pandas.DataFrame): A DataFrame containing the agricultural land data for G7 countries.
    """
    # read the data into a pandas dataframe and skip the specified rows
    df = pd.read_csv(file_path, index_col='Country Name', skiprows=skiprows)

    # drop unnecessary columns
    df.drop(['Country Code', 'Indicator Name', 'Indicator Code'], axis=1, inplace=True)

    # select only the G7 countries of interest
    g7_countries = ['Canada', 'France', 'Germany', 'Italy', 'Japan', 'United Kingdom', 'United States']
    df_g7 = df.loc[g7_countries]

    # transpose the dataframe to have years as columns
    df_g7 = df_g7.T

    # convert the index to a DatetimeIndex object
    df_g7.index = pd.to_datetime(df_g7.index)

    return df_g7


file_path = "C:/Users/kusha/OneDrive/Desktop/assignment/New folder/agriculture land.csv"
skiprows = [0,1,2,3]
df_g7 = read_worldbank_data(file_path, skiprows)

# calculate mean, median, variance, and standard deviation for each country
mean_vals = df_g7.mean()
median_vals = df_g7.median()
variance_vals = df_g7.var()
std_vals = df_g7.std()

# create the time series plot
fig, ax = plt.subplots(figsize=(15,6))
handles = []
for col in df_g7.columns:
    line, = ax.plot(df_g7.index, df_g7[col], label=col)
    handles.append(line)

# add mean and standard deviation to the legend
labels = [f"{col} (mean={mean_vals[col]:.2f}, median={median_vals[col]:.2f}, variance={variance_vals[col]:.2f}, std={std_vals[col]:.2f})" for col in df_g7.columns]
ax.legend(handles=handles, labels=labels, loc='upper left', fontsize=10, bbox_to_anchor=(1.02, 1),  title_fontsize=12)
ax.get_legend().get_lines()[-1].set_linestyle('--')
ax.get_legend().get_lines()[-1].set_linewidth(2)

# set the axis labels and title
ax.set_xlabel('Year', fontsize=10)
ax.set_ylabel('Agricultural Land (% of Land Area)', fontsize=12)
ax.set_title('Agricultural Land by G7 Countries', fontsize=16)

# add grid lines and adjust their style
ax.grid(axis='both', alpha=0.3, linestyle='--')

# display the chart
plt.show()

# print the statistical properties for each country
print("Statistical properties for G7 countries:\n")
for col in df_g7.columns:
    print(f"{col} - mean: {mean_vals[col]:.2f}, median: {median_vals[col]:.2f}, variance: {variance_vals[col]:.2f}, std: {std_vals[col]:.2f}")
