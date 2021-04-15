class Task:
    def __init__(self) -> None:
        self.is_finish = False
        pass

    def execute(self):
        pass 

    def finish(self):
        self.is_finish = True

class TaskQue:
    def __init__(self) -> None:
        # 初始化任务队列
        self.task_que = []

    def get_tasks(self):
        # getter函数，返回task队列
        return self.task_que

    # 添加新任务
    def push(self,task:Task):
        self.task_que.append(task)

    # 更新函数，对task队列中的任务集中同步更新
    def update(self):
        for task in self.task_que:
            task:Task
            task.execute()

        # 将结束的task删除
        for task in self.task_que:
            if task.is_finish:
                self.task_que.remove(task)