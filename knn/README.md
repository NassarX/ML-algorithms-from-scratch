# Implement k-Nearest Neighbors in Python

## k-Nearest Neighbors

**K-nearest neighbors (kNN) is a supervised machine learning algorithm that can be used to solve both classification and regression tasks.** 

> The value of a data point is determined by the data points around it.
> 
> - If you have one very close friend and spend most of your time with him/her, you will end up sharing similar interests and enjoying same things. That is kNN with k=1.
> - If you always hang out with a group of *5,* each one in the group has an effect on your behavior and you will end up being the average of 5. That is kNN with *k=5*.

## k-Nearest Neighbors (in 3 easy steps)

Let’s break down k-Nearest Neighbors algorithm into 3 parts:

- **Step 1**: Calculate Euclidean Distance.
- **Step 2**: Get Nearest Neighbors.
- **Step 3**: Make Predictions.

### Step 1: Calculate Euclidean Distance

The first step is to calculate the distance between two rows in a dataset.

- Euclidean Distance = sqrt(sum i to N (x1_i – x2_i)^2)

With Euclidean distance, the smaller the value, the more similar two records will be. A value of 0 means that there is no difference between two records.

A *euclidean_distance()* function implementation :

```python
# calculate the Euclidean distance between two rows
def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)):
        distance += (row1[i] - row2[i])**2
    return sqrt(distance)
```

To locate the neighbors for a new piece of data within a dataset we must first calculate the distance between each record in the dataset to the new piece of data. 

So we’re going to use the distance_matrix*()* function below to calculate the distance between each *row* vs all others.

```python
# calculate the Euclidean distance between all rows vs all others
def distance_matrix(dataset) :
    # initialize distance matrix. What will be its final shape?
    dist = []

    # Working with all rows vs all others
    for i in range(len(dataset)):
        row1 = dataset[i]
        dist_row = []
        for j in range(len(dataset)):
            row2 = dataset[j]
            euc = euclidean_distance(row1, row2)
            dist_row.append(euc)
        dist.append(dist_row)
    return dist
```

### Step 2: Get Nearest Neighbors

Once distances are calculated, Let's find the  minimum distance and the corresponding observations :

We can do this by keeping track of the distance for each record in the dataset as a tuple, sort the list of tuples by the distance (in descending order) and then retrieve the neighbors.

Below is a function named *get_neighbors()* that implements this.

```python
def closest_points(dist_matrix):
    # get variables to save closest neighbors later
    min_args, min_dist = (None, 9e99)
    for id_r, row in enumerate(dist_matrix):
        row_ = row.copy()[:id_r]
        dist = min(row_) if len(row_)>0 else 9e99 # ensures we do not call the min() function on an empty list
        # check if the row's min distance is the lowest distance found so far
        if dist<=min_dist:
            # save points' ids and their distance
            min_dist = dist 
            for id_diag, dist_val in enumerate(row_):
                if dist_val==dist:
                    min_args = (id_diag, id_r)
                    break
    return min_args, min_dist
```

Let’s explain code above :

- First *initialize* min_args,  **min_dist *variables outside the loop so their scope is defined globally and we can update and track their values at each iteration.*
- E*numerate used so we not only iterate along the rows of dist but also to keep track of the row index we are at: id_r*
- Then we *define row_ as a copy of row that only holds a slice of the values corresponding to the distances in the lower diagonal of the matrix (i.e. excludes value in row corresponding to diagonal and upper triangle as it holds redundant information).*
    
    <aside>
    💡 Since the distance matrix is a symmetric and 0-diagonal matrix (distance of the observation with itself is 0) we should only perform the search over either the upper or lower triangle of the matrix.
    
    </aside>
    
- I*terate along the current row distances t*o *find the column index responsible for the current minimum  distance . We can make use of list.index(x) method to*eturn zero-based index in the list of the first item whose value is equal to *x*. **
    
    ```python
    row_.index(min(min_dist))
    ```
    

### Step 3: Finding the n shortest distance

Finally as we manage to find the most similar (shortest distance) neighbors in the dataset, 

Let’s find next n (given) shortest distances :

```python
dist_matrix = distance_matrix(data)
n_distances = 10

distances = []
for _ in range(n_distances):
    c_points = closest_points(dist_matrix)
    distances.append(c_points)
    dist_matrix[c_points[0][1]][c_points[0][0]] = 9e99  # Increasing shortest distance value to find the next shortest distance
```