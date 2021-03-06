# CS 450 HW3 Fan Zhang A20280966
from threading import Thread, Semaphore, Condition, RLock
import random, time
from time import sleep
from time import time

#define a phil class represent philosophers
class Phil:
	def __init__(self, n ,m):
		self.id=n #philosopher id
		self.m=m #meals can eat
#get left fork
	def get_left(self,forks):
		forks[((self.id)+1) % NUM_PHIL].acquire()
#check the left fork, if not available return false
	def check_left(self,forks):
		return forks[((self.id)+1) % NUM_PHIL].acquire(blocking=False)
#check the right fork, if not available return false
	def check_right(self,forks):
		return forks[self.id].acquire(blocking=False)
# Get the right fork
	def get_right(self,forks):
		forks[self.id].acquire()
# Drop all forks
	def drop_all(self, forks):
		forks[self.id].release()
		forks[(self.id+1) % NUM_PHIL].release()
# Drop right fork
	def drop_right(self, forks):
		forks[self.id].release()
#eat decrease number of meals
	def eat(self):
		self.m-=1

# no-holding solution : Philosopher tries to pick up right fork then
# check left fork.
def no_holding(phil, forks):
	while phil.m>0:
		sleep(random.random()) #thinking
		phil.get_right(forks)
		sleep(random.random())
		if not phil.check_left(forks):
			phil.drop_right(forks)	
			sleep(random.random()) #pause between getting forks
		else:
			phil.eat()
			sleep(random.random()) #eating
			phil.drop_all(forks)

#The napkin/footman solution where a counting semaphore initialized to 
#N-1 limits the number of philosophers who can try to eat at the same 
#time.
def napkin_solution(phil, forks, napkin):
	while phil.m>0:
		sleep(random.random()) #thinking
		napkin.acquire()
		phil.get_right(forks)
		sleep(random.random()) #pause between getting forks
		phil.get_left(forks)
		phil.eat()
		sleep(random.random()) #eating
		phil.drop_all(forks)
		napkin.release()

#The even/odd solution where even-numbered philosophers are right-handed
#i.e., pick up their right and then left forks and odd-numbered philosophers
#are left-handed
def evenodd(phil, forks):
	while phil.m>0:
		sleep(random.random()) #thinking
		if phil.id%2==0:
			phil.get_right(forks)
			sleep(random.random()) #pause between getting forks
			phil.get_left(forks)
			phil.eat()
			sleep(random.random()) #eating
			phil.drop_all(forks)
		else:
			phil.get_left(forks)
			sleep(random.random()) #pause between getting forks
			phil.get_right(forks)
			phil.eat()
			sleep(random.random()) #eating
			phil.drop_all(forks)
#solution 4
#Tanenbaum  solution, where when a philosopher finishes eating, the 
#neighbors get tested to see if they can eat.
#This is philosopher class for solution 4
class Phil2:
	global can_eat
	global state
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
        	if state[self.id] != 3:
            		can_eat[self.id].wait()

	def putdown(self):
        	state[self.id]=1
        	self.test(self.right(self.id))
        	self.test(self.left(self.id))

	def test(self, i):
        	if (state[self.left(self.id)] != 3
            	and state[self.right(self.id)] != 3
            	and state[self.id] == 2):
            		state[self.id]=3
            		can_eat[self.id].notify()
	def eat(self):
		self.m-=1
		sleep(random.random())


def condition_solution(phil):
	global state
	global can_eat
	while phil.m>0:
		sleep(random.random())
		with lock:
			with can_eat[phil.id]:
				phil.pickup()
				phil.eat()
				phil.putdown()
			
def main(numofphil=5, numofmeal=10):
	global NUM_PHIL
	NUM_PHIL=numofphil
	print('Elapsed times: ')
#solution 1
# no-holding solution : Philosopher tries to pick up right fork then
# check left fork.
	random.seed(1)
	forks = [Semaphore(1) for i in range(NUM_PHIL)]
	phils=[Phil(i, numofmeal) for i in range(NUM_PHIL)]
	start = time()
	ns = [Thread(target=no_holding, args=([phils[i],forks]))
		for i in range(numofphil)]

	for n in ns:
		n.start()
	for n in ns:
		n.join()
	end = time()
	no_holdtime = (end-start)
	print('No_holding:   {:0.01f}s'.format(no_holdtime) )
#solution 2
#The napkin/footman solution where a counting semaphore initialized to 
#N-1 limits the number of philosophers who can try to eat at the same 
#time.
	random.seed(1)
	forks = [Semaphore(1) for i in range(NUM_PHIL)]
	napkin=Semaphore(NUM_PHIL-1)
	phils=[Phil(i, numofmeal) for i in range(NUM_PHIL)]
	start = time()
	ns = [Thread(target=napkin_solution, args=([phils[i],forks,napkin]))
		for i in range(numofphil)]

	for n in ns:
		n.start()
	for n in ns:
		n.join()
	end = time()
	napkintime = (end-start)
	print('Napkin:       {:0.01f}s'.format(napkintime) )
#solution 3
#The even/odd solution where even-numbered philosophers are right-handed
#i.e., pick up their right and then left forks and odd-numbered philosophers
#are left-handed
	random.seed(1)
	forks = [Semaphore(1) for i in range(NUM_PHIL)]
	phils=[Phil(i, numofmeal) for i in range(NUM_PHIL)]
	start = time()
	ns = [Thread(target=evenodd, args=([phils[i],forks]))
		for i in range(numofphil)]

	for n in ns:
		n.start()
	for n in ns:
		n.join()
	end = time()
	evenoddtime = (end-start)
	print('Even/odd:     {:0.01f}s'.format(evenoddtime) )
#solution 4
#Tanenbaum  solution, where when a philosopher finishes eating, the 
#neighbors get tested to see if they can eat.
	global can_eat
	global state
	global lock
	lock=RLock()
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
	print('Tanenbaum:    {:0.01f}s'.format(ttime))
main()
