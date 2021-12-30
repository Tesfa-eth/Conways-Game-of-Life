# Conway-s-Game-of-Life

## This collaboarative project is written between Tesfa, Swag, and Niki for [Coding Workshop](https://cs.bennington.college/courses/fall2021/coding/home).

It's a simulation of Conways's game of life, which is a game in a two-dimensional orthogonal grid of square cells.
There are two possible states of the cells, live or dead. Every cell interacts with its eight neighbours, which are 
the cells that are horizontally, vertically, or diagonally adjacent. This game is a zero-player game. 

The rules the cells follow are the ones bellow:
1) Any live cell with two or three live neighbours survives.
2) Any dead cell with three live neighbours becomes a live cell.
3) All other live cells die in the next generation. Similarly, all other dead cells stay dead.

Project status: finished

To use it:
Go to the file conways_game_of_life_improved. Then run in your unix terminal <python game.py>.

Technology used:
Language: Python
GUI Package: Pygame
GUI Menu Package: Pygame_menu
