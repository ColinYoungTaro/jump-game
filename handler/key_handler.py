from scene_title import SceneTitle
from base.command import UpdateHandler, EventHandler
from pygame.constants import KEYDOWN, K_DOWN, K_KP_ENTER, K_RETURN, K_SPACE, K_UP

class SceneTitleOnEventWin(EventHandler):
    def __call__(self, gameobj : SceneTitle, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    gameobj.btn_manager.select_prev()
                elif event.key == K_DOWN:
                    gameobj.btn_manager.select_next()
                elif event.key == K_RETURN:
                    gameobj.btn_manager.click()


