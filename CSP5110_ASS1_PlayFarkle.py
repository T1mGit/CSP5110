import CSP5110_ASS1_Functions
int_LimitTurns=0
dictionary_GameOverMessage={40:'Good Score!',50:'Great Score!',60:'Excellent Score!'}
print(('#'*25).center(100)+'\n'+('#'+' '*23+'#').center(100)+'\n'+'#   Welcome to FARKLE   #'.center(100)+'\n'+('#'+' '*23+'#').center(100)+'\n'+('#'*25).center(100))
while "yes"==CSP5110_ASS1_Functions.GetChoice('\n\n\n\n'+' '*37+'Start new game? yes/no:',('yes','no')):
	int_CountTurns=1
	int_TotalScore=0
	int_TurnScore=0
	int_LimitTurns=CSP5110_ASS1_Functions.GetDifficulty()
	print("\n\n\n\n"+"Game start!".center(100))
	while int_CountTurns<=int_LimitTurns:
		print("\n\n\n\n"+"Turn %d of %d. Score %d.".center(100)%(int_CountTurns,int_LimitTurns,int_TotalScore))
		int_TotalScore=int_TotalScore+CSP5110_ASS1_Functions.PlayOneTurn()
		int_CountTurns=int_CountTurns+1
	#endwhile
	print("\n\n\n\n"+"Game Over!".center(100))
	x=int_TotalScore-(int_TotalScore%10)
	if x>69:
		print("\n"+"Score %d!".center(100)%int_TotalScore+"\n\n"+"SUPER COOL!".center(100))
	elif x in dictionary_GameOverMessage:
		print("\n"+"Score %d!".center(100)%int_TotalScore+"\n\n"+"%s".center(100)%dictionary_GameOverMessage[x])
	else:
		print("\n"+"Score %d!".center(100)%int_TotalScore)
	#endif
#endwhile
print("\n\n\n\n"+"Thank you for playing FARKLE".center(100))
		