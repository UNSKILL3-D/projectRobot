import gen_save_maker

level_name = 'cif2'
gen_save_maker.compile_generator(f'levels/{level_name}')


def generate():
    import random as rnd
    import gen_header as gen

    temp_height = 2
    temp_width = 10
    temp_cells = gen.init_cells_arr(temp_height, temp_width)
    temp_walls = gen.init_walls_arr(temp_height, temp_width)
    gen.make_start(temp_cells, 0, 1)
    gen.make_finish(temp_cells, 9, 1)
    for temp_x in range(1, 9):
        if rnd.random() > 0.4:
            gen.change_wall_from_down(temp_walls, temp_x, 0, 1)
            gen.make_mark_checker(temp_cells, temp_x, 1)
    save_params = [temp_height, temp_width, temp_cells, temp_walls]

    return save_params
