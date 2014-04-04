# CS 450 HW3 Fan Zhang A20280966
from threading import Thread, Semaphore, Condition
import random, time
from time import sleep
from time import time


class Phil2:
	global can_eat
	global state
	global NUM_PHIL
	#thinking=1, hungry=2, eating=3
	def __init__(self,n,m):
		self.id=n
		self.m=m
	def right(self, i):
		return(i+1)%NUM_PHIL
	def left(self,i):
		return(i-1+NUM_PHIL)%NUM_PHIL
	def pickup(self):
		state[self.id]=2
		self.test(self.id)
		if state[self.id!=3]:
			can_eat[self.id].wait()
	def putdown(self):
		state[self.id]=1
		self.test(self.right())
		self.test(self.left())
	def test(self,i):
		if (state[i]==2 and state[self.right(i)]!=3 and state[self.left(i)]!=3):
			state[i]=3
			can_eat[i].notify()
	def eat(self):
		self.m-=1
		sleep(random.random())
		print('{} eat success'.format(self.id))
#where when a philosopher finishes eating, the 
#neighbors get tested to see if they can eat.	


def condition_solution(phil):
	global state
	global can_eat
	sleep(random.random())
	while phil.m>0:
		with can_eat[phil.id]:
			sleep(random.random())
			print('thinking success')
			phil.pickup()
			phil.eat()
			phil.putdown()
			sleep(random.random())
	

def main(numofphil=5, numofmeal=10):
	global NUM_PHIL
	global can_eat
	global state
	NUM_PHIL=numofphil
#solution 4
#Tanenbaum  solution, where when a philosopher finishes eating, the 
#neighbors get tested to see if they can eat.
	random.seed(1)
	#thinking=1, hungry=2, eating=3
	state = [1 for i in range(NUM_PHIL)]
	can_eat=[Condition() for i in range(numofphil)]
	phils=[Phil2(i, numofmeal) for i in range(NUM_PHIL)]
	start = time()
	ns = [Thread(target=condition_solution, args=([phils[i]]))
		for i in range(numofphil)]
	for n in ns:
		n.start()
	for n in ns:
		n.join()
	end = time()
	ttime = (end-start)
	print('Tanenbaum solution time is {:0.01f} s'.format(ttime))

main()
