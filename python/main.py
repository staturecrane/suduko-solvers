import numpy as np

from ortools.linear_solver import pywraplp


def get_row_binaries(solver, grid_char):
    rows = []
    for i in range(9):
        row_vars = []
        for j in range(9):
            variable = solver.IntVar(0, 1, f"{grid_char}-{i}-{j}")
            row_vars.append(variable)

        row_constraint = solver.RowConstraint(1, 1)
        for i in range(9):
            row_constraint.SetCoefficient(row_vars[i], 1)

        rows.append(row_vars)

    for i in range(9):
        solver.Add(
            rows[0][i]
            + rows[1][i]
            + rows[2][i]
            + rows[3][i]
            + rows[4][i]
            + rows[5][i]
            + rows[6][i]
            + rows[7][i]
            + rows[8][i]
            == 1
        )
    return rows


def main():
    solver = pywraplp.Solver(
        "sudoku_solver", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
    )

    board = []
    for i in range(9):
        board.append(get_row_binaries(solver, i))

    # horizontal contraints
    # 3 contiguous rows for each set of 3 contiguous grids
    for i in range(0, 9, 3):
        grids = board[i : i + 3]
        # 3 x 9 x 9
        for j in range(0, 9, 3):
            row = grids[0][j : j + 3] + grids[1][j : j + 3] + grids[2][j : j + 3]
            # 9 x 9
            for k in range(9):
                solver.Add(
                    row[0][k]
                    + row[1][k]
                    + row[2][k]
                    + row[3][k]
                    + row[4][k]
                    + row[5][k]
                    + row[6][k]
                    + row[7][k]
                    + row[8][k]
                    == 1
                )

    # vertical constraints
    vertical_grid_idxs = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
    for grid_idxs in vertical_grid_idxs:
        grids = [board[i] for i in grid_idxs]
        for i, j, k in vertical_grid_idxs:
            row = []
            for l in range(3):
                row.append(grids[l][i])
                row.append(grids[l][j])
                row.append(grids[l][k])

            for m in range(9):
                solver.Add(
                    row[0][m]
                    + row[1][m]
                    + row[2][m]
                    + row[3][m]
                    + row[4][m]
                    + row[5][m]
                    + row[6][m]
                    + row[7][m]
                    + row[8][m]
                    == 1
                )

    solver.Maximize(1)

    status = solver.Solve()

    board_values = []
    for grid in board:
        row_values = [
            np.argmax([x.solution_value() for x in row]).tolist() + 1 for row in grid
        ]
        board_values.append(row_values)

    return board_values


if __name__ == "__main__":
    board_values = main()
    for i in range(0, 9, 3):
        grids = board_values[i : i + 3]
        for j in range(0, 9, 3):
            one = " ".join([str(x) for x in grids[0][j : j + 3]])
            two = " ".join([str(x) for x in grids[1][j : j + 3]])
            three = " ".join([str(x) for x in grids[2][j : j + 3]])
            print(" | ".join([one, two, three]))
        print("------ ------- ------")
