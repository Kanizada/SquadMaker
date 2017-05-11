# SquadMaker

SquadMaker is a [discord.py](https://github.com/Rapptz/discord.py) based bot, the first version was created for a [specific server](https://discord.gg/waUSDfd). The idea was to make easier the squad formation on the server.

  - Colored role
  - Display players by level
  - Some others features

##### /!\ WARNING : The bot was made for this specific server, than means the first version can't be use on another server without edit /!\

### Commands
 -  Administrations
    - !restart  :    Restart the bot.
    - !stop     :    Stop the bot.
    - !purge    :    Only allowed roles can purge channel.
    - !clean    :    Delete bot's messages.
    - !fallen   :    Made to remove all roles.
    - !path    :     Use to find the path of the script.
    - !createrole :  Allow to create role.
    - !deleterole :  Allow to delete role.
 -  Informations
    - status  :     Get status of the bot.
    - disk_usage :  Get disk usage of the server.
    - ping  :       Ping command.
 -  Matchmaking
    - dispo        Command to tag "disponible".
    - ndispo       Command to untag.
    - panneau      Display a list of tagged players by level.
    - stats        Statistics of use.
    - reset        Command to remove role "disponible" from all members.
 -  Pictures
    -   cat          Send random picture about cute cats.
 -  Debug 
    -  whatsmyid    Know your id.
    - whatsmyroles Know your roles.
    - listallroles List all roles from the server.
    - raw_content  Write content raw to debug.


### Installation

Need Python (logic ?) and pip for dependency.

```sh
$ pip install aiohttp appdirs async-timeout cffi chardet ez-setup multidict packaging pycparser six PyNaCl
$ pip install pyfiglet pyparsing python-apt python-dateutil unattended-upgrades Unidecode websockets xmltodict
```

The bot work with a systemd service, need to create one or edit the bot.

### Todos

 - Cross-server
 - Maybe clean ? ("CHECK" in comment)




