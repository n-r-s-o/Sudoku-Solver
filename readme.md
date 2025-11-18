# Sudoku Solver

This project is a wip. The plan is to make a program that takes an input representation of a sudoku puzzle, as a list of lists of strings, and then solves the puzzle efficiently. My approach is to firstly invent my own algorithm to solve the problem, and then look up well-established methods online, so that I can do a side-by-side comparison and gain new insights into how I can better approach similar problems in the future.

## Project plan

### Steps completed

1. Preparation: Analyze requirements. Work out preliminary sudoku puzzle solving logic. Make a plan for which classes and data collections to inlcude to efficiently run the solving algorithm.

2. Create rough drafts of the Sudoku module's classes, including data collections.

### Steps to do

3. Add data structures for missing numbers by row, column, and blocks (9 x 9 cells).

4. Introduce `solve()` and `check_validity()` methods.

5. Refine and test.

6. Introduce more types of accepted inputs, e.g. by image. Create a method for checking if a sudoku puzzle is able to be solved, or if it has multiple solutions.

7. Research other, more well-establish sudoku algorithms online. Compare these to my solution and analyze its potential shortcomings. 