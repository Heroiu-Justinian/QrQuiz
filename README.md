# QrQuiz
This is a simple game written in python in which you can solve a Qr code that you can then scan.

# Usage
Using it is simple:

```console
$ pip install -r requirements.txt
$ python game.py some_data string 
```
Example:
```console
$ python game.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## How it works

The game takes the data and generates a QR code ( might be any kind of text, not necessarily a link ).
From the QR code, it generates an outer frame for the game which is an image and an inner grid which is the playable part
Any cell in the grid can be clicked to change its state from white to black and vice versa to solve the puzzle. 
The game will display in terminal the lines that have been solved. 

In case you want to solve the game instantly, you can press left ctrl

