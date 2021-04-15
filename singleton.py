from base.task import GameTaskQue, Task, TaskQue

class SceneTransitionTask(Task):
    def __init__(self,game,next_scene) -> None:
        super().__init__()
        self.game = game
        self.alpha = 0
        self.mode = False
        self.next = next_scene
        self.speed = 3
        
    def execute(self):
        # mode = False
        
        if not self.mode:
            self.alpha += self.speed
            if self.alpha >= 255:
                self.mode = True
                self.game.change_scene(self.next)
                self.alpha = 255
        else:
            self.alpha -= self.speed
            if self.alpha <= 0:
                self.alpha = 0
                self.finish()
        
        self.game.get_transition_layer().set_alpha(self.alpha)
        
        


class Singleton:
    def __init__(self) -> None:
        self.tasks = None

    def bind_global_task_que(self,task_que : GameTaskQue):
        self.tasks = task_que
        print(self.tasks.control_game)

    def update(self):
        self.tasks.update()

    def start_transition(self,next_scene):
        if next_scene is None:
            print("error:next_scene could not be None")
            return 

        self.tasks.push(SceneTransitionTask(self.tasks.control_game,next_scene))
        
    @staticmethod
    def get_instance():
        if not hasattr(Singleton,'instance') or Singleton.instance is None:
            Singleton.instance = Singleton()
            
        return Singleton.instance