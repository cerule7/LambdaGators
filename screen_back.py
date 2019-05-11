import pygame
import pygame_textinput
import lambda_interpreter
import lambda_ast
import os
import random
import string 

# alligator.png, dead_alligator.png ~ 300 x 74
# egg.png ~ 100 x 100
ALIVE_ALLIGATOR_IMG_KEY = 'alligator'
EGG_IMG_KEY = 'egg'
DEAD_ALLIGATOR_IMG_KEY = 'dead'
SEPARATION_DISTANCE = 20
ALLIGATOR_BASE_WIDTH = 300
ALLIGATOR_BASE_HEIGHT = 74
EGG_BASE_WIDTH = EGG_BASE_HEIGHT = 100


class App:

    def randomColor(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return (r, g, b)

    def make_library(self):
        baseColor = (65, 195, 172)  # constant value of the base color gator
        thresh = (0, 0, 0, 0)  # threshold value for pygame transform

        image_library = {}
        for char in string.ascii_lowercase:
            image_library[char] = {}  # sub-dictionary per variable

            newColor = self.randomColor()  # new random color for new var

            tempGator = pygame.image.load('Resources/alligator.png')  # loads temp Surfaces
            tempEgg = pygame.image.load('Resources/egg.png')

            pygame.transform.threshold(tempGator, tempGator, baseColor, thresh, newColor, 1, None,
                                       True)  # makes Surfaces the new var color
            pygame.transform.threshold(tempEgg, tempEgg, baseColor, thresh, newColor, 1, None, True)

            image_library[char][ALIVE_ALLIGATOR_IMG_KEY] = tempGator  # adds gator and egg to var sub-dict
            image_library[char][EGG_IMG_KEY] = tempEgg

        image_library[DEAD_ALLIGATOR_IMG_KEY] = pygame.image.load('Resources/dead_alligator.png')
        return image_library

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1280, 720
        self.background = (255, 255, 255)
        self.font = pygame.font.Font(None, 32)
        self.prev_button = self.add_prev_button()
        self.next_button = self.add_next_button()
        self.input_box = pygame_textinput.TextInput()
        self.canvas = self.add_canvas()
        self.img_lib = self.make_library()
        self.lambda_array = []
        self.alligator_surfs = {}
        self.lambda_index = -1
        self.search_box = self.add_search_box()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.next_button_color = (255, 0, 0)
        self.disabled_next_button_color = (255, 200, 200)
        self.prev_button_color = (0, 255, 0)
        self.disabled_prev_button_color = (200, 255, 200)
        self._running = True

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption('LambdaGators')
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.parse_search_box_input(False)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.search_box.collidepoint(mouse_pos):
                self.input_box.typing = True
            else:
                self.input_box.typing = False

            if self.next_button.collidepoint(mouse_pos):
                self.parse_search_box_input(True)
            elif self.prev_button.collidepoint(mouse_pos):
                if self.lambda_index > 0:
                    self.lambda_index = max(self.lambda_index-1, 0)
                    self.alligator_surfs = self.lambda_array[self.lambda_index][2]
                    self.input_box.input_string = self.lambda_array[self.lambda_index][0]
                    self.input_box.update([])

    def on_loop(self, events):
        if self.input_box.typing:
            self.input_box.update(events)

        if self.input_box.get_surface().get_width() > self.search_box.width - 10:
            self.input_box.cursor_position -= 1
            self.input_box.input_string = self.input_box.input_string[:-1]

    def on_render(self):
        self._display_surf.fill(self.background)
        color = self.prev_button_color if self.lambda_index > 0 else self.disabled_prev_button_color
        pygame.draw.rect(self._display_surf, color, self.prev_button)
        self._display_surf.blit(self.input_box.get_surface(), (
            self.search_box.x + 10,
            self.search_box.y + (self.search_box.height - self.input_box.get_surface().get_height()) / 2))
        pygame.draw.rect(self._display_surf, pygame.Color('black'), self.search_box, 2)
        text_surface = self.font.render("Prev", True, pygame.Color('black'))
        self._display_surf.blit(text_surface, (
            self.prev_button.x + (self.prev_button.width - text_surface.get_width()) / 2,
            self.prev_button.y + (self.prev_button.height - text_surface.get_height()) / 2))
        pygame.draw.rect(self._display_surf, self.next_button_color, self.next_button)
        text_surface = self.font.render("Next", True, pygame.Color('black'))
        self._display_surf.blit(text_surface, (
            self.next_button.x + (self.next_button.width - text_surface.get_width()) / 2,
            self.next_button.y + (self.next_button.height - text_surface.get_height()) / 2))
        self.render_alligator_surfs()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            self._running = False
        while self._running:
            events = pygame.event.get()
            for event in events:
                self.on_event(event)
            self.on_loop(events)
            self.on_render()
            self.clock.tick(self.fps)
        self.on_cleanup()

    def add_prev_button(self):
        width = 80
        height = 50
        return pygame.Rect(SEPARATION_DISTANCE, SEPARATION_DISTANCE, width, height)

    def add_next_button(self):
        x = self.width - self.prev_button.width - SEPARATION_DISTANCE
        return pygame.Rect(x, self.prev_button.y, self.prev_button.width, self.prev_button.height)

    def add_search_box(self):
        x = self.prev_button.x + self.prev_button.width + SEPARATION_DISTANCE
        width = self.next_button.x - (x + SEPARATION_DISTANCE)
        return pygame.Rect(x, self.prev_button.y, width, self.prev_button.height)

    def add_canvas(self):
        x = self.prev_button.x
        y = self.prev_button.y + self.prev_button.height + SEPARATION_DISTANCE
        width = self.next_button.x + self.next_button.width - self.prev_button.x
        height = self.height - y - SEPARATION_DISTANCE
        return pygame.Rect(x, y, width, height)

    def parse_search_box_input(self, should_display_next_step: bool):
        input_text = self.input_box.get_text().replace(' ', '')
        if (should_display_next_step or self.input_box.typing) and len(input_text) != 0:
            self.input_box.typing = False
            if self.lambda_index < 0 or should_display_next_step or (
                    self.lambda_index < len(self.lambda_array) and input_text != self.lambda_array[self.lambda_index][0]):
                valid, data = lambda_interpreter.get_ast(input_text)
                if valid:
                    if should_display_next_step:
                        data = lambda_interpreter.betareduce(data)
                        input_text = data.toString()
                        self.input_box.input_string = input_text
                        self.input_box.update([])
                    self.alligator_surfs = {}
                    self.generate_surfaces(data)
                    self.resize_surfaces()
                    self.lambda_array.append((input_text, data, self.alligator_surfs))
                    self.lambda_index += 1
                    return True
        return False

    def generate_surfaces(self, ast, x=0, y=0):
        if isinstance(ast, lambda_ast.Identifier):
            self.alligator_surfs[(x, y)] = self.img_lib[ast.name][EGG_IMG_KEY]
        elif isinstance(ast, lambda_ast.Abstraction):
            self.alligator_surfs[(x, y)] = self.img_lib[ast.param][ALIVE_ALLIGATOR_IMG_KEY]
            self.generate_surfaces(ast.body, x + 1, y)
        elif isinstance(ast, lambda_ast.Application):
            self.generate_surfaces(ast.lhs, x, y)
            self.generate_surfaces(ast.rhs, x, y + 1)
        else:
            raise Exception

    def resize_surfaces(self):
        coordinates = self.alligator_surfs.keys()
        max_row = max(map(lambda tuple: tuple[0], coordinates)) + 1
        max_col = max(map(lambda tuple: tuple[1], coordinates)) + 1
        total_x_seperation = SEPARATION_DISTANCE * (max_col - 1)
        total_y_seperation = SEPARATION_DISTANCE * (max_row - 1)
        max_x_alligators = max_x_eggs = -1
        max_y_alligators = max_y_eggs = -1
        objects_in_each_row = {}
        for row in range(max_row):
            curr_row_alligators = 0
            curr_row_eggs = 0
            for col in range(max_col):
                try:
                    surf = self.alligator_surfs[(row, col)]
                except KeyError:
                    continue
                if surf.get_width() == ALLIGATOR_BASE_WIDTH:
                    curr_row_alligators += 1
                elif surf.get_width() == EGG_BASE_WIDTH:
                    curr_row_eggs += 1
                else:
                    raise Exception
            objects_in_each_row[row] = (curr_row_alligators, curr_row_eggs)
            max_x_alligators = max(max_x_alligators, curr_row_alligators)
            max_x_eggs = max(max_x_eggs, curr_row_eggs)

        for col in range(max_col):
            curr_col_alligators = 0
            curr_col_eggs = 0
            for row in range(max_row):
                try:
                    surf = self.alligator_surfs[(row, col)]
                except KeyError:
                    continue
                if surf.get_height() == ALLIGATOR_BASE_HEIGHT:
                    curr_col_alligators += 1
                elif surf.get_height() == EGG_BASE_HEIGHT:
                    curr_col_eggs += 1
                else:
                    raise Exception
            max_y_alligators = max(max_y_alligators, curr_col_alligators)
            max_y_eggs = max(max_y_eggs, curr_col_eggs)

        width_ratio = ALLIGATOR_BASE_WIDTH / EGG_BASE_WIDTH
        height_ratio = ALLIGATOR_BASE_HEIGHT / EGG_BASE_HEIGHT
        surf_width = min(self.canvas.width / (max_x_alligators * width_ratio + max_x_eggs) - total_x_seperation, EGG_BASE_WIDTH)
        surf_height = min(self.canvas.height / (max_y_alligators * height_ratio + max_y_eggs) - total_y_seperation, EGG_BASE_HEIGHT)
        drawing_width = max((max_x_alligators * width_ratio * surf_width, max_x_eggs * surf_width))
        drawing_height = max((max_y_alligators * height_ratio * surf_height, max_y_eggs * surf_height))
        drawing_x = self.canvas.x + (self.canvas.width - (drawing_width + total_x_seperation)) / 2
        drawing_y = self.canvas.y + (self.canvas.height - (drawing_height + total_y_seperation)) / 2
        y_offset = drawing_y
        for row in range(max_row):
            curr_row_max_height = surf_height
            x_offset = drawing_x + (drawing_width - surf_width * (objects_in_each_row[row][0] * width_ratio + objects_in_each_row[row][1]))/2
            for col in range(max_col):
                try:
                    curr_surf = self.alligator_surfs.pop((row, col))
                except KeyError:
                    continue
                new_width = surf_width
                new_height = surf_height
                if curr_surf.get_width() == ALLIGATOR_BASE_WIDTH:
                    new_width *= width_ratio
                if curr_surf.get_height() == ALLIGATOR_BASE_HEIGHT:
                    new_height *= height_ratio
                new_width = int(new_width)
                new_height = int(new_height)
                new_surf = pygame.transform.smoothscale(curr_surf, (new_width, new_height))
                self.alligator_surfs[(x_offset, y_offset)] = new_surf
                curr_row_max_height = max(curr_row_max_height, new_height)
                x_offset += new_width + SEPARATION_DISTANCE
            y_offset += curr_row_max_height + SEPARATION_DISTANCE

    def render_alligator_surfs(self):
        coordinates = self.alligator_surfs.keys()
        if len(coordinates) == 0:
            return
        for coordinate in coordinates:
            surf = self.alligator_surfs.get(coordinate)
            self._display_surf.blit(surf, coordinate)

if __name__ == "__main__":
    myApp = App()
    myApp.on_execute()