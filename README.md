# TYPE-AND-RACE

A multiplayer 2D racing game where your typing speed drives your car. 
Built with Python and Pygame.

## Features
* Multiplayer support for up to 4 players on a local network (LAN).
* Auto-filling AI bots if there are less than 4 human players.
* Real-time typing mechanics: correct letters speed you up, wrong letters slow you down.
* Interactive Start and Restart system.

## Requirements
* Python 3.x
* Pygame

## Installation
1. Clone this repository to your local machine.
2. Install the required library using the command:
   `pip install -r requirements.txt`
3. Make sure you have the car images (`car0.png`, `car1.png`, `car2.png`, `car3.png`) in the project folder.

## How to Play
1. **Start the Server:** Open a terminal and run `python server.py`.
2. **Start the Game:** Open a new terminal and run `python client.py`.
3. **Multiplayer:** To join from another computer on the same Wi-Fi, change the IP address in `client.py` to the server's IP address, then run `client.py`.
4. Click the **START** button on the screen.
5. Type the words exactly as they appear. Type fast to win the race!

## Security Note
This game is designed for Local Area Networks (LAN) only. It uses the Python `pickle` module for network data transfer. Do not host the server on a public global network for security reasons.
## Author
Student of Inha, Ubaydullo