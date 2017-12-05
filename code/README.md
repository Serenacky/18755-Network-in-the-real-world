# Criminality Network 

#timeseies.py
read the input file 10years.csv and store all the timeseries for every crimetype's freuqency and its neighbor into timeseries.csv

# CreateInter.py
Connect mysql and read from table timeseries which contains all the timeseies for every crimetype's freuqency and its neighbor', calculate the cross correlation between
every two crime type, and write it into inter.csv, then load it into interCrime table.

# InterGephi.py
Connect mysql and read from table interCrime, set a threshold and write them into interedge.csv and internode.csv, which can create the inter-layer crime network.

# Global.py
Connect mysql and read from table timeseries, and sum crimes from all neighbors for each crime type, write it into allcrime_for_eachtype.txt, then load it into allplace table.

# GlobalToLocal.py
Connect mysql and read from table allplace, timeseries, and calculate the cross correlation
between global crime type and local crime type, and write it into global_to_local.csv, then load it into global_to_local table.

# weather.py
Connect mysql and read from table allplace, calculate the cross correlation between weather indicator and every crime type, and write it into weather.csv, then load it into weather table.

# weatherGephi 
Connect mysql and read from table weather, global_to_local,  if weather can lead to global crime and global crime can lead to local crime, and their cross correlation are all above the threshold, then write the weather and local crime into weathergephi.csv.

# unemployment
Connect mysql and read from table allplace, calculate the cross correlation between unemploy ent indicator and every crime type, and write it into unemployment.csv, then load it into unemployment table.

# unemploymentGephi
Connect mysql and read from table unemployment, global_to_local,  if unemployment can lead to global crime and global crime can lead to local crime, and their cross correlation are all above the threshold, then write the unemployment and local crime into unemploymentgephi.csv.

