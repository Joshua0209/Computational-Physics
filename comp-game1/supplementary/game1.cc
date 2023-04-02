// this code requires ROOT
#include <TROOT.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <TLine.h>
#include <TPolyMarker.h>
#include <TLatex.h>
#include <TTimer.h>
#include <TRandom3.h>
#include <TString.h>
#include <vector>
#include "player_module.h"

player_module P1;

TCanvas *g_canvas(0);
TH1F *g_frame(0);
TLatex *g_status(0);
TLatex *g_score(0);
TLatex *g_message(0);
TPolyMarker *g_block(0);
TPolyMarker *g_mine(0);
TPolyMarker *g_tank(0);
TPolyMarker *g_tank_agg(0);
TPolyMarker *g_tank_ply(0);
TPolyMarker *g_capsule(0);
TPolyMarker *g_bullet(0);
TPolyMarker *g_bullet_ply(0);
TPolyMarker *g_explosion(0);

class random_gen {
public:
    unsigned long long s1, s2;
    random_gen(unsigned long long seed = 12345678UL) {
        s1 = seed & 0xffffUL;
        s2 = (seed >> 16) & 0xffffUL;
        for(int i=0;i<20;++i) gen(); // warm up
    }
    unsigned int gen() {
        s1 = s1 ^ (s1 >> 17);
        s1 = s1 ^ (s1 << 31);
        s1 = s1 ^ (s1 >>  8);
        s2 = (s2 & 0xffffffffUL)*4294957665UL + (s2>>32);
        return static_cast<unsigned int>((s1 ^ s2) & 0xffffffffUL);
    }
    double uniform(double a = 0., double b = 1.) {
        return static_cast<double>(gen())/0xffffffff*(b-a)+a;
    }
    int randint(int a, int b) {
        return static_cast<int>(uniform(a,b+1.-1E-10));
    }
};

// let's use our own random generator
// replace time function to a fixed seed if needed
random_gen rnd(time(0));

const int map_dim = 20;
const double unit_dim = 0.05;
const double world_boundary_x[2] = {0.,1.};
const double world_boundary_y[2] = {0.,1.};

int game_status = 1;
int game_level = 1;
int game_score = 0;
TString game_message = "NEW GAME";
int game_message_delay = 40;

class sprite {
public:
    int id; // id number
    double x,y; // current position
    double dx,dy; // expected movement
    int dir; // direction of the sprite: 0 - stop / 1 - down / 2 - up / 3 - left / 4 - right
    int step; // remaining steps
    int hp; // hit point
    int charge; // frames before shooting
    int type; // type of sprite: 0 - bullet, 1 - block, 2 - mine, 3 - tank, 4 - rescure cap
    int control_opt; // 0 - user control, 1 - up/down, 2 - left/right, 3 - random, 4 - tracking
    int status; // 0 - dead, 1 - active
    
    sprite() {
        id = 0;
        x = y = 0.;
        dx = dy = 0.;
        dir = 0;
        step = 0;
        hp = 1;
        charge = 0;
        type = 0;
        control_opt = 0;
        status = 1;
    }
    
    bool detect_collision(sprite &sp) {
        if (sp.type==0 || type==0) {
            if (fabs(sp.x-x)<unit_dim*0.499 && fabs(sp.y-y)<unit_dim*0.499) return true;
        } else {
            if (fabs(sp.x-x)<unit_dim*0.998 && fabs(sp.y-y)<unit_dim*0.998) return true;
        }
        return false;
    }
};

std::vector<sprite> splist_static, splist_tank, splist_bullet, splist_bullet_ply, splist_explosion;

void init_level() {
    
    // preserve player hp to next level
    int player_hp = 8;
    for(auto& sp : splist_tank) {
        if (sp.control_opt==0) {
            player_hp = sp.hp;
            break;
        }
    }
    
    splist_static.clear();
    splist_tank.clear();
    splist_bullet.clear();
    splist_bullet_ply.clear();
    splist_explosion.clear();
    
    int nblocks = 22+game_level*3/2;
    int nmines = 2+game_level;
    if (game_level>10) nmines = 12;
    int ntanks = 2+game_level*2/3;
    if (game_level>10) ntanks = 8-(game_level-10)/2;
    int ntanks_agg = game_level/2;
    int ncapsules = 1+game_level/2;
    int map[map_dim][map_dim]{};
    
    // blocks
    for(int it=0;it<nblocks;++it) {
        int h = rnd.randint(1,4);
        int r = rnd.randint(0,map_dim-2);
        int c = rnd.randint(0,map_dim-2);
        map[r+0][c+0] = h;
        map[r+1][c+0] = h;
        map[r+0][c+1] = h;
        map[r+1][c+1] = h;
    }
    // preserved area
    map[0][0] = map[1][0] = map[2][0] = 99;
    map[0][1] = map[1][1] = map[2][1] = 99;
    map[0][2] = map[1][2] = map[2][2] = 99;
    // mines
    for(int it=0;it<nmines;++it) {
        while(1) {
            int r = rnd.randint(0,map_dim-1);
            int c = rnd.randint(0,map_dim-1);
            if (map[r][c]==0) {map[r][c] = 10; break;}
        }
    }
    // tanks
    for(int it=0;it<ntanks;++it) {
        while(1) {
            int r = rnd.randint(0,map_dim-1);
            int c = rnd.randint(0,map_dim-1);
            if (map[r][c]==0 && (r>map_dim/2 || c>map_dim/2)) {map[r][c] = 20; break;}
        }
    }
    // aggressive tanks
    for(int it=0;it<ntanks_agg;++it) {
        while(1) {
            int r = rnd.randint(0,map_dim-1);
            int c = rnd.randint(0,map_dim-1);
            if (map[r][c]==0 && (r>map_dim/2 || c>map_dim/2)) {map[r][c] = 21; break;}
        }
    }
    // rescue capsules
    for(int it=0;it<ncapsules;++it) {
        while(1) {
            int r = rnd.randint(0,map_dim-1);
            int c = rnd.randint(0,map_dim-1);
            if (map[r][c]==0) {map[r][c] = 30; break;}
        }
    }
    
    int serial_id = 1;
    
    // user control tank
    sprite player;
    player.id = serial_id++;
    player.x = unit_dim*(0.5+1);
    player.y = unit_dim*(0.5+1);
    player.dir = 0;
    player.type = 3;
    player.hp = player_hp;
    player.control_opt = 0;
    splist_tank.push_back(player);
    
    for(int r=0;r<map_dim;++r) {
        for(int c=0;c<map_dim;++c) {
            if (map[r][c]>0 && map[r][c]<10) {
                sprite block;
                block.id = serial_id++;
                block.x = unit_dim*(0.5+c);
                block.y = unit_dim*(0.5+r);
                block.type = 1;
                block.hp = map[r][c];
                splist_static.push_back(block);
            }else if (map[r][c]==10) {
                sprite mine;
                mine.id = serial_id++;
                mine.x = unit_dim*(0.5+c);
                mine.y = unit_dim*(0.5+r);
                mine.type = 2;
                splist_static.push_back(mine);
            }else if (map[r][c]==20 || map[r][c]==21) {
                sprite tank;
                tank.id = serial_id++;
                tank.x = unit_dim*(0.5+c);
                tank.y = unit_dim*(0.5+r);
                tank.dir = 0;
                tank.type = 3;
                if (map[r][c]==20) {
                    tank.hp = 2;
                    if (game_level<=3) tank.control_opt = rnd.randint(1,2);
                    else tank.control_opt = rnd.randint(1,3);
                } else if (map[r][c]==21) {
                    tank.hp = 3;
                    tank.control_opt = 4;
                }
                splist_tank.push_back(tank);
            }else if (map[r][c]==30) {
                sprite capsule;
                capsule.id = serial_id++;
                capsule.x = unit_dim*(0.5+c);
                capsule.y = unit_dim*(0.5+r);
                capsule.type = 4;
                splist_static.push_back(capsule);
            }
        }
    }
}

void animate() {
    if (!gROOT->GetListOfCanvases()->FindObject("g_canvas")) return;
    
    g_frame->Draw("axis");
    
    // tank decision
    for(auto& sp : splist_tank) {
        if (sp.type==3 && sp.step<=0) {
            int act = 0;
            double shooting_rate = 0.1+0.02*game_level;
            double moving_rate = 0.5;
            
            if (sp.control_opt==0) {
                
                int p1_score = game_score;
                int p1_player_hp = sp.hp;
                int p1_player_status = 1;
                if (sp.charge<=0) p1_player_status = 2;
                std::vector<int> p1_code;
                std::vector<double> p1_x, p1_y, p1_dx, p1_dy;
                
                for(auto& op : splist_bullet_ply) {
                    p1_code.push_back(0);
                    p1_x.push_back(op.x);
                    p1_y.push_back(op.y);
                    p1_dx.push_back(op.dx);
                    p1_dy.push_back(op.dy);
                }
                
                for(auto& op : splist_bullet) {
                    p1_code.push_back(1);
                    p1_x.push_back(op.x);
                    p1_y.push_back(op.y);
                    p1_dx.push_back(op.dx);
                    p1_dy.push_back(op.dy);
                }
                
                for(auto& op : splist_tank) {
                    if (op.control_opt==0) p1_code.push_back(2);
                    else if (op.control_opt==4) p1_code.push_back(4);
                    else p1_code.push_back(3);
                    p1_x.push_back(op.x);
                    p1_y.push_back(op.y);
                    p1_dx.push_back(op.dx);
                    p1_dy.push_back(op.dy);
                }
                
                for(auto& op : splist_static) {
                    if (op.type==1) p1_code.push_back(5);
                    else if (op.type==2) p1_code.push_back(6);
                    else if (op.type==4) p1_code.push_back(7);
                    p1_x.push_back(op.x);
                    p1_y.push_back(op.y);
                    p1_dx.push_back(op.dx);
                    p1_dy.push_back(op.dy);
                }
                act = P1.decision(p1_score,p1_player_hp,p1_player_status,p1_code,p1_x, p1_y, p1_dx, p1_dy);
                if (act<0 || act>8) act = 0;
                if (sp.charge>0 && act>=5 && act<=8) act = 0;
                
            }else if (sp.control_opt==1) {
                
                if (sp.charge<=0) { // can shoot can move
                    if (rnd.uniform()<shooting_rate) act = rnd.randint(5,6); // shoot
                }else { // can move but cannot shoot
                    if (rnd.uniform()<moving_rate) act = rnd.randint(1,2); // move
                }
                
            }else if (sp.control_opt==2) {
                
                if (sp.charge<=0) { // can shoot can move
                    if (rnd.uniform()<shooting_rate) act = rnd.randint(7,8); // shoot
                }else { // can move but cannot shoot
                    if (rnd.uniform()<moving_rate) act = rnd.randint(3,4); // move
                }
                
            }else if (sp.control_opt==3) {
                
                if (sp.charge<=0) { // can shoot can move
                    if (rnd.uniform()<shooting_rate) act = rnd.randint(5,8); // shoot
                }else { // can move but cannot shoot
                    if (rnd.uniform()<moving_rate) act = rnd.randint(1,4); // move
                }
                
            }else if (sp.control_opt==4) {
                
                if (sp.charge<=0) { // can shoot can move
                    if (rnd.uniform()<shooting_rate) {
                        act = rnd.randint(5,8);
                        for(auto& op : splist_tank) {
                            if (op.control_opt!=0) continue;
                            if (fabs(op.x-sp.x)<fabs(op.y-sp.y)) {
                                if (op.y<sp.y) act = 5;
                                else act = 6;
                            }else {
                                if (op.x<sp.x) act = 7;
                                else act = 8;
                            }
                        }
                    }
                }else { // can move but cannot shoot
                    if (rnd.uniform()<moving_rate) {
                        act = rnd.randint(1,4);
                        for(auto& op : splist_tank) {
                            if (op.control_opt!=0) continue;
                            if (fabs(op.x-sp.x)<fabs(op.y-sp.y)) {
                                if (op.y<sp.y) act = 1;
                                else act = 2;
                            }else {
                                if (op.x<sp.x) act = 3;
                                else act = 4;
                            }
                        }
                    }
                }
                
            }
            
            if (act>=5 && act<=8) {
                sprite bullet;
                bullet.x = sp.x;
                bullet.y = sp.y;
                bullet.dir = act-4;
                bullet.step = 5;
                if (bullet.dir==1) bullet.dy = -unit_dim/bullet.step;
                if (bullet.dir==2) bullet.dy = +unit_dim/bullet.step;
                if (bullet.dir==3) bullet.dx = -unit_dim/bullet.step;
                if (bullet.dir==4) bullet.dx = +unit_dim/bullet.step;
                if (sp.control_opt==0) splist_bullet_ply.push_back(bullet);
                else splist_bullet.push_back(bullet);
                if (sp.control_opt==0 || sp.control_opt==4) sp.charge = 20;
                else sp.charge = 40;
            }else if (act>=1 && act<=4) {
                sp.dir = act;
                if (sp.control_opt==0 || sp.control_opt==4) sp.step = 10;
                else sp.step = 20;
                sp.dx = sp.dy = 0.;
                if (sp.dir==1) sp.dy = -unit_dim/sp.step;
                if (sp.dir==2) sp.dy = +unit_dim/sp.step;
                if (sp.dir==3) sp.dx = -unit_dim/sp.step;
                if (sp.dir==4) sp.dx = +unit_dim/sp.step;
                
                // regularizing the positions, to avoid round-off problems
                double min_diff,min_reg;
                min_diff = min_reg = -1.;
                for(int i=0;i<map_dim;++i) {
                    double reg = unit_dim*(0.5+i);
                    double diff = fabs(reg-sp.x);
                    if (min_diff<0. || diff<min_diff) {
                        min_reg = reg;
                        min_diff = diff;
                    }
                }
                sp.x = min_reg;
                min_diff = min_reg = -1.;
                for(int i=0;i<map_dim;++i) {
                    double reg = unit_dim*(0.5+i);
                    double diff = fabs(reg-sp.y);
                    if (min_diff<0. || diff<min_diff) {
                        min_reg = reg;
                        min_diff = diff;
                    }
                }
                sp.y = min_reg;
            }
        }
    }
    
    // tank action
    for(auto& sp : splist_tank) {
        if (sp.type==3) {
            if (sp.step>0) { // moving
                sp.x += sp.dx;
                sp.y += sp.dy;
                bool collision = false;
                for(auto& op : splist_static) {
                    if (op.type==1 && sp.detect_collision(op)) {
                        collision = true; break;
                    }else if (op.type==2 && sp.detect_collision(op)) {
                        sp.hp -= 1;
                        game_score += 50;
                        if (sp.hp<=0) sp.status = 0;
                        op.status = 0;
                        
                        for(int i=0;i<3;++i) {
                            sprite explosion;
                            explosion.x = op.x+rnd.uniform(-0.3*unit_dim,+0.3*unit_dim);
                            explosion.y = op.y+rnd.uniform(-0.3*unit_dim,+0.3*unit_dim);
                            explosion.hp = rnd.randint(5,9);
                            splist_explosion.push_back(explosion);
                        }
                    }else if (op.type==4 && sp.control_opt==0 && sp.detect_collision(op)) {
                        sp.hp += 2;
                        if (sp.hp>16) sp.hp = 16;
                        game_score += 100;
                        op.status = 0;
                    }
                }
                if (sp.x-unit_dim*0.499<world_boundary_x[0]) collision = true;
                if (sp.y-unit_dim*0.499<world_boundary_y[0]) collision = true;
                if (sp.x+unit_dim*0.499>world_boundary_x[1]) collision = true;
                if (sp.y+unit_dim*0.499>world_boundary_y[1]) collision = true;
                if (collision) { // move back
                    sp.x -= sp.dx;
                    sp.y -= sp.dy;
                }
                sp.step--;
            }
            if (sp.charge>0) sp.charge--;
        }
    }
    
    // bullet action
    for(auto& sp : splist_bullet) {
        sp.x += sp.dx;
        sp.y += sp.dy;
        bool collision = false;
        for(auto& op : splist_tank) {
            if (op.control_opt!=0) continue;
            if (sp.detect_collision(op)) {
                collision = true;
                op.hp -= 1;
                if (op.hp<=0) op.status = 0;
            }
        }
        for(auto& op : splist_static) {
            if (op.type==1 && sp.detect_collision(op)) {
                collision = true;
                op.hp -= 1;
                if (op.hp<=0) op.status = 0;
            }
        }
        if (collision) {
            for(int i=0;i<3;++i) {
                sprite explosion;
                explosion.x = sp.x+rnd.uniform(-0.3*unit_dim,+0.3*unit_dim);
                explosion.y = sp.y+rnd.uniform(-0.3*unit_dim,+0.3*unit_dim);
                explosion.hp = rnd.randint(5,9);
                splist_explosion.push_back(explosion);
            }
        }
        if (sp.x<world_boundary_x[0]) collision = true;
        if (sp.y<world_boundary_y[0]) collision = true;
        if (sp.x>world_boundary_x[1]) collision = true;
        if (sp.y>world_boundary_y[1]) collision = true;
        if (collision) sp.status = 0;
    }
    
    // player bullet action
    for(auto& sp : splist_bullet_ply) {
        sp.x += sp.dx;
        sp.y += sp.dy;
        bool collision = false;
        for(auto& op : splist_tank) {
            if (op.control_opt==0) continue;
            if (sp.detect_collision(op)) {
                collision = true;
                op.hp -= 1;
                game_score += 10;
                if (op.hp<=0) {
                    op.status = 0;
                    game_score += 1000;
                    if (op.control_opt==4) game_score += 1000;
                }
            }
        }
        for(auto& op : splist_static) {
            if (op.type==1 && sp.detect_collision(op)) {
                collision = true;
                op.hp -= 1;
                game_score += 10;
                if (op.hp<=0) op.status = 0;
            }
        }
        if (collision) {
            for(int i=0;i<3;++i) {
                sprite explosion;
                explosion.x = sp.x+rnd.uniform(-0.3*unit_dim,+0.3*unit_dim);
                explosion.y = sp.y+rnd.uniform(-0.3*unit_dim,+0.3*unit_dim);
                explosion.hp = rnd.randint(5,9);
                splist_explosion.push_back(explosion);
            }
        }
        if (sp.x<world_boundary_x[0]) collision = true;
        if (sp.y<world_boundary_y[0]) collision = true;
        if (sp.x>world_boundary_x[1]) collision = true;
        if (sp.y>world_boundary_y[1]) collision = true;
        if (collision) sp.status = 0;
    }
    
    // bullet hit action
    for(auto& sp : splist_explosion) {
        if (sp.hp<=0) sp.status = 0;
        else sp.hp--;
    }
    
    // clean up "dead" objects
    std::vector<sprite> tmp;
    for(auto& sp : splist_bullet) if (sp.status!=0) tmp.push_back(sp);
    splist_bullet = tmp;
    tmp.clear();
    for(auto& sp : splist_bullet_ply) if (sp.status!=0) tmp.push_back(sp);
    splist_bullet_ply = tmp;
    tmp.clear();
    for(auto& sp : splist_static) if (sp.status!=0) tmp.push_back(sp);
    splist_static = tmp;
    tmp.clear();
    for(auto& sp : splist_tank) if (sp.status!=0) tmp.push_back(sp);
    splist_tank = tmp;
    tmp.clear();
    for(auto& sp : splist_explosion) if (sp.status!=0) tmp.push_back(sp);
    splist_explosion = tmp;
    tmp.clear();
    
    game_status = 0; // check if game over
    for(auto& sp : splist_tank)
        if (sp.control_opt==0) game_status = 1;
    if (!game_status) {
        game_message = "GAME OVER";
        game_message_delay = -1;
    }
    
    if (splist_tank.size()==1 && splist_tank[0].control_opt==0) { // level up
        if (game_level<20) {
            game_level += 1;
            game_message = Form("LEVEL %d",game_level);
        }else game_message = "LV MASTER";
        game_message_delay = 40;
        init_level();
    }
    
    // static objects
    for(auto& sp : splist_static) {
        if (sp.type==1) {
            g_block->SetMarkerColor(kGray+sp.hp-1);
            g_block->DrawPolyMarker(1,&sp.x,&sp.y);
        }else if (sp.type==2) {
            g_mine->DrawPolyMarker(1,&sp.x,&sp.y);
        } else if (sp.type==4) {
            g_capsule->DrawPolyMarker(1,&sp.x,&sp.y);
        }
    }
    
    // tank
    TString status_str("HP ");
    for(auto& sp : splist_tank) {
        if (sp.type==3 && (sp.control_opt==1 || sp.control_opt==2 || sp.control_opt==3)) {
            g_tank->DrawPolyMarker(1,&sp.x,&sp.y);
        }else if (sp.type==3 && sp.control_opt==4) {
            g_tank_agg->DrawPolyMarker(1,&sp.x,&sp.y);
        }else if (sp.type==3 && sp.control_opt==0) {
            g_tank_ply->DrawPolyMarker(1,&sp.x,&sp.y);
            for(int i=0;i<sp.hp;++i) status_str += "|";
        }
    }
    g_status->DrawLatex(0.03,1.05,status_str);
    g_score->DrawLatex(0.53,1.05,Form("Score %d",game_score));
    
    // bullet
    for(auto& sp : splist_bullet)
        g_bullet->DrawPolyMarker(1,&sp.x,&sp.y);
    
    // player bullet
    for(auto& sp : splist_bullet_ply)
        g_bullet_ply->DrawPolyMarker(1,&sp.x,&sp.y);
    
    // bullet hit
    for(auto& sp : splist_explosion)
        g_explosion->DrawPolyMarker(1,&sp.x,&sp.y);
    
    if (game_message_delay>0 || game_message_delay<0)
        g_message->DrawLatex(0.50,0.55,game_message);
        if (game_message_delay>0) game_message_delay--;
    
    g_canvas->Update();
}

void game1() {
    P1.banner();
    
    g_canvas = new TCanvas("g_canvas","",600,660);
    g_canvas->SetMargin(0.1,0.05,0.1,0.05);
    g_frame = g_canvas->DrawFrame(world_boundary_x[0],world_boundary_y[0],world_boundary_x[1],world_boundary_y[1]*1.1);
    g_frame->GetXaxis()->SetLabelSize(0.025);
    g_frame->GetYaxis()->SetLabelSize(0.025);
    
    g_block = new TPolyMarker();
    g_block->SetMarkerStyle(21);
    g_block->SetMarkerSize(2.5);
    
    g_mine = new TPolyMarker();
    g_mine->SetMarkerColor(kRed+1);
    g_mine->SetMarkerStyle(47);
    g_mine->SetMarkerSize(2);
    
    g_tank = new TPolyMarker();
    g_tank->SetMarkerColor(kCyan+1);
    g_tank->SetMarkerStyle(29);
    g_tank->SetMarkerSize(2.5);
    
    g_tank_agg = new TPolyMarker();
    g_tank_agg->SetMarkerColor(kViolet+1);
    g_tank_agg->SetMarkerStyle(29);
    g_tank_agg->SetMarkerSize(2.5);
    
    g_tank_ply = new TPolyMarker();
    g_tank_ply->SetMarkerColor(kBlue);
    g_tank_ply->SetMarkerStyle(29);
    g_tank_ply->SetMarkerSize(2.5);
    
    g_capsule = new TPolyMarker();
    g_capsule->SetMarkerColor(kGreen+1);
    g_capsule->SetMarkerStyle(34);
    g_capsule->SetMarkerSize(2);
    
    g_bullet = new TPolyMarker();
    g_bullet->SetMarkerColor(kCyan+2);
    g_bullet->SetMarkerStyle(20);
    g_bullet->SetMarkerSize(0.7);
    
    g_bullet_ply = new TPolyMarker();
    g_bullet_ply->SetMarkerColor(kBlue+1);
    g_bullet_ply->SetMarkerStyle(20);
    g_bullet_ply->SetMarkerSize(0.7);
    
    g_explosion = new TPolyMarker();
    g_explosion->SetMarkerColor(kOrange+1);
    g_explosion->SetMarkerStyle(43);
    g_explosion->SetMarkerSize(2.0);
    
    g_status = new TLatex();
    g_status->SetTextSize(0.035);
    g_status->SetTextColor(kBlue-4);
    g_status->SetTextAlign(12);
    g_status->SetTextFont(42);
    g_score = new TLatex();
    g_score->SetTextSize(0.035);
    g_score->SetTextColor(kBlue-4);
    g_score->SetTextAlign(12);
    g_score->SetTextFont(42);
    g_message = new TLatex();
    g_message->SetTextSize(0.14);
    g_message->SetTextAlign(22);
    g_message->SetTextColor(kOrange+1);
    g_message->SetTextFont(42);
    
    init_level();
    
    TTimer *timer = new TTimer(25);
    timer->SetCommand("animate()");
    timer->TurnOn();
}
