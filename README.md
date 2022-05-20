# Discord-Save-Ping
A simple Discord Bot with a save reworked ping system. It's using the discord.py package by Rapptz.
<br>
This bot is part of the german multi-gaming discord community Rosenrudel: https://discord.gg/ep8FcXT

## Usage (Slash Commands)
### User Level
#### Ping
`/ping [role]` pings the given role.

The roles, which are pingable from which role is determined by
the configuration taken by the admin with `addRule`

### Moderator Level
#### Member
`/members [role]` gives a member list of the given role.

----
#### Print Rules
`/printRules` gives all rules which where input by the admin with `addRule`

### Admin Level
#### Set Moderator Role
`/addModeratorRole [role]` sets the moderator role, which is required to use the moderator level commands. The default role name for the moderator role is 'moderator'.

----

#### Remove Moderator Role
`/removeModeratorRole [role]` removes a moderator role from the system.

----

#### Add Rule
`/addRule [role] [relation] [role]` enables pings for the given configuration.

`[relation]` can be `->`, `<-`, `<->`

##### Example
- `/addRule @Helper -> @Beginner`, enables the ping command for @Helper to ping @Beginner
- `/addRule @Helper <- @Beginner`, enables the ping command for @Beginners to ping @Helper
- `/addRule @Helper <-> @Beginner`, enables the ping command for both to ping each other
