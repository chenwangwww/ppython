import numpy as np

#[x,y,z]  [（左，右），（下，上），（后，前）]
class CoorSystem:
    def __init__(self):
        self._pos = np.array([0,0,0])

        self._forward = np.array([0,0,1])
        self._backward = np.array([0,0,-1])
        self._leftward = np.array([-1,0,0])
        self._rightward = np.array([1,0,0])
        self._downward = np.array([0,-1,0])
        self._upward = np.array([0,1,0])

    def calc_angle(self, val1, val2):
        co = np.dot(val1, val2)
        angle_radian = np.arccos(co)
        angle = angle_radian * 180 / np.pi
        return angle

    def calc_dir(self, val1, val2):
        return self.calc_angle(val1, val2) < 15

    def pos_to_dir(self, pos):
        dir = pos - self._pos
        dot = np.dot(dir, dir)
        sqrt = np.sqrt(dot)
        normal_dir = dir/sqrt
        return normal_dir

    def forward(self, value):
        return self.calc_dir(self._forward, value)

    def backward(self, value):
        return self.calc_dir(self._backward, value)

    def leftward(self, value):
        return self.calc_dir(self._leftward, value)

    def rightward(self, value):
        return self.calc_dir(self._rightward, value)

    def downward(self, value):
        return self.calc_dir(self._downward, value)

    def upward(self, value):
        return self.calc_dir(self._upward, value)

    def judge_dir(self, pos):
        normal_dir = self.pos_to_dir(pos)
        dir_txt = '未知方向'
        if self.forward(normal_dir):
            dir_txt = '前'
        elif self.backward(normal_dir):
            dir_txt = '后'
        elif self.leftward(normal_dir):
            dir_txt = '左'
        elif self.rightward(normal_dir):
            dir_txt = '右'
        elif self.downward(normal_dir):
            dir_txt = '下'
        elif self.upward(normal_dir):
            dir_txt = '上'
        return dir_txt

    def judge_dir_by_txt(self, txt):
        dir_list = ['前', '后', '左', '右', '下', '上']
        for val in dir_list:
            index = txt.find(val)
            if index > -1:
                return val
        return None

    def near_by_txt(self, dir_txt):
        move_txt = '未知移动'
        if dir_txt == '前':
            move_txt = '前进'
        elif dir_txt == '后':
            move_txt = '后退'
        elif dir_txt == '左':
            move_txt = '左转，前进'
        elif dir_txt == '右':
            move_txt = '右转，前进'
        elif dir_txt == '下':
            move_txt = '向下'
        elif dir_txt == '上':
            move_txt = '向上'
        return move_txt

    def near(self, pos):
        dir_txt = self.judge_dir(pos)
        return self.near_by_txt(dir_txt)

    def leave_by_txt(self, dir_txt):
        move_txt = '未知移动'
        if dir_txt == '前':
            move_txt = '后退'
        elif dir_txt == '后':
            move_txt = '前进'
        elif dir_txt == '左':
            move_txt = '右转，前进'
        elif dir_txt == '右':
            move_txt = '左转，前进'
        elif dir_txt == '下':
            move_txt = '向上'
        elif dir_txt == '上':
            move_txt = '向下'
        return move_txt

    def leave(self, pos):
        dir_txt = self.judge_dir(pos)
        return self.leave_by_txt(dir_txt)

    def action_by_txt(self, dir_txt, action_txt):
        move_txt = '未知移动'
        if action_txt == '接近':
            move_txt = self.near_by_txt(dir_txt)
        elif action_txt == '离开':
            move_txt = self.leave_by_txt(dir_txt)
        return move_txt

    def action(self, pos, action_txt):
        dir_txt = self.judge_dir(pos)
        return self.action_by_txt(dir_txt, action_txt)


# coor = CoorSystem()
# print(coor.forward(np.array([0,0,1])))
# print(coor.pos_to_dir(np.array([1,1,1])))
# print(coor.judge_dir(np.array([0,0,11])))

#小明在你的前方，此时为了接近他，你应该选择：1.前进；2.后退
# 你.front(小明) and 你.close（小明） =》 前进
# you = CoorSystem()
# print(you.action_by_txt('左', '接近'))

#你看见了小明，此时为了接近他，你应该选择：
# you = CoorSystem()
# print(you.action(np.array([-20,0,0]), '接近'))