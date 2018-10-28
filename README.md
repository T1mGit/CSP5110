# CSP5110
My own implemenation of the dice game 'Greed' also known a 'Farkle' based on requirements in the assignment specification for this unit.
To play, you must roll the dice, gaining points for each legal combination achieved from the dice roll. You remove at lease 1 legal combination reducing the die pool and then roll again. you repeat until you decide not to roll again or until no legal combinatins are achieved. If you roll and achieve no legal combinations you lose all accumulated points from that round. If you "Quit while your ahead" you add all the point scored in that round to your total game score.

There are two versions: 
Version 1: The main py file contains the main game loop performing function calls imported from the functions.py file
Version 2: The entire python script contained in one py file

Version 1 was designed first because the logic of the game lent itself very nicely to break into well defined functional units.
Version 2 is simply version 1 with the function calls replaced by the actual function. Version 2 came about because the functions were only called once therefore their purpose was simply for readability and did not meet any criteria of code reuse.
