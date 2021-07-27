def init_cells_arr(height, width):
    cells_arr = [[[0, 'white'] for _ in range(width)] for _ in range(height)]
    return cells_arr


def init_walls_arr(height, width):
    walls_arr = [[[0, 0] for _ in range(width)] for _ in range(height)]
    for i in range(width):
        walls_arr[-1][i][1] = 1
    for i in range(height):
        walls_arr[i][-1][0] = 1
    return walls_arr


def make_start(cells_arr, x, y, color='white'):
    cells_arr[y][x][0] = 1
    cells_arr[y][x][1] = color


def make_finish(cells_arr, x, y, color='white'):
    cells_arr[y][x][0] = 2
    cells_arr[y][x][1] = color


def make_mark_checker(cells_arr, x, y, color='white'):
    cells_arr[y][x][0] = 3
    cells_arr[y][x][1] = color


def change_wall_from_down(walls_arr, x, y, value):
    walls_arr[y][x][1] = value


def change_wall_from_right(walls_arr, x, y, value):
    walls_arr[y][x][0] = value
