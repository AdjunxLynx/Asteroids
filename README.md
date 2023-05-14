# Asteroids

This is a small project made by me to create the game Asteroids using `pygame`

## main.py

using PyGame and a simple loop, the script Blits a character onto the screen. a function called `detect_events()` reads from all inputs, and if any of the arrow keys are pressed, will call the `move()` function

### Player

if no movement events are detected, the character will slow down to a halt by multiplying its current speed by `0.99`
the `move()` function using trigonemetry to create a moving effect every frame. the hypotenuse is used as the current speed being added to current position, and theta is the angle to either the x or y axis
this allows me to find the change in x and y, add (or subtract) them to the characters current x and y coordinate and then update the screen so the player has moved.
The player also has the ability to `shoot`, which creates an instance of the class `bullet`, which cannot be controlled, and moves in a straight line.

### Bullet

whenever a bullet is created, it is added to a list of all active bullets. if the length of the list is above 4, the player cannot shoot.
this list is used to detect wether or not the player has successfully shot an asteroid.
A comparison is made to see if the coordinates of any of the bullets are within any of the Asteroids coordinates. If so, they have collided and the asteroid should be destroyed.
each bullet has a despawn timer, and also cant be spammed, so can only be shot with a cooldown timer within eachother. 

### Asteroids

during this loop, a timer has been set, so that an instance of the class `Asteroids` is created at one of the 4 corners, with a random speed and rotation.
all asteroids are stored in a variable called `Asteroids_list`. this is later used to iterate over all asteroids and check if their coordinates are within a range of the characters coordinates
this acts as a detection system to see if an asteroid has hit the player. If so, game over.

### Scoreboard

if the player successfully shoots an Asteroid, the player has their score increased by a certain amount

## Pictures

This file stores all the sprites for the `Asteroids`, `Bullet` and `Player`.

## Scores

When the player dies, the final score, along with a user made alias is created and stored in a text file
This is used to create a leaderboard within the game, by loading all the scores and displaying the top 10


