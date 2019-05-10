import pygame
import pygame_textinput
import os
import random
import string 

# alligator.png, dead_alligator.png ~ 300 x 100
# egg.png ~ 100 x 100

def randomColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return (r, g, b)
        
def makeLibrary():
    baseColor = (65, 195, 172) #constant value of the base color gator 
    thresh = (0, 0, 0, 0) #threshold value for pygame transform 

    imgLib = {} #dictionary of variables to reference alligator/func or egg/var of variable specific color
        
    for char in string.ascii_lowercase:
            imgLib[char] = {}  #sub-dictionary per variable
                
            newColor = randomColor() #new random color for new var
                
            tempGator = pygame.image.load('Resources/alligator.png') #loads temp Surfaces
            tempEgg = pygame.image.load('Resources/egg.png')

            pygame.transform.threshold(tempGator, tempGator, baseColor, thresh, newColor, 1, None, True) #makes Surfaces the new var color
            pygame.transform.threshold(tempEgg, tempEgg, baseColor, thresh, newColor, 1, None, True) 

            imgLib[char]['alligator'] = tempGator #adds gator and egg to var sub-dict 
            imgLib[char]['egg'] = tempEgg
        
    imgLib["dead"] = pygame.image.load('Resources/dead_alligator.png')
    
    return imgLib

class App:
    def __init__(self):
        self.imageLibrary = makeLibrary()
        self.varLibrary = {} #dict/collection of tuples of destination surfaces when using the transform.scale or smoothscale
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1280, 720

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.background = (255, 255, 255)
        self.font = pygame.font.Font(None, 32)
        pygame.display.set_caption('LambdaGators')
        self.next_button = self.add_next_button()
        self.prev_button = self.add_prev_button()
        self.input_box = pygame_textinput.TextInput()
        self.lambda_array = []
        self.lambda_index = -1
        self.search_box = self.add_search_box()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.typing = False
        self._running = True
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = event.pos
            if self.search_box.collidepoint(mousePos):
                self.typing = True
            else:
                self.typing = False

            if self.next_button.collidepoint(mousePos):
                if len(self.input_box.get_text()) != 0:
                    self.lambda_array.append(self.input_box.get_text())
            elif self.prev_button.collidepoint(mousePos):
                self.lambda_index = max(self.lambda_index-1, 0)

    def on_loop(self, events):
        if self.typing and self.input_box.update(events):
            self.typing = False
            self.lambda_array.append(self.input_box.get_text())
            self.lambda_index += 1
            print(self.lambda_array)

    def on_render(self):
        self._display_surf.fill(self.background)
        pygame.draw.rect(self._display_surf, (255, 0, 0), self.next_button)
        pygame.draw.rect(self._display_surf, (0, 255, 0) if self.lambda_index > 0 else (200, 255, 200),
                         self.prev_button)
        self._display_surf.blit(self.input_box.get_surface(), (
            self.search_box.x + 10, self.search_box.y + (self.search_box.height - self.input_box.get_surface().get_height()) / 2),
                                (0, 0, self.search_box.width - 35, self.search_box.height))
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
        pass

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