class Sudoku:
    # __rows = list[Sudoku.Vector]
    # __columns = list[Sudoku.Vector]
    # __missing_nums_dict = dict[str, list[int]]

    def __init__(self, board: list[list[int]]) -> None:
        # Assert that the board argument meets the criteria of a valid 
        # sudoku board.
        assert len(board) == 9
        for row in board:
            assert len(row) == 9

        rows, columns = Sudoku.__unpack_vectors(self, board)
        self.__rows = rows
        self.__columns = columns

        missing_row_nums = Sudoku.__calculate_missing_nums(self, "rows")
        missing_col_nums = Sudoku.__calculate_missing_nums(self, "columns")
        self.__missing_nums_dict = missing_row_nums|missing_col_nums

    def __repr__(self) -> str:
        representation = " " * 6
        for v in range(9):
            representation += f"v{v + 1}  "
        representation += "\n" + (" " * 6) + ("_" * 35) + "\n"
        for row in self.__rows:
            representation += repr(row) + "\n"
        return representation

    def __unpack_vectors(self, board: list[list[int]]) -> tuple[
        list[Sudoku.Vector], 
        list[Sudoku.Vector]
        ]:
        rows: list[Sudoku.Vector] = []
        columns: list[Sudoku.Vector] = []
        row_counter = 1
        column_counter = 1

        # Populate the list of columns.
        for column in range(9):
            col_name = f"v{str(column + 1)}"
            vertical_vector = Sudoku.Vector(name=col_name)
            columns.append(vertical_vector)

        # Populate the list of rows.
        for row in board:
            row_name = f"h{str(row_counter)}"
            horizontal_vector = Sudoku.Vector(name=row_name)

            for num in row:
                cell = self.Cell(
                    row=row_name,
                    col=f"v{str(column_counter)}", 
                    value=num
                    )
                    
                horizontal_vector.add_cell(cell)
                columns[column_counter - 1].add_cell(cell)
                column_counter += 1

            rows.append(horizontal_vector)
            row_counter += 1
            column_counter = 1
        
        return rows, columns

    def __calculate_missing_nums(self, type: str) -> dict[str, list[int]]:
        assert type == "rows" or "columns"
        missing_nums_dict = {}

        if type == "rows":
            collection = self.__rows
        else:
            collection = self.__columns

        for vector in collection:
            name = vector.get_name()
            cells = vector.get_cells_list()
            nums = []
            missing_nums = []

            for cell in cells:
                nums.append(cell.get_value())

            for num in range(9):
                if num + 1 not in nums:
                    missing_nums.append(num + 1)

            missing_nums_dict[name] = missing_nums

        return missing_nums_dict

    def get_rows(self) -> list[Vector]:
        return self.__rows
    
    def get_columns(self) -> list[Vector]:
        return self.__columns
    
    def solve(self) -> None:
        # TODO
        pass

    def print_missing_nums(self) -> None:
        print("__Missing values__")
        for key in self.__missing_nums_dict.keys():
            print(f"{key}: {self.__missing_nums_dict[key]}")
        print()

    class Vector:
        # __name: str
        # __cells: list[Sudoku.Cell]

        def __init__(self, name: str) -> None:
            self.__name = name
            self.__cells: list[Sudoku.Cell] = []

        def __repr__(self) -> str:
            representation = f"{self.__name}   |_"
            for cell in self.__cells:
                value = cell.get_value()
                if value == 0:
                    value = "_"
                representation += str(value) + "_|_"
            return representation[0:-1]

        def add_cell(self, cell) -> None:
            assert isinstance(cell, Sudoku.Cell)
            self.__cells.append(cell)

        def remove_cell(self, cell_to_remove) -> bool:
            assert isinstance(cell_to_remove, Sudoku.Cell)
            for cell in self.__cells:
                if cell == cell_to_remove:
                    self.__cells.remove(cell)
                    return True
            return False
        
        def get_name(self) -> str:
            return self.__name
        
        def get_cells_list(self) -> list[Sudoku.Cell]:
            return self.__cells
        
    class Cell:
        # __row: str
        # __column: str
        # __value: int
        # __possible_values: list[int] | None

        def __init__(self, row: str, col: str, value: int = 0) -> None:
            self.__row = row
            self.__column = col
            self.__value = value
            
            if value != 0:
                self.__possible_values = [value]
            else:
                self.__possible_values = None

        # Needless?
        def __eq__(self, other) -> bool:
            assert isinstance(other, Sudoku.Cell)
            has_same_row = self.__row == other.get_row()
            has_same_column = self.__column == other.get_col()

            if has_same_row and has_same_column:
                return True
            else:
                return False 

        def get_possible_values(self) -> list|None:
            return self.__possible_values

        def set_possible_values(self, values: list[int]) -> None:
            self.possible_values = values

        def get_row(self) -> str:
            return self.__row
    
        def get_col(self) -> str:
            return self.__column

        def get_value(self) -> int:
            return self.__value

        def set_value(self, value: int) -> None:
            self.__value = value