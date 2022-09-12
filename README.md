# Pihole-domain-list-control
Automate Pi-Hole DNS sinkhole's whitelists/blacklists. Apply automated changes based on time to Pi-Hole Gravity database's table 'domainlist' to allow or restrict queries. Control access to resources, select users whom apply changes to, select time to control DNS traffic.

* Dependencies:

  * Running Pi-Hole
  
  * Existing domain blacklists/whitelists
    
    * Can check using Web GUI or directly in Gravity.db
   
**The script changes domain-list state according to it's comment. This way many blacklists/whitelists can be targeted at a time. That is why you may want to apply pattern comment to all the domain-lists you wish to change state. You can target many comment patterns same-times affecting many groups at a time.**

For example regular expression blacklist to deny all DNS queries would be `'.*'` - comment 'Learning Time', and regular expression whitelist (to allow queries only for selected resources) `'.*github.com'` - comment 'Learning Time'. This way you can use 'Learning Time' comment as the reference to 2 domain-lists: blacklist (`'.*'`) and whitelist (`'.*github.com'`). Enabling both will end-up with successful reach of any GitHub.com link nothing more.

To affect certain users or certain user groups:

 * Create new non-default group (Example in Web GUI)
 
![github-pihole-groups-main](https://user-images.githubusercontent.com/43132663/186899940-9f4c403b-eccb-491d-8b96-1cc3bc4cb2bb.PNG)

![github-group-management](https://user-images.githubusercontent.com/43132663/186899938-b9f454c5-ca62-4634-a0b2-8cffd825c587.PNG)

 * Select clients from drop-down menu and assign them to your certain group

![github-select-client](https://user-images.githubusercontent.com/43132663/186899941-80a3ade4-3273-495e-960f-780d9d192682.PNG)

 * By default newly created domains are assigned to Default group, you need to change group assignment after creation.

![github-domain-group-assignment](https://user-images.githubusercontent.com/43132663/186899930-e9299876-9a68-4416-bf29-8d94cced329b.PNG)

You can add new domains directly to Gravity database, to add domains in disabled mode, this will prevent affecting restrictions to all the default group users. After creation change assigned group and state to enabled. Documentation for Gravity database found:

```
https://docs.pi-hole.net/database/gravity/
```
# Overview

The script `domain-list-ctrl.py` uses sqlite3 and re modules as well as argparse for the use of arguments.
See below command for help (do not forget to correct the path): 

```
/path/to/python3 /path/to/domain-list-ctrl.py -h
```

The pattern for use would be:

```
python3 domain-list-ctrl.py <enabled/disabled> <domainlist_comment/domainlist_comment_list>
```

This pattern will be used in Linux services onwards.

## Steps

### 1. Place the script 

Choose the directory to store `domain-list-ctrl.py`.

### 2. Create systemd .service with .timers

Examples found below:

* Create service unit with argument (run commands as root or evaluated user)

```
nano /etc/systemd/system/gravity-domain-list-ctrl@.service
```

Content example:
    
```
[Unit]
Description=Changes state for marked domains

[Service]
Type=oneshot
Restart=on-failure
ExecStart=/usr/bin/python3 /usr/local/usr-pihole-scripts/domain-list-ctrl.py %i -c 'Learning Time'
ExecStartPost=/bin/systemctl start reload-domainlists.service

[Install]
WantedBy=multi-user.target
```

* Create service unit to only update the lists WITHOUT flushing the cache or restarting the DNS server right after the Domain state change

```
[Unit]
Description=Reload lists after changes

[Service]
Type=simple
ExecStart=/usr/bin/bash /usr/local/bin/pihole restartdns reload-lists

[Install]
WantedBy=multi-user.target
```

***Change path to stored location of domain-list-ctrl.py script. Place your domain-list's comments instead of 'Learning Time' and divided with `space` bar if using more than one comment***

* Create enabling timer unit with argument (run commands as root or evaluated user)

```
nano /etc/systemd/system/gravity-domain-list-ctrl@enabled.timer
```

Content example:
    
```
[Unit]
Description=Triggers change of state for marked domains

[Timer]
OnCalendar=*-*-* 08:30:00

[Install]
WantedBy=timers.target
```

* Create disabling timer unit with argument (run commands as root or evaluated user)


```
nano /etc/systemd/system/gravity-domain-list-ctrl@disabled.timer
```

Content example:
    
```
[Unit]
Description=Triggers change of state for marked domains

[Timer]
OnCalendar=*-*-* 16:30:00

[Install]
WantedBy=timers.target
```

### 3. After creation of units enable ones

Reload systemctl daemons (run as root or evaluated user)

```
systemctl daemon-reload
```

Enable all the units (run as root or evaluated user ***change values inside each <>***)

```
systemctl enable gravity-domain-list-ctrl@<enabled/disabled>.<service/timer>
```

Start each timer (run as root or evaluated user ***change values inside <>***)

```
systemctl start gravity-domain-list-ctrl@<enabled/disabled>.timer
```
