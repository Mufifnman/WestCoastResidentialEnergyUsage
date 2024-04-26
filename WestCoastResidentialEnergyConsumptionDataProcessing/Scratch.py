# Load data
# Define paths as strings
net_generation_for_all_sectors_path = 'USEIA_Data/Net_generation_for_all_sectors.csv'
ng_cons_sum_dcu_nus_a_path = 'USEIA_Data/NG_CONS_SUM_DCU_NUS_A.csv'
ng_cons_sum_dcu_sca_a_path = 'USEIA_Data/NG_CONS_SUM_DCU_SCA_A.csv'
ng_cons_sum_dcu_sor_a_path = 'USEIA_Data/NG_CONS_SUM_DCU_SOR_A.csv'
washington_ng_data_path = 'USEIA_Data/NG_CONS_SUM_DCU_SWA_A.csv'
retail_sales_of_electricity_path = 'USEIA_Data/Retail_sales_of_electricity.csv'

# Read CSV files using the defined paths
# Net_generation_for_all_sectors = pd.read_csv(net_generation_for_all_sectors_path)
# NG_CONS_SUM_DCU_NUS_A = pd.read_csv(ng_cons_sum_dcu_nus_a_path)
# NG_CONS_SUM_DCU_SCA_A = pd.read_csv(ng_cons_sum_dcu_sca_a_path)
# NG_CONS_SUM_DCU_SOR_A = pd.read_csv(ng_cons_sum_dcu_sor_a_path)
# NG_CONS_SUM_DCU_SWA_A = pd.read_csv(washington_ng_data_path)
# Retail_sales_of_electricity = pd.read_csv(retail_sales_of_electricity_path)

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


    if (read_in_electrival_usage):
        washington_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, 'Washington')
        oregon_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, "Oregon")
        california_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, "California")
        west_coast_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, "Pacific Contiguous")
        united_states_electricity_data = parse_electricity_data_by_sector(retail_sales_of_electricity_path, year_of_interest, "United States")
        print(west_coast_electricity_data)

        parse_natural_gas_data_for_state_at_year()