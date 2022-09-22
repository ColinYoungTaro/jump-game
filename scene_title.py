
from base.command import EventHandler, InputHandler, UpdateHandler
from singleton import Singleton
from scene_game import SceneGame
from pygame import surface
from base.button import Button, ButtonManager
import pygame.sprite
from base.mscene import Scene

COLOR_DEFAULT = (0xee,0xee,0xee)
COLOR_SELECTED = (220,100,100)

class SceneTitle(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.sprite_group = pygame.sprite.Group()
        self.btn_manager = ButtonManager()

        self.update_handler : UpdateHandler = None 
        self.events_handler : EventHandler = None 

        # self.show()
    def add_buttons(self, buttons):
        self.btn_manager.add_buttons(buttons)
        self.btn_manager.set_pos(240,160)
        self.next_scene = self
        
        for btn in self.btn_manager.get_btns():
            self.sprite_group.add(btn)

    def change_scene(self,scene):
        Singleton.get_instance().start_transition(scene)

    def update(self):
        super().update()
        import scene_game
        self.btn_manager.refresh()
        self.sprite_group.update()

        if self.update_handler:
            self.update_handler(self)

    def handle_input(self):
        pass 

    def show(self,screen):
        # self.btn.show()
        self.btn_manager.show()
        self.surface.fill((40,40,52))
        self.sprite_group.draw(self.surface)
        return self.surface

    def event(self, events):
        if self.events_handler:
            self.events_handler(self, events)

    
    def register_update_handler(self, handler : InputHandler):
        self.update_handler = handler

    def register_events_handler(self, handler : EventHandler):
        self.events_handler = handler
