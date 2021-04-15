from base.task import TaskQue


class Singleton:
    def __init__(self) -> None:
        self.tasks = TaskQue()

    def update(self):
        self.tasks.update()
        
    @staticmethod
    def get_instance():
        if not hasattr(Singleton,'instance') or Singleton.instance is None:
            Singleton.instance = Singleton()
            
        return Singleton.instance