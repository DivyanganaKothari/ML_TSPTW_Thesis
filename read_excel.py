import pandas as pd
import numpy as np

#entries_shipment = pd.read_excel("shipments_entries.xlsx")

#distance_matrix = pd.read_excel("distanceMatrix.xlsx",index_col=0)
"""

# Extract the unique nodes from shipment details
unique_address_ids = set(entries_shipment["AddressId"])

# print(unique_address_ids)
# Get the common address IDs between distance matrix and unique IDs
common_address_ids = list(set(distance_matrix.index) & unique_address_ids)

# Filter the entries to only include rows with AddressId in the common_address_ids
filtered_entries = entries_shipment[entries_shipment['AddressId'].isin(common_address_ids)]

# Create dictionaries for start time and end time
start_time_dict = dict(zip(filtered_entries['AddressId'], filtered_entries['Von1']))
end_time_dict = dict(zip(filtered_entries['AddressId'], filtered_entries['Bis1']))

# print(start_time_dict)
# print(end_time_dict)

print(len(common_address_ids))
# Create a new DataFrame with only the common address IDs as the columns and indices
new_distance_matrix = pd.DataFrame(np.nan, index=common_address_ids, columns=common_address_ids)


# Remove duplicates from the index and columns of the distance matrix
distance_matrix = distance_matrix.loc[~distance_matrix.index.duplicated(keep='first')]
distance_matrix = distance_matrix.loc[:, ~distance_matrix.columns.duplicated(keep='first')]


# Iterate over the common AddressIds, and for each AddressId, copy the corresponding row and column from the original
# distance matrix to the new DataFrame
for address_id in common_address_ids:
    new_distance_matrix.loc[address_id] = distance_matrix.loc[address_id, common_address_ids]
    new_distance_matrix.loc[:, address_id] = distance_matrix.loc[common_address_ids, address_id]


# Remove the rows and columns with all NaN values
new_distance_matrix.dropna(how='all', inplace=True)
new_distance_matrix.dropna(axis=1, how='all', inplace=True)


# Write the new distance matrix to a new Excel file
# new_distance_matrix.to_excel("new_distance_matrix.xlsx")


new_distance_matrix = pd.read_excel("new_distance_matrix.xlsx", index_col=0)
# Create a mapping from DataFrame's indices and columns to sequential integers
index_mapping = {value: i + 1 for i, value in enumerate(new_distance_matrix.index)}
column_mapping = {value: i + 1 for i, value in enumerate(new_distance_matrix.columns)}


# Replace the indices and columns of the DataFrame with the sequential integers
new_distance_matrix.index = [index_mapping[i] for i in new_distance_matrix.index]
new_distance_matrix.columns = [column_mapping[i] for i in new_distance_matrix.columns]

# Write the updated DataFrame to a new Excel file
# new_distance_matrix.to_excel("new_distance_matrix_with_sequential_integers.xlsx")
# Create a reverse mapping from sequential integers to original address IDs
reverse_index_mapping = {value: key for key, value in index_mapping.items()}

n = len(index_mapping)

# nrows=100, usecols= range(101)
# print("Index Mapping:", index_mapping)
# print("Column Mapping:", column_mapping)


new_distance_matrix_with_sequential_integers = pd.read_excel("new_distance_matrix_with_sequential_integers.xlsx", nrows=5, usecols= range(6),index_col=0)

# Convert the DataFrame to a nested dictionary
nested_dict = new_distance_matrix_with_sequential_integers.to_dict()

# Convert to the expected format
expected_dict = {}
for i in nested_dict:
    for j in nested_dict[i]:
        expected_dict[(i, j)] = nested_dict[i][j]

# Now expected_dict has the desired format
#print(expected_dict)



# mapping the address ids to sequential integers in the DataFrame

# Convert 'Von1' and 'Bis1' to strings in the format 'YYYY-MM-DD HH:MM:SS'
entries_shipment['Von1'] = entries_shipment['Von1'].dt.strftime('%Y-%m-%d %H:%M:%S')
entries_shipment['Bis1'] = entries_shipment['Bis1'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Assuming entries_shipment is the DataFrame and "AddressId" is the column with the address IDs
grouped = entries_shipment.groupby(["AddressId"])

# Create a mapping from grouped address IDs to sequential integers
address_id_mapping = {group: i for i, group in enumerate(grouped.groups.keys(), start=1)}


# Create a new column in the DataFrame with the mapped integers
entries_shipment["MappedId"] = entries_shipment["AddressId"].map(address_id_mapping)

# Sort the DataFrame by 'AddressId'
entries_shipment = entries_shipment.sort_values(by='AddressId')

# Select only the columns you need
selected_columns = entries_shipment[["MappedId","AddressId", "StopZeit", "Von1", "Bis1", "Von2", "Bis2", "Strasse", "Hausnr", "PLZ", "Ort", "Latitude", "Longitude"]]

# Write the selected columns to a new Excel file
selected_columns.to_excel("shipments_entries_with_mapped_ids.xlsx", index=False)
# Step 1: Read the new Excel file with the mapped IDs

entries_shipment = pd.read_excel("shipments_entries_with_mapped_ids.xlsx")
# Assuming common_address_ids is a list of address IDs that you want to keep
# Step 2: Filter the entries to only include rows with AddressId in the common_address_ids
filtered_entries = entries_shipment[entries_shipment['AddressId'].isin(common_address_ids)]
# Step 3: Convert timestamps to total seconds since the start of the day
filtered_entries['Von1'] = pd.to_datetime(filtered_entries['Von1'])
filtered_entries['Bis1'] = pd.to_datetime(filtered_entries['Bis1'])

filtered_entries['Von1'] = filtered_entries['Von1'].dt.hour * 3600 + filtered_entries['Von1'].dt.minute * 60 + filtered_entries['Von1'].dt.second

filtered_entries['Bis1'] = filtered_entries['Bis1'].dt.hour * 3600 + filtered_entries['Bis1'].dt.minute * 60 + filtered_entries['Bis1'].dt.second
# Remove duplicate rows based on 'MappedId'

filtered_entries = filtered_entries.drop_duplicates(subset='MappedId', keep='first')

filtered_entries.to_excel("filtered_shipments_entries_with_mapped_ids.xlsx", index=False)

"""
# Read the filtered shipments entries file
filtered_entries = pd.read_excel("filtered_shipments_entries_with_mapped_ids.xlsx", nrows=30)

# Create lists for start time and end time
start_time_list = filtered_entries['Von1'].tolist()
end_time_list = filtered_entries['Bis1'].tolist()

# Create dictionaries for start time and end time
e = {i+1: start_time for i, start_time in enumerate(start_time_list)}
l = {i+1: end_time for i, end_time in enumerate(end_time_list)}

#print(e)
#print(l)

n = filtered_entries['MappedId'].nunique()
#print(n)

"""
new_distance_matrix = pd.read_excel("new_distance_matrix.xlsx")


# Create a DataFrame with address IDs as the index and columns
df = pd.DataFrame(new_distance_matrix, index=new_distance_matrix.index, columns=new_distance_matrix.columns)
# Drop the 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])
# Convert the index and columns to integers
df.index = df.index.astype(int)
df.columns = df.columns.astype(int)
# Set the index to be the same as the columns
df.index = df.columns

# Sort the DataFrame rows and columns
df.sort_index(axis=0, inplace=True)

# Save the reordered distance matrix to an Excel file
df.to_excel("reordered_distance_matrix.xlsx")

df.sort_index(axis=1, inplace=True)
df.to_excel("reordered_distance_matrix_new.xlsx")
# Create a mapping from DataFrame's indices to sequential integers
index_mapping = {value: i + 1 for i, value in enumerate(df.index)}
column_mapping = {value: i + 1 for i, value in enumerate(df.columns)}
# Replace the indices of the DataFrame with the sequential integers
df.index = [index_mapping[i] for i in df.index]
df.columns = [column_mapping[i] for i in df.columns]

# Save the updated DataFrame to an Excel file
df.to_excel("final_distance_matrix_new.xlsx")

 """

final_distance_matrix_new=pd.read_excel("final_distance_matrix_new.xlsx",nrows=30, usecols=range(31),index_col=0)
# Convert the DataFrame to a nested dictionary
nested_dict = final_distance_matrix_new.to_dict()

# Convert to the expected format
expected_dict = {}
for i in nested_dict:
    for j in nested_dict[i]:
        expected_dict[(i, j)] = nested_dict[i][j]

# Now expected_dict has the desired format
#print(expected_dict)




"""
#method for code
def read_excel_data():
    # Your existing code to read the Excel file goes here
    filtered_entries = pd.read_excel("filtered_shipments_entries_with_mapped_ids.xlsx")
    final_distance_matrix_new = pd.read_excel("final_distance_matrix_new.xlsx", nrows=len(filtered_entries),
                                              usecols=range(len(filtered_entries) + 1), index_col=0)
    # Continue with your existing code
    return filtered_entries, final_distance_matrix_new


def process_data(filtered_entries, final_distance_matrix_new):
    # Your existing code to process the data goes here
    # Convert the DataFrame to a nested dictionary\

    # Create lists for start time and end time
    start_time_list = filtered_entries['Von1'].tolist()
    end_time_list = filtered_entries['Bis1'].tolist()

    # Create dictionaries for start time and end time
    e = {i + 1: start_time for i, start_time in enumerate(start_time_list)}
    l = {i + 1: end_time for i, end_time in enumerate(end_time_list)}

    nested_dict = final_distance_matrix_new.to_dict()
    # Convert to the expected format
    expected_dict = {}
    for i in nested_dict:
        for j in nested_dict[i]:
            expected_dict[(i, j)] = nested_dict[i][j]

    n = filtered_entries['MappedId'].nunique()

    # Now expected_dict has the desired format
    return expected_dict, e, l, n
"""