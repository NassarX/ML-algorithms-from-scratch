import csv
from math import sqrt


# load & read output file and convert it to python list
def load_csv(csv_file):
    dateset = []
    with open(csv_file, 'r') as file:
        # next(file)  # skip header
        reader = csv.reader(file)
        dateset = list(reader)

    return dateset


# Convert string column to float
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())


# calculate the Euclidean distance between two rows
def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)):
        distance += (row1[i] - row2[i]) ** 2
    return sqrt(distance)


# calculate the Euclidean distance between all rows vs all others
def distance_matrix(train_dateset):
    # initialize distance matrix. What will be its final shape?
    dist = []

    # Working with all rows vs all others
    for i in range(len(train_dateset)):
        row1 = train_dateset[i]
        dist_row = []
        for j in range(len(train_dateset)):
            row2 = train_dateset[j]
            euc = euclidean_distance(row1, row2)
            dist_row.append(euc)
        dist.append(dist_row)
    return dist


def closest_points(matrix):
    # get variables to save closest neighbors later
    min_args, min_dist = (None, 9e99)
    for id_r, row in enumerate(matrix):
        row_ = row.copy()[:id_r]
        dist = min(row_) if len(row_) > 0 else 9e99  # ensures we do not call the min() function on an empty list
        # check if the row's min distance is the lowest distance found so far
        if dist <= min_dist:
            # save points' ids and their distance
            min_dist = dist
            for id_diag, dist_val in enumerate(row_):
                if dist_val == dist:
                    min_args = (id_diag, id_r)
                    break
    return min_args, min_dist


filename = "file.csv"

# Load dataset csv file
dataset = load_csv(filename)

# Convert string column to float
for i in range(len(dataset[0])):
    str_column_to_float(dataset, i)

# Calculate the Euclidean distance between all rows
dist_matrix = distance_matrix(dataset)

n_distances = 10
distances = []
for _ in range(n_distances):
    c_points = closest_points(dist_matrix)
    distances.append(c_points)
    # Increasing shortest distance value to find the next shortest distance
    dist_matrix[c_points[0][1]][c_points[0][0]] = 9e99

for index, dist in distances:
    print(index, dist)
