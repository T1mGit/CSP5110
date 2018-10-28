# CSP5110
<h2>Farkle - The Game of Greed</h2>
<p>My own implemenation of the dice game 'Greed' also known as 'Farkle' based on requirements in the assignment specification for this unit.
<p>To play, you must roll the dice, gaining points for each legal combination achieved from the dice roll.<br>You remove at least 1 legal combination reducing the die pool and then roll again.<br>Repeat until you decide not to roll again or until no legal combinatins are achieved. If you roll and achieve no legal combinations you lose all accumulated points from that round. If you "Quit while your ahead" you add all the point scored in that round to your total game score.

<p>There are two versions:<br>
Version 1: The main py file contains the main game loop performing function calls imported from the functions.py file.<br>
Version 2: The entire python script contained in one py file.

<p>Version 1 was designed first because the logic of the game lent itself very nicely to break into well defined functional units.<br>
Version 2 is simply version 1 with the function calls replaced by the actual function. Version 2 came about because the functions were only called once therefore their purpose was simply for readability and did not meet any criteria of code reuse.

<h2>Quizzle - A simple quiz to test your general ignorance</h2>
The Quizzle script has the admin.py and the quizzle.py file both of which are run independantly.<br>
admin.py is a command line script which is used to create and manage the data file data.txt for the quiz.<br>
quizzle.py uses the tkinter library to create a gui for displaying questions and recieving answers. quizzle.py reads the data.txt file (which is in JSON format) to obtain a selection of 5 quiz questions.
