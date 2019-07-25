#shoot.py

import curses
import time
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
from H_shoot import *


curses.initscr()
win = curses.newwin(height, width, y_begin, x_begin)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

key = 0
#function to display object on the window
def print_obj(obj,h_char,b_char):
	if inrange(obj.head[0],y_begin,y_begin+height-1) and inrange(obj.head[1],x_begin,x_begin+width-1):
		win.addch(obj.head[0],obj.head[1],h_char)
	
	for i in range(len(obj.body)):
		if inrange(obj.head[0]+obj.body[i][0],y_begin,y_begin+height-1) and inrange(obj.head[1]+obj.body[i][1],x_begin,x_begin+width-1):
			win.addch(obj.head[0]+obj.body[i][0] , obj.head[1]+obj.body[i][1] , b_char)

			
def move_up(obj,num):
	if obj.head[0]<y_begin+3:
		obj.alive = False
		return 0
	print_obj(obj,' ',' ')

	temp = obj.head.pop(0)
	temp -=num
	obj.head.insert(0,temp)

	print_obj(obj,obj.headshape,obj.bodyshape)

def move_down(obj,num):
	if obj.head[0]>y_begin+height-4:
		obj.alive = False
		return 0
	
	print_obj(obj,' ',' ')
	
	temp = obj.head.pop(0)
	temp +=num
	obj.head.insert(0,temp)


	print_obj(obj,obj.headshape,obj.bodyshape)

def move_right(obj,num):

	print_obj(obj,' ',' ')

	if obj.head[1]>x_begin+width-2:
		obj.head[1] = x_begin+2

	temp = obj.head.pop(1)
	temp +=num
	obj.head.insert(1,temp)

	print_obj(obj,obj.headshape,obj.bodyshape)

	
def move_left(obj,num):
	print_obj(obj,' ',' ')

	if obj.head[1]<x_begin+2:
		obj.head[1] = x_begin+width-2
	temp = obj.head.pop(1)
	temp -=num
	obj.head.insert(1,temp)

	print_obj(obj,obj.headshape,obj.bodyshape)		


def move_left_down(obj,num):
	if obj.head[0]>y_begin+height-3:
		obj.alive = False
		return 0
	
	print_obj(obj,' ',' ')
	
	if obj.head[1]<x_begin+2:
		obj.head[1] = x_begin+width-2

	temp_x = obj.head.pop()
	temp_y = obj.head.pop()
	temp_x -=num
	temp_y +=num
	obj.head.insert(0,temp_y)
	obj.head.insert(1,temp_x)

	print_obj(obj,obj.headshape,obj.bodyshape)		

def move_right_down(obj,num):
	if  obj.head[0]>y_begin+height-3:
		obj.alive = False
		return 0
	
	print_obj(obj,' ',' ')

	
	if obj.head[1]>x_begin+width-2:
		obj.head[1] = x_begin+2
	temp_x = obj.head.pop()
	temp_y = obj.head.pop()
	temp_x +=num
	temp_y +=num
	obj.head.insert(0,temp_y)
	obj.head.insert(1,temp_x)
	
	print_obj(obj,obj.headshape,obj.bodyshape)		

	
#game settin is processed on this function
def proceed(m_bullets,m_units):
	global level
	global kill_cnt
	global score
	global b_mv_cnt
# delete dead bullets and monsters 
	i=0
	while i<len(m_bullets):
		if m_bullets[i].alive ==False:
			print_obj(m_bullets[i],' ',' ')
			del m_bullets[i]
		else: #check if bullet hit the monsters
			b_head = m_bullets[i].head
			for k in range(len(m_units)):
				for l in range(len(m_units[k].surface)):
					if  b_head[1]== m_units[k].head[1]+m_units[k].surface[l][1] and inrange(m_units[k].head[0]+m_units[k].surface[l][0] , b_head[0] - m_bullets[i].stride -1 , b_head[0] +1):
						m_bullets[i].alive = False
						m_units[k].life -= 1
						m_units[k].headshape = str(m_units[k].life%10)
						m_units[k].bodyshape = body_ch[int(m_units[k].life/10)]
			i +=1;
#check whether monster still alive		
	for i in range(len(m_units)):
		if m_units[i].life <1:
			kill_cnt += 1
			if kill_cnt >=7:            #7 kill = 1 level up
				level += 1
				kill_cnt = 0
				if level<9: game_speed = 0.16 - 0.012*level  #speed goes up as level rise
			score += m_units[i].point
			m_units[i].alive = False
		if m_units[i].alive == False:
			print_obj(m_units[i],' ',' ')
			del m_units[i]
			break

# generate random ramdom monster that has max_life = 5+level*2
	if b_mv_cnt%2:
		mon_generate(randint(1,mon_num),5+level*3)	

#move objects as time flow		
	for i in range(len(m_bullets)):
		move_up(m_bullets[i],m_bullets[i].stride)
	b_mv_cnt += 1
	if b_mv_cnt >=b_mv_per_u_mv:
		b_mv_cnt = 0
		for i in range(len(m_units)):
			Unit_move(m_units[i])


#to control each unit's unique movement. 	
def Unit_move(unit):
	dir_ = unit.movement[unit.move_index]
	if dir_ == l_:
		move_left(unit,unit.stride)
	elif dir_ == r_:
		move_right(unit,unit.stride)
	elif dir_ == u_:
		move_up(unit,unit.stride)
	elif dir_ == d_:
		move_down(unit,unit.stride)
	elif dir_ == ld_:
		move_left_down(unit,unit.stride)
	elif dir_ == rd_:
		move_right_down(unit,unit.stride)
	unit.move_index = (unit.move_index+1)%len(unit.movement)

#generate monster	
def mon_generate(mode,max_life):
	if mode ==1:
		units.append(monster1(randint(x_begin+1,x_begin+width-1),randint(3,max_life),randint(0,mv_num-1)))
	if mode ==2:
		units.append(monster2(randint(x_begin+1,x_begin+width-1),randint(3,max_life),randint(0,mv_num-1)))
	if mode ==3:
		units.append(monster3(randint(x_begin+1,x_begin+width-1),randint(3,max_life),randint(0,mv_num-1)))
	if mode ==4:
		units.append(monster4(randint(x_begin+1,x_begin+width-1),randint(3,max_life),randint(0,mv_num-1)))
	

game_speed = 0.16 # object moves in every this sec - initialization. go fast as level goes up
game_on=True    #game is on playing
score = 0
level = 1   #level goes up as kill_cnt goes up
kill_cnt = 0  #count kil_cunt to change level
b_mv_cnt = 0   #if b_mv_cnt == b_mv_per_U_mv, b_mv_cnt = 0 again
now_clk = prev_clk = time.time() #game clock setting for overall game setting
jet = plane()
bullets = []
units = []
	
while key !=27:  #press esc to terminate game
	key = win.getch()
#print Score and Game Title
	win.addstr(0, 2, 'Score : ' + str(score) + ' Level: ' +str(level)+' ')
	win.addstr(0, 29, ' SHOOTING ')                    
	if key == KEY_UP:
		move_up(jet,1)
	elif key == KEY_DOWN:
		move_down(jet,1)
	elif key == KEY_RIGHT:
		move_right(jet,1)
	elif key == KEY_LEFT:
		move_left(jet,1)
	if key == ord(' '): #press space to shoot
		if len(bullets) == 0:
			bullets.append(bullet(jet.head))
		elif bullets[len(bullets)-1].head !=jet.head:
			bullets.append(bullet(jet.head))
	#check whether the game is over or not
	for i in range(len(jet.body)):
		for j in range(len(units)):
			for k in range(len(units[j].body)):
				if jet.head[0]+ jet.body[i][0] == units[j].head[0]+units[j].body[k][0] and jet.head[1]+jet.body[i][1] == units[j].head[1]+units[j].body[k][1]:
					game_on = False	
					break

	if game_on == False: #game over
		break

	now_clk = time.time()
	if now_clk - prev_clk >game_speed:
		proceed(bullets,units) #every setting in moment is in proceed function
		prev_clk = now_clk


curses.endwin()
print('your score is:  '+str(score) )
