use POSIX qw/floor/;
use POSIX qw/ceil/;
use POSIX qw/strftime/;
#use strict;

# This is version with inputfile handling and additional changes for advanced testing.
# Added bugfixes : Bug 1 & 2; Aslo init values can be set to 0;
# 16th input is ignored from inputfile is still in.
# 	Added command line input. Must be filename in same dir, with one command on each row. Commands executed on one by one, no logic.
# 	Exection log does not show whitespace commands, but those count as commands for 16th-bug.
# 
# Added functionality:
#   * User volume value in addition to real volume - done
#   * Headphones support? - 
#   *

print "VolumeControl component with inputfile handling, unit testing interface\n";
print "\n";
 

#Input file parsing 
$inputfileinuse = 0;	
my $num_args = $#ARGV + 1;
if ($num_args > 0) {
	$input_file = $ARGV[0];
	if (-e $input_file) 
	{
		open (INFILE, $input_file);
		while (<INFILE>) {
			chomp;
			#($in_command, $in_param ) = split(" ");
			#print "$in_command, $in_param \n";
			push @input_commands, [ split " " ];
		}
		close (INFILE);
		$inputfileinuse = 1;	
	}
	else
	{
		print "Input file missing! \n";
		$inputfileinuse = 0;	
	}
}

#Count the inputfile commands + params
$commands_in_inputfile = 0;
foreach $row (0..@input_commands-1)
{
  #foreach $column (0..@{$input_commands[$row]})
  #{
  #  print "Element [$row][$column] = $input_commands[$row][$column] \n";
  #}
  $commands_in_inputfile++;
}
 

 
#create logfile
$filename = "log0";
$i = 1;
while (-e $filename.'.txt')
{
  $filename++;
}
open (MYFILE, '>'.$filename.'.txt');
my $date = strftime "%m/%d/%Y %H:%M:%S", localtime;
print MYFILE "$date \n";

$tvuservol = 20; 
$tvvol = 20;
$mobilevol = 10;
$state = 0; 
$mute = 0;
$nr_of_init = 0;
$nr_of_connects = 0;
$range_min = 0;
$range_max = 0;
$current_tvvol = 0;
$command_in_use_row = 0;

while (1)
{
    print "UserVol=$tvuservol, ";
	print "TV=$tvvol ";
	if ($mute){
	  print ",muted, ";}
	else{
	  print ",playing, ";}
	print "Mobile=$mobilevol, ";  
	if ($state){
	  print "connected\n";}
	else{
	  print "disconnected\n";}
	print "Enter command: ";
	if ($inputfileinuse)
	{
		if ($commands_in_inputfile == $command_in_use_row)
		{
			$inputfileinuse = 0;
			print MYFILE "$tvuservol, $tvvol, $mobilevol, mute=$mute, connect=$state : End of input file, exiting\n";
			print " End of input file, exiting \n";
			print MYFILE "NR of inits: $nr_of_init \n";
			print MYFILE "NR of connects: $nr_of_connects \n";
			close (MYFILE);
			exit;
		}
		$x = "$input_commands[$command_in_use_row][0] $input_commands[$command_in_use_row][1]";
		$command_in_use_row++;
		#Next IF adds new Bug, nr6 - every 16th command from file input is ignored.
		$is_sixteenth = $command_in_use_row % 16;
		if ($is_sixteenth == 0 ){$command_in_use_row++;}
		print "$x \n";
	}
	else
	{
		$x = <STDIN>;
		chomp $x;
	}
		$y=0;
		$x = uc($x); #Convert input to uppercase to help the user with case sensitivity crap
		$x =~ s/\s*$//;  #delete whitespace from right.
		if ($x eq "") {next} #if empty, start again.
		#Add to log file.
		print MYFILE "$tvuservol, $tvvol, $mobilevol, mute=$mute, connect=$state : $x\n";
		#Check if paramter is there and separate parameter
		if (($sep_pos=(index $x, " ")) != -1 ) 
		{
		$y = substr($x, $sep_pos+1, 2); #parameter 
		$x = substr($x, 0, $sep_pos); #main command
		#print "DEBUG: $x | $y | $sep_pos\n";
		if ($y !~ /^\d+$/ || $y < 0 || $y > 90 || length($y) > 2) {print "Invalid parameter.\n\n"; next;}	  
		}
	#}
	if ($x eq "EXIT") 
		{
			print MYFILE "NR of inits: $nr_of_init \n";
			print MYFILE "NR of connects: $nr_of_connects \n";
			close (MYFILE);
			exit;
		}
	if ($x eq "HELP") 
	 {
	   print "-----------------------------------\n";
	   print "reset - initializes the component to default - volume tv=20, mobile=10,\n";
	   print "        unmuted, state=disconnected. Clears memory. \n";
	   print "tvsetinitvol ## - Set initial volume in tv, before connecting device.\n";
	   print "                  Values 0..90. Alias 'tsiv' \n";
	   print "tvincvol - incremrent volume on TV. Alias 'tiv' \n";
	   print "tvdecvol - decrement volume on TV. Alias 'tdv' \n";
#	   print "tvgetvol - Get current volume in TV. Alias 'tgv' \n"; # for next version
	   print "mute - Toggles Mute TV volume \n";
	   print "connect - Connects the mobile device. Alias 'cnt' \n";
	   print "disconnect - Disconnects the mobile device. Alias 'dcnt' \n";
	   print "mobilesetinitvol ## - Set initial volume in MobileDevice, before \n";
       print "                      connecting device. Values 0..20. Alias 'msiv' \n";
	   print "mobileincvol - incremrent volume on TV. Alias 'miv' \n";
	   print "mobiledecvol - decrement volume on TV. Alias 'mdv' \n";
#	   print "mobilegetvol - Get current volume in TV. Alias 'mgv' \n"; # for next version
	   print "\nhelp - prints this help.\n";	   
	   print "-----------------------------------\n";
	   print "\n";
	   next;
	 }
	if ($x eq "RESET") 
	  {
		print "Initialized. \n";
		$tvuservol = 20;
		$tvvol = 20;
		$mobilevol = 10;
		$state = 0; 
		$mute = 0;	   
		$nr_of_init = $nr_of_init+1;
		next;
	  }
	if ($x eq "MUTE") 
	  {
	   if (!$mute) 
	   {
			$mute = 1; 
			$tvuservol = "0"; # user is shown 0 if muted
		}
	   else
	   {
	   # If TV vol is greater than 70 unmuting brings it down to 70
			if ($tvvol>70){$tvvol=70;}
			$tvuservol = $tvvol;
			$mute=0;
	   }
		next;
	  }
	if (($x eq "TVSETINITVOL" || $x eq "TSIV" ) && $y > -1 )
	{
		$tvvol = $y;
		$tvuservol = $tvvol;
		next;
	}
	# Increment TV vol.
	if ($x eq "TVINCVOL" || $x eq "TIV" ) 
	{
		if ($state) 
		{
			#Recalculate new range.
			$current_tvvol = $current_tvvol + 2;
			$tvuservol = $tvuservol + 2; # how is this different from current_tvvol? - can't remember how that was used.
			$range_max = $range_max + 2;
			$tvvol = ceil(($range_max/20)*$mobilevol);
			if ($tvvol > 90) {$tvvol=90;} #TV vol limit 90
			if ($tvuservol > 90) {$tvuservol=90;} #TV User Shown vol limit 90
		}
		if ($mute) 
		  {
		    if ($tvvol>70){$tvvol=70;} #uncomment this to fix the "BUG nr1"
			$tvuservol = $tvvol; # user shown volume is back to real value.
			$mute=0;
		  }
		if (!$state)
		{		
			$tvvol = $tvvol+2;
			if ($tvvol > 90) {$tvvol=90;} #TV vol limit 90
			$tvuservol = $tvvol; 			
			next;
		}
		next;
	}
	# Decrement TV vol.
	if ($x eq "TVDECVOL" || $x eq "TDV" ) 
	{
		if ($state) 
		{
			#Recalculate new range.
			$current_tvvol = $current_tvvol - 2; #Uncomment to fix bug nr2.
			$tvuservol = $tvuservol - 2;
			$range_max = $range_max-2;
			$tvvol = floor(($range_max/20)*$mobilevol);
			if ($tvvol < 0) {$tvvol=0;}
			if ($tvuservol < 0) {$tvuservol=0;}
		}
		else
		{
			$tvvol = $tvvol-2;
			if ($tvvol < 0) {$tvvol=0;}
			$tvuservol = $tvvol; 		
		}
		if ($mute) 
		  {
		    if ($tvvol>70){$tvvol=70;} 
			$tvuservol = $tvvol; 		
			$mute=0;
		  }
		next;
	}
	#Get TV volume - for future versions.
	if ($x eq "TVGETVOL" || $x eq "TGV" )
	{
	   print "$tvvol \n";
	   next;
	} 	
	#Get Mobile volume - for future versions.
	if ($x eq "MOBILEGETVOL" || $x eq "MGV" )
	{
	   print "$mobilevol \n";
	   next;
	}
	#Set Mobile Inital volume		
	if (($x eq "MOBILESETINITVOL" || $x eq "MSIV" ) && $y > -1)
	{
		$mobilevol = $y;
		if ($mobilevol > 20) {$mobilevol=20;}		
		next;
	}
	#Increment Mobile Vol
	if ($x eq "MOBILEINCVOL" || $x eq "MIV" ) 
	{
		if (!$state) 
		  {
		    print "not connected\n";
			next;
		  }
		else 
		{
			$mobilevol = $mobilevol+1;
			if ($mobilevol > 20) {$mobilevol=20;}
			$tvvol = ceil(($range_max/20)*$mobilevol);
			# Bug here, as the the upper range is not checked for TV, thus one can get over 90.
		}
		next;
	}
#Decrement Mobile Vol
	if ($x eq "MOBILEDECVOL" || $x eq "MDV" ) 
	{
		if (!$state) 
		  {
		    print "not connected\n";
			next;
		  }
		else 
		{
			$mobilevol = $mobilevol-1;
			if ($mobilevol < 0) {$mobilevol=0;}
			$tvvol = floor(($range_max/20)*$mobilevol);
			# Bug here, as the the lower range is not checked for TV, thus one can get under 0.
		}
		next;
	}
#Connect Mobile Device
	if ($x eq "CONNECT" || $x eq "CNT" ) 
	{
		if ($state) 
		{
		    print "Already connected\n";
			next;
		}
		else 
		{
			$state = 1;
			$current_tvvol = $tvvol;
			$range_max = $tvvol;
			$range_min = 0;
			# User vol is not changed thus that value is not changed :)
			#set TV vol to fraction, depending on the mobilevolvalue
			$tvvol = floor(($tvvol/20)*$mobilevol);
			$nr_of_connects = $nr_of_connects+1;
			next;
		}
	}
#Disconnect Mobile Device
	if ($x eq "DISCONNECT" || $x eq "DCNT" ) 
	{
		if (!$state) 
		  {
		    print "Already disconnected\n";
			next;
		  }
		else 
		{
			$state = 0;
			$tvvol = $current_tvvol;
			# User vol is not changed thus that value is not changed :)
			# Needs to take into account if the VOL was changed after connecting on the TV side. 
			# BUG nr.2 - Disconnecting should not increase the volume more than fraction change to full. 40 and 10M, connect -> 20 -> 5x step_dw_tv -> 10 disconnect -> 20, NOT 40.
			# Bug 2 is fixed in this version.
			$range_max = 0;
			$range_min = 0;
		}
		next;
	}

	print "Illegal command\n";
#	if ($x !~ /^\d+$/ || $x < 0 || $x > 50 || length($x) > 2) {print "Come on. Follow the rules.\n\n"; next;}	

	}
close (MYFILE); 
