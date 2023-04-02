import numpy as np
import random as rd


class player_module:

    # Constructor, allocate any private date here
    def __init__(self):
        self.player_x, self.player_y = 0., 0.
        self.player_dx, self.player_dy = 0., 0.
        self.hp = 8
        # normal tanks, aggressive tanks, capsules, bullets, mines
        self.weight = [5, 10, 15*8, 70, 80]
        self.blocked = False
        self.blocked_twice = 0
        self.score = -1
        self.score_jam = 0
    # Please update the banner according to your information

    def banner(self):
        print('------------------------')
        print('Joshua_final')
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

    def dist(self, x, y):
        dist = (x - self.player_x)**2 + (y - self.player_y)**2
        if dist != 0:
            return dist
        else:
            return 100

    def decision(self, score, player_hp, player_status, code, x, y, dx, dy):
        class player_data:
            def __init__(self, x, y, dx, dy):
                self.x, self.y, self.dx, self.dy = x, y, dx, dy

            def get_all(self):
                return self.x, self.y, self.dx, self.dy

        # update player location
        for i in range(len(code)):
            if (code[i] == 2):
                self.player_x = x[i]
                self.player_y = y[i]
                self.player_dx = dx[i]
                self.player_dy = dy[i]
                self.hp = player_hp
                break

        self.is_block = [False, False, False, False]  # down, up, left, right
        self.is_mine = [False, False, False, False]  # down, up, left, right
        self.alert = False
        self.how_move = [0, 0, 0, 0]
        self.available_move = [1, 2, 3, 4]
        self.is_side = [False, False, False, False]

        # check if player is at sides
        for i in range(4):
            if round(self.player_x, 3) == 0.975:
                self.is_side[3] = True
            elif round(self.player_x, 3) == 0.025:
                self.is_side[2] = True
            elif round(self.player_y, 3) == 0.975:
                self.is_side[1] = True
            elif round(self.player_y, 3) == 0.025:
                self.is_side[0] = True

        # check if the player is blocked
        for i in range(len(code)):
            if code[i] == 5:
                if round(y[i], 3) == round(self.player_y, 3):
                    if round(x[i] - self.player_x, 2) == 0.05:
                        self.is_block[3] = True
                    if round(x[i] - self.player_x, 2) == -0.05:
                        self.is_block[2] = True
                if round(x[i], 3) == round(self.player_x, 3):
                    if round(y[i] - self.player_y, 2) == 0.05:
                        self.is_block[1] = True
                    if round(y[i] - self.player_y, 2) == -0.05:
                        self.is_block[0] = True

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

        def closest(code_n):
            min_x, min_y, min_dx, min_dy, min_dist = 0., 0., 0., 0., -1
            for i in range(len(code)):
                if code[i] == code_n:
                    dist = self.dist(x[i], y[i])
                    if min_dist < 0. or dist < min_dist:
                        min_dist = dist
                        min_x, min_y, min_dx, min_dy = x[i], y[i], dx[i], dy[i]
            return min_x, min_y, min_dx, min_dy

        # closest tank
        tank3 = player_data(*closest(3))

        # closest aggressive tank
        tank4 = player_data(*closest(4))

        # find healing capsule
        capsule = player_data(*closest(7))

        # find nearest bullet
        bullet = player_data(*closest(1))

        # decision making

        # avoid blocks
        for i in range(3, -1, -1):
            if self.is_block[i] or self.is_side[i] or self.is_mine[i]:
                self.available_move.pop(i)

        # being shot at curent block
        for i in range(len(code)):
            if code[i] == 1:
                bul = player_data(x[i], y[i], dx[i], dy[i])
                if round(self.player_x, 3) == round(bul.x, 3) and round(bul.dy, 3) == 0:
                    if abs(self.player_y - bul.y) < abs(bul.dy)*20:
                        self.alert = True
                        self.how_move[2] -= self.weight[3]
                        self.how_move[3] -= self.weight[3]

                elif round(self.player_y, 3) == round(bul.y, 3) and round(bul.dy, 3) == 0:
                    if abs(self.player_x - bul.x) < abs(bul.dx)*20:
                        self.alert = True
                        self.how_move[0] -= self.weight[3]
                        self.how_move[1] -= self.weight[3]

        def shoot(closest_x, closest_y, closest_dx, closest_dy, code_n):
            if 4 in code and round(abs(tank4.x - self.player_x), 2) == round(abs(tank4.y - self.player_y), 2) == 0.05:
                act = 6
            else:
                if abs(self.player_x - closest_x) < abs(self.player_y - closest_y):
                    if closest_y < self.player_y:
                        act = 5
                    else:
                        act = 6
                else:
                    if closest_x < self.player_x:
                        act = 7
                    else:
                        act = 8

            return act

        def close_weight(closest_x, closest_y, closest_dx, closest_dy, code_n):
            weight = {3: self.weight[0],
                      7: self.weight[2]/(code.count(3)+code.count(4)*4)/self.hp}
            # to avoid all enemy died before eating all capsules and to debug for that the capsule cannot be eaten
            if (self.hp < 16 and code.count(4) == 0 and code.count(3) < 2 and code.count(7) != 0) or self.dist(capsule.x, capsule.y) < 0.086:
                weight[3] = 0

            w = weight[code_n] / self.dist(closest_x, closest_y)
            if closest_x < self.player_x:
                self.how_move[2] += w
            elif closest_x > self.player_x:
                self.how_move[3] += w
            if closest_y < self.player_y:
                self.how_move[0] += w
            elif closest_y > self.player_y:
                self.how_move[1] += w

        if (player_status == 1) or self.alert == True:
            if 4 in code:
                act = 0
                if round(tank4.x - self.player_x, 2) == 0 and round(tank4.y - self.player_y, 2) == 0.05 and tank4.dx < 0:
                    act = 4
                elif round(tank4.x - self.player_x, 2) == 0 and round(tank4.y - self.player_y, 2) == -0.05 and tank4.dx > 0:
                    act = 3
                # else:
                #     if (1 not in self.available_move) and (2 not in self.available_move):
                #         if 3 in self.available_move:
                #             act = 3
                #         elif 4 in self.available_move:
                #             act = 4
                #     elif (3 not in self.available_move) and (4 not in self.available_move):
                #         if 1 in self.available_move:
                #             act = 1
                #         elif 2 in self.available_move:
                #             act = 2
                #     elif (1 not in self.available_move) and (2 in self.available_move):
                #         act = 2
                #     elif (2 not in self.available_move) and (1 in self.available_move):
                #         act = 1
                #     elif (3 not in self.available_move) and (4 in self.available_move):
                #         act = 4
                #     elif (4 not in self.available_move) and (3 in self.available_move):
                #         act = 3

            else:
                w = self.weight[3] / self.dist(tank3.x, tank3.y)
                if round(tank3.dx, 3) == 0:
                    if round(abs(self.player_x-tank3.x), 2) <= 0.05:
                        if self.player_x < tank3.x:
                            self.how_move[3] -= w
                        elif self.player_x > tank3.x:
                            self.how_move[2] -= w
                        else:
                            self.how_move[2] -= w
                            self.how_move[3] -= w
                elif round(tank3.dy, 3) == 0:
                    if round(abs(self.player_y-tank3.y), 2) <= 0.05:
                        if self.player_y < tank3.y:
                            self.how_move[1] -= w
                        elif self.player_y > tank3.y:
                            self.how_move[0] -= w
                        else:
                            self.how_move[0] -= w
                            self.how_move[1] -= w

                if 7 in code and self.hp < 16:
                    close_weight(*capsule.get_all(), 7)
                if 3 in code:
                    close_weight(*tank3.get_all(), 3)
                # avoid mines
                for i in range(len(self.is_mine)):
                    if self.is_mine[i]:
                        self.how_move[i] -= self.weight[4]

                # avoid bullets
                for i in range(len(code)):
                    if code[i] == 1:
                        bul = player_data(x[i], y[i], dx[i], dy[i])
                        # detect blocks around being shot
                        for move in self.available_move:
                            new_x, new_y = self.player_x, self.player_y
                            if move == 1:
                                new_y -= 0.05
                            elif move == 2:
                                new_y += 0.05
                            elif move == 3:
                                new_x -= 0.05
                            elif move == 4:
                                new_x += 0.05

                            if round(new_y, 3) == round(bul.y, 3) and round(bul.dy, 3) == 0:
                                if abs(self.player_x - bul.x) < abs(bul.dx)*30:
                                    self.how_move[move - 1] -= self.weight[3]
                            if round(new_x, 3) == round(bul.x, 3) and round(bul.dx, 3) == 0:
                                if abs(self.player_y - bul.y) < abs(bul.dy)*30:
                                    self.how_move[move - 1] -= self.weight[3]

                act_arg = -float("inf")
                act = []
                for move in self.available_move:
                    if act_arg < self.how_move[move-1]:
                        act_arg = self.how_move[move-1]
                        act = [move]
                    elif act_arg == self.how_move[move-1]:
                        act += [move]
                print(self.how_move)
                print(act)
                act = rd.choice(act)
                print(act)
                print("----------------------------------------------------------------")

            # avoid stupid things
            if self.blocked_twice > 3:
                act = 0
            if self.blocked:
                self.blocked_twice += 1
            else:
                self.blocked_twice = 0

            if 4 not in code:
                best = sorted(range(len(self.how_move)),
                              key=self.how_move.__getitem__, reverse=True)
                for move in best:
                    # move is in [0,1,2,3]
                    if act != move + 1:
                        if not (self.is_mine[move] or self.is_side[move]):
                            if self.is_block[move]:
                                self.blocked = True
                                self.shoot_block = move + 1 + 4
                                break
                    else:
                        break

        # --------------------------------------------------------------------------------------------------------------------
        else:
            if self.blocked:
                act = self.shoot_block
                self.blocked = False
            elif 4 in code:
                act = shoot(*tank4.get_all(), 4)
            # elif (self.hp != 16 and code.count(3) < 3 and code.count(7) != 0) or self.dist(capsule.x, capsule.y) < 0.086:
            #     act = shoot(*capsule.get_all(), 7)
            else:
                try:
                    act = shoot(*tank3.get_all(), 3)
                except:
                    choices = [5, 6, 7, 8]
                    for i in range(3, -1, -1):
                        if self.is_block[i]:
                            choices.pop(i)
                    act = rd.choice(choices)

        # --------------------------------------------------------------------------------------------------------------------
        # avoid more stupid things
        if 4 not in code:
            if self.score == score:
                self.score_jam += 1
            else:
                self.score_jam = 0
            if self.score_jam >= 30:
                if player_status == 1:
                    act = rd.choice([1, 2, 3, 4])
                else:
                    act = rd.choice([5, 6, 7, 8])
                print("Score jam")
            self.score = score

        # for aggressive tanks
        # if 4 in code:
        if round(self.player_x, 3) == round(bullet.x, 3):
            if abs(self.player_y - bullet.y) <= 0.086:
                if (3 in self.available_move) and (4 in self.available_move):
                    act = rd.choice([3, 4])
                elif 4 in self.available_move:
                    act = 4
                elif 3 in self.available_move:
                    act = 3
        elif round(self.player_y, 3) == round(bullet.y, 3):
            if abs(self.player_x - bullet.x) <= 0.086:
                if abs(self.player_y - bullet.y) <= 0.086:
                    if (1 in self.available_move) and (2 in self.available_move):
                        act = rd.choice([1, 2])
                    elif 1 in self.available_move:
                        act = 1
                    elif 2 in self.available_move:
                        act = 2

        print(self.blocked)
        for how in self.how_move:
            print(round(how, 0), end=' ')
        print()
        print(self.available_move)
        print(self.blocked, self.blocked_twice)
        print("-----------------------------------------")
        return act
