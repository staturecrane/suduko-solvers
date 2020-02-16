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
        "simple_mip_program", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
    )

    board = []
    for i in range(9):
        board.append(get_row_binaries(solver, i))

    solver.Maximize(1)

    status = solver.Solve()

    board_values = []
    for grid in board:
        row_values = [np.argmax([x.solution_value() for x in row]) + 1 for row in grid]
        board_values.append(row_values)

    print(board_values)

if __name__ == "__main__":
    main()
