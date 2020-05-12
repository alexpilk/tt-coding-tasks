# General

All programs were written using TDD. Please see commit history for details.

### Requirements

- Python 3.8
- pip-tools-5.1.2

### Installing requirements

`python3.8 -m pip install -r requirements.txt`

### Running tests

`python3.8 -m pytest <app_name>/tests`

# Solution explanations

## Boggle

First, all cells containing the first letter of the word are found.  
Then the algorithm recursively searches all neighbors of all cells for the next letter.  
Each path is explored either until a solution is found or next letter cannot be found. 

## Merging lists

Implemented solution selects pairs of lists and merges them until only one list remains.  
Two lists are merged by comparing their first elements and adding them into a new list until only one element remains in either list.

Two lists are merged in `O(n)`.
Every merge cycle reduces number of lists by two, which results in `O(log k)`.  
Overall time complexity is `O(n * log k)` where n is the number f elements and k is the number of lists.

## Sudoku solver

Implemented algorithm works on easy to medium level sudokus.

#### Neighbor search 
Fills in cells which have only one possible value based on values of vertical, horizontal and 33 section neighbors  

#### Option search
Checks all neighbors for possible solution and fills in given cell if one of it's possible solution is unique with regard to its neighbors.
For example, cell can be either 2 or 3, but on the horizontal line other cells can only be 1, 2 or 4. In this case current cell becomes 3.

### Algorithm
Neighbor search is run in a loop until it has no more cells to fill.  
Option search runs until it fills the first cell.  
This repeats until both searches stop solving cells.
