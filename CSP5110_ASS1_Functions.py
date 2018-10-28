import random
import unicodedata
def GetChoice(string_PromptText,tuple_ValidResponse):
	bool_ResponseIsValid=False
	string_Choice=""
	while bool_ResponseIsValid==False:
		string_Choice=input(string_PromptText)
		try:
			tuple_ValidResponse.index(string_Choice)
			bool_ResponseIsValid=True
		except ValueError as err:
			bool_ResponseIsValid=False
			print("\nInvalid input.\nString input is case senstive.\nChoose from: ", tuple_ValidResponse)
		#endtry
	#endwhile
	return string_Choice
#endFunction



def RollNDice(int_NumberOfDice):
	list_DiceRoll=list()
	for count in range(0,int_NumberOfDice):
		list_DiceRoll.append(random.randint(1,6))
	#endfor
	list_DiceRoll.sort()
	print("\nDice Roll:",end="")
	for d in list_DiceRoll:
		print(unicodedata.lookup("DIE FACE-"+str(d)),sep='',end='')
	#endfor
	print()
	return list_DiceRoll
#endfunction

def AllFourOne(int_DieFrequency, int_DieValue):
	if (int_DieValue==1) and (int_DieFrequency>=4):
		return 20
	else:
		return int_DieFrequency*int_DieValue
	#Endif
#EndFunction

def ReservePoints(list_Dice):
	int_DieFrequency=0
	int_Points=0
	int_DiceRemaining=len(list_Dice)
	string_Response=""
	bool_Straight_Exists=True
	#One match at a time, Display the match then ask to reserve points. Repeat for other matches.
	for int_DieValue in range(1,7): #range(start,stop) start value is included. Stop value is excluded.
		int_DieFrequency=list_Dice.count(int_DieValue)
		if int_DieFrequency>1:		
			print("\nMatching %d x %s. Can Reserve %d points." %(int_DieFrequency,unicodedata.lookup("DIE FACE-"+str(int_DieValue)),AllFourOne(int_DieFrequency,int_DieValue)))
			string_Response=GetChoice("Reserve points? yes/no:",('yes','no'))
			if string_Response=="yes":
				int_Points=int_Points+AllFourOne(int_DieFrequency,int_DieValue)
				int_DiceRemaining=int_DiceRemaining-int_DieFrequency
			#endif
			bool_Straight_Exists=False
		#endif
	#endfor
	if (bool_Straight_Exists==True) and len(list_Dice)==6:
		print("\nYOU ROLLED A STRAIGHT!!! 50 POINTS")
		int_Points=50
	#Endif
	print("\nThis Roll:%d points reserved. %d dice remaing."%(int_Points,int_DiceRemaining))
	return int_Points, int_DiceRemaining
#endfunction

def GetDifficulty():
	int_MaxTurns=0
	string_Difficulty=""
	string_Difficulty=GetChoice("\n\nSelect Difficulty. easy/normal:",('easy','normal'))
	if string_Difficulty=="normal":
		int_MaxTurns=3
		print("Selected: normal")
	elif string_Difficulty=="easy":
		int_MaxTurns=4
		print("Selected: easy")
	else:
		int_MaxTurns=0
		print("Selected: Skip Turn")
	#endif
	return int_MaxTurns
#endFunction

def PlayOneTurn():
	list_DiceRoll=list()
	int_RollPoints=0
	int_TurnScore=0
	int_NextRollDice=6
	bool_EndTurn=False
	while bool_EndTurn==False:
		list_DiceRoll=RollNDice(int_NextRollDice)
		int_RollPoints, int_NextRollDice=ReservePoints(list_DiceRoll)
		if int_RollPoints==0:
			bool_EndTurn=True
			print("%d reserved points lost."%int_TurnScore)
			int_TurnScore=0
		else:
			int_TurnScore=int_TurnScore+int_RollPoints
			if int_NextRollDice>1:
				if "yes"==GetChoice("\n\n\n\nRoll Again? yes/no:",('yes','no')):
					bool_EndTurn=False
				else:
					bool_EndTurn=True
				#endif
			else:
				bool_EndTurn=True
				print("\nToo few dice to continue rolling.")
			#Endif
		#Endif
	#EndWhile
	print("You won %d points this turn."%int_TurnScore)
	input("Press 'Enter' to continue")
	#if int_TurnScore==0:
		#input("Press 'Enter' to Continue")
	return int_TurnScore
	#EndFunction