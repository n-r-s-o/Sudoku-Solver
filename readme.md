# Sudoku Solver

This project is a wip. The plan is to make a program that takes an input representation of a Sudoku puzzle, as a list of lists of ints (0 represents missing values), and then solves the puzzle efficiently. My approach is to firstly invent my own algorithm to solve the problem, and then to look up well-established methods online, so that I can do a side-by-side comparison and gain new insights into how I can better approach similar problems in the future.

## Project plan

### Completed steps

1. Preparation: Analyze requirements. Work out preliminary Sudoku puzzle solving logic. Make a plan for which classes and data collections to inlcude to efficiently run the solving algorithm.

2. Create rough drafts of the Sudoku module's classes, including data collections.

3. Add data structures for missing numbers by row, column, and blocks (9 x 9 cells).

4. Introduce `solve()` and `assert_validity()` methods.

5. Refine and test. Flesh out and improve upon the documentation.

6. Research other, more well-established Sudoku algorithms online. Compare these to my solution and analyze its potential shortcomings. 

### Potential future steps

7. Introduce more types of accepted inputs, e.g. by image. Create a method for checking if a Sudoku puzzle is able to be solved, or if it has multiple solutions.
