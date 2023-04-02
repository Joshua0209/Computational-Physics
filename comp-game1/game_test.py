import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

import player_module_1 as PM
# import player_module_ver1 as PM
P1 = PM.player_module()
P1.banner()


class random_gen:
    def __init__(self, seed=12345678):
        self.s1 = np.uint64(seed & 0xffff)
        self.s2 = np.uint64((seed >> 16) & 0xffff)
        for i in range(20):
            self.gen()  # warm up

    def gen(self):
        self.s1 = self.s1 ^ (self.s1 >> np.uint64(17))
        self.s1 = self.s1 ^ (self.s1 << np.uint64(31))
        self.s1 = self.s1 ^ (self.s1 >> np.uint64(8))
        self.s2 = (self.s2 & np.uint64(0xffffffff)) * \
            np.uint64(4294957665) + (self.s2 >> np.uint64(32))
        return ((self.s1 ^ self.s2) & np.uint64(0xffffffff))

    def uniform(self, a=0., b=1.):
        return float(self.gen())/0xffffffff*(b-a)+a

    def randint(self, a, b):
        return int(self.uniform(a, b+1.-1E-10))


# let's use our own random generator
# replace time function to a fixed seed if needed
rnd = random_gen(int(time.time()))

fig = plt.figure(figsize=(10, 11), dpi=60)
ax = plt.axes(xlim=(0., 1.), ylim=(0., 1.1))

ms_scale = 2.3
g_block0,     = ax.plot([], [], marker='s', ms=ms_scale *
                        10, color=(0.8, 0.8, 0.8), ls='None')
g_block1,     = ax.plot([], [], marker='s', ms=ms_scale *
                        10, color=(0.6, 0.6, 0.6), ls='None')
g_block2,     = ax.plot([], [], marker='s', ms=ms_scale *
                        10, color=(0.4, 0.4, 0.4), ls='None')
g_block3,     = ax.plot([], [], marker='s', ms=ms_scale *
                        10, color=(0.2, 0.2, 0.2), ls='None')
g_mine,       = ax.plot([], [], marker='X', ms=ms_scale *
                        8, color=(0.8, 0.0, 0.0), ls='None')
g_tank,       = ax.plot([], [], marker='*', ms=ms_scale *
                        10, color=(0.0, 0.8, 0.8), ls='None')
g_tank_agg,   = ax.plot([], [], marker='*', ms=ms_scale *
                        10, color=(0.6, 0.2, 1.0), ls='None')
g_tank_ply,   = ax.plot([], [], marker='*', ms=ms_scale *
                        10, color=(0.0, 0.0, 1.0), ls='None')
g_capsule,    = ax.plot([], [], marker='P', ms=ms_scale *
                        8, color=(0.0, 0.8, 0.0), ls='None')
g_bullet,     = ax.plot([], [], marker='o', ms=ms_scale *
                        3, color=(0.0, 0.6, 0.6), ls='None')
g_bullet_ply, = ax.plot([], [], marker='o', ms=ms_scale *
                        3, color=(0.0, 0.0, 0.8), ls='None')
g_explosion,  = ax.plot([], [], marker=(
    4, 1, 0), ms=ms_scale * 8, color=(1.0, 0.6, 0.2), ls='None')

g_status = ax.text(0.03, 1.05, '', fontsize=22, color=(
    0.2, 0.2, 1.0), ha='left', va='center')
g_score = ax.text(0.53, 1.05, '', fontsize=22, color=(
    0.2, 0.2, 1.0), ha='left', va='center')
g_message = ax.text(0.50, 0.55, '', fontsize=88, color=(
    1.0, 0.6, 0.2), ha='center', va='center')

map_dim = 20
unit_dim = 0.05
world_boundary_x = [0., 1.]
world_boundary_y = [0., 1.]

game_status = 1
game_level = 1  # TODO:
game_score = 0
game_message = 'NEW GAME'
game_message_delay = 40


class sprite:
    def __init__(self):
        self.id = 0  # id number
        self.x, self.y = 0., 0.  # current position
        self.dx, self.dy = 0., 0.  # expected movement
        self.dir = 0  # direction of the sprite: 0 - stop / 1 - down / 2 - up / 3 - left / 4 - right
        self.step = 0  # remaining steps
        self.hp = 1  # hit point
        self.charge = 0  # frames before shooting
        self.type = 0  # type of sprite: 0 - bullet, 1 - block, 2 - mine, 3 - tank, 4 - rescure cap
        # 0 - user control, 1 - up/down, 2 - left/right, 3 - random, 4 - tracking
        self.control_opt = 0
        self.status = 1  # 0 - dead, 1 - active

    def detect_collision(self, sp):
        if (sp.type == 0 or self.type == 0):
            if (abs(sp.x-self.x) < unit_dim*0.499 and abs(sp.y-self.y) < unit_dim*0.499):
                return True
        else:
            if (abs(sp.x-self.x) < unit_dim*0.998 and abs(sp.y-self.y) < unit_dim*0.998):
                return True
        return False


splist_static, splist_tank, splist_bullet, splist_bullet_ply, splist_explosion = [], [], [], [], []


def init_level():
    global map_dim, unit_dim, world_boundary_x, world_boundary_y
    global game_status, game_level, game_score, game_message, game_message_delay
    global splist_static, splist_tank, splist_bullet, splist_bullet_ply, splist_explosion

    # preserve player hp to next level
    player_hp = 8  # TODO:
    for sp in splist_tank:
        if (sp.control_opt == 0):
            player_hp = sp.hp
            break

    splist_static, splist_tank, splist_bullet, splist_bullet_ply, splist_explosion = [], [], [], [], []

    nblocks = 22+game_level*3//2
    nmines = 2+game_level
    if (game_level > 10):
        nmines = 12
    ntanks = 2+game_level*2//3
    if (game_level > 10):
        ntanks = 8-(game_level-10)//2
    ntanks_agg = game_level//2
    ncapsules = 1+game_level//2
    map = np.zeros((map_dim, map_dim), dtype='int32')

    # blocks
    for it in range(nblocks):
        h = rnd.randint(1, 4)
        r = rnd.randint(0, map_dim-2)
        c = rnd.randint(0, map_dim-2)
        map[r+0, c+0] = h
        map[r+1, c+0] = h
        map[r+0, c+1] = h
        map[r+1, c+1] = h

    # preserved area
    map[0, 0] = map[1, 0] = map[2, 0] = 99
    map[0, 1] = map[1, 1] = map[2, 1] = 99
    map[0, 2] = map[1, 2] = map[2, 2] = 99
    # mines
    for it in range(nmines):
        while (True):
            r = rnd.randint(0, map_dim-1)
            c = rnd.randint(0, map_dim-1)
            if (map[r, c] == 0):
                map[r, c] = 10
                break
    # tanks
    for it in range(ntanks):
        while (True):
            r = rnd.randint(0, map_dim-1)
            c = rnd.randint(0, map_dim-1)
            if (map[r, c] == 0 and (r > map_dim//2 or c > map_dim//2)):
                map[r, c] = 20
                break
    # aggressive tanks
    for it in range(ntanks_agg):
        while (True):
            r = rnd.randint(0, map_dim-1)
            c = rnd.randint(0, map_dim-1)
            if (map[r, c] == 0 and (r > map_dim//2 or c > map_dim//2)):
                map[r, c] = 21
                break
    # rescue capsules
    for it in range(ncapsules):
        while (True):
            r = rnd.randint(0, map_dim-1)
            c = rnd.randint(0, map_dim-1)
            if (map[r, c] == 0):
                map[r, c] = 30
                break

    serial_id = 1

    # user control tank
    player = sprite()
    player.id = serial_id
    serial_id += 1
    player.x = unit_dim*(0.5+1)
    player.y = unit_dim*(0.5+1)
    player.dir = 0
    player.type = 3
    player.hp = player_hp
    player.control_opt = 0
    splist_tank.append(player)

    for r in range(map_dim):
        for c in range(map_dim):
            if (map[r, c] > 0 and map[r, c] < 10):
                block = sprite()
                block.id = serial_id
                serial_id += 1
                block.x = unit_dim*(0.5+c)
                block.y = unit_dim*(0.5+r)
                block.type = 1
                block.hp = map[r, c]
                splist_static.append(block)
            elif (map[r, c] == 10):
                mine = sprite()
                mine.id = serial_id
                serial_id += 1
                mine.x = unit_dim*(0.5+c)
                mine.y = unit_dim*(0.5+r)
                mine.type = 2
                splist_static.append(mine)
            elif (map[r, c] == 20 or map[r, c] == 21):
                tank = sprite()
                tank.id = serial_id
                serial_id += 1
                tank.x = unit_dim*(0.5+c)
                tank.y = unit_dim*(0.5+r)
                tank.dir = 0
                tank.type = 3
                if (map[r, c] == 20):
                    tank.hp = 2
                    if (game_level <= 3):
                        tank.control_opt = rnd.randint(1, 2)
                    else:
                        tank.control_opt = rnd.randint(1, 3)
                elif (map[r, c] == 21):
                    tank.hp = 3
                    tank.control_opt = 4
                splist_tank.append(tank)
            elif (map[r, c] == 30):
                capsule = sprite()
                capsule.id = serial_id
                serial_id += 1
                capsule.x = unit_dim*(0.5+c)
                capsule.y = unit_dim*(0.5+r)
                capsule.type = 4
                splist_static.append(capsule)


def init():
    global g_block0, g_block1, g_block2, g_block3
    global g_mine, g_tank, g_tank_agg, g_tank_ply, g_capsule
    global g_bullet, g_bullet_ply, g_explosion
    global g_status, g_score, g_message

    g_block0.set_data([], [])
    g_block1.set_data([], [])
    g_block2.set_data([], [])
    g_block3.set_data([], [])
    g_mine.set_data([], [])
    g_tank.set_data([], [])
    g_tank_agg.set_data([], [])
    g_tank_ply.set_data([], [])
    g_capsule.set_data([], [])
    g_bullet.set_data([], [])
    g_bullet_ply.set_data([], [])
    g_explosion.set_data([], [])

    g_status.set(text='')
    g_score.set(text='')
    g_message.set(text='')

    return g_block0, g_block1, g_block2, g_block3, g_mine, g_tank, g_tank_agg, g_tank_ply, g_capsule, g_bullet, g_bullet_ply, g_explosion, g_status, g_score, g_message


def animate(frame):
    global g_block0, g_block1, g_block2, g_block3
    global g_mine, g_tank, g_tank_agg, g_tank_ply, g_capsule
    global g_bullet, g_bullet_ply, g_explosion
    global g_status, g_score, g_message
    global map_dim, unit_dim, world_boundary_x, world_boundary_y
    global game_status, game_level, game_score, game_message, game_message_delay
    global splist_static, splist_tank, splist_bullet, splist_bullet_ply, splist_explosion

    # tank decision
    for sp in splist_tank:
        if (sp.type == 3 and sp.step <= 0):
            act = 0
            shooting_rate = 0.1+0.02*game_level
            moving_rate = 0.5

            if (sp.control_opt == 0):

                p1_score = game_score
                p1_player_hp = sp.hp
                p1_player_status = 1
                if (sp.charge <= 0):
                    p1_player_status = 2
                p1_code = []
                p1_x, p1_y, p1_dx, p1_dy = [], [], [], []

                for op in splist_bullet_ply:
                    p1_code.append(0)
                    p1_x.append(op.x)
                    p1_y.append(op.y)
                    p1_dx.append(op.dx)
                    p1_dy.append(op.dy)

                for op in splist_bullet:
                    p1_code.append(1)
                    p1_x.append(op.x)
                    p1_y.append(op.y)
                    p1_dx.append(op.dx)
                    p1_dy.append(op.dy)

                for op in splist_tank:
                    if (op.control_opt == 0):
                        p1_code.append(2)
                    elif (op.control_opt == 4):
                        p1_code.append(4)
                    else:
                        p1_code.append(3)
                    p1_x.append(op.x)
                    p1_y.append(op.y)
                    p1_dx.append(op.dx)
                    p1_dy.append(op.dy)

                for op in splist_static:
                    if (op.type == 1):
                        p1_code.append(5)
                    elif (op.type == 2):
                        p1_code.append(6)
                    elif (op.type == 4):
                        p1_code.append(7)
                    p1_x.append(op.x)
                    p1_y.append(op.y)
                    p1_dx.append(op.dx)
                    p1_dy.append(op.dy)

                act = P1.decision(
                    p1_score, p1_player_hp, p1_player_status, p1_code, p1_x, p1_y, p1_dx, p1_dy)
                if (type(act) != type(1)):
                    act = 0
                if (act < 0 or act > 8):
                    act = 0
                if (sp.charge > 0 and act >= 5 and act <= 8):
                    act = 0

            elif (sp.control_opt == 1):

                if (sp.charge <= 0):  # can shoot can move
                    if (rnd.uniform() < shooting_rate):
                        act = rnd.randint(5, 6)  # shoot
                else:  # can move but cannot shoot
                    if (rnd.uniform() < moving_rate):
                        act = rnd.randint(1, 2)  # move

            elif (sp.control_opt == 2):

                if (sp.charge <= 0):  # can shoot can move
                    if (rnd.uniform() < shooting_rate):
                        act = rnd.randint(7, 8)  # shoot
                else:  # can move but cannot shoot
                    if (rnd.uniform() < moving_rate):
                        act = rnd.randint(3, 4)  # move

            elif (sp.control_opt == 3):

                if (sp.charge <= 0):  # can shoot can move
                    if (rnd.uniform() < shooting_rate):
                        act = rnd.randint(5, 8)  # shoot
                else:  # can move but cannot shoot
                    if (rnd.uniform() < moving_rate):
                        act = rnd.randint(1, 4)  # move

            elif (sp.control_opt == 4):

                if (sp.charge <= 0):  # can shoot can move
                    if (rnd.uniform() < shooting_rate):
                        act = rnd.randint(5, 8)
                        for op in splist_tank:
                            if (op.control_opt != 0):
                                continue
                            if (abs(op.x-sp.x) < abs(op.y-sp.y)):
                                if (op.y < sp.y):
                                    act = 5
                                else:
                                    act = 6
                            else:
                                if (op.x < sp.x):
                                    act = 7
                                else:
                                    act = 8
                else:  # can move but cannot shoot
                    if (rnd.uniform() < moving_rate):
                        act = rnd.randint(1, 4)
                        for op in splist_tank:
                            if (op.control_opt != 0):
                                continue
                            if (abs(op.x-sp.x) < abs(op.y-sp.y)):
                                if (op.y < sp.y):
                                    act = 1
                                else:
                                    act = 2
                            else:
                                if (op.x < sp.x):
                                    act = 3
                                else:
                                    act = 4

            if (act >= 5 and act <= 8):
                bullet = sprite()
                bullet.x = sp.x
                bullet.y = sp.y
                bullet.dir = act-4
                bullet.step = 5
                if (bullet.dir == 1):
                    bullet.dy = -unit_dim/bullet.step
                if (bullet.dir == 2):
                    bullet.dy = +unit_dim/bullet.step
                if (bullet.dir == 3):
                    bullet.dx = -unit_dim/bullet.step
                if (bullet.dir == 4):
                    bullet.dx = +unit_dim/bullet.step
                if (sp.control_opt == 0):
                    splist_bullet_ply.append(bullet)
                else:
                    splist_bullet.append(bullet)
                if (sp.control_opt == 0 or sp.control_opt == 4):
                    sp.charge = 20
                else:
                    sp.charge = 40
            elif (act >= 1 and act <= 4):
                sp.dir = act
                if (sp.control_opt == 0 or sp.control_opt == 4):
                    sp.step = 10
                else:
                    sp.step = 20
                sp.dx = sp.dy = 0.
                if (sp.dir == 1):
                    sp.dy = -unit_dim/sp.step
                if (sp.dir == 2):
                    sp.dy = +unit_dim/sp.step
                if (sp.dir == 3):
                    sp.dx = -unit_dim/sp.step
                if (sp.dir == 4):
                    sp.dx = +unit_dim/sp.step

                # regularizing the positions, to avoid round-off problems
                min_diff, min_reg = -1., -1.
                for i in range(map_dim):
                    reg = unit_dim*(0.5+i)
                    diff = abs(reg-sp.x)
                    if (min_diff < 0. or diff < min_diff):
                        min_reg = reg
                        min_diff = diff
                sp.x = min_reg

                min_diff, min_reg = -1., -1.
                for i in range(map_dim):
                    reg = unit_dim*(0.5+i)
                    diff = abs(reg-sp.y)
                    if (min_diff < 0. or diff < min_diff):
                        min_reg = reg
                        min_diff = diff
                sp.y = min_reg

    # tank action
    for sp in splist_tank:
        if (sp.type == 3):
            if (sp.step > 0):
                sp.x += sp.dx
                sp.y += sp.dy
                collision = False
                for op in splist_static:
                    if (op.type == 1 and sp.detect_collision(op)):
                        collision = True
                        break
                    elif (op.type == 2 and sp.detect_collision(op)):
                        sp.hp -= 1
                        game_score += 50
                        if (sp.hp <= 0):
                            sp.status = 0
                        op.status = 0

                        for i in range(3):
                            explosion = sprite()
                            explosion.x = op.x + \
                                rnd.uniform(-0.3*unit_dim, +0.3*unit_dim)
                            explosion.y = op.y + \
                                rnd.uniform(-0.3*unit_dim, +0.3*unit_dim)
                            explosion.hp = rnd.randint(5, 9)
                            splist_explosion.append(explosion)

                    elif (op.type == 4 and sp.control_opt == 0 and sp.detect_collision(op)):
                        sp.hp += 2
                        if (sp.hp > 16):
                            sp.hp = 16
                        game_score += 100
                        op.status = 0

                if (sp.x-unit_dim*0.499 < world_boundary_x[0]):
                    collision = True
                if (sp.y-unit_dim*0.499 < world_boundary_y[0]):
                    collision = True
                if (sp.x+unit_dim*0.499 > world_boundary_x[1]):
                    collision = True
                if (sp.y+unit_dim*0.499 > world_boundary_y[1]):
                    collision = True
                if (collision):  # move back
                    sp.x -= sp.dx
                    sp.y -= sp.dy
                sp.step -= 1

            if (sp.charge > 0):
                sp.charge -= 1

    # bullet action
    for sp in splist_bullet:
        sp.x += sp.dx
        sp.y += sp.dy
        collision = False
        for op in splist_tank:
            if (op.control_opt != 0):
                continue
            if (sp.detect_collision(op)):
                collision = True
                op.hp -= 1
                if (op.hp <= 0):
                    op.status = 0

        for op in splist_static:
            if (op.type == 1 and sp.detect_collision(op)):
                collision = True
                op.hp -= 1
                if (op.hp <= 0):
                    op.status = 0

        if (collision):
            for i in range(3):
                explosion = sprite()
                explosion.x = sp.x+rnd.uniform(-0.3*unit_dim, +0.3*unit_dim)
                explosion.y = sp.y+rnd.uniform(-0.3*unit_dim, +0.3*unit_dim)
                explosion.hp = rnd.randint(5, 9)
                splist_explosion.append(explosion)

        if (sp.x < world_boundary_x[0]):
            collision = True
        if (sp.y < world_boundary_y[0]):
            collision = True
        if (sp.x > world_boundary_x[1]):
            collision = True
        if (sp.y > world_boundary_y[1]):
            collision = True
        if (collision):
            sp.status = 0

    # player bullet action
    for sp in splist_bullet_ply:
        sp.x += sp.dx
        sp.y += sp.dy
        collision = False
        for op in splist_tank:
            if (op.control_opt == 0):
                continue
            if (sp.detect_collision(op)):
                collision = True
                op.hp -= 1
                game_score += 10
                if (op.hp <= 0):
                    op.status = 0
                    game_score += 1000
                    if (op.control_opt == 4):
                        game_score += 1000

        for op in splist_static:
            if (op.type == 1 and sp.detect_collision(op)):
                collision = True
                op.hp -= 1
                game_score += 10
                if (op.hp <= 0):
                    op.status = 0

        if (collision):
            for i in range(3):
                explosion = sprite()
                explosion.x = sp.x+rnd.uniform(-0.3*unit_dim, +0.3*unit_dim)
                explosion.y = sp.y+rnd.uniform(-0.3*unit_dim, +0.3*unit_dim)
                explosion.hp = rnd.randint(5, 9)
                splist_explosion.append(explosion)

        if (sp.x < world_boundary_x[0]):
            collision = True
        if (sp.y < world_boundary_y[0]):
            collision = True
        if (sp.x > world_boundary_x[1]):
            collision = True
        if (sp.y > world_boundary_y[1]):
            collision = True
        if (collision):
            sp.status = 0

    # bullet hit action
    for sp in splist_explosion:
        if (sp.hp <= 0):
            sp.status = 0
        else:
            sp.hp -= 1

    # clean up "dead" objects
    tmp = []
    for sp in splist_bullet:
        if (sp.status != 0):
            tmp.append(sp)
    splist_bullet = tmp
    tmp = []
    for sp in splist_bullet_ply:
        if (sp.status != 0):
            tmp.append(sp)
    splist_bullet_ply = tmp
    tmp = []
    for sp in splist_static:
        if (sp.status != 0):
            tmp.append(sp)
    splist_static = tmp
    tmp = []
    for sp in splist_tank:
        if (sp.status != 0):
            tmp.append(sp)
    splist_tank = tmp
    tmp = []
    for sp in splist_explosion:
        if (sp.status != 0):
            tmp.append(sp)
    splist_explosion = tmp

    game_status = 0  # check if game over
    for sp in splist_tank:
        if (sp.control_opt == 0):
            game_status = 1
    if (game_status == 0):
        game_message = 'GAME OVER'
        game_message_delay = -1

    if (len(splist_tank) == 1 and splist_tank[0].control_opt == 0):  # level up
        if (game_level < 20):
            game_level += 1
            game_message = 'LEVEL %d' % game_level
        else:
            game_message = 'LV MASTER'
        game_message_delay = 40
        init_level()

    # static objects
    vx, vy = [], []
    for sp in splist_static:
        if (sp.type == 1 and sp.hp == 1):
            vx.append(sp.x)
            vy.append(sp.y)
    g_block0.set_data(vx, vy)
    vx, vy = [], []
    for sp in splist_static:
        if (sp.type == 1 and sp.hp == 2):
            vx.append(sp.x)
            vy.append(sp.y)
    g_block1.set_data(vx, vy)
    vx, vy = [], []
    for sp in splist_static:
        if (sp.type == 1 and sp.hp == 3):
            vx.append(sp.x)
            vy.append(sp.y)
    g_block2.set_data(vx, vy)
    vx, vy = [], []
    for sp in splist_static:
        if (sp.type == 1 and sp.hp == 4):
            vx.append(sp.x)
            vy.append(sp.y)
    g_block3.set_data(vx, vy)
    vx, vy = [], []
    for sp in splist_static:
        if (sp.type == 2):
            vx.append(sp.x)
            vy.append(sp.y)
    g_mine.set_data(vx, vy)
    vx, vy = [], []
    for sp in splist_static:
        if (sp.type == 4):
            vx.append(sp.x)
            vy.append(sp.y)
    g_capsule.set_data(vx, vy)

    # tank
    status_str = 'HP '
    vx, vy = [], []
    for sp in splist_tank:
        if (sp.type == 3 and (sp.control_opt == 1 or sp.control_opt == 2 or sp.control_opt == 3)):
            vx.append(sp.x)
            vy.append(sp.y)
    g_tank.set_data(vx, vy)
    vx, vy = [], []
    for sp in splist_tank:
        if (sp.type == 3 and sp.control_opt == 4):
            vx.append(sp.x)
            vy.append(sp.y)
    g_tank_agg.set_data(vx, vy)
    vx, vy = [], []
    for sp in splist_tank:
        if (sp.type == 3 and sp.control_opt == 0):
            vx.append(sp.x)
            vy.append(sp.y)
            # for i in range(sp.hp): status_str = status_str+'|'
            status_str += str(sp.hp)  # TODO: changed
    g_tank_ply.set_data(vx, vy)

    g_status.set(text=status_str)
    g_score.set(text='Score %d' % game_score)

    # bullet
    vx, vy = [], []
    for sp in splist_bullet:
        vx.append(sp.x)
        vy.append(sp.y)
    g_bullet.set_data(vx, vy)

    # player bullet
    vx, vy = [], []
    for sp in splist_bullet_ply:
        vx.append(sp.x)
        vy.append(sp.y)
    g_bullet_ply.set_data(vx, vy)

    # bullet hit
    vx, vy = [], []
    for sp in splist_explosion:
        vx.append(sp.x)
        vy.append(sp.y)
    g_explosion.set_data(vx, vy)

    if (game_message_delay > 0 or game_message_delay < 0):
        g_message.set(text=game_message)
        if (game_message_delay > 0):
            game_message_delay -= 1

    return g_block0, g_block1, g_block2, g_block3, g_mine, g_tank, g_tank_agg, g_tank_ply, g_capsule, g_bullet, g_bullet_ply, g_explosion, g_status, g_score, g_message


init_level()

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=10, interval=2)
plt.show()
