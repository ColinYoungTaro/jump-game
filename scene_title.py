
from key import PORT, query_key
from pygame.display import update
from singleton import Singleton
from scene_game import SceneGame
from pygame import surface
from base.button import Button, ButtonManager
from pygame.constants import KEYDOWN, K_DOWN, K_KP_ENTER, K_RETURN, K_SPACE, K_UP
from pygame.key import get_pressed
import pygame.sprite
from base.mscene import Scene

COLOR_DEFAULT = (0xee,0xee,0xee)
COLOR_SELECTED = (220,100,100)

class SceneTitle(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.sprite_group = pygame.sprite.Group()
        self.btn_manager = ButtonManager()

        self.btn_manager.add_buttons([
            Button("start game",COLOR_DEFAULT,"start_game",COLOR_SELECTED,call_back=lambda:self.change_scene(SceneGame())),
            Button("exit game",COLOR_DEFAULT,"exit_game",COLOR_SELECTED,call_back=lambda:exit(0))
        ])
        self.btn_manager.set_pos(240,160)
        self.next_scene = self
        
        for btn in self.btn_manager.get_btns():
            self.sprite_group.add(btn)

        # self.show()

    def change_scene(self,scene):
        Singleton.get_instance().start_transition(scene)

    def update(self):
        super().update()
        import scene_game
        self.btn_manager.refresh()
        self.sprite_group.update()
        key = query_key()
        if not key:
            return 
        # print(key)
        if key == PORT.UP:
            self.btn_manager.select_prev()
        elif key == PORT.DOWN:
            self.btn_manager.select_next()
        elif key == PORT.ENTER:
            self.btn_manager.click()


    def handle_input(self):
        pass 

    def show(self,screen):
        # self.btn.show()
        self.btn_manager.show()
        self.surface.fill((40,40,52))
        self.sprite_group.draw(self.surface)
        return self.surface

    def event(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.btn_manager.select_prev()
                elif event.key == K_DOWN:
                    self.btn_manager.select_next()
                elif event.key == K_RETURN:
                    self.btn_manager.click()
    