import numpy as np
import random as rd


class player_module:

    # Constructor, allocate any private date here
    def __init__(self):
        self.player_x, self.player_y = 0., 0.
        self.safety_range = 0.20
        # normal tanks, aggressive tanks, capsules, bullets, mines
        self.weight = [1, 0.5, 1.25, 30, 25]
    # Please update the banner according to your information

    def banner(self):
        print('------------------------')
        print('Joshua')
        print('ID: b10202012')
        print('------------------------')

#   Decision making function for moving your tank, toward next decision frame:
#   simply return an integer as
#   0 - standby
#   1 - move down  (y -)
#   2 - move up    (y +)
#   3 - move left  (x -)
#   4 - move right (x +)
#   5 - cannon fire down
#   6 - cannon fire up
#   7 - cannon fire left
#   8 - cannon fire right
#   ------------------------
#   The input arguments consist of
#   score = current score
#   player_hp = current hp
#   player_status
#       1 - can only move [hence you can only return 1-4]
#       2 - can move / can fire cannon [hence you can return 1-4 or 5-8]
#   code = type of objects
#       0 - your cannon-shot
#       1 - enemy's cannon-shot
#       2 - player tank
#       3 - enemy tank
#       4 - enemy tank (stronger)
#       5 - block
#       6 - mine
#       7 - rescue capsule
#   x,y,dx,dy = coordinate of the objects, and current displacement

    def decision(self, score, player_hp, player_status, code, x, y, dx, dy):

        # update player location
        for i in range(len(code)):
            if (code[i] == 2):
                self.player_x = x[i]
                self.player_y = y[i]
                break

        self.is_blocked = [False, False, False, False]  # down, up, left, right
        self.is_mine = [False, False, False, False]  # down, up, left, right
        self.alert = False
        self.how_move = [100, 100, 100, 100]

        # check if the player is blocked
        for i in range(len(code)):
            if code[i] == 5:
                if round(y[i], 3) == round(self.player_y, 3):
                    if round(x[i] - self.player_x, 2) == 0.05 or round(self.player_x, 3) == 0.975:
                        self.is_blocked[3] = True
                    if round(x[i] - self.player_x, 2) == -0.05 or round(self.player_x, 3) == 0.025:
                        self.is_blocked[2] = True
                if round(x[i], 3) == round(self.player_x, 3):
                    if round(y[i] - self.player_y, 2) == 0.05 or round(self.player_y, 3) == 0.975:
                        self.is_blocked[1] = True
                    if round(y[i] - self.player_y, 2) == -0.05 or round(self.player_y, 3) == 0.025:
                        self.is_blocked[0] = True

        # check if there is mine around the player
        for i in range(len(code)):
            if code[i] == 6:
                if round(y[i], 3) == round(self.player_y, 3):
                    if round(x[i] - self.player_x, 2) == 0.05:
                        self.is_mine[3] = True
                    if round(x[i] - self.player_x, 2) == -0.05:
                        self.is_mine[2] = True
                if round(x[i], 3) == round(self.player_x, 3):
                    if round(y[i] - self.player_y, 2) == 0.05:
                        self.is_mine[1] = True
                    if round(y[i] - self.player_y, 2) == -0.05:
                        self.is_mine[0] = True

        # closest tank
        self.closest3_x, self.closest3_y = 0., 0.
        self.closest3_dx, self.closest3_dy = 0., 0.
        min_dist3 = -1.
        for i in range(len(code)):
            if code[i] == 3:
                dist3 = (x[i] - self.player_x) ** 2 + \
                    (y[i] - self.player_y) ** 2
                if min_dist3 < 0. or dist3 < min_dist3:
                    min_dist3 = dist3
                    self.closest3_x, self.closest3_y = x[i], y[i]
                    self.closest3_dx, self.closest3_dy = dx[i], dy[i]

        # closest aggressive tank
        self.closest4_x, self.closest4_y = 0., 0.
        self.closest4_dx, self.closest4_dy = 0., 0.
        min_dist4 = -1.
        for i in range(len(code)):
            if code[i] == 4:
                dist4 = (x[i] - self.player_x) ** 2 + \
                    (y[i] - self.player_y) ** 2
                if min_dist4 < 0. or dist4 < min_dist4:
                    min_dist4 = dist4
                    self.closest4_x, self.closest4_y = x[i], y[i]
                    self.closest4_dx, self.closest4_dy = dx[i], dy[i]

        # find healing capsule
        self.capsule_x, self.capsule_y = 0., 0.
        min_dist_cap = -1.
        for i in range(len(code)):
            if code[i] == 7:
                dist_cap = (x[i] - self.player_x) ** 2 + \
                    (y[i] - self.player_y) ** 2
                if min_dist_cap < 0. or dist_cap < min_dist_cap:
                    min_dist_cap = dist_cap
                    self.capsule_x, self.capsule_y = x[i], y[i]

        # decision making

        # avoid blocks
        self.available_move = [1, 2, 3, 4]
        for i in range(3, -1, -1):
            if self.is_blocked[i]:
                self.available_move.pop(i)

        # being shot at curent block
        for i in range(len(code)):
            if code[i] == 1:
                bul_x, bul_y = x[i], y[i]
                bul_dx, bul_dy = dx[i], dy[i]
                if round(self.player_x, 3) == round(bul_x, 3) and round(bul_dy, 3) == 0:
                    if abs(self.player_y - bul_y) < abs(bul_dy)*20:
                        self.alert = True
                        self.how_move[2] -= self.weight[3]
                        self.how_move[3] -= self.weight[3]
                        print(round(x[i], 3), round(y[i], 3), dx[i], dy[i])
                        print(round(self.player_x, 3), round(self.player_y, 3))

                elif round(self.player_y, 3) == round(bul_y, 3) and round(bul_dy, 3) == 0:
                    if abs(self.player_x - bul_x) < abs(bul_dx)*20:
                        self.alert = True
                        self.how_move[0] -= self.weight[3]
                        self.how_move[1] -= self.weight[3]
                        print(round(x[i], 3), round(y[i], 3), dx[i], dy[i])
                        print(round(self.player_x, 3), round(self.player_y, 3))

        def shoot(closest_x, closest_y, closest_dx, closest_dy):
            if round(self.player_x, 3) != round(closest_x, 3) and round(self.player_y, 3) != round(closest_y, 3):
                if round(closest_dx, 3) == 0:
                    if closest_y < self.player_y:
                        act = 5
                    else:
                        act = 6
                elif round(closest_dy, 3) == 0:
                    if closest_x < self.player_x:
                        act = 7
                    else:
                        act = 8
                else:
                    act = rd.choice([5, 6, 7, 8])
            elif round(self.player_x, 3) == round(closest_x, 3):
                if closest_y < self.player_y:
                    act = 5
                else:
                    act = 6
            elif round(self.player_y, 3) == round(closest_y, 3):
                if closest_x < self.player_x:
                    act = 7
                else:
                    act = 8
            return act
            # TODO: round

        if (player_status == 1) or self.alert == True:
            def dist(closest_x, closest_y):
                dist = ((closest_x - self.player_x)**2 +
                        (closest_y - self.player_y)**2)**0.5
                if dist != 0:
                    return dist
                else:
                    return 100

            def close_weight(closest_x, closest_y, closest_dx, closest_dy, code_n):
                weight = {3: self.weight[0],
                          4: self.weight[1], 7: self.weight[2]}
                if closest_x < self.player_x:
                    self.how_move[2] += weight[code_n] / \
                        dist(closest_x, closest_y)
                elif closest_x > self.player_x:
                    self.how_move[3] += weight[code_n] / \
                        dist(closest_x, closest_y)
                if closest_y < self.player_y:
                    self.how_move[0] += weight[code_n] / \
                        dist(closest_x, closest_y)
                elif closest_y > self.player_y:
                    self.how_move[1] += weight[code_n] / \
                        dist(closest_x, closest_y)

                if (abs(closest_x - self.player_x) > self.safety_range) and (code_n == (3 or 4)):
                    if abs(closest_x - self.player_x) > abs(closest_y - self.player_y):
                        self.how_move[0] += weight[code_n] / \
                            dist(closest_x, closest_y)
                        self.how_move[1] += weight[code_n] / \
                            dist(closest_x, closest_y)
                else:
                    if closest_dy > 0:
                        self.how_move[1] += weight[code_n] / \
                            dist(closest_x, closest_y)
                    elif closest_dy < 0:
                        self.how_move[0] += weight[code_n] / \
                            dist(closest_x, closest_y)

                if (abs(closest_y - self.player_y) > self.safety_range) and (code_n == (3 or 4)):
                    if abs(closest_x - self.player_x) < abs(closest_y - self.player_y):
                        self.how_move[2] += weight[code_n] / \
                            dist(closest_x, closest_y)
                        self.how_move[3] += weight[code_n] / \
                            dist(closest_x, closest_y)
                else:
                    if closest_dx > 0:
                        self.how_move[3] += weight[code_n] / \
                            dist(closest_x, closest_y)
                    elif closest_dx < 0:
                        self.how_move[2] += weight[code_n] / \
                            dist(closest_x, closest_y)

            if 4 in code:
                act = close_weight(self.closest4_x, self.closest4_y,
                                   self.closest4_dx, self.closest4_dy, 4)
            if 7 in code and player_hp < 16:
                act = close_weight(self.capsule_x, self.capsule_y, 0, 0, 7)
            if 3 in code:
                act = close_weight(self.closest3_x, self.closest3_y,
                                   self.closest3_dx, self.closest3_dy, 3)

            # avoid mines
            for i in range(len(self.is_mine)):
                if self.is_mine[i]:
                    self.how_move[i] -= self.weight[4]

            # avoid bullets
            for i in range(len(code)):
                if code[i] == 1:
                    bul_x, bul_y = x[i], y[i]
                    bul_dx, bul_dy = dx[i], dy[i]
                    # detect blocks around being shot
                    for j in range(len(self.available_move)-1, -1, -1):
                        if self.available_move[j] == 1:
                            new_x, new_y = self.player_x, self.player_y - 0.05
                        elif self.available_move[j] == 2:
                            new_x, new_y = self.player_x, self.player_y + 0.05
                        elif self.available_move[j] == 3:
                            new_x, new_y = self.player_x - 0.05, self.player_y
                        elif self.available_move[j] == 4:
                            new_x, new_y = self.player_x + 0.05, self.player_y

                        if round(new_y, 3) == round(bul_y, 3) and round(bul_dy, 3) == 0:
                            if abs(self.player_x - bul_x) < abs(bul_dx)*30:
                                self.how_move[self.available_move[j] -
                                              1] -= self.weight[3]
                        if round(new_x, 3) == round(bul_x, 3) and round(bul_dx, 3) == 0:
                            if abs(self.player_y - bul_y) < abs(bul_dy)*30:
                                self.how_move[self.available_move[j] -
                                              1] -= self.weight[3]

            act_arg = 0
            act = []
            for move in self.available_move:
                if act_arg < self.how_move[move-1]:
                    act_arg = self.how_move[move-1]
                    act = [move]
                elif act_arg == self.how_move[move-1]:
                    act += [move]
            act = rd.choice(act)
        # --------------------------------------------------------------------------------------------------------------------
        # else:
        #     if 4 in code:
        #         act = shoot(self.closest4_x, self.closest3_x,
        #                     self.closest4_dx, self.closest4_dy)
        #     elif self.closest3_x < self.safety_range and self.closest3_y < self.safety_range:
        #         act = shoot(self.closest3_x, self.closest3_y,
        #                     self.closest3_dx, self.closest3_dy)
        #     else:
        #         choices = [5, 6, 7, 8]
        #         for i in range(3, -1, -1):
        #             if not self.is_blocked[i]:
        #                 choices.pop(i)
        #         act = rd.choice(choices)
        else:
            if 4 in code:
                if round(abs(self.closest4_x - self.player_x), 2) == round(abs(self.closest4_y - self.player_y), 2) == 0.05:
                    act = 6
                elif abs(self.closest4_x - self.player_x) < abs(self.closest4_y - self.player_y):
                    if self.closest4_y < self.player_y:
                        act = 5
                    else:
                        act = 6
                else:
                    if self.closest4_x < self.player_x:
                        act = 7
                    else:
                        act = 8
            elif 7 in code:
                act = rd.choice([5, 6, 7, 8])

            else:
                if abs(self.closest3_x - self.player_x) < abs(self.closest3_y - self.player_y):
                    if self.closest3_y < self.player_y:
                        act = 5
                    else:
                        act = 6
                else:
                    if self.closest3_x < self.player_x:
                        act = 7
                    else:
                        act = 8

        return act
