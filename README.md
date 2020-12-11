# Discord-Save-Ping
A simple Discord Bot with a save reworked ping system. It's using the discord.py package by Rapptz.
<br>
This bot is part of the german multi-gaming discord community Rosenrudel: https://discord.gg/ep8FcXT

## Usage
In this guide, the standard command prefix '$' is used.
This can be changed in the config file.
### User Level
#### Ping
`$ping [role name (without "@")]` pings the given role.

The roles, which are pingable from which role is determined by
the configuration taken by the admin with `addRule`

### Moderator Level
#### Member
`$members [role name]` gives a member list of the given role.

----
#### Print Rules
`$printRules` gives all rules which where input by the admin with `addRule`

### Admin Level
#### Set Moderator Role
`$addModeratorRole [role name]` sets the moderator role, which is required to use the moderator level commands. The default role name for the moderator role is 'moderator'.

----

#### Remove Moderator Role
`$removeModeratorRole [role name]` removes a moderator role from the system.

----

#### Add Rule
`$addRule [role mention 1] [relation] [role mention 2]` enables pings for the given configuration.

`[relation]` can be `->` (alias for empty), `<-`, `<->`

#### Set Default Role
`$setDefaultRole [role name]` sets a default role. If no role name is given, the default role is deleted.

#### Display Default Role
`$defaultRole` returns the current default role.

##### Example
- `$addRule @Helper -> @Beginner`, enables the ping command for @Helper to ping @Beginner
- `$addRule @Helper <- @Beginner`, enables the ping command for @Beginners to ping @Helper
- `$addRule @Helper <-> @Beginner`, enables the ping command for both to ping each other
