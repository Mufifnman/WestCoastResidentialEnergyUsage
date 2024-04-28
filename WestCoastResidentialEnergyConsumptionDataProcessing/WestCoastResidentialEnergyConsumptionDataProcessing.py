import pandas as pd
import matplotlib.pyplot as plt
import os
from enum import Enum

class Region(Enum):
    WASHINGTON = "Washington"
    OREGON = "Oregon"
    CALIFORNIA = "California"
    WEST_COAST = "West Coast"
    UNITED_STATES = "United States"

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


def make_pie_chart_of_natural_gas_data(state_data_for_one_year, location_name, year, save_folder, show = False):
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

    title = f'Natural Gas Consumption by Sector in {location_name} ({year})'
    plt.title(title, fontsize=16, pad=18)
    plt.tight_layout()
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
    filepath = save_folder + title
    plt.savefig(filepath, transparent=True)

    # Display the pie chart
    if show:
        plt.show()

def make_pie_chart_of_electrical_data(state_data_for_one_year, location_name, year, save_folder, show = False):
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

    title = f'Electricity Consumption by Sector in {location_name} ({year})'
    plt.title(title, fontsize=16, pad=18)
    plt.tight_layout()
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
    filepath = save_folder + title
    plt.savefig(filepath, transparent=True)

    # Display the pie chart
    if show:
        plt.show()

def make_pie_chart_of_combined_data(state_data_for_one_year, location_name, year, save_folder, combined = True, show = False):
    data_row = state_data_for_one_year.iloc[0]

    # Prepare data for the pie chart, excluding the 'Date' column
    sectors = ['Residential', 'Commercial', 'Industrial', 'Vehicle Fuel', 'Other']

    # Define labels and colors for the pie chart
    labels = ['Residential', 'Commercial', 'Industrial', 'Vehicle Fuel', 'Other']
    base_colors = {
        'Residential': 'skyblue',
        'Commercial': 'yellowgreen',
        'Industrial': 'coral',
        'Vehicle Fuel': 'gold',
        'Other': 'lightpink'
    }
    darker_colors = {
        'Residential Electricity': '#5d99d6',  # Slightly darker than skyblue
        'Commercial Electricity': '#80c000',   # Slightly darker than yellowgreen
        'Industrial Electricity': '#e6735c',   # Slightly darker than coral
        'Vehicle Fuel Electricity': '#e6b800', # Slightly darker than gold
        'Other Electricity': '#ff85b3',        # Slightly darker than lightpink
    }

    if(not combined):
        electricity_sectors = ['Residential Electricity', 'Commercial Electricity', 'Industrial Electricity', 'Vehicle Fuel Electricity', 'Other Electricity']
        interleaved_sectors = [val for pair in zip(sectors, electricity_sectors) for val in pair]
        sectors = interleaved_sectors
        interleaved_labels = [val for pair in zip(labels, electricity_sectors) for val in pair]
        labels = interleaved_labels
    
    colors = [base_colors.get(sector, darker_colors.get(sector, 'grey')) for sector in sectors]
    consumption_values = [data_row[sector] for sector in sectors]

    # Function to format pie chart percentages and adjust label positioning
    def autopct_format(pct):
        return f'{pct:.1f}%' if pct >= 5 else ''


    # Create the pie chart with improved label positioning
    plt.figure(figsize=(12, 8))
    wedges, texts, autotexts = plt.pie(consumption_values, labels=labels, colors=colors,
                                        autopct=autopct_format, startangle=140,
                                        textprops={'fontsize': 14}, pctdistance=0.85)

    # Adjust the position of labels to ensure they don't overlap
    for text, autotext in zip(texts, autotexts):
        if autotext.get_text() == '':
            text.set_visible(False)

    title = f'Natural gas use by Sector in {location_name} ({year})'
    plt.title(title, fontsize=16, pad=18)
    plt.tight_layout()
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
    filepath = save_folder + title
    if combined: 
        filepath += ' combined'
    plt.savefig(filepath, transparent=True)

    # Display the pie chart
    if show:
        plt.show()

def make_pie_chart_of_electrical_source_data(state_data_for_one_year, location_name, year, save_folder, show = False):
    data_row = state_data_for_one_year.iloc[0]

    # Prepare data for the pie chart, excluding the 'Date' column
    sources = ['Fossil Fuels', 'Renewable']
    consumption_values = [data_row[source] for source in sources]

    # Define labels and colors for the pie chart
    labels = ['Fossil Fuels', 'Renewable']
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

    title = f'Electricity Production by Carbon Footprint in {location_name} ({year})'
    plt.title(title, fontsize=16, pad=18)
    plt.tight_layout()
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
    filepath = save_folder + title
    plt.savefig(filepath, transparent=True)

    # Display the pie chart
    if show:
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


def allocate_ng_to_electricity_sectors(ng_data, electricity_data, combine):
    sectors = ['Residential', 'Commercial', 'Industrial', 'Vehicle Fuel', 'Other']
    # Find the proportion of natural gas used for electric power
    ng_for_electric_power = ng_data['Electric Power'].iloc[0]
    total_electricity_usage = electricity_data.drop(columns=['Date', 'Total Delivered']).sum(axis=1).iloc[0]

    # Calculate the percentage of each sector's usage out of the total usage
    sector_percentages = electricity_data.drop(columns=['Date', 'Total Delivered']).div(total_electricity_usage)

    # Allocate natural gas usage to each electricity sector based on the percentage
    ng_allocation = sector_percentages.apply(lambda x: x * ng_for_electric_power)

    # You can either add this directly to the electricity_data or create a new DataFrame
    # Here we will add it directly to the electricity_data DataFrame
    if (combine):
        for sector in ng_allocation.columns:
            if sector not in ng_data.columns:
                ng_data[sector] = 0
            ng_data[sector] = ng_data[sector] +  ng_allocation[sector].values
    else:
        print ("combine!")
        for sector in ng_allocation.columns:
            if sector not in ng_data.columns:
                ng_data[sector] = 0
            ng_data[sector + " Electricity"] = ng_allocation[sector].values

    return ng_data

def residential_energy_use_over_time(start_year, end_year, region : Region, save_folder = '../', show_all = False):
    all_years_data = []
    
    for year in range(start_year, end_year + 1):
        if (region is Region.WEST_COAST):
            w_ng_d = parse_natural_gas_data_for_state_at_year(ng_data_path_dict[Region.WASHINGTON], year) 
            o_ng_d = parse_natural_gas_data_for_state_at_year(ng_data_path_dict[Region.OREGON], year) 
            c_ng_d = parse_natural_gas_data_for_state_at_year(ng_data_path_dict[Region.CALIFORNIA], year) 
            ng_usage_raw_data = combine_state_ng_data([w_ng_d, o_ng_d, c_ng_d])
        else:
            ng_usage_raw_data = parse_natural_gas_data_for_state_at_year(ng_data_path_dict[region], year)
        
        electricity_usage_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year, electricity_data_region_string[region])

        combined_ng_usage_data = allocate_ng_to_electricity_sectors(ng_usage_raw_data, electricity_usage_data, True)\
        
        
        # Extract only the residential data for the year
        residential_value = combined_ng_usage_data.loc[combined_ng_usage_data['Date'] == year, 'Residential'].iloc[0]
        if (show_all) :
            commercial_value = combined_ng_usage_data.loc[combined_ng_usage_data['Date'] == year, 'Commercial'].iloc[0]
            Industrial_value = combined_ng_usage_data.loc[combined_ng_usage_data['Date'] == year, 'Industrial'].iloc[0]
            vehicle_value = combined_ng_usage_data.loc[combined_ng_usage_data['Date'] == year, 'Vehicle Fuel'].iloc[0]
            other_value = combined_ng_usage_data.loc[combined_ng_usage_data['Date'] == year, 'Other'].iloc[0]
        # sectors = ['Commercial', 'Industrial', 'Vehicle Fuel', 'Other']
        # total_value = residential_value
        # for sector in sectors:
        #     total_value = total_value + combined_ng_usage_data.loc[combined_ng_usage_data['Date'] == year, sector].iloc[0]
        # residential_percentage = residential_value / total_value
        
        if (show_all) :
            all_years_data.append({'Year': year, 'Residential': residential_value, 'Commercial' : commercial_value, 'Industrial' : Industrial_value,'Vehicle Fuel' : vehicle_value, 'Other' : other_value})
        else:
            all_years_data.append({'Year': year, 'Residential': residential_value})

    # Convert the list of dictionaries to a DataFrame
    all_years_df = pd.DataFrame(all_years_data)
    all_years_df.set_index('Year', inplace=True)  # Set 'Year' as the index

    # Plotting
    plt.figure(figsize=(10, 5))
    if show_all:
        # Define a color map for the sectors
        color_map = {
            'Residential': 'blue',
            'Commercial': 'green',
            'Industrial': 'red',
            'Vehicle Fuel': 'purple',
            'Other': 'orange'
        }
        for sector, color in color_map.items():
            all_years_df[sector].plot(kind='line', marker='o', color=color, label=sector)

    else:
        all_years_df['Residential'].plot(kind='line', marker='o', color='blue', label='Residential')
    title = f'Residential Natural Gas Use Over Time in {print_region_string[region]}'  # Assuming Region is an enum with readable names
    plt.title(title)
    plt.xlabel('Year')
    years = range(start_year, end_year + 1, 2)
    plt.xticks(years)
    plt.ylabel('(MMcf)')
    plt.grid(True)
    # plt.show()
    
    filepath = save_folder + title
    plt.savefig(filepath, transparent=True)

    return all_years_df
    

Washington_NG_Data_Path = 'USEIA_Data/NG_CONS_SUM_DCU_SWA_A.csv'
Oregon_NG_Data_Path = 'USEIA_Data/NG_CONS_SUM_DCU_SOR_A.csv'
California_NG_Data_Path = 'USEIA_Data/NG_CONS_SUM_DCU_SCA_A.csv'
US_NG_Data_Path = 'USEIA_Data/NG_CONS_SUM_DCU_NUS_A.csv'
retail_sales_of_electricity_path = 'USEIA_Data/Retail_sales_of_electricity.csv'
net_generation_for_all_sectors_path = 'USEIA_Data/Net_generation_for_all_sectors.csv'

ng_data_path_dict = {
    Region.WASHINGTON: 'USEIA_Data/NG_CONS_SUM_DCU_SWA_A.csv',
    Region.OREGON: 'USEIA_Data/NG_CONS_SUM_DCU_SOR_A.csv',
    Region.CALIFORNIA: 'USEIA_Data/NG_CONS_SUM_DCU_SCA_A.csv',
    Region.UNITED_STATES: 'USEIA_Data/NG_CONS_SUM_DCU_NUS_A.csv'
}
electricity_data_region_string = {
    Region.WASHINGTON: "Washington",
    Region.OREGON: "Oregon",
    Region.CALIFORNIA: "California",
    Region.WEST_COAST: "Pacific Contiguous",
    Region.UNITED_STATES: "United States"
}
print_region_string = {
    Region.WASHINGTON: "Washington",
    Region.OREGON: "Oregon",
    Region.CALIFORNIA: "California",
    Region.WEST_COAST: "The West Coast",
    Region.UNITED_STATES: "The United States"
}

if __name__ == "__main__":

    year_of_interest = 2016

    read_in_ng_data = False
    read_in_electrival_usage = False
    read_in_electrical_generation = False
    plot_data_over_years = True

    show = False

    save_folder = f'../{year_of_interest}/'

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    if (read_in_ng_data):
        washington_data_2022 = parse_natural_gas_data_for_state_at_year(Washington_NG_Data_Path, year_of_interest) 
        oregon_data_2022 = parse_natural_gas_data_for_state_at_year(Oregon_NG_Data_Path, year_of_interest)
        california_data_2022 = parse_natural_gas_data_for_state_at_year(California_NG_Data_Path, year_of_interest)
        west_coast_data_2022 = combine_state_ng_data([washington_data_2022, oregon_data_2022, california_data_2022])
        us_data_2022 = parse_natural_gas_data_for_state_at_year(US_NG_Data_Path, year_of_interest)

        make_pie_chart_of_natural_gas_data(washington_data_2022, "Washington", year_of_interest, save_folder)
        make_pie_chart_of_natural_gas_data(oregon_data_2022, "Oregon", year_of_interest, save_folder)
        make_pie_chart_of_natural_gas_data(california_data_2022, "California", year_of_interest, save_folder)
        make_pie_chart_of_natural_gas_data(west_coast_data_2022, 'the West Coast', year_of_interest, save_folder)
        make_pie_chart_of_natural_gas_data(us_data_2022, "The United States", year_of_interest, save_folder)
    
    if (read_in_electrival_usage):
        washington_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, 'Washington')
        oregon_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, "Oregon")
        california_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, "California")
        west_coast_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, "Pacific Contiguous")
        united_states_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, "United States")

        make_pie_chart_of_electrical_data(washington_electricity_data, 'Washington', year_of_interest, save_folder)
        make_pie_chart_of_electrical_data(oregon_electricity_data, "Oregon", year_of_interest, save_folder)
        make_pie_chart_of_electrical_data(california_electricity_data, "California", year_of_interest, save_folder)
        make_pie_chart_of_electrical_data(west_coast_electricity_data, 'the West Coast', year_of_interest, save_folder)
        make_pie_chart_of_electrical_data(united_states_electricity_data, "The United States", year_of_interest, save_folder)

    if (read_in_electrical_generation):
        washington_electrical_generation_data = parse_electricity_generation_data_carbon(net_generation_for_all_sectors_path, year_of_interest, 'Washington')
        washington_electrical_generation_data = calculate_renewable_vs_fossil(washington_electrical_generation_data)
        make_pie_chart_of_electrical_source_data(washington_electrical_generation_data, "Washington", year_of_interest)

    if (read_in_ng_data and read_in_electrival_usage):
        combine = True

        combined_data_washington = allocate_ng_to_electricity_sectors(washington_data_2022, washington_electricity_data, combine)
        combined_data_oregon = allocate_ng_to_electricity_sectors(oregon_data_2022, oregon_electricity_data, combine)
        combined_data_california = allocate_ng_to_electricity_sectors(california_data_2022, california_electricity_data, combine)
        combined_data_west_coast = allocate_ng_to_electricity_sectors(west_coast_data_2022, west_coast_electricity_data, combine)
        combined_data_us = allocate_ng_to_electricity_sectors(us_data_2022, united_states_electricity_data, combine)

        make_pie_chart_of_combined_data(combined_data_washington, "Washington", year_of_interest, save_folder, combine)
        make_pie_chart_of_combined_data(combined_data_oregon, "Oregon", year_of_interest, save_folder, combine)
        make_pie_chart_of_combined_data(combined_data_california, "California", year_of_interest, save_folder, combine)
        make_pie_chart_of_combined_data(combined_data_west_coast, "the West Coast", year_of_interest, save_folder, combine)
        make_pie_chart_of_combined_data(combined_data_us, "The United States", year_of_interest, save_folder, combine)

    if (plot_data_over_years):
        residential_energy_use_over_time(2002, 2023, Region.WASHINGTON)
        residential_energy_use_over_time(2002, 2023, Region.OREGON)
        residential_energy_use_over_time(2002, 2023, Region.CALIFORNIA)
        residential_energy_use_over_time(2002, 2023, Region.WEST_COAST)
        residential_energy_use_over_time(2002, 2023, Region.UNITED_STATES)
        
        
    

    
    


