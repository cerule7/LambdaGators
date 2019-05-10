import pygame
import pygame_textinput

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1280, 720

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.background = (255, 255, 255)
        self.font = pygame.font.Font(None, 32)
        pygame.display.set_caption('Lambdagators')
        self.next_button = self.add_next_button()
        self.prev_button = self.add_prev_button()
        self.input_box = pygame_textinput.TextInput()
        self.lambda_array = []
        self.lambda_index = -1
        self.search_box = self.add_search_box()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.next_button_color = (255, 0, 0)
        self.disabled_next_button_color = (255, 200, 200)
        self.prev_button_color = (0, 255, 0)
        self.disabled_prev_button_color = (200, 255, 200)
        self._running = True
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.input_box.typing = False
                if self.lambda_index < 0 or (self.lambda_index < len(self.lambda_array) and self.input_box.get_text() != self.lambda_array[self.lambda_index]):
                    self.lambda_array.append(self.input_box.get_text())
                    self.lambda_index += 1
                    print(self.lambda_array)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.search_box.collidepoint(mouse_pos):
                self.input_box.typing = True
            else:
                self.input_box.typing = False

            if self.next_button.collidepoint(mouse_pos):
                if len(self.input_box.get_text()) != 0:
                    if self.lambda_index == len(self.lambda_array) - 1 and self.input_box.get_text() != self.lambda_array[self.lambda_index]:
                        self.lambda_array.append(self.input_box.get_text())
                    else:
                        self.lambda_index += 1
            elif self.prev_button.collidepoint(mouse_pos):
                if self.lambda_index > 0:
                    self.lambda_index = max(self.lambda_index-1, 0)

    def on_loop(self, events):
        if self.input_box.typing:
            self.input_box.update(events)

        if self.input_box.get_surface().get_width() > self.search_box.width - 10:
            self.input_box.cursor_position -= 1
            self.input_box.input_string = self.input_box.input_string[:-1]

    def on_render(self):
        self._display_surf.fill(self.background)
        color = self.next_button_color if self.lambda_index != len(
            self.lambda_array) - 1 else self.disabled_next_button_color
        pygame.draw.rect(self._display_surf, color, self.next_button)
        color = self.prev_button_color if self.lambda_index > 0 else self.disabled_prev_button_color
        pygame.draw.rect(self._display_surf, color, self.prev_button)
        self._display_surf.blit(self.input_box.get_surface(), (
            self.search_box.x + 10,
            self.search_box.y + (self.search_box.height - self.input_box.get_surface().get_height()) / 2))
        pygame.draw.rect(self._display_surf, pygame.Color('black'), self.search_box, 2)
        text_surface = self.font.render("Next", True, pygame.Color('black'))
        self._display_surf.blit(text_surface, (
            self.next_button.x + (self.next_button.width - text_surface.get_width()) / 2,
            self.next_button.y + (self.next_button.height - text_surface.get_height()) / 2))
        text_surface = self.font.render("Prev", True, pygame.Color('black'))
        self._display_surf.blit(text_surface, (
            self.prev_button.x + (self.prev_button.width - text_surface.get_width()) / 2,
            self.prev_button.y + (self.prev_button.height - text_surface.get_height()) / 2))
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

    def add_next_button(self):
        y = self.height / 15
        width = 80
        x = self.width - width - 20
        height = 50
        return pygame.Rect(x, y, width, height)

    def add_prev_button(self):
        x = 20
        return pygame.Rect(x, self.next_button.y, self.next_button.width, self.next_button.height)

    def add_search_box(self):
        x = self.prev_button.x + self.prev_button.width + 10
        width = self.next_button.x - (x + 10)
        return pygame.Rect(x, self.next_button.y, width, self.next_button.height)


if __name__ == "__main__":
    myApp = App()
    myApp.on_execute()
