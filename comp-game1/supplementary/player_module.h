#include <vector>

class player_module {
public:
    double player_x, player_y;
    
    // Constructor, allocate any private date here
    player_module() : player_x(0.), player_y(0.) {}
    
    // Please update the banner according to your information
    void banner() {
        printf("------------------------\n");
        printf("Author: your_name_here\n");
        printf("ID: bxxxxxxxx\n");
        printf("------------------------\n");
    }

/*  Decision making function for moving your tank, toward next decision frame:
    simply return an integer as
    0 - standby
    1 - move down  (y -)
    2 - move up    (y +)
    3 - move left  (x -)
    4 - move right (x +)
    5 - cannon fire down
    6 - cannon fire up
    7 - cannon fire left
    8 - cannon fire right
    ------------------------
    The input arguments consist of
    score = current score
    player_hp = current hp
    player_status
        1 - can only move [hence you can only return 1-4]
        2 - can move / can fire cannon [hence you can return 1-4 or 5-8]
    code = type of objects
        0 - your cannon-shot
        1 - enemy's cannon-shot
        2 - player tank
        3 - enemy tank
        4 - enemy tank (stronger)
        5 - block
        6 - mine
        7 - rescue capsule
    x,y,dx,dy = coordinate of the objects, and current displacement
 */
    int decision(int score, int player_hp, int player_status,
                 std::vector<int> &code,
                 std::vector<double> &x, std::vector<double> &y,
                 std::vector<double> &dx, std::vector<double> &dy) {
        
        // update player location
        for(int i=0;i<static_cast<int>(code.size());++i) {
            if (code[i]==2) {
                player_x = x[i];
                player_y = y[i];
                break;
            }
        }
        
        // look for the closest emeny tank
        double closest_x(0.), closest_y(0.);
        double min_dist = -1.;
        for(int i=0;i<static_cast<int>(code.size());++i) {
            if (code[i]==3 || code[i]==4) {
                double dist = pow(x[i]-player_x,2)+pow(y[i]-player_y,2);
                if (min_dist<0. || dist<min_dist) {
                    min_dist = dist;
                    closest_x = x[i];
                    closest_y = y[i];
                }
            }
        }
        // decision making
        int act = 0;
        if (player_status==1) {
            if (fabs(closest_x-player_x)<fabs(closest_y-player_y)) {
                if (closest_y<player_y) act = 1;
                else act = 2;
            }else {
                if (closest_x<player_x) act = 3;
                else act = 4;
            }
        }else {
            if (fabs(closest_x-player_x)<fabs(closest_y-player_y)) {
                if (closest_y<player_y) act = 5;
                else act = 6;
            }else {
                if (closest_x<player_x) act = 7;
                else act = 8;
            }
        }
        return act;
    }
};
