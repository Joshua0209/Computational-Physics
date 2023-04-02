import random as rd
# TODO: path choice, don't be too close


class player_module:

    # Constructor, allocate any private date here
    def __init__(self):
        self.player_x, self.player_y = 0., 0.
        self.player_dx, self.player_dy = 0., 0.

    # Please update the banner according to your information

    def banner(self):
        print('------------------------')
        print('Author: your_name_here')
        print('ID: bxxxxxxxx')
        print('------------------------')

    def decision(self, score, player_hp, player_status, code, x, y, dx, dy):

        # update player location
        for i in range(len(code)):
            if (code[i] == 2):
                self.player_x = x[i]
                self.player_y = y[i]
                break

        self.is_bullet = [False, False, False, False]
        self.is_blocked = [False, False, False, False]  # down, up, left, right
        self.is_mine = [False, False, False, False]  # down, up, left, right

        # detect bullet
        # for i in range(len(code)):
        #     if code[i] == 1:
        #         if abs(x[i] - self.player_x) < 0.026:
        #             if -0.085 <= round(y[i] - self.player_y, 3) <= -0.05:
        #                 self.is_bullet[0] = True
        #             elif 0.05 <= round(y[i] - self.player_y, 3) <= 0.085:
        #                 self.is_bullet[1] = True
        #         elif abs(y[i] - self.player_y) < 0.026:
        #             if -0.085 <= round(x[i] - self.player_x, 3) <= -0.05:
        #                 self.is_bullet[2] = True
        #             elif 0.05 <= round(x[i] - self.player_x, 3) <= 0.085:
        #                 self.is_bullet[3] = True
        #         elif 0.026 < abs(x[i] - self.player_x) < 0.036:
        #             if y[i] < self.player_y:
        #                 if (x[i] < self.player_x and dx[i] > 0) or (x[i] > self.player_x and dx[i] < 0):
        #                     self.is_bullet[0] = True
        #             if y[i] > self.player_y:
        #                 if (x[i] < self.player_x and dx[i] > 0) or (x[i] > self.player_x and dx[i] < 0):
        #                     self.is_bullet[1] = True
        #         elif 0.025 < abs(y[i] - self.player_y) < 0.036:
        #             if x[i] < self.player_x:
        #                 if (y[i] < self.player_y and dy[i] > 0) or (y[i] > self.player_y and dy[i] < 0):
        #                     self.is_bullet[2] = True
        #             if x[i] > self.player_x:
        #                 if (y[i] < self.player_y and dy[i] > 0) or (y[i] > self.player_y and dy[i] < 0):
        #                     self.is_bullet[3] = True

        # find the nearest bullet

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
        min_dist3 = -1.
        for i in range(len(code)):
            if code[i] == 3:
                dist3 = (x[i] - self.player_x) ** 2 + \
                    (y[i] - self.player_y) ** 2
                if min_dist3 < 0. or dist3 < min_dist3:
                    min_dist3 = dist3
                    self.closest3_x, self.closest3_y = x[i], y[i]

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

        # find nearest block
        self.block_x, self.block_y = 0., 0.
        min_dist_block = -1.
        for i in range(len(code)):
            if code[i] == 5:
                dist_block = (x[i] - self.player_x) ** 2 + \
                    (y[i] - self.player_y) ** 2
                if min_dist_block < 0. or dist_block < min_dist_block:
                    min_dist_block = dist_block
                    self.block_x, self.block_y = x[i], y[i]

        # find nearest bullet
        self.bullet_x, self.bullet_y = 0., 0.
        min_dist_bullet = -1.
        for i in range(len(code)):
            if code[i] == 1:
                dist_bullet = (x[i] - self.player_x) ** 2 + \
                    (y[i] - self.player_y) ** 2
                if min_dist_bullet < 0. or dist_bullet < min_dist_bullet:
                    min_dist_bullet = dist_bullet
                    self.bullet_x, self.bullet_y = x[i], y[i]

        # find available move
        self.available_move = [1, 2, 3, 4]
        for i in range(3, -1, -1):
            if self.is_blocked[i] or self.is_mine[i]:
                self.available_move.pop(i)

        def hit_by_bullet(self, code, x, y, dx, dy, act):
            is_hit = False
            for i in range(len(code)):
                if code[i] == 1:
                    bul_x, bul_y = x[i] + dx[i], y[i] + dy[i]
                    if act == 1:
                        new_x, new_y = self.player_x, self.player_y - 0.05
                    elif act == 2:
                        new_x, new_y = self.player_x, self.player_y + 0.05
                    elif act == 3:
                        new_x, new_y = self.player_x - 0.05, self.player_y
                    elif act == 4:
                        new_x, new_y = self.player_x + 0.05, self.player_y

                    if round(abs(bul_x - new_x), 3) <= 0.15 and round(abs(bul_y - new_y), 3) <= 0.15:
                        is_hit = True
                        break
            return is_hit

        # determine the best move (AI)

        def best_move(self, n):
            pred_min_dist = 1000
            if n == 4:
                tank_x, tank_y = self.closest4_x, self.closest4_y
            elif n == 3:
                tank_x, tank_y = self.closest3_x, self.closest3_y
            else:
                tank_x, tank_y = self.capsule_x, self.capsule_y

            b_move = 0

            for move in self.available_move:
                if not hit_by_bullet(self, code, x, y, dx, dy, move):
                    if move == 1:
                        new_x, new_y = self.player_x, self.player_y - 0.005
                    elif move == 2:
                        new_x, new_y = self.player_x, self.player_y + 0.005
                    elif move == 3:
                        new_x, new_y = self.player_x - 0.005, self.player_y
                    else:
                        new_x, new_y = self.player_x + 0.005, self.player_y

                    new_dist = (new_x - tank_x) ** 2 + (new_y - tank_y) ** 2

                    if new_dist < pred_min_dist:
                        pred_min_dist, b_move = new_dist, move
                    elif new_dist == pred_min_dist:
                        b_move = rd.choice([b_move, move])
                else:
                    pass

            return b_move

        # available move for finding blocks
        # self.available_blocks = [1, 2, 3, 4]
        # for i in range(3, -1, -1):
        #     if self.is_mine[i] or self.is_bullet[i]:
        #         self.available_blocks.pop(i)
        # def best_move_blocks(self):
        #     pred_min_dist = 1000
        #     b_move = 0
        #     for move in self.available_blocks:
        #         if move == 1:
        #             new_x, new_y = self.player_x, self.player_y - 0.005
        #         elif move == 2:
        #             new_x, new_y = self.player_x, self.player_y + 0.005
        #         elif move == 3:
        #             new_x, new_y = self.player_x - 0.005, self.player_y
        #         else:
        #             new_x, new_y = self.player_x + 0.005, self.player_y
        #         new_dist = (new_x - self.block_x) ** 2 + (new_y - self.block_y) ** 2
        #         if new_dist < pred_min_dist:
        #             pred_min_dist, b_move = new_dist, move
        #     return b_move

        # dodge aggressive tanks
        # self.is_4 = [False, False, False, False]
        # for i in range(len(code)):
        #     if code[i] == 4:
        #         if round(y[i], 3) == round(self.player_y, 3):
        #             if round(x[i] - self.player_x, 2) == 0.05:
        #                 self.is_4[3] = True
        #             if round(x[i] - self.player_x, 2) == -0.05:
        #                 self.is_4[2] = True
        #         if round(x[i], 3) == round(self.player_x, 3):
        #             if round(y[i] - self.player_y, 2) == 0.05:
        #                 self.is_4[1] = True
        #             if round(y[i] - self.player_y, 2) == -0.05:
        #                 self.is_4[0] = True
        #
        # self.available_4_move = [1, 2, 3, 4]
        # for i in range(3, -1, -1):
        #     if self.is_blocked[i] or self.is_mine[i] or self.is_bullet[i] or self.is_4[i]:
        #         self.available_4_move.pop(i)
        #
        # def best_move_4(self):
        #     pred_min_dist = 0.
        #     b_move = 0
        #     for move in self.available_blocks:
        #         if move == 1:
        #             new_x, new_y = self.player_x, self.player_y - 0.005
        #         elif move == 2:
        #             new_x, new_y = self.player_x, self.player_y + 0.005
        #         elif move == 3:
        #             new_x, new_y = self.player_x - 0.005, self.player_y
        #         else:
        #             new_x, new_y = self.player_x + 0.005, self.player_y
        #         new_dist = (new_x - self.closest4_x) ** 2 + (new_y - self.closest4_y) ** 2
        #         if new_dist > pred_min_dist:
        #             pred_min_dist, b_move = new_dist, move
        #     return b_move

        # deal with aggressive

        if player_status == 1:
            if 4 in code:
                act = 0
                if round(self.closest4_x - self.player_x, 2) == 0 and round(self.closest4_y - self.player_y, 2) == 0.05 and self.closest4_dx < 0:
                    act = 4
                elif round(self.closest4_x - self.player_x, 2) == 0 and round(self.closest4_y - self.player_y, 2) == -0.05 and self.closest4_dx > 0:
                    act = 3
            elif 7 in code:
                act = best_move(self, 7)

            # elif 5 in code:
            #     act = best_move_blocks(self)
            else:
                act = best_move(self, 3)
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
            # elif 5 in code:
            #     if abs(self.block_x - self.player_x) < abs(self.block_y - self.player_y):
            #         if self.block_y < self.player_y:
            #             act = 5
            #         else:
            #             act = 6
            #     else:
            #         if self.block_x < self.player_x:
            #             act = 7
            #         else:
            #             act = 8
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
        if round(self.player_x, 3) == round(self.bullet_x, 3):
            if abs(self.player_y - self.bullet_y) <= 0.086:
                act = rd.choice([3, 4])
        elif round(self.player_y, 3) == round(self.bullet_y, 3):
            if abs(self.player_x - self.bullet_x) <= 0.086:
                act = rd.choice([1, 2])
        else:
            pass

        return act
