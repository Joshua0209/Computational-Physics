import numpy as np

class player_module:

    # Constructor, allocate any private date here
    def __init__(self):
        self.player_x, self.player_y = 0., 0.
    
    # Please update the banner according to your information
    def banner(self):
        print('------------------------')
        print('Author: 吳尚謙')
        print('ID: b10202028')
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
                dx=dx[i]
                dy=dy[i]
                break        
        closest_x, closest_y = 0., 0.
        closest_x2, closest_y2 = 0., 0.
        closest_x3, closest_y3 = 0., 0.
        closest_x4, closest_y4 = 0., 0.
        closest_x5, closest_y5 = 0., 0.
        closest_x6, closest_y6 = 0., 0.
        closest_x7, closest_y7 = 0., 0.
        closest_x8, closest_y8 = 0., 0.
        a=0.
        b=0.
        a2=0.
        b2=0.
        min_dist = -1.
        min_dist2=-1.
        min_dist3=-1.
        min_dist4=-1.
        min_dist5=-1.

        min_dist6=-1.
        min_dist7=100
        min_dist8=100
        for i in range(len(code)):
            if (code[i]==3 or code[i]==4 ):
                dist = (x[i]-player_x)**2+(y[i]-player_y)**2
                if (min_dist<0. or dist<min_dist ):
                    min_dist = dist
                    
                    closest_x = x[i]
                    closest_y = y[i]
        for i in range(len(code)):
            if (code[i]==0):
                dist6 = (x[i]-player_x)**2+(y[i]-player_y)**2
                if (min_dist6<0. or dist6<min_dist6 ):
                    min_dist6 = dist6
                    closest_x6 = x[i]
                    closest_y6 = y[i]
        #closest shot
        for i in range(len(code)):
            if(code[i]==1):
                dist2 = (x[i]-player_x)**2+(y[i]-player_y)**2
                if (min_dist2<0. or dist2<min_dist2 ):
                    min_dist2 = dist2
                    a=closest_x2-x[i]
                    b=closest_y2-y[i]
                    closest_x2 = x[i]
                    closest_y2 = y[i]
        for i in range(len(code)):
            if(code[i]==1):
                dist7 = (x[i]-player_x)**2+(y[i]-player_y)**2
                if (dist7>dist2 and dist2<min_dist7 ):
                    min_dist7 = dist7
                    a2=closest_x7-x[i]
                    b2=closest_y7-y[i]
                    closest_x7 = x[i]
                    closest_y7 = y[i]            
        #closest block         
        for i in range(len(code)):
            if (code[i]==5):
                dist3 = (x[i]-player_x)**2+(y[i]-player_y)**2
                if (min_dist3<0. or dist3<min_dist3 ):
                    min_dist3 = dist3
                    closest_x3 = x[i]
                    closest_y3 = y[i]
        for i in range(len(code)):
            if (code[i]==5):
                dist8 = (x[i]-player_x)**2+(y[i]-player_y)**2
                if (dist8>dist3 and dist8<min_dist8 ):
                    min_dist8 = dist8
                    closest_x8 = x[i]
                    closest_y8 = y[i]
        #closest resue
        for i in range(len(code)):
            if (code[i]==7):
                dist4 = (x[i]-player_x)**2+(y[i]-player_y)**2
                if (min_dist4<0. or dist4<min_dist4 ):
                    min_dist4 = dist4
                    closest_x4 = x[i]
                    closest_y4 = y[i]
        #closest mine
        for i in range(len(code)):
            if (code[i]==6):
                dist5 = (x[i]-player_x)**2+(y[i]-player_y)**2
                if (min_dist5<0. or dist5<min_dist5 ):
                    min_dist5 = dist5
                    closest_x5 = x[i]
                    closest_y5 = y[i]
        # decision making
        act = 0
        if (player_status==1):
            if ((abs(closest_x-player_x)**2+abs(closest_y-player_y)**2)**(1/2)<0.09 ):
                if (abs(closest_x-player_x)>=abs(closest_y-player_y)):
                    if(closest_y-player_y>0.):
                        if(0.3>closest_y-player_y>=0.):
                            act=1

                    elif(closest_y-player_y<-0.):
                        if(-0.3<closest_y-player_y<=-0.):
                            act=2

                    else:
                        if(0.03>closest_x-player_x>=0.0 ):
                            if((abs(closest_y3-player_y)==0 and (closest_x3-player_x)>-0.07) or (abs(closest_y8-player_y)==0 and (closest_x8-player_x)>-0.07) or player_x<0.1):
                                act=4
                            else:
                                act=3
                        elif(-0.03<closest_x-player_x<=-0.0 ):
                            if((abs(closest_y3-player_y)==0 and (closest_x3-player_x)<0.07) or (abs(closest_y8-player_y)==0 and (closest_x8-player_x)<0.07) or player_x>0.9):
                                 act=3
                            else:
                                act=4
                        else:
                            if((abs(closest_x3-player_x)==0 and (closest_y3-player_y)<0.07) or (abs(closest_x8-player_x)==0 and (closest_y8-player_y)<0.07)):
                                 act=1
                            elif((abs(closest_x3-player_x)==0 and (closest_y3-player_y)>-0.07) or (abs(closest_x3-player_x)==0 and (closest_y3-player_y)>-0.07)):
                                 act=2
                            else:
                                if(closest_x4!=0 and closest_y4!=0 ):
                                    if (closest_y4<player_y):
                                        act = 1
                                    else:
                                        act = 2
                                    
                                elif(player_y==0.025):
                                    if(abs(closest_y3-player_y)==0 and (closest_x3-player_x)<0.07):
                                         act=3
                                    elif(abs(closest_y3-player_y)==0 and (closest_x3-player_x)>-0.07):
                                         act=4
                                    else:
                                        if(player_x>0.5):
                                            act=3
                                        else:
                                            act=4
                                else:
                                    if(player_y>0.5):
                                            act=1
                                    else:
                                            act=2
                                
                                
                elif(abs(closest_x-player_x)<abs(closest_y-player_y)):
                    if(closest_x-player_x>0.):
                        if(0.3>closest_x-player_x>=0.0 ):
                            act=3

                    elif(closest_x-player_x<-0.):
                        if(-0.3<closest_x-player_x<=-0.0 ):
                            act=4

                    else:
                        if(0.03>closest_y-player_y>=0.0 ):
                            if((abs(closest_x3-player_x)==0 and (closest_y3-player_y)>-0.07) or (abs(closest_x3-player_x)==0 and (closest_y3-player_y)>-0.07) or player_y<0.1) :
                                act=2
                            else:
                                act=1
                        elif(-0.03<closest_y-player_y<=-0.0 ):
                            if((abs(closest_x3-player_x)==0 and (closest_y3-player_y)<0.07) or (abs(closest_x8-player_x)==0 and (closest_y8-player_y)<0.07) or player_y>0.9):
                                act=1
                            else:
                                act=2
                        else:
                            if((abs(closest_y3-player_y)==0 and (closest_x3-player_x)<0.07) or (abs(closest_y8-player_y)==0 and (closest_x8-player_x)<0.07)):
                                 act=3
                            elif((abs(closest_y3-player_y)==0 and (closest_x3-player_x)>-0.07) or (abs(closest_y8-player_y)==0 and (closest_x8-player_x)>-0.07)):
                                 act=4
                            else:                            
                                if(closest_x4!=0 and closest_y4!=0  ):
                                    if (closest_x4<player_x):
                                        act = 3
                                    else:
                                        act =4
                                elif(player_x==0.025):
                                    if((abs(closest_x3-player_x)==0 and (closest_y3-player_y)<0.07) or (abs(closest_x8-player_x)==0 and (closest_y8-player_y)<0.07)):
                                         act=1
                                    elif((abs(closest_x3-player_x)==0 and (closest_y3-player_y)>-0.07) or (abs(closest_x3-player_x)==0 and (closest_y3-player_y)>-0.07)) :
                                         act=2
                                    else:                                        
                                        if(player_y>0.5):
                                            act=1
                                        else:
                                            act=2
                                else:
                                    if(player_x>0.5):
                                        act=3
                                    else:
                                        act=4
                                

                        
            else:        
                if(closest_x4!=0 and closest_y4!=0 and 0.<=abs(closest_x4-player_x)<0.3 and 0.<=abs(closest_y4-player_y)<0.3 and player_hp!=16):
                    if (abs(closest_x4-player_x)<=abs(closest_y4-player_y)):
                        if (closest_y4<player_y):
                            act = 1
                        else:
                            act = 2
                    elif(abs(closest_x4-player_x)>=abs(closest_y4-player_y)):
                        if (closest_x4<player_x):
                            act = 3
                        else:
                            act =4
                else:
                    if (0.09<(abs(closest_x-player_x)**2+abs(closest_y-player_y)**2)**(1/2)<0.3):                                    
                        if (abs(closest_x-player_x)<=abs(closest_y-player_y)):
                            if(closest_x-player_x>0.025): 
                                act=4
                            elif(closest_x-player_x<-0.025):
                                act=3
                            else:
                                if(0.3>closest_y-player_y>0.025 ):
                                    act=1
                                elif(-0.3<closest_y-player_y<-0.025 ):
                                    act=2
                        elif(abs(closest_x-player_x)>abs(closest_y-player_y) ):
                            if(closest_y-player_y>0.025):
                                act=2
                            elif(closest_y-player_y<-0.025):
                                act=1
                            else:
                                if(0.3>closest_x-player_x>0.025 ):
                                    act=3
                                elif(-0.3<closest_x-player_x<-0.025 ):
                                    act=4
                    else:
                        if(closest_x4!=0 and closest_y4!=0 and 0.<=abs(closest_x4-player_x)<1.0 and 0.<=abs(closest_y4-player_y)<1.0 and player_hp!=16):
                            if (abs(closest_x4-player_x)<=abs(closest_y4-player_y)):
                                if (closest_y4<player_y):
                                    act = 1
                                else:
                                    act = 2
                            elif(abs(closest_x4-player_x)>=abs(closest_y4-player_y)):
                                if (closest_x4<player_x):
                                    act = 3
                                else:
                                    act =4
                        else:
                            if (abs(closest_x-player_x)<=abs(closest_y-player_y)):
                                if (closest_y<player_y):
                                    act = 1
                                else:
                                    act = 2
                            elif (abs(closest_x-player_x)>=abs(closest_y-player_y)):
                                if (closest_x<player_x):
                                    act = 3
                                else:
                                    act =4
                    #excape mine
            while ((abs(closest_x5-player_x)==0 and abs(closest_y5-player_y)<=0.07) or (abs(closest_y5-player_y)==0 and abs(closest_x5-player_x)<=0.07 )):
                if(abs(closest_x5-player_x)==0 and abs(closest_y5-player_y)<=0.07):
                    if((act== 2 and 0<closest_y5-player_y <=0.07) or (act==1 and 0>closest_y5-player_y >=-0.07)):
                        if((closest_x4-player_x)>0):
                            act=4
                        elif((closest_x4-player_x)<0):
                            act=3
                        else:
                            if((closest_x6-player_x)>0):
                                act=4
                            elif((closest_x6-player_x)<0):
                                act=3
                            else:
                                if(player_x>0.5):
                                    act=3
                                else:
                                    act=4
                        break
                    else:
                        act=act
                        break
                elif(abs(closest_y5-player_y)==0 and abs(closest_x5-player_x)<=0.07):
                    if((act==4 and 0<closest_x5-player_x <=0.07) or (act==3 and 0>closest_x5-player_x >=-0.07)):
                        if((closest_y4-player_y)>0):
                            act=2
                        elif((closest_y4-player_y)<0):
                            act=1
                        else:
                            if((closest_y6-player_y)>0):
                                act=2
                            elif((closest_y6-player_y)<0):
                                act=1
                            else:
                                if(player_y>0.5):
                                    act=1
                                else:
                                    act=2
                        break
                    else:
                        act=act
                        break
            #escape bullet            
            
        else:
            
                if ((abs(closest_x-player_x)<0.05 or abs(closest_y-player_y)<0.05) and (abs(closest_x-player_x)**2+abs(closest_y-player_y)**2)**(1/2)<0.3):
                    if(abs(closest_x-player_x)<0.05 and abs(closest_y-player_y)<0.05):
                        if (abs(closest_x-player_x)<abs(closest_y-player_y)):
                            if (closest_y<player_y):
                                act = 5
                            else:
                                act = 6
                        else:
                            if (closest_x<player_x):
                                act = 7
                            else:
                                act = 8
                    elif (abs(closest_x-player_x)<0.05):
                        if (closest_y<player_y):
                            act = 5
                        else:
                            act = 6
                    else:
                        if (closest_x<player_x):
                            act = 7
                        else:
                            act = 8
                
                else:
                    if ((abs(closest_x3-player_x)**2+abs(closest_y3-player_y)**2)**(1/2)<0.07 and abs(closest_x3-player_x)<=abs(closest_y3-player_y)):
                        if (-0.07<closest_y3-player_y<0):
                            act = 5
                        elif (0<closest_y3-player_y<0.07):
                            act = 6
                        else:
                            if (abs(closest_x-player_x)<abs(closest_y-player_y)):
                                if (closest_y<player_y):
                                    act = 5
                                else:
                                    act = 6
                            else:
                                if (closest_x<player_x):
                                    act = 7
                                else:
                                    act = 8
                                        
                                    
                    elif((abs(closest_x3-player_x)**2+abs(closest_y3-player_y)**2)**(1/2)<0.07 and abs(closest_x3-player_x)>=abs(closest_y3-player_y)):
                        if (-0.07<closest_x3-player_x<0):
                            act = 7
                        elif (0<closest_x3-player_x<0.07):
                            act = 8
                        else:
                            if (abs(closest_x-player_x)<abs(closest_y-player_y)):
                                if (closest_y<player_y):
                                    act = 5
                                else:
                                    act = 6
                            else:
                                if (closest_x<player_x):
                                    act = 7
                                else:
                                    act = 8
                    else:
                        if (abs(closest_x-player_x)<abs(closest_y-player_y)):
                            if (closest_y<player_y):
                                act = 5
                            else:
                                act = 6
                        else:
                            if (closest_x<player_x):
                                act = 7
                            else:
                                act = 8


        #escape bullet
        while((abs(closest_x2-player_x)**2+abs(closest_y2-player_y)**2 )**(1/2)<0.25 and (abs(closest_x-player_x)**2+abs(closest_y-player_y)**2)**(1/2)>0.09 ):
                    if((0.10>closest_y2-player_y>0.015 or 0.10>closest_y7-player_y>0.015) and act==2):
                            if( -0.05>closest_x7-player_x>=-0.13 ):
                                act=4
                            elif(0.05<closest_x7-player_x<=0.13 ):
                                act=3
                            else:
                                if(closest_x2-player_x>0):
                                    act=3
                                else:
                                    act=4
                            
                    elif((-0.10<closest_y2-player_y<-0.015 or -0.10<closest_y7-player_y<-0.015) and act==1):
                            if(-0.05>closest_x7-player_x>=-0.13 ):
                                act=4
                            elif(0.05<closest_x7-player_x<=0.13 ):
                                act=3
                            else:
                                if(closest_x2-player_x>0):
                                    act=3
                                else:
                                    act=4
                    elif((0.10>closest_x2-player_x>0.015 or 0.10>closest_x7-player_x>0.015) and act==4):
                            if(-0.05>closest_y7-player_y>=-0.13  ):
                                act=2
                            elif(0.05<closest_y7-player_y<=0.13 ):
                                act=1
                            else:
                                if(closest_y2-player_y>0):
                                    act=1
                                else:
                                    act=2
                            
                    elif((-0.10<closest_x2-player_x<-0.015 or -0.10<closest_x7-player_x<-0.015) and act==3):
                            if(-0.05>closest_y7-player_y>=-0.13 ):
                                act=2
                            elif(0.05<closest_y7-player_y<=0.13 ):
                                act=1
                            else:
                                if(closest_y2-player_y>0):
                                    act=1
                                else:
                                    act=2
                    elif(abs(closest_y2-player_y)<abs(closest_x2-player_x) ):                        
                        
                        if(abs(closest_y2-player_y)<=0.01):
                            if(closest_x2-player_x>=0.16 ):
                                act=3
                            elif(closest_x2-player_x<=-0.16 ):
                                act=4
                            else:
                                if((abs(closest_x3-player_x)==0 and (closest_y3-player_y)<0.07) or (abs(closest_x8-player_x)==0 and (closest_y8-player_y)<0.07)):
                                    act=1
                                elif((abs(closest_x3-player_x)==0 and (closest_y3-player_y)>-0.07) or (abs(closest_x3-player_x)==0 and (closest_y3-player_y)>-0.07)):
                                    act=2
                                else:
                                    if(0>=closest_y7-player_y>=-0.07 and a2!=0):
                                        act=2
                                    elif(player_y<0.1):
                                        act=2
                                    elif(0<=closest_y7-player_y<=0.07 and a2!=0):
                                        act=1
                                    else:
                                        if(player_y>0.5):
                                            act=1
                                        else:
                                            act=2
                            
                             
                                    
                    elif(abs(closest_y2-player_y)>=abs(closest_x2-player_x)):
                        
                            
                        if(abs(closest_x2-player_x)<=0.01):
                            if(closest_y2-player_y>=0.16 ):
                                act=1
                            elif(closest_y2-player_y<=-0.16 ):
                                act=2
                            else:
                                if((abs(closest_y3-player_y)==0 and (closest_x3-player_x)<0.07) or (abs(closest_y8-player_y)==0 and (closest_x8-player_x)<0.07)):
                                     act=3
                                elif((abs(closest_y3-player_y)==0 and (closest_x3-player_x)>-0.07) or(abs(closest_y8-player_y)==0 and (closest_x8-player_x)>-0.07)):
                                     act=4
                                else:
                                    if(0>=closest_x7-player_x>=-0.07 and b2!=0):
                                        act=4
                                    elif(player_x<0.1):
                                        act=4
                                    elif(0<=closest_x7-player_x<=0.07 and b2!=0):
                                        act=3
                                    
                                    else:
                                        if(player_x>0.5):
                                            act=3
                                        else:
                                            act=4
                                
                            
                            
                            
                    break

                
            
        return act
