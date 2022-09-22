from scene_title import SceneTitle
from base.command import UpdateHandler, EventHandler
from key import PORT, query_key

class SceneTitleOnUpdateRPI(UpdateHandler):
    def __call__(self, gameobj : SceneTitle):
        key = query_key()
        if not key:
            return 
        if key == PORT.UP:
            gameobj.btn_manager.select_prev()
        elif key == PORT.DOWN:
            gameobj.btn_manager.select_next()
        elif key == PORT.ENTER:
            gameobj.btn_manager.click()