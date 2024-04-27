import pandas as pd
import matplotlib.pyplot as plt


def parse_natural_gas_data_for_state_at_year(path_to_state_data, year_of_interest):
    data_for_state = pd.read_csv(path_to_state_data, skiprows=2)

    # Cleanup
    data_for_state = data_for_state.dropna(subset=['Date'])
    data_for_state['Date'] = data_for_state['Date'].astype(int)
    data_for_state = data_for_state.fillna(0)
    
    # Drop the unwanted 'Unnamed: 10' column if it exists
    if 'Unnamed: 10' in data_for_state.columns:
        data_for_state.drop(columns=['Unnamed: 10'], inplace=True)

    # Dynamic renaming based on keywords to filter out location names, and get eveyrthign on the same naming scheme
    keywords = {
        'Residential': 'Residential',
        'Commercial': 'Commercial',
        'Industrial': 'Industrial',
        'Vehicle Fuel Consumption': 'Vehicle Fuel',
        'Electric Power': 'Electric Power',
        'Delivered to Consumers': 'Total Delivered'
    }
    rename_columns = {}
    for col in data_for_state.columns:
        for keyword, new_name in keywords.items():
            if keyword in col:
                rename_columns[col] = new_name

    data_for_state.rename(columns=rename_columns, inplace=True)

    # Select the relevant columns based on the expected consumption categories
    columns_of_interest = ['Date'] + list(keywords.values())
    data_for_state = data_for_state[columns_of_interest]
    
    data_for_specific_year = data_for_state[data_for_state['Date'] == year_of_interest]

    return data_for_specific_year


def make_pie_chart_of_natural_gas_data(state_data_for_one_year, location_name, year):
    data_row = state_data_for_one_year.iloc[0]

    # Prepare data for the pie chart, excluding the 'Date' and 'Total Delivered' columns
    sectors = ['Residential', 'Commercial', 'Industrial', 'Vehicle Fuel', 'Electric Power']
    consumption_values = [data_row[sector] for sector in sectors]

    # Define labels and colors for the pie chart
    labels = ['Residential', 'Commercial', 'Industrial', 'Vehicle Fuel', 'Electric Power']
    colors = ['skyblue', 'yellowgreen', 'coral', 'gold', 'lightpink']

    # Function to format pie chart percentages and adjust label positioning
    def autopct_format(pct):
        return f'{pct:.1f}%' if pct >= 5 else ''

    # Create the pie chart with improved label positioning
    plt.figure(figsize=(10, 8))
    wedges, texts, autotexts = plt.pie(consumption_values, labels=labels, colors=colors, 
                                       autopct=autopct_format, startangle=140, 
                                       textprops={'fontsize': 14}, pctdistance=0.85)

    # Adjust the position of labels to ensure they don't overlap
    for text, autotext in zip(texts, autotexts):
        if autotext.get_text() == '':
            text.set_visible(False)

    plt.title(f'Natural Gas Consumption by Sector in {location_name} ({year})', fontsize=16, pad=18)
    plt.tight_layout()
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.

    # Display the pie chart
    plt.show()

def make_pie_chart_of_electrical_data(state_data_for_one_year, location_name, year):
    data_row = state_data_for_one_year.iloc[0]

    # Prepare data for the pie chart, excluding the 'Date' column
    sectors = ['Residential', 'Commercial', 'Industrial', 'Vehicle Fuel', 'Other']
    consumption_values = [data_row[sector] for sector in sectors]

    # Define labels and colors for the pie chart
    labels = ['Residential', 'Commercial', 'Industrial', 'Vehicle Fuel', 'Other']
    colors = ['skyblue', 'yellowgreen', 'coral', 'gold', 'lightpink']

    # Function to format pie chart percentages and adjust label positioning
    def autopct_format(pct):
        return f'{pct:.1f}%' if pct >= 5 else ''

    # Create the pie chart with improved label positioning
    plt.figure(figsize=(10, 8))
    wedges, texts, autotexts = plt.pie(consumption_values, labels=labels, colors=colors, 
                                       autopct=autopct_format, startangle=140, 
                                       textprops={'fontsize': 14}, pctdistance=0.85)

    # Adjust the position of labels to ensure they don't overlap
    for text, autotext in zip(texts, autotexts):
        if autotext.get_text() == '':
            text.set_visible(False)

def make_pie_chart_of_electrical_source_data(state_data_for_one_year, location_name, year):
    data_row = state_data_for_one_year.iloc[0]

    # Prepare data for the pie chart, excluding the 'Date' column
    sources = ['Residential', 'Commercial', 'Industrial', 'Vehicle Fuel', 'Other']
    consumption_values = [data_row[source] for source in sources]

    # Define labels and colors for the pie chart
    labels = ['Residential', 'Commercial', 'Industrial', 'Vehicle Fuel', 'Other']
    colors = ['skyblue', 'yellowgreen', 'coral', 'gold', 'lightpink']

    # Function to format pie chart percentages and adjust label positioning
    def autopct_format(pct):
        return f'{pct:.1f}%' if pct >= 5 else ''

    # Create the pie chart with improved label positioning
    plt.figure(figsize=(10, 8))
    wedges, texts, autotexts = plt.pie(consumption_values, labels=labels, colors=colors, 
                                       autopct=autopct_format, startangle=140, 
                                       textprops={'fontsize': 14}, pctdistance=0.85)

    # Adjust the position of labels to ensure they don't overlap
    for text, autotext in zip(texts, autotexts):
        if autotext.get_text() == '':
            text.set_visible(False)

    plt.title(f'Electricity Consumption by Sector in {location_name} ({year})', fontsize=16, pad=18)
    plt.tight_layout()
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.

    # Display the pie chart
    plt.show()

def combine_state_ng_data(data_frames):
    # Combine all data frames by summing up their values
    combined_data = pd.concat(data_frames).groupby('Date').sum()
    # Reset the index so 'Date' becomes a column again, if you want to keep the 'Date' information
    combined_data.reset_index(inplace=True)
    return combined_data



def parse_electricity_data_by_sector(path_to_data, year_of_interest, location_string):
    # Load data
    data = pd.read_csv(path_to_data, skiprows=4)

    # Select only the relevant year column along with the description
    data = data[['description', str(year_of_interest)]]

    # Cleanup and prepare data
    data['Sector'] = data['description'].str.extract(r': (.*)')[0].fillna(data['description'])

    # Convert "--" to NaN to handle it easily later and fill with 0
    data[str(year_of_interest)] = pd.to_numeric(data[str(year_of_interest)], errors='coerce').fillna(0)

    # Map sector descriptions to standardized sector names
    rename_map = {
        'all sectors': 'Total Delivered',
        'residential': 'Residential',
        'commercial': 'Commercial',
        'industrial': 'Industrial',
        'transportation': 'Vehicle Fuel',
        'other': 'Other'
    }
    data['Sector'] = data['Sector'].apply(lambda x: rename_map.get(x.lower().strip(), x.strip()))

    # Filter only location specific data
    location_data = data[data['description'].str.contains(location_string)]

    # Pivot the data to have sectors as columns
    location_data_pivot = location_data.pivot_table(index='description', columns='Sector', values=str(year_of_interest), aggfunc='sum').fillna(0)

    # Reset index to drop the description from the index (removes 'description' from being part of the data)
    location_data_pivot = location_data_pivot.reset_index(drop=True)

    # Sum across the rows if needed (this ensures you get one row of summary data)
    location_final = location_data_pivot.sum(axis=0).to_frame().transpose()
    location_final.insert(0, 'Date', year_of_interest)

    return location_final

def parse_electricity_generation_data_carbon(path_to_data, year_of_interest, location_string):
    # Load data
    data = pd.read_csv(path_to_data, skiprows=4)

    # Select only the relevant year column along with the description
    data = data[['description', str(year_of_interest)]]

    # Cleanup and prepare data
    data['Source'] = data['description'].str.extract(r': (.*)')[0].fillna(data['description'])

    # Convert "--" to NaN to handle it easily later and fill with 0
    data[str(year_of_interest)] = pd.to_numeric(data[str(year_of_interest)], errors='coerce').fillna(0)

    # Map source descriptions to standardized source names
    rename_map = {
        'all fuels': 'Total Generated',
        'coal': 'Coal',
        'petroleum liquids': 'Petroluem',
        'petroleum coke': 'Petroleum Coke',
        'natural gas': 'Natural Gas',
        'other': 'Other gases'
    }
    data['Source'] = data['Source'].apply(lambda x: rename_map.get(x.lower().strip(), x.strip()))

    # Filter only location specific data
    location_data = data[data['description'].str.contains(location_string)]

    # Pivot the data to have sectors as columns
    location_data_pivot = location_data.pivot_table(index='description', columns='Source', values=str(year_of_interest), aggfunc='sum').fillna(0)

    # Reset index to drop the description from the index (removes 'description' from being part of the data)
    location_data_pivot = location_data_pivot.reset_index(drop=True)

    # Sum across the rows if needed (this ensures you get one row of summary data)
    location_final = location_data_pivot.sum(axis=0).to_frame().transpose()
    location_final.insert(0, 'Date', year_of_interest)

    return location_final

def calculate_renewable_vs_fossil(data):
    # Sum the fossil fuel sources to a new column 'Fossil Fuels'
    fossil_fuels_sources = ['Coal', 'Natural Gas', 'Petroleum Coke', 'Petroluem']
    data['Fossil Fuels'] = data[fossil_fuels_sources].sum(axis=1)

    # Subtract 'Fossil Fuels' from 'Total Generated' to get 'Renewable'
    if 'Total Generated' not in data.columns:
        # If "Total Generated" is under a different name such as "all fuels (utility-scale)"
        data['Total Generated'] = data['all fuels (utility-scale)']
    data['Renewable'] = data['Total Generated'] - data['Fossil Fuels']

    # Drop the individual fossil fuels columns if desired
    # data = data.drop(columns=fossil_fuels_sources)

    return data

Washington_NG_Data_Path = 'USEIA_Data/NG_CONS_SUM_DCU_SWA_A.csv'
Oregon_NG_Data_Path = 'USEIA_Data/NG_CONS_SUM_DCU_SOR_A.csv'
California_NG_Data_Path = 'USEIA_Data/NG_CONS_SUM_DCU_SCA_A.csv'
US_NG_Data_Path = 'USEIA_Data/NG_CONS_SUM_DCU_NUS_A.csv'
retail_sales_of_electricity_path = 'USEIA_Data/Retail_sales_of_electricity.csv'
net_generation_for_all_sectors_path = 'USEIA_Data/Net_generation_for_all_sectors.csv'

if __name__ == "__main__":

    year_of_interest = 2022

    read_in_ng_data = True
    read_in_electrival_usage = True
    read_in_electrical_generation = False

    if (read_in_ng_data):
        washington_data_2022 = parse_natural_gas_data_for_state_at_year(Washington_NG_Data_Path, year_of_interest) 
        oregon_data_2022 = parse_natural_gas_data_for_state_at_year(Oregon_NG_Data_Path, year_of_interest)
        california_data_2022 = parse_natural_gas_data_for_state_at_year(California_NG_Data_Path, year_of_interest)

        west_coast_data_2022 = combine_state_ng_data([washington_data_2022, oregon_data_2022, california_data_2022])

        make_pie_chart_of_natural_gas_data(washington_data_2022, "Washington", year_of_interest)
        # make_pie_chart_of_natural_gas_data(oregon_data_2022, "Oregon", year_of_interest)
        # make_pie_chart_of_natural_gas_data(california_data_2022, "California", year_of_interest)
        # make_pie_chart_of_natural_gas_data(west_coast_data_2022, 'the West Coast', year_of_interest)
        # us_data_2022 = parse_natural_gas_data_for_state_at_year(US_NG_Data_Path, year_of_interest)
        # make_pie_chart_of_natural_gas_data(us_data_2022, "The United States", year_of_interest)
    
    if (read_in_electrival_usage):
        washington_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, 'Washington')
        oregon_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, "Oregon")
        california_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, "California")
        west_coast_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, "Pacific Contiguous")
        united_states_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, "United States")

        make_pie_chart_of_electrical_data(washington_electricity_data, 'Washington', year_of_interest)

    if (read_in_electrical_generation):
        washington_electrical_generation_data = parse_electricity_generation_data_carbon(net_generation_for_all_sectors_path, year_of_interest, 'Washington')
        washington_electrical_generation_data = calculate_renewable_vs_fossil(washington_electrical_generation_data)

        print(washington_electrical_generation_data)

    
    
    


