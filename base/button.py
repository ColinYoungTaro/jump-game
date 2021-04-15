from pygame import Rect, Vector2, color, draw
import pygame
from pygame.font import SysFont
from base.game_object import gameObject

class Button(gameObject):

    def __init__(
            self,context_default,color_default,\
            context_select=None,color_select=None,\
            font=None,call_back=None
    ) -> None:
        super().__init__()
        self.is_select = False

        self.context_default = context_default
        self.context_select = context_select if context_select is not None else context_default

        self.color_default = color_default
        self.color_select = color_select if color_select is not None else color_default

        self.font = font if font is not None else SysFont("宋体", 25, bold=True, italic=False)

        self.image = self.font.render(self.context_default, True, (0xee,0xee,0xee))
        self.on_click = call_back
        self.rect = self.image.get_rect()

    def show(self):
        self.rect.x = self.pos.x - self.rect.w // 2
        self.rect.y = self.pos.y - self.rect.h // 2
        if not self.is_select:
            self.image = self.font.render(self.context_default, True, self.color_default)
        else:
            self.image = self.font.render(self.context_default, True, self.color_select)

    def set_select(self,is_select):
        self.is_select = is_select


class ButtonManager:
    VERTICAL = 0
    HORIZONTAL = 1
    def __init__(self) -> None:
        self.btn_list = [] 
        self.select_id = -1 
        self.pos = Vector2(0,0)
        self.show_pattern = ButtonManager.HORIZONTAL
        self.interval_x = 10
        self.interval_y = 20

    def set_pos(self,x,y):
        self.pos = Vector2(x,y)

    def add_buttons(self,buttons):
        for button in buttons:
            self.btn_list.append(button)
            if self.select_id == -1:
                self.select_id = 0

    def get_btns(self):
        return self.btn_list

    def refresh(self):
        render_y = self.pos.y
        for i,btn in enumerate(self.btn_list):
            btn:Button
            btn.set_select(i == self.select_id)
            btn.set_pos(self.pos.x,render_y)
            render_y+=(self.interval_y+btn.rect.h)

        return self.select_id

    def show(self):
        for btn in self.btn_list:
            btn.show()

    def select_next(self):
        if self.select_id < len(self.btn_list) - 1:
            self.select_id += 1 
    
    def select_prev(self):
        if self.select_id > 0:
            self.select_id -= 1 

    def on_adjusted(self):
        pass 

    def click(self):
        btn = self.btn_list[self.select_id]
        # TODO __call__
        if btn and btn.on_click:
            btn.on_click()