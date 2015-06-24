import os
import datetime
import string
import math

print ("VolumeControl component, unit testing interface")

f_name = "log"

#Find a new filename
fnum = 0
filename = f_name + str(fnum) + ".log"

if os.path.isfile(filename) == False:
	fo = open(filename,"w");	
else:
	while os.path.isfile(filename) == True :
		fnum = fnum+1;
		filename = f_name + str(fnum) + ".log"
		if fnum>100:
			break;

if (fnum>100):			
	if (os.path.isfile(filename) == True):
		print ("over 100 logs. No empty file");
		exit();
else:
	fo = open(filename,"w");	
	
now = datetime.datetime.now()
fo.write(now.strftime("%m/%d/%Y %H:%M:%S \n"));

#main stuff

tvvol = 20;
mobilevol = 10;
state = False; 
mute = False;
nr_of_init = 0;
nr_of_connects = 0;
range_min = 0;
range_max = 0;
current_tvvol = 0;

while True:
	print ("TV=" + str(tvvol), end="") 
	if (mute):
	  print (",muted, ", end="")
	else:
	  print (",playing, ", end="")
	print ("Mobile="+str(mobilevol), end="")  
	if (state):
	  print (" connected");
	else:
	  print (" disconnected");
	
	#Init values and Get input
	x = str("");
	y = 0;
	x2 = str("");
	xx = input("Enter command: ");
	
	#Make sure input is valid alphanumeric. 
	zz = str(xx).replace(" ", "")	
	while (zz.isalnum()) == False:
		print ("Invalid input");
		xx = input("Enter command: ");
		zz = str(xx).replace(" ", "")
		
	#Get command+params 
	command = str(xx).split()

	#Convert input to uppercase to help the user with case sensitivity crap
	i=0;
	for xparam in command: 
		command[i]=command[i].upper();
		i=i+1;
	
	#get the 1st command from the input
	x = command[0];
		
	#get the parameter, valid range 0..99
	if (len(command)>1):
		if (command[1].isdecimal()):
			if (int(command[1])<100) and (int(command[1])>0):	#BUG, can't select init value to zero
				y = int(command[1]);
			else:
				print ("Invalid parameter.");
				continue;
		else:
			print ("Invalid parameter.");
			continue;
		
	#if empty, start again. Should not happen.
	if (x == ""):
		continue;		
	
	#Add to log file current state + input-command
	fo.write(str(tvvol)+" "+str(mobilevol)+" mute="+str(mute)+" connent="+str(state)+":"+str(x)+" "+str(x2)+"\n");
	
	#Command Handling
	if (x == "EXIT"): 
		fo.write("NR of inits: "+str(nr_of_init)+" \n");
		fo.write("NR of connects: "+str(nr_of_connects)+" \n");
		fo.close();
		break;	
		
	#Command Help
	if (x == "HELP"):
	   print ("-----------------------------------");
	   print ("reset - initializes the component to default - volume tv=20, mobile=10,");
	   print ("        unmuted, state=disconnected. Clears memory. ");
	   print ("tvsetinitvol ## - Set initial volume in tv, before connecting device.");
	   print ("                  Values 0..90. Alias 'tsiv' ");
	   print ("tvincvol - incremrent volume on TV. Alias 'tiv' ");
	   print ("tvdecvol - decrement volume on TV. Alias 'tdv' ");
#	   print "tvgetvol - Get current volume in TV. Alias 'tgv' "); # for next version
	   print ("mute - Toggles Mute TV volume ");
	   print ("connect - Connects the mobile device. Alias 'cnt' ");
	   print ("disconnect - Disconnects the mobile device. Alias 'dcnt' ");
	   print ("mobilesetinitvol ## - Set initial volume in MobileDevice, before ");
	   print ("                      connecting device. Values 0..20. Alias 'msiv' ");
	   print ("mobileincvol - incremrent volume on TV. Alias 'miv' ");
	   print ("mobiledecvol - decrement volume on TV. Alias 'mdv' ");
#	   print "mobilegetvol - Get current volume in TV. Alias 'mgv' "); # for next version
	   print ("\nhelp - prints this help.");	   
	   print ("-----------------------------------");
	   continue;
	   
	if (x == "RESET"):
		print ("Initialized.");
		tvvol = 20;
		mobilevol = 10;
		state = 0; 
		mute = 0;	   
		nr_of_init = nr_of_init+1;
		continue;
			
	if (x == "MUTE"):
		if (mute==0):
			mute = 1;
		else:
			# If TV vol is greater than 70 unmuting brings it down to 70
			if (tvvol>70):
				tvvol=70;
			mute=0;
		continue;
	  
	#Set TV Initial volume
	if (((x == "TVSETINITVOL") or (x == "TSIV" )) and (y !=0)):
		tvvol = y;
		continue;
	
	# Increment TV vol.
	if (x == "TVINCVOL" or x == "TIV" ): 
		if (state==True): 
			#Recalculate new range.
			current_tvvol = current_tvvol + 2;
			range_max = range_max +2;
			tvvol = math.ceil((range_max/20)*mobilevol);
			if (tvvol > 90): 
				tvvol=90; #TV vol limit 90
		if (mute==True): 
			#if (tvvol>70):tvvol=70; #uncomment this to fix the "BUG nr1"
			mute=0;
		if (state==False):
			tvvol = tvvol+2;
			if (tvvol > 90):
				tvvol=90; #TV vol limit 90
			continue;
		continue;

	# Decrement TV vol.
	if (x == "TVDECVOL" or x == "TDV" ):
		if (state) :
			#Recalculate new range.
			#current_tvvol = $current_tvvol - 2; #Uncomment to fix bug nr2.
			range_max = range_max-2;
			tvvol = math.floor((range_max/20)*mobilevol);
			if (tvvol < 0): tvvol=0;
		else:
			tvvol = tvvol-2;
			if (tvvol < 0): tvvol=0;
		if (mute):
			if (tvvol>70):tvvol=70; 
			mute=0;
		continue;

	#Get TV volume - for future versions.
	if (x == "TVGETVOL" or x == "TGV" ):
	   print (tvvol);
	   continue;

	#Get Mobile volume - for future versions.
	if (x == "MOBILEGETVOL" or x == "MGV" ):
	   print (mobilevol);
	   continue;

	#Set Mobile Inital volume		
	if ((x == "MOBILESETINITVOL" or x == "MSIV" ) and y !=0):
		mobilevol = y;
		if (mobilevol > 20): mobilevol=20;		
		continue;
	   
	#Increment Mobile Vol
	if (x == "MOBILEINCVOL" or x == "MIV" ):
		if (state==False):
			print ("not connected");
			continue;
		else: 
			mobilevol += 1;
			if (mobilevol > 20): mobilevol=20;
			tvvol = math.ceil((range_max/20)*mobilevol);
		continue;

	#Decrement Mobile Vol
	if (x == "MOBILEDECVOL" or x == "MDV" ): 
		if (state==False):
			print ("not connected");
			continue;
		else:
			mobilevol -= 1;
			if (mobilevol < 0): mobilevol=0;
			tvvol = math.floor((range_max/20)*mobilevol);
		continue;

	#Connect Mobile Device
	if (x == "CONNECT" or x == "CNT" ): 
		if (state):
			print ("Already connected");
			continue;
		else:
			state = True;
			current_tvvol = tvvol;
			range_max = tvvol;
			range_min = 0;
			#set TV vol to fraction, depending on the mobilevolvalue
			tvvol = math.floor((tvvol/20)*mobilevol);
			nr_of_connects += 1;
			continue;

	#Disconnect Mobile Device
	if (x == "DISCONNECT" or x == "DCNT" ): 
		if (state==False): 
			print ("Already disconnected");
			continue;
		else:
			state = 0;
			tvvol = current_tvvol;
			# Needs to take into account if the VOL was changed after connecting on the TV side. 
			# BUG nr.2 - Disconnecting should not increase the volume more than fraction change to full. 40 and 10M, connect -> 20 -> 5x step_dw_tv -> 10 disconnect -> 20, NOT 40.
			range_max = 0;
			range_min = 0;
		continue;

#This should be the end of big while loop.   
	
	
# Debug output of input main command.		
# print ("This was the last main command: ", x);

    
#End of program, close open file.
if (fo.closed==False):
	fo.close();


#print("hello world!")

#mylist=[1,2,3,4,5,6,0,2,1,1,2,3,4,1]

#biggest = -1

#for x in mylist:
#	if mylist[x] > biggest:
#		biggest = mylist[x]
		
#print (biggest)



