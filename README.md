# My-Bad-Bad-Ice-Cream
This is my attempt to recreate the popular game. The game supports both single-player and multi-player mode so you can choose between playing
with a friend on a local network or playing by yourself.

## How to play:
Move the player with the arrow key, make/break ice with the space key

## How to setup and run:
1. Either download a zip file or clone this repository
2. Create a virtual environment by typing:
```
python -m venv venv
```
3. Install the dependencies:
```
pip install -r requirements.txt
```
4. To start the game run the following file:
```
python main.py
```
5. If you want to play in multi-player mode you have to do the following first:
- Copy the IPv4 address of the machine on which you are going to run the server <br>
In the cmd type:
```
ipconfig
```
and find the IPv4 address
- Paste the address to the SERVER variable in the server.py and client.py files
<img width="557" alt="image" src="https://user-images.githubusercontent.com/92211354/218333720-bfc3a49d-843d-4720-95ab-f883bab94c4f.png">

- Make sure to run the server file before choosing a level in multiplayer mode:
```
python server.py
```
If someone else connected to the server has also chosen the same level, you both will be playing together.

## How to run the tests:
- To run the tests type:
```
python -m unittest discover -s tests
```
This will run all of the tests in tests directory <br>
- To run a specific test type:
```
python -m unittest discover -s tests -p "test_[name of the module].py"
```