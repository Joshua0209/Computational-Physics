import numpy as np

class player_module:

    # Constructor, allocate any private date here
    def __init__(self):
        self.player_x, self.player_y = 0., 0.
    
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
            if (code[i]==2):
                player_x = x[i]
                player_y = y[i]
                break
        
        # look for the closest emeny tank
        closest_x, closest_y = 0., 0.
        min_dist = -1.
        for i in range(len(code)):
            if (code[i]==3 or code[i]==4):
                dist = (x[i]-player_x)**2+(y[i]-player_y)**2
                if (min_dist<0. or dist<min_dist):
                    min_dist = dist
                    closest_x = x[i]
                    closest_y = y[i]

        # decision making
        act = 0
        if (player_status==1):
            if (abs(closest_x-player_x)<abs(closest_y-player_y)):
                if (closest_y<player_y): act = 1
                else: act = 2
            else:
                if (closest_x<player_x): act = 3
                else: act = 4
        else:
            if (abs(closest_x-player_x)<abs(closest_y-player_y)):
                if (closest_y<player_y): act = 5
                else: act = 6
            else:
                if (closest_x<player_x): act = 7
                else: act = 8
            
        return act
