from base.mscene import Scene
from base.task import GameTaskQue, Task, TaskQue

class SceneTransitionTask(Task):
    def __init__(self,game,next_scene:Scene) -> None:
        super().__init__()
        self.game = game
        self.alpha = 0
        self.mode = False
        self.next = next_scene
        self.speed = 3
        # self.game.scene.disable()
        
        
    def execute(self):
        # mode = False
        if not self.mode:
            self.alpha += self.speed
            if self.alpha >= 255:
                self.mode = True
                if not self.next:
                    exit()
                self.game.change_scene(self.next)
                self.alpha = 255
        else:
            self.alpha -= self.speed
            if self.alpha <= 0:
                self.alpha = 0
                self.finish()
        
        self.game.get_transition_layer().set_alpha(self.alpha)
        
        
# 全局控制器，单例模式，从Game框架中单独拿出来
# 负责各个游戏对象之间实现一些全局的操作，比如调用场景转换
class Singleton:

    def __init__(self) -> None:
        self.tasks = None

    # 绑定全局的任务队列
    def bind_global_task_que(self,task_que : GameTaskQue):
        assert(isinstance(task_que,GameTaskQue))
        self.tasks = task_que
        print(self.tasks.control_game)

    def update(self):
        self.tasks.update()

    def start_transition(self,next_scene):
        # if next_scene is None:
        #     print("error:next_scene could not be None")
        #     return
        self.tasks.control_game.scene.disable()
        self.tasks.push(SceneTransitionTask(self.tasks.control_game,next_scene))
        
    @staticmethod
    def get_instance():
        if not hasattr(Singleton,'instance') or Singleton.instance is None:
            Singleton.instance = Singleton()
            
        return Singleton.instance
