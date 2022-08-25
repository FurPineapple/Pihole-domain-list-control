# Pihole-domain-list-control
Apply automated changes based on time to Pi-Hole Gravity database's table 'domainlist'. Control access to resources using blacklists/whitelists as well as wildcarded lists.

* Dependencies:

  * Running Pi-Hole
  
  * Existing domain blacklists/whitelists
    
    * Can check using Web GUI or directly in Gravity.db
   
>**The script changes domain-list state according to it's comment. This way many blacklists/whitelists can be targeted at a time. That is why you may want to apply pattern comment to all the domain-lists you wish to change state. You can target many comment patterns sametimes affecting many groups at a time.**

For example regular expression blacklist to deny all DNS queries would be `'.*'` - comment 'Learning Time', and regular expression whitelist (to allow queries only for selected resources) `'.*github.com'` - comment 'Learning Time'. This way you can use 'Learning Time' comment as the refference to 2 domain-lists: blacklist (`'.*'`) and whitelist (`'.*github.com'`). Enabling both will end-up with successful reach of any GitHub.com link nothing more.

# To change state automatically create systemd .service with .timers

> Example found below:

### Create service unit with argument (run commands as root or evaluated user)

```
nano /etc/systemd/system/gravity-domain-list-ctrl@.service
```

>Content example:
    
```
[Unit]
Description=Changes state for marked domains

[Service]
Type=simple
ExecStart=/usr/bin/python3 /usr/local/usr-pihole-scripts/domain-list-ctrl.py %i -c 'Learning Time'

[Install]
WantedBy=multi-user.target
```

***Place your domain-list's comments instead of 'Learning Time' and divided with `space` bar if using more than one comment***

### Create enabling timer unit with argument (run commands as root or evaluated user)

```
nano /etc/systemd/system/gravity-domain-list-ctrl@enabled.timer
```

>Content example:
    
```
[Unit]
Description=Triggers change of state for marked domains

[Timer]
OnCalendar=*-*-* 08:30:00

[Install]
WantedBy=timers.target
```

### Create disabling timer unit with argument (run commands as root or evaluated user)


```
nano /etc/systemd/system/gravity-domain-list-ctrl@disabled.timer
```

>Content example:
    
```
[Unit]
Description=Triggers change of state for marked domains

[Timer]
OnCalendar=*-*-* 16:30:00

[Install]
WantedBy=timers.target
```

# After creation of units enable ones

>Reload systemctl daemons (run as root or evaluated user)

```
systemctl daemon-reload
```

>Enable all the units (run as root or evaluated user ***change values inside each <>***)

```
systemctl enable gravity-domain-list-ctrl@<enabled/disabled>.<service/timer>
```

>Start each timer (run as root or evaluated user ***change values inside <>***)

```
systemctl start gravity-domain-list-ctrl@<enabled/disabled>.timer
```
