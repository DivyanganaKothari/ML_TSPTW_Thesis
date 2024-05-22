import pandas as pd


def create_instance(nrows, skiprows=0):
    # Read the Excel files
    filtered_entries = pd.read_excel("filtered_shipments_entries_with_mapped_ids.xlsx", nrows=nrows, skiprows=range(1, skiprows+1))

    final_distance_matrix_new = pd.read_excel("final_distance_matrix_new.xlsx", nrows=nrows, usecols=range(nrows + 1),
                                              index_col=0, skiprows=range(1, skiprows+1))
    # Get the unique 'MappedId' values and sort them
    unique_ids = sorted(filtered_entries['MappedId'].unique())

    # Create a mapping from the original IDs to sequential integers
    id_mapping = {id: i + 1 for i, id in enumerate(unique_ids)}

    # Apply the mapping to the 'MappedId' column
    filtered_entries['MappedId'] = filtered_entries['MappedId'].map(id_mapping)


    # Extract start and end times
    start_time_list = filtered_entries['Von1'].tolist()
    end_time_list = filtered_entries['Bis1'].tolist()
    start_time = {filtered_entries.loc[i, 'MappedId']: start_time for i, start_time in enumerate(start_time_list)}
    end_time = {filtered_entries.loc[i, 'MappedId']: end_time for i, end_time in enumerate(end_time_list)}

    # Convert the DataFrame to a nested dictionary
    nested_dict = final_distance_matrix_new.to_dict()

    # Convert to the expected format
    expected_dict = {}
    for i in nested_dict:
        for j in nested_dict[i]:
            expected_dict[(i, j)] = nested_dict[i][j]

    # Create a mapping from the original keys to sequential integers
    key_mapping = {key: i + 1 for i, key in enumerate(expected_dict.keys())}

    # Create a new dictionary with the updated keys using the mapping
    updated_dict = {}
    counter = 1
    for key, value in expected_dict.items():
        updated_dict[(
        counter // len(nested_dict) + 1 if counter % len(nested_dict) != 0 else counter // len(nested_dict),
        counter % len(nested_dict) if counter % len(nested_dict) != 0 else len(nested_dict))] = value
        counter += 1

    # Define instance data
    instance = {
        'distance_matrix': updated_dict,
        'earliest_times': start_time,
        'latest_times': end_time
    }

    return instance


instance_1 = create_instance(10)
instance_2 = create_instance(10, skiprows=10)
instance_3= create_instance(10, skiprows=20)
instance_4= create_instance(10, skiprows=30)
instance_5= create_instance(10, skiprows=40)
instance_6= create_instance(10, skiprows=50)
instance_7= create_instance(10, skiprows=60)
instance_8= create_instance(10, skiprows=70)
instance_9= create_instance(10, skiprows=80)
instance_10= create_instance(10, skiprows=90)

instances = [instance_1, instance_2, instance_3, instance_4, instance_5, instance_6, instance_7, instance_8, instance_9, instance_10]

# Create Excel file with multiple sheets
with pd.ExcelWriter('instances_1_with_10_nodes.xlsx') as writer:
    for i, instance in enumerate(instances):
        # Convert the dictionaries to DataFrames
        distance_matrix_df = pd.DataFrame.from_dict(instance['distance_matrix'], orient='index')
        earliest_times_df = pd.DataFrame(list(instance['earliest_times'].items()), columns=['MappedId', 'earliest_times'])
        latest_times_df = pd.DataFrame(list(instance['latest_times'].items()), columns=['MappedId', 'latest_times'])

        # Save the DataFrames to Excel
        distance_matrix_df.to_excel(writer, sheet_name=f'instance_{i+1}_distance_matrix')
        earliest_times_df.to_excel(writer, sheet_name=f'instance_{i+1}_earliest_times')
        latest_times_df.to_excel(writer, sheet_name=f'instance_{i+1}_latest_times')