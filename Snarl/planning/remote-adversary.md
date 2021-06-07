## Remote adversary

we extend to our protocol of server-client interaction for remote adversary.
- the first thing we add to our server protocol is that if remote adversary is activated, server no only wait for human 
players, but also wait for human controlled adversaries, so our game start after all human players and human adversaries
  registered.
  
- now move messages have an additional key "by", indicates which type of actor in the game attempt to move(Player, Adversary)

- now server will also send `adv-update` message to all player adversary clients, an `adv-update` message is similar to
`player-update` message, it no longer has players' `name` and `id`, and the `position` refers to the position of current
  human controlled adversary.
  
- `start-level`, `end-level` and `end-game` will also send to adversary client
if remote adversary is activated.
