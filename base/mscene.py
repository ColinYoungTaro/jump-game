# 场景 继承自gameObject
from base.task import TaskQue

class Scene():
    def __init__(self) -> None:
        super().__init__()
        self.task_que = TaskQue()
    
    def post_task(self,task):
        self.task_que.push(task)

    def event(self,events):
        pass 

    def update(self):
        self.task_que.update()

    def dispose(self):
        pass 


