        Monitor
    Version 1.0 Written by Larry K Williams, II.  

    This is meant to monitor a local network for connectivity.  It's pretty
simple but i'll lay out the basic framework and how to configure it. 

Things you need:
    1. A server that can run python and flask (on Linux with cron)
    2. A few minutes to configure this.
    
Files to configure:
    1. hosts.txt 
    2. cronjob on your linux distro.

hosts.txt:
    This file needs to be single lines containing the hosts you want to 
    monitor.  For example:
        router.lan.com
        media.lan.com
        switch1.lan.com
    Don't put any comments in this file.  Just raw host names.

cronjob:
    *NOTE:
        This isn't meant to be a tutorial on using cronjob.  Please look up
        how to use and configure a cronjob if you are not familiar.  
    using "crontab -e" create an entry pointing to "connection_tester.py" and
    running it in it's parent directory.  For example (all as one line):
        (cd /home/username/automation && /usr/bin/env python3 
            /home/username/automation/connection_tester.py)
    Of course, yours will be different depending on where you installed this
    and set up your own server.  If you only need the script then the server
    info doesn't really matter.
    *NOTE 2:
        NOTICE that you should configure the cronjob to run in intervals of 
        every two minutes.  "*/2 * * * *" would be the appropriate time.  IF 
        you change this, please change this also in the connection_tester.py
        file as this calculated in the web site as well.  The tester script 
        doesn't know how long you set it for so it will need to be manually
        changed on the varialbe "interval_amount" at the top of the script.

After that, with a properly set up server, you should be able to get your
monitoring status within minutes. A few things to note:
    1. The cronjob interval needs to be 2 minutes.  See above.
    2. hosts.txt needs to be just hosts names.  That's it.
    3. The script needs to be able to write out hostspings.txt
    4. Most failures to get this to work boil down to improper configuration.
    5. The tooltips on the HTML side are calculated with the information in 
        the hostspings.txt file.
