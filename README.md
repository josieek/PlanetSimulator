Kudos to Tech With Tim

I used his tutorial, which can be found [here](https://www.youtube.com/watch?v=WTLPmUHTPqo&t=3052s),
to create the starting code, with the planets orbiting the sun. This was very well explained and easy to follow, even 
when I had little prior experience with python.

I then added moons of mars and earth by creating the Moon class, a subclass of Planet.
The moon class overrides the update_position method. Rather than taking into account the force of all planets, 
for this basic simulator it is sufficient to only take into account the gravitational force from the parent planet.
This method also updates the parent planet's velocity after taking the gravity of the moon into account

The draw method is also overriden so that the moons' orbits are not drawn

I determined the initial orbital speed of the moons using the formula v = sqrt(Gm/r), where m is the mass of a moon
and r is the distance from the planet centers