import re
import json
import sys
import textwrap

def SaveChanges(datalist):
    try:
        f=open("data.txt","w")
        json.dump(datalist,f,indent=4)
    except IOError as e:
        print(e+"\n\nQuestions not saved")
    except ValueError as e:
        print(e+"\n\nQuestions not saved")
    finally:
        f.close()

#-----------------------------------------------------------------------------------
#   The InputSomething functions take a string input and compares that input to
#   several regular expressions which coresepond to the input options available
#   to the user. It will keep prompting until a regular expression matches.
#   It will return the entire matched expression as a string.
#   If no expression is specificed, the default expression is used.
def InputSomething(str_prompt,default=r".+"):
    pRex=re.compile(default)
    match=None
    while match==None:
        text=input(str_prompt)
        text=text.strip()
        text=text.lower()
        match=re.fullmatch(pRex,text)
        if match==None:
            print("Input not recognised. Try again.")
    return match.group()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#   InputInt prompts the user to inter a positive integer between lb and ub.

def InputInt(str_prompt,lb=1,ub=9999999):
    valid=False
    while not valid:
        try:
            num=int(input(str_prompt))
            valid=True
            if num<lb or num>ub:
                print("Error. Expected integer between",lb,"and",ub)
                valid=False
        except:
            print("Error. Not a number.")
            valid=False
    return num
	

#-----------------------------------------------------------------------------------
#               Main Program Start Here
#----------------------------------------------------------------------------------
datalist=[]
f=None
search=''
index=(-1)
optVal=None
option=""
difficultyCount=[0,0,0,0,0]
#-------------Open JSON File
try:
    f=open("data.txt","r")
    datalist=json.load(f)
except IOError as e:
    print(e)
    print("Creating new file...")
    try:
        f=open("data.txt","x")
    except IOError as e:
        print("Could not create file. \n%s"%e)
        sys.exit()
    
except ValueError as e:
    print(e)
    datalist=[]
finally:
    f.close()



print('='*100+'\n'+'QUIZLE ADMINISTRATOR'.center(100)+'\n'+'='*100+'\n')



while option!= 'q':
#--------------------------------- comment--------------------------------------#
#	Instead of checking the list for each of l, s, v and d						#
#	The list will be checked at the start and the options will not be displayed #
#	Only the add option will be available										#
#   input is checked using regular expression. Allows letter or letter+Num      #
#-------------------------------------------------------------------------------#
    continueEditing='y'
    numRecords=len(datalist)
    print("Choose [q]uit [h]elp [a]dd ",end="")
    validOptions=r"[aAhHqQ]"
    if numRecords>0:
        print("[L]ist [s]earch [v]iew [d]ifficulty [x]delete")
        validOptions=r"([vx] [1-9][0-9]*)|(s [a-z0-9\:\?\.\']+)|[adhlqsvx]"

#----------------------------------comment--------------------------------------#		
#    Get user input. check if they have entered a flag command (see help)	#
#    InputSomething already vetted input so we know that the option is in 	#
#    in the first symbol of the input and index is the second symbol sepated	#
#    by one space. therefore it can be split into two.							#
#-------------------------------------------------------------------------------#
    option=InputSomething("=: ",validOptions)
    optVal=option.split(' ')
    if len(optVal)>1:
        option=optVal[0]
        optVal=optVal[1]
        if optVal.isdigit():
            index=int(optVal)-1
    else:
        optVal=None  # if the optVal wasnt supplied set to None to check later and prompt
		
#----Check user index is within bounds else reset and prompt for index
    if index>=numRecords:
        print("Out of bounds")
        index=(-1)
    
    if option=='a':
        state=1
        prompt="Enter Question:"
        validOptions=r"[ a-z0-9\'\?\:\.]+|/d [1-5] /q [ a-z0-9\'\?\:\.]+ (/a [ a-z0-9\'\?\:\.]+)+"
        qDic=None
        while state<5:
            
            print(prompt)
            myinput=InputSomething("=: ",validOptions)
            #print('myinput=',myinput,sep='')
            #print('state=',state,sep='')
#-------------------------------------comment--------------------------------------#
#    only at this prompt we will check if the user has opted for single entry or step by step
#    single entry means the string will look like '/d # /q text /a text {/a text ...}'
#    if this happens state variable will go immediately to 4 the finish state
#    otherwise it will count up and prompt each time
#-----------------------------------------------------------------------------------#
            if myinput[0:2] == '/d' and state==1:
                qDic=dict({'d':'','q':'','a':[]})
                myinput=myinput.split('/')
                qDic['d']=myinput[1].strip()[2:len(myinput[1].strip())]
                qDic['q']=myinput[2].strip()[2:len(myinput[2].strip())]
                for i in range(3,len(myinput)):
                    qDic['a'].append(myinput[i].strip()[2:len(myinput[i].strip())])
                prompt="Continue adding questions?(y/n):"
                validOptions=r'[yn]'
                state=4
            elif state==1:      #question only has been entered
                qDic=dict({'d':'','q':'','a':[]})
                qDic['q']=myinput
                prompt="Enter Answer:"
                validOptions=r'[ a-z0-9\'\?\:\.]+'
                state=2
            elif state==2:      #answer has been entered
                qDic['a'].append(myinput)
                if InputSomething("Add another answer?(y/n):",r'[yn]')=='n':
                    prompt="Enter Difficulty:"
                    validOptions=r'[1-5]'
                    state=3
            elif state==3:      #difficulty has been entered
                qDic['d']=myinput
                prompt="Continue adding questions?(y/n):"
                validOptions=r'[yn]'
                state=4
            else:               #option to continue or not entering questions
                state=5
                datalist.append(qDic)
                if myinput=='y':
                    prompt="Enter Question:"
                    validOptions=r"[ a-z0-9\'\?\:\.]+|/d [1-5] /q [ a-z0-9\'\?\:\.]+ (/a [ a-z0-9\'\?\:\.]+)+"
                    state=1
            #print("state after if=",state,sep='')
            
        SaveChanges(datalist)
    elif numRecords>0:
        if option=='l':
            print("\n\n\nQuestions:")
            for i in range(0,numRecords):
                print("%d) %s"%(i+1,datalist[i]['q']))
            print()
        elif option=='s':
            if optVal==None:
                optVal=InputSomething("Enter searchable word =: ",r'[a-z0-9\:\?\.\']+')
            print('='*43+'SEARCH RESULTS'+'='*43+'\n          |')
            countRecords=0
            for record in datalist:
                if (optVal in record['q']) or (optVal in str(record['a'])):
                    print('          |\n          | Question: %s\n          | Answer: %s\n          | Difficulty: %s'%(textwrap.shorten(record['q'],50),record['a'],record['d']))
                    countRecords=countRecords+1
            print('          |'+str(str(countRecords)+' RECORDS FOUND').center(78)+'          \n','          |\n'+'='*100,sep='')
        elif option=='v':
            if index<0:
                index=InputInt("Enter the question number to view (n<="+str(numRecords)+").\n=:",1,numRecords)-1 #inputInt get a 1 indexed number so need to subtract 1
            print('#\n#  question: '+datalist[index]['q']+'\n#  answer: ',datalist[index]['a'],'\n#  difficulty: '+datalist[index]['d']+'\n#')
        elif option=='x':
            if index<0:
                index=InputInt("Enter the index of question to delete(n<="+str(numRecords)+").\n=:",ub=numRecords)-1 #inputInt get a 1 indexed number so need to subtract 1
            datalist.pop(index)
            SaveChanges(datalist)
            print("Question deleted.")
        elif option=='d':
            for i in range(1,6):
                print("   |-----Difficulty Level {0} Question-----\n   |".format(i))
                for j in range(0,len(datalist)):
                    if datalist[j]['d']==str(i):
                        difficultyCount[i-1]+=1
                        print("   |   {0}) {1}".format(j+1,datalist[j]['q']) )
                print("   |")
            print("   |------------SUMARY------------\n   |\
			\n   |   Difficulty 1: {0} questions.\
			\n   |   Difficulty 2: {1} questions.\
			\n   |   Difficulty 3: {2} questions.\
			\n   |   Difficulty 4: {3} questions.\
			\n   |   Difficulty 5: {4} questions.\n\n".format(difficultyCount[0],
			difficultyCount[1],
			difficultyCount[2],
			difficultyCount[3],
			difficultyCount[4]))				
    if option=='h':
        print('\n'*5+
            '='*41+'USING QUIZLE ADMIN'+'='*41+'\n'+
            '----------COMMAND INTERFACE----------'.center(100)+
            '\n          a         - Add a question. This command has no options.'+
			'\n          d         - List available questions grouped by difficulty. This command has not options.'+
            '\n          L         - List available questions. This command has no options.'+
            '\n          s         - Search in questions and answers.'+
            '\n          s word    - Search for word in questions and answers (short cut).'+
            '\n          v         - View a qestion.'+
            '\n          v #       - View question number #.'+
            '\n          x         - Delete a question.'+
            '\n          x #       - Delete question number #.'+
            '\n          q         - Quit.\n'+
            '----------ADDING QUESTIONS----------'.center(100)+
            '\n          You can add questions in two ways:'+
            '\n          1)Type question and answer at the prompt - or -'+
            '\n          2)Use the following specific format to add questions.'+
            '\n\n          /d # /q text /a text {/a text ...}'+
            '\n\n          #         - Difficulty level from 1 to 5.'+
            '\n          text      - A string of alphanumeric and space (ascii 32) characters.'+
            '\n\n          You must enter the difficulty, one question and at least one answer.'+
            '\n          Additional answers are optional.'+
            '\n          You must use this format exactly otherwise you will get an error.'+
            '\n          Note: The only punction allowed are . \' ? and :'+'\n'*5
              )
    index=(-1)    #reset search and index to detect 
    optVal=None
