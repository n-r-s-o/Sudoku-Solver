from collections import defaultdict

class Sudoku:
    # __rows: list[Sudoku.Vector]
    # __columns: list[Sudoku.Vector]
    # __all_cells: list[Sudoku.Cell]
    # __blocks: list[Sudoku.Block]

    def __init__(self, board: list[list[int]]) -> None:
        # Assert that the board argument meets the criteria of a valid 
        # sudoku board.
        assert len(board) == 9
        for row in board:
            assert len(row) == 9

        rows, columns, cells, blocks = Sudoku.__unpack_vectors(self, board)
        self.__rows = rows
        self.__columns = columns
        self.__all_cells = cells
        self.__blocks = blocks

    def __repr__(self) -> str:
        representation = " " * 6
        for v in range(9):
            representation += f"v{v + 1}  "
        representation += "\n" + (" " * 6) + ("_" * 35) + "\n"
        for row in self.__rows:
            representation += str(row) + "\n"
        return representation

    def __unpack_vectors(self, board: list[list[int]]) -> tuple[
        list[Sudoku.Vector], 
        list[Sudoku.Vector],
        list[Sudoku.Cell],
        list[Sudoku.Block]
        ]:
        rows: list[Sudoku.Vector] = []
        columns: list[Sudoku.Vector] = []
        cells: list[Sudoku.Cell] = []
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

                # print(f"row: {row_id}, col: {col_id}")

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

                # print(f"adding {num} to block {cell_block_id}")
                # print(f"unknown nums in block {cell_block_id}: {cell_block.get_unknown_values()}")

                cell = self.Cell(
                    row=row_vector,
                    col=columns[column_counter-1],
                    block=cell_block,
                    value=num
                    )
                
                row_vector.add_cell(cell)
                columns[column_counter - 1].add_cell(cell)
                cells.append(cell)
                column_counter += 1

            rows.append(row_vector)
            row_counter += 1
            column_counter = 1
        
        return rows, columns, cells, blocks
        
    def get_rows(self) -> list[Vector]:
        return self.__rows
    
    def get_columns(self) -> list[Vector]:
        return self.__columns
    
    def solve(self) -> None:
        # For each block in the puzzle
        for block in self.__blocks:
            print(f"known block values: {block.get_known_values()}")
            unknowns = block.get_unknown_values()
            # If the block has unknown/missing values
            if len(unknowns) != 0:
                # For each cell in that block
                for cell in block.get_cells():
                    # If the cell's value is missing, remove overlaps 
                    # between the block's missing numbers and 
                    # the numbers already present in the cell's row 
                    # and column. Then update the cell's possible
                    # values to reflect remaining possibilities.
                    if cell.get_value() == 0:
                        possible_values = unknowns
                        vectors = [cell.get_row(), cell.get_col()]

                        print(f"on cell: h{cell.get_row().get_id()}, v{cell.get_col().get_id()}")

                        for vector in vectors:
                            temp_possible_values = possible_values
                            print(f"  row {vector.get_id()}:")
                            for existing_value in vector.get_known_values():
                                if existing_value in temp_possible_values:
                                    print(f"    can't be {existing_value}")
                                    temp_possible_values.remove(existing_value)
                            print(f"  poss. {temp_possible_values}")

                            # If there's only one possible value for the cell,
                            # set its value to that. Otherwise note its new
                            # possible values.
                            if len(temp_possible_values) == 1:
                                value = temp_possible_values[0]
                                cell.set_value(value)
                                print(f"cell could only have value {value}")
                                unknowns.remove(value)
                                block.add_known_value(value)
                                for vector in vectors:
                                    vector.add_known_value(value)
                            else:
                                cell.set_possible_values(temp_possible_values)

                # For each cell in that block
                # for cell in block.get_cells():

        # print(repr(self))

    class Block:
        # __id: int
        # __known_values: list[int]
        # __unknown_values: list[int]
        # __cells: list[Sudoku.Cell]
        
        def __init__(self, id: int) -> None:
            self.__id = id
            self.__known_values: list[int] = []
            self.__unknown_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            self.__cells = []

        def get_id(self) -> int:
            return self.__id

        def get_unknown_values(self) -> list[int]:
            return self.__unknown_values
        
        def get_known_values(self) -> list[int]:
            return self.__known_values

        def add_known_value(self, value: int) -> None:
            self.__known_values.append(value)
            print(f"unknown values: {self.__unknown_values}")
            self.__unknown_values.remove(value)

        def add_cell(self, cell) -> None:
            assert isinstance(cell, Sudoku.Cell)
            self.__cells.append(cell)
            value = cell.get_value()
            if value != 0:
                self.add_known_value(value)

        def get_cells(self) -> list[Sudoku.Cell]:
            return self.__cells

    class Vector:
        # __orientation: str
        # __id: int
        # __cells: list[Sudoku.Cell]
        # __unknown_values: list[int]
        # __known_values: list[int]

        def __init__(self, id: int, orientation: str) -> None:
            assert orientation == "row" or "column"
            self.__orientation = orientation
            self.__id = id
            self.__cells: list[Sudoku.Cell] = []
            self.__known_values: list[int] = []
            self.__unknown_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        def __repr__(self) -> str:
            if self.__orientation == "row":
                name = "h"
            else:
                name = "v"
            return f"{name}{self.__id}"

        def __str__(self) -> str:
            representation = f"{repr(self)}   |_"
            for cell in self.__cells:
                value = cell.get_value()
                if value == 0:
                    value = "_"
                representation += str(value) + "_|_"
            return representation[0:-1]

        def add_cell(self, cell) -> None:
            assert isinstance(cell, Sudoku.Cell)
            self.__cells.append(cell)
            value = cell.get_value()

            if value != 0:
                self.__known_values.append(value)
                self.__unknown_values.remove(value)

        def get_id(self) -> int:
            return self.__id
        
        def get_cells(self) -> list[Sudoku.Cell]:
            return self.__cells
        
        def get_unknown_values(self) -> list[int]:
            return self.__unknown_values
        
        def get_known_values(self) -> list[int]:
            return self.__known_values

        def add_known_value(self, value: int) -> None:
            self.__known_values.append(value)
            self.__unknown_values.remove(value)

    class Cell:
        # __row: Sudoku.Vector
        # __column: Sudoku.Vector
        # __block: Sudoku.Block
        # __value: int
        # __possible_values: list[int] | None

        def __init__(self, row: Sudoku.Vector, col: Sudoku.Vector, block: Sudoku.Block, value: int = 0) -> None:
            self.__row = row
            self.__column = col
            self.__block = block
            self.__value = value
            
            if value != 0:
                self.__possible_values = [value]
            else:
                self.__possible_values = None

            block.add_cell(self)

        # Needless?
        def __eq__(self, other) -> bool:
            assert isinstance(other, Sudoku.Cell)
            has_same_row = self.__row.get_id() == other.get_row()
            has_same_column = self.__column == other.get_col()

            if has_same_row and has_same_column:
                return True
            else:
                return False 

        def get_possible_values(self) -> list|None:
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