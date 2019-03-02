# Scratch-Over

Link to [Scratch Project](https://scratch.mit.edu/projects/198253712/)

Lang = Python

# Reason

A week or two ago (Date today is 2/22/19), I decided to learn a little bit of Python. I didn't know what would be a good project to work on, but eventually I thought up of an old Scratch project that the U of U Coding Boot Camp assigned before the course began. That project can be found [here](https://scratch.mit.edu/projects/198253712/). Seemed like the perfect thing to port over to Python. 

So far, it seems like all of my code is spaghetti, but it works.

# Things

* ~~Fix music timing, starts too early sometimes~~
* Fix music while paused in transition (Kinda fixed)
  * This fix can be applied to make sure the powerups don't have the same problem
* Powerups kinda fixed too, the pausing mechanic throws off the timing and can potentially be abused to get a power up spawned just by waiting awhile in the pause menu
  * Can possibly remedy this by applying the exact fix you used to fix the music timing

# Later Things

## To Do 2

* Clean/Organize
* Meow sound on game over
* Change web sprite on powerup?
* Change direction of fly_cat randomlY?
* Maybe add input from pause to have immediate response? And maybe if key is still held, don't delete it?
  * Might have to make the event loop almost the same as the main game event loop to do this
* Add mute button?
* Add volume control on main game and/or pause screen and/or start screen?

# Known Bugs

* Sometimes fly_cat will crash the game, err given: cannot pop from empty list (interesting)
  * Make fly_cat invulnerable for half a second or one?
* Sometimes The game won't start on enter/space but will play the music. Just push esc/enter, and this will unfreeze and put you into the game
* Occasional lag
* Music has weird timing while transitioning every now and then
* Pausing may disrupt the powerups (slight fix implemented)

* More bugs to come!

# Fixes That Might Need More Stress Testing

* Game crash from button inputs going to main game from start screen and pause screen
* Check collision in spawn causing game to crash on pause