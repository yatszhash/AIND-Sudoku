# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A:  
   At a given phase, if there are the boxes with the completely same possible values in a given unit, 
   and the number of these boxes equals to the number of their possible values,
   each value of the possible values must be in separate one of these box when a given sudoku
   is completely solved. 
   Therefore, each of the possible values can be removed from the other boxes in the same unit at the phase. 
   
   These reduction sometimes can enable us to reduce possible value in another units sharing same boxes in the same way.
   
# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: 
   In the diagonal sudoku, there are more units by two than the normal sudoku.
   
   If the box are in a diagonal line, 
   in addition to in the same row unit, column unit and square unit, 
   there are peers in the diagonal line. 
   
   In the eliminate strategy, the increased peers enable us to more certainly reduce possible values in a given box 
   because it's more possible a box has solved box in the same peers.
   
   In the one choice strategy and in the naked twins, 
   the increased units increase our chance to reduce the possible values.
   
   
### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.