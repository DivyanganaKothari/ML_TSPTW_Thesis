import pandas as pd
import numpy as np

entries_shipment = pd.read_excel("shipments_entries.xlsx", nrows=100)

distance_matrix = pd.read_excel("distanceMatrix.xlsx", index_col=0)

# Save the address IDs from both sheets to two separate lists
address_ids_entries = entries_shipment["AddressId"].tolist()
address_ids_distance = distance_matrix.index.tolist()
print(address_ids_entries)
print(address_ids_distance)

# Find the common address IDs
common_address_ids = list(set(address_ids_entries) & set(address_ids_distance))

print(common_address_ids)



# print(unique_address_ids)



# Filter the entries to only include rows with AddressId in the common_address_ids
#filtered_entries = entries_shipment[entries_shipment['AddressId'].isin(common_address_ids)]



# Create dictionaries for start time and end time
#start_time_dict = dict(zip(filtered_entries['AddressId'], filtered_entries['Von1']))
#end_time_dict = dict(zip(filtered_entries['AddressId'], filtered_entries['Bis1']))

#print(start_time_dict)
#print(end_time_dict)

e={}
l={}

# Convert timestamps to total seconds since the start of the day
#for key in start_time_dict:
#    e[key] = (start_time_dict[key] - pd.Timestamp(start_time_dict[key].date())).total_seconds()
#    l[key] = (end_time_dict[key] - pd.Timestamp(end_time_dict[key].date())).total_seconds()

#print(e)
#print(l)
"""

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

"""
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




# Create new dictionaries for start time and end time with sequential integers as keys
#e_seq = {i: e.get(reverse_index_mapping[i], None) for i in range(1, n + 1)}
#l_seq = {i: l.get(reverse_index_mapping[i], None) for i in range(1, n + 1)}

# For e_seq
#e_seq_values_not_none = [value for value in e_seq.values() if value is not None]

# For l_seq
#l_seq_values_not_none = [value for value in l_seq.values() if value is not None]

#print(e_seq_values_not_none)
#print(l_seq_values_not_none)

new_distance_matrix_with_sequential_integers = pd.read_excel("new_distance_matrix_with_sequential_integers.xlsx", index_col=0)
# print("Index Mapping:", index_mapping)
# print("Column Mapping:", column_mapping)


# Convert the DataFrame to a nested dictionary
nested_dict = new_distance_matrix_with_sequential_integers.to_dict()

# Convert to the expected format
expected_dict = {}
for i in nested_dict:
    for j in nested_dict[i]:
        expected_dict[(i, j)] = nested_dict[i][j]

# Now expected_dict has the desired format
#print(expected_dict)

# n = len(new_distance_matrix_with_sequential_integers)  # Assuming index_mapping contains the mapping of original IDs to sequential integers



