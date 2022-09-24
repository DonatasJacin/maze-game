# maze-game

This is my end of A-level project. It is a game which generates mazes following a number of different maze generation algorithms 
such as Binary Tree and Aldous-Broder. A goal is placed randomly in the maze and the player must navigate the maze to the goal. 
The shortest path to the goal is calculated with Dijkstra's algorithm, and this distance is divided by player speed to achieve the minimum
time taken to reach the goal. A small amount of extra time is added and the player must get to the goal in the given time.

As the player progresses through the game, the maze sizes increase, the maze generation algorithm becomes more random (less biased) and the
density of dead-ends in the maze is increased. The difficulty of the game is dynamic.

The implementation of this game is done in python, with the use of pygame.

For an in-depth report, check the attached documentation.
