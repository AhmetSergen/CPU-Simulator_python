from scipy.stats import poisson
import matplotlib.pyplot as plt
import os
import numpy as np
import random
import matplotlib.pyplot as plt; plt.rcdefaults()

#|SJF========|------\
#                   CPU
#|FCFS=======|------/

def prand(lam): #random number with poisson formula
	#numpy.random.poisson(lambda, size)
	poissonlist = np.random.poisson(lam, 10)
	return np.average(poissonlist)
	
def urand(): #uniform random number
	return int(random.randint(1,101))
 
  
#____________________________________________________________________________MAİN____________________________________________________________________________

counter=0     #CPU clock loop counter
foreground=[] #foreground queue
background=[] #background queue
farrive=[]    #arrival times for foreground queue
fexecute=[]   #execute times for foreground queue (processes are executed right at these moments)
barrive=[]    #arrival times for background queue
bexecute=[]   #execute times for background queue (processes are executed right at these moments)
fburst=[]     #foreground burst times
bburst=[]     #background burst times
fLenTime=[]   #lenght of foreground queue for each clock loop x=time y=len(foreground)
bLenTime=[]	  #lenght of background queue for each clock loop x=time y=len(background)
ffree = True  #foreground dispatch allow; if same process has highest priority before one clock loop, and its not terminated yet : FALSE
bfree = True  #background dispatch allow; if queue has just terminated a process and not processing any process at the moment and ready to dispatch : TRUE
CPUbusy = 0   #every unit time of cpu spend busy. parameter for CPU utilization
fratio = 60   #(priority ratio)default ratio for selecting next queue to execute a process. changes automatically in adaptive cpu mode 
fratioTime=[] #priority ratio for foreground queue for each clock loop x=time y=fratio
bratioTime=[] #priority ratio for background queue for each clock loop x=time y=fratio
cpam = 0      #current amount of process


#scenario and parameter select
sce = int(input("Select Scenario:\n1:Balanced\n2:Foreground majority\n3:Background majority\n"))
blen = int(input("Burst Lenght:\n1:Short\n2:Medium\n3:Long\n"))
mpam = int(input("Total process amount:\n")) #max process amount
admode = int(input("Adaptive Mode:\n1:Off\n2:On\n"))
#maxc = int(input("Maximum clock count:\n"))

if(sce==1): #scenario 1:Balanced
	fsce=25 #foreground scenario value
	bsce=25 #background scenario value
elif(sce==2):#scenario 2:Foreground majority
	fsce=30
	bsce=20
else:        #scenario 3:Background majority
	fsce=20
	bsce=30
	
if(blen==1): #burst lenght 1:Short
	fblen=3
	bblen=3
elif(blen==2):#burst lenght 2:Medium
	fblen=5
	bblen=5
else: 		  #burst lenght 3:Long
	fblen=7
	bblen=7

#**********CPU starts**************
while(1): 
	counter+=1 #CPU clock counter
	
	newfp = urand() #possibility value for a foreground process joined to foreground queue
	newbp = urand() #possibility value for a background process joined to background queue
	
	#**********NEW PROCESS*********
	#if current process amount <= max process amount
	if((newfp < fsce) and (cpam<mpam) ): #a new process joins to foreground queue
		cpam+=1
		fpburst = int(prand(fblen)) #foreground process lenght (burst time)
		if(len(foreground)==0): #if there was no process in queue
			foreground.append(fpburst) #append a new process to foreground queue
			fburst.append(fpburst)	   #append a new burst lenght to foreground burst array
			farrive.append(counter)	   #append a new arrive time to foreground arrive array
		else:
			for x in range(len(foreground)): #sort processes. put longest process to end of queue
				if(x==0 and ffree==False):
					foreground.insert(x+1, fpburst)
					fburst.append(fpburst)
					farrive.append(counter)
					break
				elif(fpburst < foreground[x]): 
					foreground.insert(x, fpburst)
					fburst.append(fpburst)
					farrive.append(counter)
					break
				elif((x+1)==len(foreground)):
					foreground.append(fpburst)
					fburst.append(fpburst)
					farrive.append(counter)
					break
			
	if((newbp < bsce) and (cpam<mpam) ): #a new process joins to background queue
		cpam+=1
		bpburst = int(prand(bblen))
		background.append(bpburst)
		bburst.append(bpburst)
		barrive.append(counter)
	
	
	fLenTime.append(len(foreground)) #add lenght data for current clock loop
	bLenTime.append(len(background))
	#**********EXECUTE PROCESS**********	
	rand = urand()
	
	#if((len(foreground)>0 and len(background)==0) or (ffree==False) or ( len(foreground) > 0 and bfree==True and fratio >= rand ) ):
	#FOREGROUND
	if( (ffree==False) or (len(foreground)>0 and len(background)==0) or (len(foreground)>0 and bfree==True and fratio >= rand)  ): #if another process is not already running, if FOREGROUND queue is not empty
		foreground[0]-=1             #execute highest priority process by one cpu clock time	  
		if(foreground[0] == 0):      #if first process is terminated, pop first process, and shift array
			foreground.pop(0)
			fexecute.append(counter) #record execute time of that process to fexecute array
			ffree=True               #foreground queue is no longer running a processç its free
		else:
			ffree=False
			
	#BACKGROUND
	elif(len(background) > 0):  #if BACKGROUND queue is not empty
		background[0]-=1
		if(background[0] == 0): #if first process is terminated, pop first process, and shift array
			background.pop(0)
			bexecute.append(counter)
			bfree=True
		else:
			bfree=False

	if(len(foreground) > 0 or len(background) > 0 ):
		CPUbusy += 1 #required data for computing CPU utility. 
		
		
	print("__________NEW CLOCK LOOP__________")
	print("Clock counter:",counter)
	print("*Foreground Queue:",foreground)
	print("*Background Queue:",background)
	print("Foreground Free:",ffree)
	print("Background Free:",bfree)	
	print("F.Arrive:",farrive)
	print("F.Execute:",fexecute)
	print("B.Arrive:",barrive)
	print("B.Execute:",bexecute)
	print("F.Burst:",fburst)
	print("B.Burst:",bburst)
	if((admode==2) and (len(foreground)>len(background)+2) and fratio <=80): #change ratio values for adaptive mode
		fratio +=10
		print("Foreground ratio increased")
	if((admode==2) and (len(background)>len(foreground)+2) and fratio >=20):
		fratio -=10
		print("Foreground ratio decreased")
	
	fratioTime.append(fratio)
	bratioTime.append(100-fratio)
	
	if( cpam>=mpam and len(foreground)==0 and len(background)==0 ): #if there is no more process left and all queues are empty. end while loop
		break
	os.system("pause")
	

print("===============END OF SIMULATION===============")

foret = np.subtract(fexecute,farrive) #foreground response times for each foreground process
boret = np.subtract(bexecute,barrive) #foreground response times for each foreground process
fturnaround = np.add(foret,fburst)    #foreground turnaround times for each foreground process
bturnaround = np.add(boret,bburst)    #background turnaround times for each background process
throughput = (cpam/counter)           #Throughput
CPUuti = (CPUbusy/counter)            #CPU Utilisation

ftotal = 0
btotal=0
for i in range (len(foret)): #Calculate overall response time
	ftotal += foret[i]
for j in range (len(boret)):
	btotal += boret[j]
if (len(foret)==0):
	flenr = 1
else :
	flenr = len(foret)
if (len(boret)==0):
	blenr = 1
else :
	blenr = len(boret)
	
foverall = ftotal/flenr                  #overall response time result for foreground 
boverall = btotal/blenr                  #overall response time result for background
overallResponseT = (foverall+boverall)/2 #overall response time results for both queues

ftotal = 0
btotal=0
foverall = 0
boverall = 0
for i in range (len(fturnaround)): #Calculate overall turnaround time
	ftotal += fturnaround[i]
for j in range (len(bturnaround)):
	btotal += bturnaround[j]
if (len(fturnaround)==0):
	flent = 1
else :
	flent = len(fturnaround)
if (len(bturnaround)==0):
	blent = 1
else :
	blent = len(bturnaround)
	
foverall = ftotal/flent					   #overall turnaround time result for foreground
boverall = btotal/blent                    #overall turnaround time result for background
overallTurnaroundT = (foverall+boverall)/2 #overall turnaround time for both queues
timeArr = np.arange(0, counter)            #array for clock counter [0,1,2,3 ... counter]
foretTimeArr = np.arange(0, len(foret))
boretTimeArr = np.arange(0, len(boret))
fAvgLen = np.sum(fLenTime) / len(fLenTime) #foreground average length
bAvgLen = np.sum(bLenTime) / len(bLenTime) #background average length





print("CPU Utility:",CPUuti)
print("Throughput:",throughput)
print("Overall Response Time:",overallResponseT)
print("Overall Turnaround Time",overallTurnaroundT)
print("F.Arrival Times:",farrive)
print("F.Execute Times:",fexecute)
print("B.Arrival Times:",barrive)
print("B.Execute Times:",bexecute)
print("F.Burst Times:",fburst)
print("B.Burst Times:",bburst)
print("F.Response Times:",foret)
print("B.Response Times:",boret)
print("F.Turnaround Times:",fturnaround)
print("B.Turnaround Times:",bturnaround)
print("F.Average Length:",fAvgLen)
print("B.Average Length:",bAvgLen)
print("F.Length-Time:",fLenTime)
print("B.Length-Time:",bLenTime)



#________________________________________________________________DRAW GRAPH________________________________________________________________

#*****Foreground Response Times
f1 = plt.figure(1)
pIDforet = np.arange(0, len(foret)) 
plt.bar(pIDforet, foret, tick_label = pIDforet, 
width = 0.2, color = ['red', 'green','blue'])   
plt.xlabel('Process ID') 
plt.ylabel('Response Time(Clock Loop)') 
plt.title('Foreground Response Times') 


#*****Background Response Times
f2 = plt.figure(2)
pIDboret = np.arange(0, len(boret)) 
plt.bar(pIDboret, boret, tick_label = pIDboret, 
width = 0.2, color = ['red', 'green','blue'])   
plt.xlabel('Process ID') 
plt.ylabel('Response Time(Clock Loop)') 
plt.title('Background Response Times') 
 
 
#*****Foreground Turnaround Times
f3 = plt.figure(3)
pIDfturnaround = np.arange(0, len(fturnaround)) 
plt.bar(pIDfturnaround, fturnaround, tick_label = pIDfturnaround, 
width = 0.2, color = ['red', 'green','blue'])   
plt.xlabel('Process ID') 
plt.ylabel('Turnaround Time(Clock Loop)') 
plt.title('Foreground Turnaround Times') 


#*****Background Turnaround Times
f4 = plt.figure(4)
pIDbturnaround = np.arange(0, len(bturnaround)) 
plt.bar(pIDbturnaround, bturnaround, tick_label = pIDbturnaround, 
width = 0.2, color = ['red', 'green','blue'])   
plt.xlabel('Process ID') 
plt.ylabel('Turnaround Time(Clock Loop)') 
plt.title('Background Turnaround Times') 
plt.show()


#*****CPU Utility & Throughput
f1 = plt.figure(1)
objects = ('CPU Utility', 'Throughput')
y_pos = np.arange(2)
bartitles = [CPUuti,throughput]
plt.bar(y_pos, bartitles, align='center', alpha=1)
plt.xticks(y_pos, objects)
plt.ylabel('Value')
plt.title('CPU Utilisation & Throughput')


#*****Overall Response Time & Overall Turnaround Time
f2 = plt.figure(2)
objects = ('Overall Response Time', 'Overall Turnaround Time')
y_pos = np.arange(2)
bartitles = [overallResponseT,overallTurnaroundT]
plt.bar(y_pos, bartitles, align='center', alpha=1)
plt.xticks(y_pos, objects)
plt.ylabel('Value')
plt.title('Overall Response Time & Turnaround Time')


#*****Avarage Queue Lengths
f3 = plt.figure(3)
objects = ('Foreground', 'Background')
y_pos = np.arange(2)
bartitles = [fAvgLen,bAvgLen]
plt.bar(y_pos, bartitles, align='center', alpha=1)
plt.xticks(y_pos, objects)
plt.ylabel('Value')
plt.title('Average Queue Lengths')
plt.show()


#*****Queue Lengths - Time
f1 = plt.figure(1)
fig, ax = plt.subplots()
fig.suptitle('Queue Lengths - Time')
ax.plot(timeArr, fLenTime, label="Foreground")
ax.plot(timeArr, bLenTime, label="Background")
ax.legend()
ax.set(xlabel='CPU Clock Loop', ylabel='Length(Number of process)')
ax.grid()


#*****Priority - Time
f2 = plt.figure(2)
fig, ax = plt.subplots()
fig.suptitle('Queue Priority')
ax.plot(timeArr, fratioTime, label="Foreground")
ax.plot(timeArr, bratioTime, label="Background")
ax.legend()
ax.set(xlabel='CPU Clock Loop', ylabel='Priority')
ax.grid()
plt.show()




