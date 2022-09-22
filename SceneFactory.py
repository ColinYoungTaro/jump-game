import platform

from scene_title import SceneTitle
from singleton import Singleton
from base.button import Button, ButtonManager
COLOR_DEFAULT = (0xee,0xee,0xee)
COLOR_SELECTED = (220,100,100)

class GameSceneFactory:
    @staticmethod
    def getTitleScene():
        start_scene = SceneTitle()
        if platform.system() != 'Windows':
            from handler.rpi_handler import SceneTitleOnUpdateRPI
            from key import init_keys
            start_scene.register_update_handler(
                SceneTitleOnUpdateRPI()
            )
            init_keys()
        else:
            from handler.key_handler import SceneTitleOnEventWin
            start_scene.register_events_handler(
                SceneTitleOnEventWin()
            )
        start_scene.add_buttons([
            Button("start game",COLOR_DEFAULT,"start_game",COLOR_SELECTED,call_back=lambda:Singleton.get_instance().start_transition(
                GameSceneFactory.getMainScene()
            )),
            Button("exit game",COLOR_DEFAULT,"exit_game",COLOR_SELECTED,call_back=lambda:exit(0))
        ])
        return start_scene

    @staticmethod
    def getMainScene():
        from scene_game import SceneGame

        main_scene = SceneGame()
        main_scene.on_fail = lambda : Singleton.get_instance().start_transition(
            GameSceneFactory.getTitleScene()
        )

        return main_scene