class Sudoku:
    """
    A class used to solve sudoku puzzles. In these kinds of puzzles, 
    each row, column, and block (3x3 grid of cells) should have the 
    numbers 1-9 spread over exactly 9 cells. 

    Attributes
    ----------
    __rows: list[Sudoku.Vector]
    __columns: list[Sudoku.Vector]
    __blocks: list[Sudoku.Block]

    Methods
    -------
    __unpack_vectors(board: list[list[int]])
        Given a game board input, creates each Cell of the board and 
        returns a tuple containing a list of rows, a list of columns, 
        and a list of blocks. These are assigned to __rows, __columns,
        and __blocks in the constructor.
    get_rows()
        Returns __rows.
    get_columns()
        Returns __columns.
    is_completed()
        Returns a boolean to indicate whether the puzzle is finished 
        or not.
    assert_validity()
        Raises an InvalidGameSolution exception if each subsection of 
        a sudoku puzzle doesn't contain exactly the values 1-9.
    solve_block(block: Sudoku.Block)
        Attemps to find missing Cell values of a Block, given what 
        known values of said Cell's row and columns are.
    solve()
        Solves a sudoku puzzle.

    Inner classes
    -------------
    Subsection
    Block(Subsection)
    Vector(Subsection)
    Cell
    InvalidGameSolution(Exception) 

    """

    def __init__(self, board: list[list[int]]) -> None:
        """
        Takes the special input of a sudoku board's game data. This is 
        represented as a list of 9 rows containing 9 values. Each 
        value can be a number of 1-9 to represent a final value, or 0 
        to represent a missing one. No values can be duplicates.

        Example
        -------
        board = [
            [3, 1, 0, 6, 0, 5, 4, 0, 0], 
            [6, 0, 4, 2, 1, 0, 0, 8, 3], 
            [9, 0, 0, 0, 3, 0, 0, 2, 0], 
            [2, 4, 7, 5, 6, 0, 0, 3, 0], 
            [8, 6, 0, 1, 0, 0, 0, 0, 0], 
            [0, 0, 5, 3, 0, 2, 6, 7, 0], 
            [0, 8, 0, 0, 0, 0, 0, 0, 4], 
            [0, 3, 0, 0, 0, 0, 7, 6, 2], 
            [5, 0, 0, 0, 7, 0, 8, 0, 9]
            ]
        """
        # Assert that the board argument meets the criteria of a valid 
        # sudoku board.
        assert len(board) == 9
        for row in board:
            assert len(row) == 9

        rows, columns, blocks = Sudoku.__unpack_vectors(self, board)
        self.__rows: list[Sudoku.Vector] = rows
        self.__columns: list[Sudoku.Vector] = columns
        self.__blocks = blocks

    def __repr__(self) -> str:
        """Represent a Sudoku object as a 9x9 grid with cell values."""
        representation = " " * 6
        for column in range(9):
            representation += f"v{column + 1}  "
        representation += f"\n{" " * 6}{"_" * 35}\n"
        for row in self.__rows:
            representation += f"{str(row)}\n"
        return representation

    def __unpack_vectors(self, board: list[list[int]]) -> tuple[
        list[Sudoku.Vector], 
        list[Sudoku.Vector],
        list[Sudoku.Block]
        ]:
        rows: list[Sudoku.Vector] = []
        columns: list[Sudoku.Vector] = []
        blocks: list[Sudoku.Block] = []
        row_counter = 1
        column_counter = 1

        # Populate the lists of columns and blocks.
        for num in range(9):
            col_vector = Sudoku.Vector(orientation="column", id=(num + 1))
            columns.append(col_vector)
            new_block = Sudoku.Block(id=(num + 1))
            blocks.append(new_block)

        # Populate the list of rows.
        for row in board:
            row_vector = Sudoku.Vector(orientation="row", id=(row_counter))

            for num in row:
                row_id = row_vector.get_id()
                col_id = columns[column_counter-1].get_id()

                if row_id in (1,2,3) and col_id in (1,2,3):
                    cell_block_id = 1
                elif row_id in (1,2,3) and col_id in (4,5,6):
                    cell_block_id = 2
                elif row_id in (1,2,3) and col_id in (7,8,9):
                    cell_block_id = 3
                elif row_id in (4,5,6) and col_id in (1,2,3):
                    cell_block_id = 4
                elif row_id in (4,5,6) and col_id in (4,5,6):
                    cell_block_id = 5
                elif row_id in (4,5,6) and col_id in (7,8,9):
                    cell_block_id = 6
                elif row_id in (7,8,9) and col_id in (1,2,3):
                    cell_block_id = 7
                elif row_id in (7,8,9) and col_id in (4,5,6):
                    cell_block_id = 8
                elif row_id in (7,8,9) and col_id in (7,8,9):
                    cell_block_id = 9
                
                for block in blocks:
                    if block.get_id() == cell_block_id:
                        cell_block = block

                self.Cell(
                    row=row_vector,
                    col=columns[column_counter-1],
                    block=cell_block,
                    value=num
                    )

                column_counter += 1

            rows.append(row_vector)
            row_counter += 1
            column_counter = 1
        
        return rows, columns, blocks
        
    def get_rows(self) -> list[Sudoku.Vector]:
        return self.__rows
    
    def get_columns(self) -> list[Sudoku.Vector]:
        return self.__columns

    def is_completed(self) -> bool:
        for vectors in [self.__rows, self.__columns]:
            for vector in vectors:
                if len(vector.get_known_values()) != 9:
                    return False
        return True

    def assert_validity(self) -> None:
        subsections: list[list[Sudoku.Vector] | list[Sudoku.Block]] = [
            self.__rows, 
            self.__columns, 
            self.__blocks
            ]
        
        for areas in subsections:
            for area in areas:
                values = area.get_known_values()
                values.sort()

                if values != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    raise Sudoku.InvalidGameSolution(
                        "Error! This game was solved incorrectly."
                        )
            
    def solve_block(self, block: Sudoku.Block) -> None:
        unknown_values = block.get_unknown_values()
        # If the block has unknown/missing values, attempt to find the 
        # value of each empty cell.
        if len(unknown_values) != 0:
            for cell in block.get_cells():
                # If a cell's value is missing, remove overlaps 
                # between the block's missing numbers and the numbers 
                # already present in the cell's row and column. Then 
                # update the cell's possible values to reflect 
                # remaining possibilities.
                if cell.get_value() == 0:
                    possible_values = unknown_values.copy()
                    vectors = [cell.get_row(), cell.get_col()]

                    for vector in vectors:
                        for existing_value in vector.get_known_values():
                            if existing_value in possible_values:
                                possible_values.remove(existing_value)

                        # If there's only one possible value for this 
                        # cell, set its value to that, add it to its 
                        # block's known values, and run solve_block() 
                        # again. Otherwise, simply note its new 
                        # possible values.
                        if len(possible_values) == 1:
                            value = possible_values[0]
                            cell.set_value(value)
                            block.add_known_value(value)

                            for vector in vectors:
                                vector.add_known_value(value)

                            self.solve_block(block)
                        else:
                            cell.set_possible_values(possible_values)
    
    def solve(self) -> None:
        """Solves the Sudoku puzzle.

        While the Sudoku puzzle hasn't been completed yet, iterate 
        through each of its 9 blocks. If a block hasn't been solved,
        call the solve_block() function on it. Finally, assert that
        the puzzle solution is valid.
        """

        while not self.is_completed():
            for block in self.__blocks:
                unknown_values = block.get_unknown_values()

                if len(unknown_values) != 0:
                    self.solve_block(block)

        self.assert_validity()

    class Subsection:
        """
        A parent class that represents subsections of a sudoku puzzle, 
        each of which contain 9 cells. 

        Attributes
        ----------
        __id: int
        __cells: list[Sudoku.Cell]
        __unknown_values: list[int]
        __known_values: list[int]

        Methods
        -------
        get_id()
            Returns the subsection's id, which is between 1 and 9.
        add_cell(cell: Sudoku.Cell)
            Adds a Cell object to __cells. There ought to be 9 cells.
        get_unknown_values()
            Returns a list of ints, representing each value between 
            1-9 that has yet to be assigned to one of the subsection's 
            cells.
        get_known_values()
            Returns a list of ints, representing each value between 
            1-9 that has already been assigned to one of the 
            subsection's cells.
        add_known_value(value: int)
            Adds an int value to __known_values and removes it from
            __unknown_values.
        get_cells()
            Returns __cells.

        """

        def __init__(self, id: int) -> None:
            self.__id = id
            self.__cells: list[Sudoku.Cell] = []
            self.__known_values: list[int] = []
            self.__unknown_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        def get_id(self) -> int:
            return self.__id

        def add_cell(self, cell: Sudoku.Cell) -> None:
            self.__cells.append(cell)
            value = cell.get_value()
            if value != 0:
                self.__known_values.append(value)
                print(self.__unknown_values)
                self.__unknown_values.remove(value)

        def get_unknown_values(self) -> list[int]:
            return self.__unknown_values
        
        def get_known_values(self) -> list[int]:
            return self.__known_values
        
        def add_known_value(self, value: int) -> None:
            self.__known_values.append(value)
            self.__unknown_values.remove(value)

        def get_cells(self) -> list[Sudoku.Cell]:
            return self.__cells

    class Block(Subsection):
        """
        A child class extending Subsection. Each has 9 cells.
        """

        def __init__(self, id: int) -> None:
            super().__init__(id)

    class Vector(Subsection):
        """
        A child class extending Subsection. A vector can be either a 
        column or a row of a sudoku puzzle. Each has 9 cells.

        Attributes
        ----------
        __orientation: str
            Must only be "row" or "column".
        """

        def __init__(self, id: int, orientation: str) -> None:
            super().__init__(id)
            assert orientation == "row" or "column"
            self.__orientation = orientation

        def __repr__(self) -> str:
            if self.__orientation == "row":
                name = "h"
            else:
                name = "v"
            return f"{name}{self.get_id()}"

        def __str__(self) -> str:
            representation = f"{repr(self)}   |_"
            for cell in self.get_cells():
                value = cell.get_value()
                if value == 0:
                    value = "_"
                representation += str(value) + "_|_"
            return representation[0:-1]

    class Cell:
        """
        A class that represents indivdual cells in a sudoku puzzle.

        Attributes
        ----------
        __row: Sudoku.Vector
        __column: Sudoku.Vector
        __value: int
        __possible_values: list[int]|None

        Methods
        -------
        get_possible_values()
            Returns a list of ints of which one will be set to the 
            Cell's value later. 
        set_possible_values(values: list[int])
            Populates __possible_values.
        get_row()
            Returns the row Vector that contains the Cell.
        get_col()
            Returns the column Vector that contains the Cell.
        get_value()
            Returns the current value of the cell. A missing value is 
            represented by a 0.
        set_value(value: int)
            Sets __value to the deduced final value and sets 
            __possible_values to Nonel.
        """

        def __init__(
                self, 
                row: Sudoku.Vector, 
                col: Sudoku.Vector, 
                block: Sudoku.Block, 
                value: int = 0
                ) -> None:
            self.__row = row
            self.__column = col
            self.__value = value
            self.__possible_values = None
            block.add_cell(self)
            row.add_cell(self)
            col.add_cell(self)

        def get_possible_values(self) -> list[int]|None:
            return self.__possible_values

        def set_possible_values(self, values: list[int]) -> None:
            self.possible_values = values

        def get_row(self) -> Sudoku.Vector:
            return self.__row
    
        def get_col(self) -> Sudoku.Vector:
            return self.__column

        def get_value(self) -> int:
            return self.__value

        def set_value(self, value: int) -> None:
            self.__value = value
            self.__possible_values = None

    class InvalidGameSolution(Exception):
        """A simple custom Exception class."""
        pass