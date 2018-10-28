#########################################################################################
#							FARKLE The Game of Greed									#
#								Written by Tim Hyde										#
#									Python 3.6.2										#
#						Version:2.0 Created:2017-08-06									#
#																						#
#Reference for standard libraries:														#
#Gaddis, T. (2015). Starting out with Python:Third edition.								#
#	Harlow, England: Pearson Education Limmited											#
#Python Software Foundation. Python Language Reference, version 2.7.					#
#	Available at http://www.python.org													#
#																						#
#########################################################################################
import random
import unicodedata

############################### - FUNCTION DEFINITIONS - #################################


#GetChoice receives input from the user as a string and validates to ensure that it is
#matches exactly the options provided in the ValidResponse parameter.
#The valid response tuple can be any length, but is only ever 2 in this application.
def GetChoice(string_PromptText,tuple_ValidResponse):
	bool_ResponseIsValid=False
	string_Choice=""
	while bool_ResponseIsValid==False:
		string_Choice=input(string_PromptText).lower()
		#try:                                                           DELETED THIS LINE
		if string_Choice in tuple_ValidResponse:
			tuple_ValidResponse.index(string_Choice)
			bool_ResponseIsValid=True
		#except ValueError as err:                                      DELETED THIS LINE
		else:
			bool_ResponseIsValid=False
			print("\nInvalid input.\nChoose from: ", tuple_ValidResponse)
		#endtry
	#endwhile
	return string_Choice
#endFunction



#########################################################################################	
#********************************MAIN FUNCTION START************************************#
#########################################################################################
dictionary_GameOverMessage={40:'Good Score!',50:'Great Score!',60:'Excellent Score!'}

print(('#'*25).center(100)+'\n'+('#'+' '*23+'#').center(100)+'\n'+'#   Welcome to FARKLE   #'.center(100)+'\n'+('#'+' '*23+'#').center(100)+'\n'+('#'*25).center(100))
while "yes"==GetChoice('\n\n\n\n'+' '*37+'Start new game? yes/no:',('yes','no')):
	int_CountTurns=1
	int_TotalScore=0
	int_TurnScore=0

	#**********************CONCEPTUAL FUNCTION - GetDifficulty - Start Here***************
	#Calculates the number of turns, 3 for 'normal' difficulty, 4 for 'easy'
	int_MaxTurns=0
	string_Difficulty=""
	string_Difficulty=GetChoice("\n\nSelect Difficulty. easy/normal:",('easy','normal'))
	if string_Difficulty=="normal":
		int_MaxTurns=3
		print("Selected: normal")
	else: #string_Difficulty=="easy":
		int_MaxTurns=4
		print("Selected: easy")
	#else:
		#int_MaxTurns=0
		#print("Selected: Skip Turn")
	#endif
	#END - GetDifficulty *****************************************************************

	#***********************MAIN GAME LOOP************************************************
	#Loop until all turns played
	print("\n\n\n\n"+"Game start!".center(100))
	while int_CountTurns<=int_MaxTurns:
		print("\n\n\n\n"+"Turn %d of %d. Score %d.".center(100)%(int_CountTurns,int_MaxTurns,int_TotalScore))
		
		#************************* CONCEPTUAL FUNCTION - PlayOneTurn - Starts Here********
		int_TurnScore=0
		int_NextRollDice=6
		bool_EndTurn=False
		while bool_EndTurn==False:
			#int_RollPoints and list_DiceRoll must be reset every roll but int_TurnScore must accumulate
			int_RollPoints=0
			list_DiceRoll=list()
			int_AllFourOneScore=0
		#endwhile
		
			
			#**************CONCEPTUAL FUNCTION - RollNDice - Starts Here****************
			#Produces a list of 6 die, randomly generated
			for count in range(0,int_NextRollDice):
				list_DiceRoll.append(random.randint(1,6))
			#endfor
			list_DiceRoll.sort()
			print("\nDice Roll:",end="")
			for d in list_DiceRoll:
				print(unicodedata.lookup("DIE FACE-"+str(d)),sep='',end='')
			#endfor
			print()
			#END - RollNDice*************************************************************


			
			#***************CONCEPTUAL FUNCTION - Reserve Points - Start here*********
			#calculates the reserve points from one roll and the remaing dice
			int_DieFrequency=0
			string_Response=""
			bool_Straight_Exists=True
			#One match at a time, Display the match then ask to reserve points. Repeat for other matches.
			for int_DieValue in range(1,7): #range(start,stop) start value is included. Stop value is excluded.
				int_DieFrequency=list_DiceRoll.count(int_DieValue)
				if int_DieFrequency>1:
				
				
					#****************CONCEPTUAL FUNCTION - AllFourOne - Starts here***************
					if (int_DieValue==1) and (int_DieFrequency>=4):
						int_AllFourOneScore=20
					else:
						int_AllFourOneScore=int_DieFrequency*int_DieValue
					#Endif
					#END - AllFourOne**************************************************************	

			
					print("\nMatching %d x %s. Can Reserve %d points." %(int_DieFrequency,unicodedata.lookup("DIE FACE-"+str(int_DieValue)),int_AllFourOneScore))
					string_Response=GetChoice("Reserve points? yes/no:",('yes','no'))
					if string_Response=="yes":
						int_RollPoints=int_RollPoints+int_AllFourOneScore
						int_NextRollDice=int_NextRollDice-int_DieFrequency
					#endif
					bool_Straight_Exists=False
				#endif
			#endfor
			if (bool_Straight_Exists==True) and len(list_DiceRoll)==6:
				print("\nYOU ROLLED A STRAIGHT!!! 50 POINTS")
				int_RollPoints=50
				int_NextRollDice=0
			#Endif
			print("\nThis Roll:%d points reserved. %d dice remaing."%(int_RollPoints,int_NextRollDice))
			#END - Reserve Points****************************************************************


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
		#END - PlayOneTurn************************************************************************


		int_TotalScore=int_TotalScore+int_TurnScore
		int_CountTurns=int_CountTurns+1
	#endwhile
	print("\n\n\n\n"+"Game Over!".center(100))
#*************************************************************************************

#********************PRINT SCORE*************************************************
	x=int_TotalScore-(int_TotalScore%10)
	if x>69:
		print("\n"+"Score %d!".center(100)%int_TotalScore+"\n\n"+"SUPER COOL!".center(100))
	elif x in dictionary_GameOverMessage:
		print("\n"+"Score %d!".center(100)%int_TotalScore+"\n\n"+"%s".center(90)%dictionary_GameOverMessage[x])
	else:
		print("\n"+"Score %d!".center(100)%int_TotalScore)
	#endif
#*******************************************************************************
#*******************************************************************************
#Endwhile
print("\n\n\n\n"+"Thank you for playing FARKLE".center(100))
		
