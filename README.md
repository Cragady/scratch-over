# Scratch-Over

Link to [Scratch Project](https://scratch.mit.edu/projects/198253712/)

Lang = Python

# Reason

On 2/15/19, I decided to learn a little bit of Python. I didn't know what would be a good project to work on, but eventually I thought up of an old Scratch project that the U of U Coding Boot Camp assigned before the course began. That project can be found [here](https://scratch.mit.edu/projects/198253712/). Seemed like the perfect thing to port over to Python. 

So far, it seems like all of my code is spaghetti, but it works.

As of 3/2/19, this project operates in a way that is very similar to the scratch version of this game. All that's left is minor game changes, some bug fixes, and maybe code cleanup/reorganization. 

I know this code is a mess, but this was a for-fun-project to try to learn and get a grasp on Python. Now from here, if I continue to pursue projects utilizing Python, I'll be sure to read up on good coding conventions for this language, and heavily implement these practices. For now, this project can be put on a back-burner while I start practicing JavaScript again.

# Get The Basics (If you're new like me)

* You will have to install pygame globally, or in a virtual environment (This is how I installed it)
  * Terminal/CLI
    * `python -m pip install -U pygame --user`

# Module Versions

* (In the future I'll find a way to make the Python equivalent to package.json)
* python @ 3.7.2
* pygame @ 1.9.4

# Things

* ~~Fix music timing, starts too early sometimes~~
* Fix music while paused in transition (Kinda mostly fixed)
  * This fix can be applied to make sure the powerups don't have the same problem
* Powerups kinda fixed too, the pausing mechanic throws off the timing and can potentially be abused to get a power up spawned just by waiting awhile in the pause menu
  * Can possibly remedy this by applying the exact fix you used to fix the music timing

# Later Things

## To Do 2

* Clean/Organize?
* Change web sprite on powerup?
* Change direction of fly_cat randomlY?
* Maybe add input from pause to have immediate response? And maybe if key is still held, don't delete it?
  * Might have to make the event loop almost the same as the main game event loop to do this
* Add mute button?
* Add volume control on main game and/or pause screen and/or start screen?

# Known Bugs

* Sometimes The game will pause immediately if enter is pressed too quickly on start screen. Just push esc/enter, and this will unpause and put you into the game
* Occasional lag
* Music has weird timing while transitioning every now and then
  * Especially when pausing before/during transition
* Pausing may disrupt the powerups (slight fix implemented)

* More bugs to come!

# Fixes That Might Need More Stress Testing

* Game crash from button inputs going to main game from start screen and pause screen
* Check collision in spawn causing game to crash on pause
* fly_cat crashes game (seems to be fixed with the testing so far)

# Extra Notes

### Png crush images that have been edited

* [How to do](https://stackoverflow.com/questions/22745076/libpng-warning-iccp-known-incorrect-srgb-profile/29337595#29337595)
* In Terminal/CLI
  * `pngcrush -ow -rem allb -reduce file.png`