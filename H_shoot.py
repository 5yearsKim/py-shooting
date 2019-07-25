#H_shoot.py
###############################################################################
#you can change basic setting of game in this file
#created by KIM, HYUNWOO -  YONSEI EE
##################################################################################
b_mv_per_u_mv = 4 #bullet move per unit move - bullets move faster than monster!

width =65 
height=40
x_begin =0
y_begin =0

#enumerate direction as number
l_ =0
r_=1
u_ = 2
d_ = 3
ld_=4  #left down
rd_=5  #right down

body_ch = ['*','&','!','F']


mv_list = [ [d_] ,
		[ld_,d_],
		[rd_,d_],
		[d_,l_,r_],
		[rd_,r_],
		[ld_,l_],
		[rd_, r_, r_],
		[ld_, l_, l_],
		[ld_,ld_,u_,rd_,rd_,u_ ] ]
mon_num = 4
mv_num = len(mv_list)

class plane: 
	def __init__(self):
		self.head = [y_begin+height-6,x_begin+int(height/2)]
		self.body = [[1,-1],[1,0],[1,1]]
		self.headshape = '^'
		self.bodyshape = 'X'
		self.alive = True  #this variable means nothing to class "plane"

class bullet:
	def __init__(self,m_head):
		self.head = m_head.copy()
		self.body = []
		self.headshape = '^'
		self.bodyshape = '^'
		self.alive = True
		self.stride = 2
class Unit:
	def __init__(self,x_pos,life):
		self.head = [y_begin,x_pos]
		self.alive = True
		self.life = life 
		self.bodyshape = body_ch[int(self.life/10)]
		self.headshape = str(self.life%10)
		self.move_index = 0
		self.point = int(life*life/10) #give higher point when player killed strong Monster


class monster1(Unit):
	def __init__(self,xpos,life, mv):
		super().__init__(xpos,life)
		self.body = [[-1,1],[-1,-1]]
		self.surface = [[0,0],[-1,1],[-1,-1]]
		self.stride = 1
		self.movement =mv_list[mv] 

class monster2(Unit):
	def __init__(self,xpos,life, mv):
		super().__init__(xpos,life)
		self.body = [[-1,-1],[-1,1],[-2,-2],[-2,2],[-1,3],[-1,-3],[0,4],[0,-4],[-1,0],[-2,0],[-3,0],[-4,-1],[-4,1]]
		self.surface = [[-1,-1],[-1,1],[-2,-2],[-2,2],[-1,3],[-1,-3],[0,4],[0,-4]]
		self.stride = 3
		self.movement =mv_list[mv] 

class monster3(Unit):
	def __init__(self,xpos,life, mv):
		super().__init__(xpos,life)
		self.body = [[1,1],[1,-1],[0,2],[0,1],[0,-1],[0,-2],[-1,1],[-1,0],[-1,-1],[-2,-1],[-2,1]]
		self.surface = [[0,0],[1,1],[1,-1],[0,2],[0,-2]]
		self.stride = 2
		self.movement =mv_list[mv] 

class monster4(Unit):
	def __init__(self,xpos,life, mv):
		super().__init__(xpos,life)
		self.body = [[-1,0]]
		self.surface = [[0,0]]
		self.stride = 1
		self.movement =mv_list[mv] 
		self.point = int(life*life/10)*2 #give double point for monster4



#return  a<x<b?
def inrange(x, a, b):
	return x<b and x>a
