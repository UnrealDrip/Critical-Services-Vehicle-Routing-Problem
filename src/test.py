# The selected_chromosome list
selected_chromosome = [8, 0, 2, 6, 4, 1, 9, 5, 7, 3]
selected_chromosome_copy = [8, 0, 2, 6, 4, 1, 9, 5, 7, 3]
vehicle_route = []

# Extract the first two even numbers and their following odd number indices
for i in range(2):
    even_numbers_indices = []
    odd_following_indices = []
    even_count = 0
    for i, num in enumerate(selected_chromosome):
        if num % 2 == 0 and even_count < 1:
            even_numbers_indices.append(num)
            vehicle_route.append(num)
            even_count += 1
            odd_following_indices.append(num+1)
            vehicle_route.append(num+1)
        elif even_count == 1:
            break
    # Remove the used numbers from the list
    indices_to_delete = even_numbers_indices + odd_following_indices
    indices_to_delete.sort(reverse=True)
    for i in indices_to_delete:
        del selected_chromosome[selected_chromosome.index(i)]

# Create a dictionary with the values in the selected_chromosome list as keys
# and their indices as values
indices = {num: i for i, num in enumerate(selected_chromosome_copy)}

# Sort the numbers to arrange list by their corresponding indices in the
# selected_chromosome list using the indices dictionary
sorted_numbers = sorted(vehicle_route, key=lambda num: indices[num])

# Print the updated list index = selected_list.index(value)
print(sorted_numbers)


