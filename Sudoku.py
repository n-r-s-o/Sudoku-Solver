class Sudoku:
    """
    A class used to solve Sudoku puzzles. In these kinds of puzzles, 
    each row, column, and block (3x3 grid of cells) should have the 
    numbers 1-9 spread over exactly 9 cells, without duplicate values.

    Attributes
    ----------
    __rows: list[Sudoku.Vector]
    __columns: list[Sudoku.Vector]
    __cells: list[Sudoku.Cell]
    __blocks: list[Sudoku.Block]
    __initial_state: str

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
    get_cells()
        Returns __cells.
    get_initial_state()
        Return __initial_state, a string representation of the board 
        as it was when Sudoku was initialized.
    is_completed()
        Returns a boolean to indicate whether the puzzle is finished 
        or not.
    assert_validity()
        Raises an InvalidGameSolution exception if each subsection of 
        a Sudoku puzzle doesn't contain exactly the values 1-9.
    __deduce_block_values(block: Sudoku.Block)
        Attemps to find missing Cell values of a Block, given what 
        known values of said Cell's row and columns are. It cannot 
        always solve puzzles single-handedly.
    __value_is_safe(cell: Sudoku.Cell, value: int)
        Returns True if a Cell's value doesn't exist in its given row, 
        column, or Block. Otherwise returns False.
    __solve_recursively(cells: list[Sudoku.Cell], index: int)
        Recursively solves Sudoku puzzles in a brute-force manner. 
        It's less efficient than using deduction.
    solve()
        Solves a Sudoku puzzle. Initially, __deduce_block_values() is 
        called, but if this proves insufficient, __solve_recursively() 
        is called as well.

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
        Takes the special input of a Sudoku board's game data. This is 
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
        # Sudoku board.
        assert len(board) == 9
        for row in board:
            assert len(row) == 9

        rows, columns, blocks, cells = Sudoku.__unpack_vectors(self, board)
        self.__rows: list[Sudoku.Vector] = rows
        self.__columns: list[Sudoku.Vector] = columns
        self.__blocks: list[Sudoku.Block] = blocks
        self.__cells: list[Sudoku.Cell] = cells
        self.__initial_state: str = repr(self)

    def __unpack_vectors(self, board: list[list[int]]) -> tuple[
        list[Sudoku.Vector], 
        list[Sudoku.Vector],
        list[Sudoku.Block],
        list[Sudoku.Cell]
        ]:
        rows: list[Sudoku.Vector] = []
        columns: list[Sudoku.Vector] = []
        blocks: list[Sudoku.Block] = []
        cells: list[Sudoku.Cell] = []
        row_counter = 1
        column_counter = 1

        # Populate the lists of columns and blocks.
        for num in range(9):
            col_vector = Sudoku.Vector(orientation="column", id=(num + 1))
            columns.append(col_vector)
            new_block = Sudoku.Block(id=(num + 1))
            blocks.append(new_block)

        # Populate the lists of rows and cells.
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

                cell = self.Cell(
                    row=row_vector,
                    col=columns[column_counter-1],
                    block=cell_block,
                    value=num
                    )
                cells.append(cell)
                column_counter += 1

            rows.append(row_vector)
            row_counter += 1
            column_counter = 1
        
        return rows, columns, blocks, cells

    def __repr__(self) -> str:
        """Represent a Sudoku object as a 9x9 grid with cell values."""

        representation = " " * 6
        for column in range(9):
            representation += f"v{column + 1}  "
        representation += f"\n{" " * 6}{"_" * 35}\n"
        for row in self.__rows:
            representation += f"{str(row)}\n"
        return representation     

    def get_rows(self) -> list[Sudoku.Vector]:
        return self.__rows
    
    def get_columns(self) -> list[Sudoku.Vector]:
        return self.__columns

    def get_cells(self) -> list[Sudoku.Cell]:
        return self.__cells

    def get_initial_state(self) -> str:
        return self.__initial_state

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
            
    def __deduce_block_values(self, block: Sudoku.Block) -> None:
        unknown_values = block.get_unknown_values()
        # If the block has unknown/missing values, attempt to deduce 
        # the value of each empty cell.
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

                            self.__deduce_block_values(block)
                        else:
                            cell.set_possible_values(possible_values)

    def __value_is_safe(self, cell: Sudoku.Cell, value: int) -> bool:
        subsections: list[Sudoku.Subsection] = [
            cell.get_row(), 
            cell.get_col(), 
            cell.get_block()
            ]
        
        for section in subsections: 
            if value in section.get_known_values():
                return False

        return True

    def __solve_recursively(self, cells: list[Sudoku.Cell], index: int):
        try:
            cell = cells[index]
        except IndexError:
            return True

        # Base case: The final Cell of the puzzle has been reached.
        if len(cells) == index:
            possible_values = cell.get_possible_values()
            if possible_values != None:
                for value in possible_values:
                    if self.__value_is_safe(cell, value):
                        cell.set_value(value)
                        cell.get_block().add_known_value(value)
                        cell.get_row().add_known_value(value)
                        cell.get_col().add_known_value(value)
                        return True
            else:
                return True

        value = cell.get_value()

        # If cell is already occupied then move forward
        if value != 0 and self.__value_is_safe(cell, value):
            return self.__solve_recursively(cells, index + 1)

        for num in range(1, 10):
            
            # If it is safe to place num at current position
            if self.__value_is_safe(cell, num):
                cell.set_value(num)
                cell.get_block().add_known_value(num)
                cell.get_row().add_known_value(num)
                cell.get_col().add_known_value(num)
                
                if self.__solve_recursively(cells, index + 1):
                    return True
                
                cell.set_value(0)
                cell.get_block().remove_known_value(num)
                cell.get_row().remove_known_value(num)
                cell.get_col().remove_known_value(num)

        return False

    def solve(self) -> None:
        """Solves the Sudoku puzzle.

        While the Sudoku puzzle hasn't been completed yet, iterate 
        through each of its 9 blocks. If a block hasn't been solved,
        call the __deduce_block_values() function on it. If the 
        Sudoku puzzle's state remains unchanged after any of the 
        iterations, call __solve_recursively() to solve it. Once it is 
        solved, assert that the puzzle solution is valid, and print the
        solution.
        
        """

        while not self.is_completed():
            initial_state = repr(self)

            for block in self.__blocks:
                unknown_values = block.get_unknown_values()

                if len(unknown_values) != 0:
                    self.__deduce_block_values(block)

            current_state = repr(self)

            if initial_state == current_state:
                unknown_cells: list[Sudoku.Cell] = []

                for cell in self.get_cells():
                    if cell.get_value() == 0:
                        unknown_cells.append(cell)

                self.__solve_recursively(unknown_cells, 0)

        self.assert_validity()

        print(f"Initial puzzle state:\n\n {self.get_initial_state()}\n")
        print(f"Solved puzzle state:\n\n {repr(self)}")

    class Subsection:
        """
        A parent class that represents subsections of a Sudoku puzzle, 
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
                self.__unknown_values.remove(value)

        def get_unknown_values(self) -> list[int]:
            return self.__unknown_values
        
        def get_known_values(self) -> list[int]:
            return self.__known_values
        
        def remove_known_value(self, value: int) -> None:
            self.__unknown_values.append(value)
            if value in self.__known_values:
                self.__known_values.remove(value)
        
        def add_known_value(self, value: int) -> None:
            self.__known_values.append(value)
            if value in self.__unknown_values:
                self.__unknown_values.remove(value)

        def get_cells(self) -> list[Sudoku.Cell]:
            return self.__cells

    class Block(Subsection):
        """A child class extending Subsection. Each has 9 cells."""

        def __init__(self, id: int) -> None:
            super().__init__(id)

    class Vector(Subsection):
        """
        A child class extending Subsection. A vector can be either a 
        column or a row of a Sudoku puzzle. Each has 9 cells.

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
        A class that represents indivdual cells in a Sudoku puzzle.

        Attributes
        ----------
        __row: Sudoku.Vector
        __column: Sudoku.Vector
        __value: int
        __possible_values: list[int]|None
        __block: Sudoku.Block

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
            Sets __value to the believed final value and sets 
            __possible_values to None.

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
            self.__block = block
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
        
        def get_block(self) -> Sudoku.Block:
            return self.__block

        def get_value(self) -> int:
            return self.__value

        def set_value(self, value: int) -> None:
            self.__value = value
            self.__possible_values = None

    class InvalidGameSolution(Exception):
        """A simple custom Exception class."""

        pass