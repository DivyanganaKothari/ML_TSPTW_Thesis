import pandas as pd

# Convert the DataFrame to a nested list

filtered_entries = pd.read_excel("filtered_shipments_entries_with_mapped_ids.xlsx")

final_distance_matrix_new = pd.read_excel("final_distance_matrix_new.xlsx", index_col=0)
"""
distance_matrix = final_distance_matrix_new.values.tolist()


    # Extract start and end times
start_times = filtered_entries['Von1'].tolist()
end_times = filtered_entries['Bis1'].tolist()

    # Combine start and end times to create time windows
time_windows = list(zip(start_times, end_times))
print(time_windows)
print(distance_matrix)
"""
#filter entry based on zip codes and extract the time windows

# Assuming 'PLZ' is the column with zipcodes and 'address_id' is the column with address ids
zipcodes = [2345, 2340, 2336, 2350, 2360, 2364, 2714, 2718]

# Filter the entries for the given zipcode
filtered_by_zipcodes = filtered_entries[filtered_entries['PLZ'].isin(zipcodes)]

start_times = filtered_by_zipcodes['Von1'].tolist()
end_times = filtered_by_zipcodes['Bis1'].tolist()

# Combine start and end times to create time windows
time_windows = list(zip(start_times, end_times))

# Extract longitude and latitude for the filtered entries
longitude = filtered_by_zipcodes['Longitude'].tolist()
latitude = filtered_by_zipcodes['Latitude'].tolist()

# Combine longitude and latitude to create coordinates
coordinates = list(zip(latitude, longitude))

print(coordinates)

# Extract MappedId for the filtered entries
mapped_ids = filtered_by_zipcodes['MappedId'].tolist()

# Filter the rows and columns of the original distance matrix
new_distance_matrix = final_distance_matrix_new.loc[mapped_ids, mapped_ids]
# Convert the new DataFrame to a nested list
new_distance_matrix_list = new_distance_matrix.values.tolist()

print(new_distance_matrix_list)
#print(mapped_ids)
print(len(mapped_ids))
print(time_windows)
