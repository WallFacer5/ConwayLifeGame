import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse


'''
@Author: wallfacer (Yanhan Zhang)
@Time: 2019/12/30 11:21
'''


class CellsMachine:
    def __init__(self, dim=20, prob=0.2):
        self.dim = dim
        self.prob = 1 - prob
        self.map_matrix = self.map_generate()
        self.img = plt.imshow(self.map_matrix, cmap='gray_r')

    def map_generate(self):
        map_matrix = np.random.random([self.dim, self.dim])
        map_matrix[map_matrix >= self.prob] = 1
        map_matrix[map_matrix < self.prob] = 0
        return map_matrix

    @staticmethod
    def pos_add(pos1, pos2):
        return pos1[0] + pos2[0], pos1[1] + pos2[1]

    def count_neighbor(self, pos):
        relative = [
            [-1, -1], [-1, 0], [-1, 1],
            [0, -1], [0, 1],
            [1, -1], [1, 0], [1, 1]
        ]
        neighbors = 0
        for r in relative:
            cur_neighbor = self.pos_add(r, pos)
            if cur_neighbor[0] in range(self.dim) and cur_neighbor[1] in range(self.dim):
                if self.map_matrix[cur_neighbor[0]][cur_neighbor[1]] == 1:
                    neighbors += 1
        return neighbors

    def iter_step(self, step):
        new_map = np.zeros([self.dim, self.dim])
        for i in range(self.dim):
            for j in range(self.dim):
                if self.map_matrix[i][j] == 1:
                    if self.count_neighbor((i, j)) in (2, 3):
                        new_map[i][j] = 1
                else:
                    if self.count_neighbor((i, j)) == 3:
                        new_map[i][j] = 1
        self.map_matrix = new_map
        self.img.set_data(new_map)
        return self.img

    def text_print_map(self):
        for i in range(self.map_matrix.shape[0]):
            for j in range(self.map_matrix.shape[1]):
                print(int(self.map_matrix[i][j]), end=' ')
            print()
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Conway\'s Life Game')
    parser.add_argument('-d', '--dim', default='100')
    parser.add_argument('-p', '--prob', default='0.2')
    args = parser.parse_args()
    dim = int(args.dim)
    prob = float(args.prob)
    fig, ax = plt.subplots()
    machine = CellsMachine(dim, prob)
    ani = FuncAnimation(fig, machine.iter_step, interval=1)
    plt.show()
