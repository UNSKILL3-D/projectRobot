import math
import os
import random
import time
from tkinter import *

import numpy as np


# noinspection PyProtectedMember
class GUI:
    __canvas_scale = 1
    __fst_lh = 59  # first
    __fst_lw = 16
    __lh = __fst_lh * __canvas_scale  # line height
    __lw = __fst_lw * __canvas_scale  # line weight
    __margin = 8
    __window = Tk()
    __palette = dict(back='#171717', grid='#FFFFFF', grid_tr='#3a3a3a', red_grid='#FF4940', red_grid_tr='#3A1E1D')
    __canvas_delta_margin = 0
    __canvas = Canvas(__window, width=600, height=600, bg=__palette['back'], highlightthickness=0)

    grid_width = 10
    grid_height = 5
    robots = []
    field_cells = []
    field_walls = []
    field_marks = []
    is_sandbox_active = False
    field = None
    colors = ['white', 'red', 'blue', 'green', 'purple', 'yellow']
    fps = [DoubleVar()]
    status_bar_text = 0

    def __init__(self, btn_start, btn_step, statusbar, sandbox, scale):
        self.status_bar_text = statusbar
        self.__canvas_scale = scale
        self.is_sandbox_active = sandbox
        self.__window.configure(bg='#323232')
        self.__canvas.bind("<Button-1>", self.sandbox_clicked_left)
        self.__canvas.bind("<MouseWheel>", self.sandbox_wheel)
        self.__canvas.bind("<Button-3>", self.sandbox_clicked_right)
        if self.is_sandbox_active:
            sandbox_text = Label(text='Sandbox', fg='yellow', border='0', bg='#323232')
            sandbox_text.grid(column=0, row=0, sticky=NW, padx=self.__margin, pady=(self.__margin, 0))
        self.__canvas.grid(column=0, row=1, columnspan=3, padx=self.__margin, pady=self.__margin)
        self.btn_start = btn_start
        self.btn_step = btn_step
        self.btn_exit = self.generate_button('Выход', self.exit_clicked)
        self.btn_start.grid(column=0, row=2, pady=self.__margin)
        self.btn_step.grid(column=1, row=2, pady=self.__margin)
        self.btn_exit.grid(column=2, row=2, pady=self.__margin)
        statusbar = Label(textvariable=self.status_bar_text[0], border='0', bg='#323232', font=('Comic Sans MS', 14),
                          fg='white')
        statusbar.grid(column=0, row=3, columnspan=2, sticky=W, padx=self.__margin)
        self.field_walls = [[[random.randint(0, 3), random.randint(0, 3)] for _ in range(10)] for _ in
                            range(5)]
        scale_speed = Scale(from_=1, to=10, orient='horizontal', bg='#323232', bd='0', fg='#FFFFFF',
                            troughcolor="#707070", variable=self.fps[0], borderwidth=0, highlightthickness=0)
        scale_speed.grid(column=2, row=3, pady=(0, self.__margin))
        if True:  
            b, a = math.modf(self.__canvas_scale)
            a = int(a)
            b = int(round(b, 2) * 100)
            a, b = int(str(a) + str(b)), 10 ** len(str(b))
            # noinspection PyGlobalUndefined
            global images_robots
            images_robots = {}
            colors = ['red', 'blue', 'green', 'purple', 'yellow']
            for i in colors:
                images_robots.update({i: PhotoImage(file=f'robots/{i}.png').zoom(a).subsample(b)})
            # noinspection PyGlobalUndefined
            global images_end
            images_end = {}
            colors = ['white', 'red', 'blue', 'green', 'purple', 'yellow']
            for i in colors:
                images_end.update({i: PhotoImage(file=f'images/end/{i}.png').zoom(a).subsample(b)})
            # noinspection PyGlobalUndefined
            global images_marks
            images_marks = {}
            for i in colors:
                images_marks.update({i: PhotoImage(file=f'images/marks/{i}.png').zoom(a).subsample(b)})
            # noinspection PyGlobalUndefined
            global images_mark_places
            images_mark_places = {}
            for i in colors:
                images_mark_places.update({i: PhotoImage(file=f'images/mark_places/{i}.png').zoom(a).subsample(b)})

    @staticmethod
    def exit_clicked():
        # noinspection PyProtectedMember
        os._exit(0)
        # exit()

    # noinspection DuplicatedCode
    def sandbox_clicked_left(self, event):
        if self.is_sandbox_active:
            x = event.x
            y = event.y
            x -= self.__margin
            y -= self.__margin
            is_cell = False
            wall_id = 0
            if x % (self.__lh + self.__lw) > self.__lw and y % (self.__lh + self.__lw) > self.__lw:
                is_cell = True
            elif x % (self.__lh + self.__lw) < self.__lw < y % (self.__lh + self.__lw):
                wall_id = 0
            elif x % (self.__lh + self.__lw) > self.__lw > y % (self.__lh + self.__lw):
                wall_id = 1
            x //= (self.__lh + self.__lw)
            y //= (self.__lh + self.__lw)
            x = int(x)
            y = int(y)
            if is_cell:
                self.field._change_cell(x, y, 1)
            elif wall_id == 0:
                self.field._change_wall(x - 1, y, 1, 0)
            else:
                self.field._change_wall(x, y - 1, 1, 1)

    # noinspection DuplicatedCode
    def sandbox_clicked_right(self, event):
        if self.is_sandbox_active:
            x = event.x
            y = event.y
            x -= self.__margin
            y -= self.__margin
            is_cell = False
            wall_id = 0
            if x % (self.__lh + self.__lw) > self.__lw and y % (self.__lh + self.__lw) > self.__lw:
                is_cell = True
            elif x % (self.__lh + self.__lw) < self.__lw < y % (self.__lh + self.__lw):
                wall_id = 0
            elif x % (self.__lh + self.__lw) > self.__lw > y % (self.__lh + self.__lw):
                wall_id = 1
            x //= (self.__lh + self.__lw)
            y //= (self.__lh + self.__lw)
            x = int(x)
            y = int(y)
            if is_cell:
                self.field._change_cell(x, y, -1)
            elif wall_id == 0:
                self.field._change_wall(x - 1, y, -1, 0)
            else:
                self.field._change_wall(x, y - 1, -1, 1)

    def sandbox_wheel(self, event):
        if self.is_sandbox_active:
            x = event.x
            y = event.y
            x -= self.__margin
            y -= self.__margin
            is_cell = False
            if x % (self.__lh + self.__lw) > self.__lw and y % (self.__lh + self.__lw) > self.__lw:
                is_cell = True
            x //= (self.__lh + self.__lw)
            y //= (self.__lh + self.__lw)
            x = int(x)
            y = int(y)
            if is_cell:
                if 0 <= y < len(self.field_cells) and 0 <= x < len(self.field_cells[0]):
                    if event.delta > 0:
                        self.field_cells[y][x][1] = self.colors[(self.colors.index(self.field_cells[y][x][1]) + 1) % 6]
                    else:
                        self.field_cells[y][x][1] = self.colors[(self.colors.index(self.field_cells[y][x][1]) + 5) % 6]

    @staticmethod
    def generate_button(text, command):
        return Button(text=text, background='#37DB79', foreground='#FFFFFF', font='14', border='0', command=command,
                      activebackground='#37DB79', activeforeground='#FFFFFF')

    def close(self):
        self.__window.destroy()

    def __waiting_for_continue(self):
        self.update_frame()

    def __draw_line(self, x, y, is_horizontal, color):
        if is_horizontal:
            self.__canvas.create_polygon(x, y + self.__lw // 2, x + self.__lw // 2, y + self.__lw,
                                         x + self.__lh - self.__lw // 2, y + self.__lw, x + self.__lh,
                                         y + self.__lw // 2, x + self.__lh - self.__lw // 2, y, x + self.__lw // 2, y,
                                         fill=color, outline="")
        else:
            self.__canvas.create_polygon(x + self.__lw // 2, y, x + self.__lw, y + self.__lw // 2, x + self.__lw,
                                         y + self.__lh - self.__lw // 2, x + self.__lw // 2, y + self.__lh, x,
                                         y + self.__lh - self.__lw // 2, x, y + self.__lw // 2, fill=color, outline="")

    def __draw_grid(self, x, y, width, height):
        for w in range(width + 1):
            for h in range(height):
                n_wall = self.field_walls[h][w - 1][0]
                wall_color = self.__palette['grid_tr']
                if n_wall == 1:
                    wall_color = self.__palette['grid']
                elif n_wall == 2:
                    wall_color = self.__palette['red_grid']
                elif n_wall == 3:
                    wall_color = self.__palette['red_grid_tr']
                self.__draw_line(x + w * (self.__lh + self.__lw), y + h * (self.__lh + self.__lw) + self.__lw, False,
                                 wall_color)
        for w in range(width):
            for h in range(height + 1):
                n_wall = self.field_walls[h - 1][w][1]
                wall_color = self.__palette['grid_tr']
                if n_wall == 1:
                    wall_color = self.__palette['grid']
                elif n_wall == 2:
                    wall_color = self.__palette['red_grid']
                elif n_wall == 3:
                    wall_color = self.__palette['red_grid_tr']
                self.__draw_line(x + w * (self.__lh + self.__lw) + self.__lw, y + h * (self.__lh + self.__lw), True,
                                 wall_color)

    def __draw_start(self, x, y, color):
        self.__canvas.create_rectangle(x + 5, y + 5, x + 15, y + 15, fill=color, outline='')
        # self.__canvas.create_image(x, y, anchor='nw', image=images_start[color])

    def __draw_end(self, x, y, color):
        self.__canvas.create_image(x, y, anchor='nw', image=images_end[color])

    def __draw_mark(self, x, y, color):
        # self.__canvas.create_oval(x + self.__lh // 2 - 15, y + self.__lh // 2 - 15, x + self.__lh // 2 + 15,
        #                           y + self.__lh // 2 + 15, fill=color, outline='')
        self.__canvas.create_image(x + self.__lh // 2, y + self.__lh // 2, anchor='center', image=images_marks[color])

    def __draw_mark_place(self, x, y, color):
        self.__canvas.create_image(x + self.__lh // 2, y + self.__lh // 2, anchor='center',
                                   image=images_mark_places[color])

    def __draw_cells(self):
        if self.field_cells:
            for i in range(len(self.field_cells)):
                for j in range(len(self.field_cells[0])):
                    x = self.__margin + (self.__lw + self.__lh) * i + self.__lw + self.__canvas_delta_margin
                    y = self.__margin + (self.__lw + self.__lh) * j + self.__lw + self.__canvas_delta_margin
                    if self.field_cells[i][j][0] == 1:
                        self.__draw_start(y, x, self.field_cells[i][j][1])
                    elif self.field_cells[i][j][0] == 2:
                        self.__draw_end(y, x, self.field_cells[i][j][1])
                    elif self.field_cells[i][j][0] == 3:
                        self.__draw_mark_place(y, x, self.field_cells[i][j][1])
        if self.field_marks:
            for i in range(len(self.field_cells)):
                for j in range(len(self.field_cells[0])):
                    x = self.__margin + (self.__lw + self.__lh) * i + self.__lw + self.__canvas_delta_margin
                    y = self.__margin + (self.__lw + self.__lh) * j + self.__lw + self.__canvas_delta_margin
                    if self.field_marks[i][j] is not None:
                        self.__draw_mark(y, x, self.field_marks[i][j])

    def __draw_robot(self, pos_x, pos_y, color):
        x = self.__margin + (self.__lw + self.__lh) * pos_x + self.__lw + self.__canvas_delta_margin
        y = self.__margin + (self.__lw + self.__lh) * pos_y + self.__lw + self.__canvas_delta_margin
        # self.__canvas.create_rectangle(x, y, x + self.__lh, y + self.__lh, fill=color, outline='')
        self.__canvas.create_image(x, y, anchor='nw', image=images_robots[color])

    __was_canvas_updated = False

    def update_frame(self):
        self.__canvas.delete("all")
        # if self.__was_canvas_updated:
        #     self.__canvas_scale = min(self.__window.winfo_width()/
        #     self.__canvas.winfo_width(),self.__window.winfo_height()/self.__canvas.winfo_height())
        #     print(self.__canvas_scale)
        self.__lh = self.__fst_lh * self.__canvas_scale  # line height
        self.__lw = self.__fst_lw * self.__canvas_scale  # line weight
        self.__canvas.config(width=self.grid_width * (self.__lw + self.__lh) +
                             self.__lw + 2 * self.__margin + self.__canvas_delta_margin,
                             height=self.grid_height * (self.__lw + self.__lh) +
                             self.__lw + 2 * self.__margin + self.__canvas_delta_margin)
        self.__was_canvas_updated = True
        self.__draw_grid(self.__margin + self.__canvas_delta_margin, self.__margin + self.__canvas_delta_margin,
                         self.grid_width, self.grid_height)
        self.__draw_cells()
        for robot in self.robots:
            self.__draw_robot(robot._get_x(), robot._get_y(), robot.color)
        # self.__draw_robot(1, 2)
        self.__window.update()

    def main_loop(self):
        self.__window.mainloop()


# noinspection PyProtectedMember
class Field:
    __cells = []
    __walls = []
    __robots = []
    __marks = []
    __start_cords = {'white': [0, 0]}
    __finish_colors = {'white'}
    __is_paused = True
    __waiting_for_next_step = False
    __is_sandbox_active = False
    __is_first_robot = True
    __filename = ""
    __status_bar_text = [StringVar()]
    __is_finished = False

    def __init__(self, level, width=1, height=1, sandbox=False, canvas_scale=1.0):
        self.__filename = level
        self.__is_sandbox_active = sandbox
        self.width = width
        self.height = height
        self.__cells = [[[0, 'white'] for _ in range(width)] for _ in range(height)]  # [0] - type, [1] - color
        self.__marks = [[None for _ in range(width)] for _ in range(height)]
        # [0] - wall from right, [1] - wall from down
        self.__walls = [[[0, 0] for _ in range(width)] for _ in range(height)]
        for i in range(width):
            self.__walls[-1][i][1] = 1
        for i in range(height):
            self.__walls[i][-1][0] = 1
        self.__btn_start = self.__generate_button('Старт', self.__start_clicked)
        self.__btn_step = self.__generate_button('Шаг', self.__step_clicked)

        self.__GUI = GUI(self.__btn_start, self.__btn_step, self.__status_bar_text, sandbox, canvas_scale)
        self.__GUI.field = self
        self.__GUI.robots = self.__robots
        self.__GUI.field_walls = self.__walls
        self.__GUI.field_cells = self.__cells
        self.__GUI.field_marks = self.__marks
        self.__status_bar_text[0].set('Running')
        try:
            self.__load()
        except FileNotFoundError:
            pass
        finally:
            for i in range(self.height):
                for j in range(self.width):
                    if self.__cells[i][j][0] == 1:
                        self.__start_cords[self.__cells[i][j][1]] = [j, i]
                    elif self.__cells[i][j][0] == 2:
                        self.__finish_colors.add(self.__cells[i][j][1])
            if random.randint(0, 1):
                self.__invert_red_walls()
            self.update()

    def __check_success(self):
        success = 0
        for i in self.__robots:
            if self.__cells[i._get_y()][i._get_x()][0] == 2 and (
                    self.__cells[i._get_y()][i._get_x()][1] == i.color
                    or (self.__cells[i._get_y()][i._get_x()][1] == 'white' and i.color not in self.__finish_colors)):
                success += 1
        if success == len(self.__robots) and self.__check_marks() and not self.__is_sandbox_active:
            return True
        else:
            return False

    def __check_marks(self):
        check = True
        for i in range(self.height):
            for j in range(self.width):
                if self.__cells[i][j][0] == 3 and (
                        (self.__cells[i][j][1] != self.__marks[i][j] and self.__cells[i][j][1] != 'white') or
                        self.__marks[i][j] is None):
                    check = False
        return check

    @staticmethod
    def __generate_button(text, command):
        return Button(text=text, background='#37DB79', foreground='#FFFFFF', font='14', border='0', command=command,
                      activebackground='#37DB79', activeforeground='#FFFFFF')

    @staticmethod
    def __generate_image_button(img, command):
        return Button(image=img, command=command, border='0')

    def __start_clicked(self):
        self.__is_paused = not self.__is_paused
        if self.__GUI.btn_start['text'] == 'Пауза':
            self.__GUI.btn_start['text'] = 'Старт'
        else:
            self.__GUI.btn_start['text'] = 'Пауза'

    def __step_clicked(self):
        self.__waiting_for_next_step = True

    def _change_cell(self, x, y, delta):
        if len(self.__cells) > y >= 0 and len(self.__cells[0]) > x >= 0:
            self.__cells[y][x][0] = (self.__cells[y][x][0] + delta + 4) % 4

    def _change_wall(self, x, y, delta, orientation):
        if len(self.__walls) - 1 > y >= 0 and len(self.__walls[0]) - 1 > x >= 0:
            self.__walls[y][x][orientation] = (self.__walls[y][x][orientation] + 4 + delta) % 4
            self.update()

    def __invert_red_walls(self):
        for i in range(len(self.__walls)):
            for j in range(len(self.__walls[i])):
                if self.__walls[i][j][0] == 2:
                    self.__walls[i][j][0] = 3
                elif self.__walls[i][j][0] == 3:
                    self.__walls[i][j][0] = 2
                if self.__walls[i][j][1] == 2:
                    self.__walls[i][j][1] = 3
                elif self.__walls[i][j][1] == 3:
                    self.__walls[i][j][1] = 2

    def update(self):
        if self.__is_sandbox_active:
            self.__save()
        self.__GUI.grid_width = self.width
        self.__GUI.grid_height = self.height
        self.__GUI.update_frame()
        while ((self.__is_paused or self.__is_sandbox_active) and not self.__waiting_for_next_step) \
                or self.__is_finished:
            self.__GUI.update_frame()
            if self.__is_sandbox_active:
                self.__save()
        self.__waiting_for_next_step = False
        if not self.__is_paused and not self.__is_first_robot:
            time.sleep(1.0 / self.__GUI.fps[0].get())

    def init_robot(self, cl):
        if not self.__is_sandbox_active:
            if cl not in self.__start_cords:
                robot = Robot(self, len(self.__robots), cl,
                              self.__start_cords['white'][0], self.__start_cords['white'][1])
            else:
                robot = Robot(self, len(self.__robots), cl,
                              self.__start_cords[cl][0], self.__start_cords[cl][1])
            self.__robots.append(robot)
            if self.__is_first_robot:
                self.__is_first_robot = False
            self.update()
            return robot
        else:
            print("Error: can't init robot in sandbox mode")
            # noinspection PyProtectedMember
            os._exit(1)

    def _check_wall(self, robot_id, direction):
        x = self.__robots[robot_id]._get_x()
        y = self.__robots[robot_id]._get_y()
        if abs(direction[0]) == 1:
            return self.__walls[y + min(0, direction[0])][x][1] in (1, 2)
        elif abs(direction[1]) == 1:
            return self.__walls[y][x + min(0, direction[1])][0] in (1, 2)

    def _paint_cell(self, robot_id, color):
        self.__marks[self.__robots[robot_id]._get_y()][self.__robots[robot_id]._get_x()] = color
        self.update()

    def _get_cell_color(self, robot_id):
        return self.__marks[self.__robots[robot_id]._get_y()][self.__robots[robot_id]._get_x()]

    def __save(self):
        save_file = np.array(['static', np.array([self.height, self.width, self.__cells, self.__walls], dtype=object)],
                             'user', dtype=object)
        np.save(f'levels/{self.__filename}', save_file)

    def __load(self):
        save_file = np.load(f'levels/{self.__filename}.npy', allow_pickle=True)
        if not (self.__is_sandbox_active and save_file[0] == 'dynamic'):
            if save_file[0] == 'static':
                save_params = save_file[1]
            else:
                save_file = save_file[1]
                exec(save_file)
                save_params = eval('generate()')
            self.height = save_params[0]
            self.width = save_params[1]
            self.__cells = save_params[2]
            self.__walls = save_params[3]
            self.__marks = [[None for _ in range(self.width)] for _ in range(self.height)]
            self.__GUI.field_walls = self.__walls
            self.__GUI.field_cells = self.__cells
            self.__GUI.field_marks = self.__marks

    def _fail(self):
        self.__status_bar_text[0].set('Fail')
        self.__is_finished = True
        self.update()

    def done(self):
        if self.__status_bar_text[0].get() == 'Running':
            if self.__check_success():
                self.__status_bar_text[0].set('Success')
            else:
                self.__status_bar_text[0].set('Fail')
        self.__is_finished = True
        self.update()


# noinspection PyProtectedMember
class Robot:
    __x = 0
    __y = 0
    color = ''
    __field = Field
    __id = 0
    __forced_updates = True

    def __init__(self, field, current_id, cl, x=0, y=0):
        self.__field = field
        self.__id = current_id
        self.__x = x
        self.__y = y
        self.color = cl

    def _get_x(self):
        return self.__x

    def _get_y(self):
        return self.__y

    # movement
    def right(self):
        if not self.__field._check_wall(self.__id, [0, 1]):
            self.__x += 1
        else:
            self.__field._fail()
        if self.__forced_updates:
            self.__field.update()

    def left(self):
        if not self.__field._check_wall(self.__id, [0, -1]):
            self.__x -= 1
        else:
            self.__field._fail()
        if self.__forced_updates:
            self.__field.update()

    def down(self):
        if not self.__field._check_wall(self.__id, [1, 0]):
            self.__y += 1
        else:
            self.__field._fail()
        if self.__forced_updates:
            self.__field.update()

    def up(self):
        if not self.__field._check_wall(self.__id, [-1, 0]):
            self.__y -= 1
        else:
            self.__field._fail()
        if self.__forced_updates:
            self.__field.update()

    # wall checking
    def wall_from_right(self):
        return self.__field._check_wall(self.__id, [0, 1])

    def wall_from_left(self):
        return self.__field._check_wall(self.__id, [0, -1])

    def wall_from_down(self):
        return self.__field._check_wall(self.__id, [1, 0])

    def wall_from_up(self):
        return self.__field._check_wall(self.__id, [-1, 0])

    def free_from_right(self):
        return not self.__field._check_wall(self.__id, [0, 1])

    def free_from_left(self):
        return not self.__field._check_wall(self.__id, [0, -1])

    def free_from_down(self):
        return not self.__field._check_wall(self.__id, [1, 0])

    def free_from_up(self):
        return not self.__field._check_wall(self.__id, [-1, 0])

    # marking
    def paint(self):
        self.__field._paint_cell(self.__id, self.color)

    def clear(self):
        self.__field._paint_cell(self.__id, None)

    def get_color(self):
        return self.__field._get_cell_color(self.__id)
