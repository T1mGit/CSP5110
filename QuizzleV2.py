import tkinter
from tkinter import messagebox
import sys
import json
import random
#-----Application Class-------------
class Application:
    


    
    def __init__(self):
        #----Attributes----
        self.totalQuestions=0                       #holds the number of questions obtained from the datafile
        self.currentScore=0                         #The current score as a percentage of correct questions from questions asked
        self.questionsAnswered=0                    #the number of questions asked/answered
        self.questionsCorrect=0                     #the number of crrectly answered questions
        self.questionsAlreadyAsked=[-1,-1,-1,-1,-1] #tracks which questions asked so they are not repeated
        self.datalist=[]                            #the data lsit
        self.nextQuestion=-1                        #the next question which will be randomly selected from 0 to totalquestions-1 (datalist is 0 indexed)
        self.popUpState=False
        textfont=('Helvetica','12')
        
       
        #-------Define Main window Window properties--------
        self.mainWin=tkinter.Tk()
        self.mainWin.title("Quizzle")
        self.mainWin.geometry("600x150+300+300")
        self.mainWin.resizable(width=False,height=False)

        #Middle Frame to hold Text Box and button
        self.midFrame=tkinter.Frame(self.mainWin,
                                    cursor="spraycan",
                                    bg="green"
                                    )
        self.midFrame.grid(row=3,
                           column=0,
                           ipadx=270,
                           ipady=8)


        #Configure the encouragment label
        self.lblPwrMsgText=tkinter.StringVar()
        self.lblPwrMsg=tkinter.Label(self.mainWin,
                                      font=("Times New Roman","10"),
                                      textvariable=self.lblPwrMsgText,
                                      cursor="trek",
                                      bg="yellow",
                                      fg="red",
                                     padx=300,
                                     pady=8)
        self.lblPwrMsgText.set("")
        self.lblPwrMsg.grid(row=1,
                            column=0)
        
        #Configure the Question display label
        self.lblQuesText=tkinter.StringVar()                                    #using StringVar as the reference text variable which updates text display on the object
        self.lblQues=tkinter.Label(self.mainWin,
                                   font=textfont,
                                   textvariable=self.lblQuesText,
                                   cursor="gumby",
                                   bg="pink",
                                   padx=270,
                                   pady=8)
        self.lblQuesText.set("NoQuestions")
        self.lblQues.grid(row=2,
                          column=0)

        #configure the Question counter label
        self.lblQCntMsgText=tkinter.StringVar()
        self.lblQCntMsg=tkinter.Label(self.mainWin,
                                      font=("Times New Roman","10","bold"),
                                      textvariable=self.lblQCntMsgText,
                                      cursor="trek",
                                      bg="purple",
                                      fg="yellow",
                                      padx=270,
                                      pady=8)
        self.lblQCntMsgText.set("NoQuestions")
        self.lblQCntMsg.grid(row=4,
                             column=0)

        #configure entry text box
        self.textBoxText=tkinter.StringVar()
        self.textBox=tkinter.Entry(self.midFrame,
                                   font=textfont,
                                   width=40,
                                   cursor="pencil",
                                   textvariable=self.textBoxText
                                   )
        self.textBoxText.set("")
        self.textBox.bind("<Return>",self.EnterKeyPressEvent)
        self.textBox.grid(row=1,
                          column=0,
                          columnspan=1,
						  sticky="E")       #When binding keys, the call to grid() or pack() must come after the call to bind() other wise error
        
        #configure the submit button
        self.butSubmit=tkinter.Button(self.midFrame,
                                      command=self.CheckAnswer,
                                      text="Submit Answer",
                                      cursor="spider",
                                      takefocus=True,
                                      padx=10
                                      )
        self.butSubmit.grid(row=1,
                             column=1,
                             columnspan=1,
                            sticky='W')
        
#configure columns
        self.midFrame.columnconfigure(0,weight=1)
        self.midFrame.columnconfigure(1,weight=1)
        self.midFrame.rowconfigure(1,weight=1)
        self.mainWin.columnconfigure(0,weight=1)
        for i in range(1, 4):
            self.mainWin.rowconfigure(i,weight=1)

        #--------Define popUp window properties------------
        self.popMsgText=tkinter.StringVar()                                     #Contains the text for popup message
        self.popButText=tkinter.StringVar()                                     #String Var for button text
        self.popUp=tkinter.Toplevel(self.mainWin,
                                    cursor="gobbler",
									bg="yellow",
                                    takefocus=True)#Cursor for popup
        self.popUp.protocol("WM_DELETE_WINDOW",self.PopButCallBack)
        self.popUp.geometry('300x150+450+300')
        self.popUp.resizable(width=False,
                             height=False)
        self.popUp.withdraw()                                                   #Window is hiddent to begin with



        #popup window Button properties
        self.popBut=tkinter.Button(self.popUp,
                                   font=('Helvetica','12'),
                                   cursor="pirate",
                                   textvariable=self.popButText,
                                   command=self.PopButCallBack,
                                   pady=10,
                                   padx=60,
                                   fg="Yellow",
                                   bg="blue"
                                   )
        self.popBut.bind('<Return>',self.PopButCallBack)
        self.popBut.grid(row=2,
                          column=0,sticky="N")
        #popup message label properties
        self.popMsgLbl=tkinter.Label(self.popUp,
                                     font=('Helvetica','12'),
                                     textvariable=self.popMsgText,
                                     pady=5,
                                     padx=150,
                                     justify='center',
                                     bg="green",
									 cursor="gumby"
                                     )
        self.popMsgLbl.grid(row=1,column=0,sticky="S")

        #Configure Rows and columns
        self.popUp.rowconfigure(1,weight=1)
        self.popUp.rowconfigure(2,weight=1)
        self.popUp.columnconfigure(0,weight=1)
        

        #-------------Open JSON File
        #---Exit if cannot open file.
        #Change properties of popup message to show error
        #only quit when the button is pressed
        f=None
        try:
            f=open("data.txt","r")
            self.datalist=json.load(f)
            print("Data file successfully opened.")
        except IOError as e:
            self.ShowPopupMessage("Quit!","Error. Could not open data.txt","Error!")
            #messagebox
            print(e)
            sys.exit(1)
            return
        except ValueError as e:
            print(e)
        finally:
            if f is not None:
                f.close()

        #-------Check Datalist has enoough questions--------
        self.totalQuestions=len(self.datalist)
        print("Total Questions:",self.totalQuestions)
        if self.totalQuestions<5:
            self.ShowPopupMessage("Quit","Insufficient number of questions","Error!")
            print("Insufficient number of Questions")
            sys.exit(0)
            return


        #-------Call the Load Questions functions
        self.SetNextRandomQuestion()
        self.LoadQuestion()

        tkinter.mainloop()

        
    #----The popup window is being used for several popups.
    #----The Button text is being changed and is checked
    #----to which state the pop is in therefor where to
    #----quit or continue
    #quit (or continue) when the button is pressed
    def PopButCallBack(self,e=None):
        if self.popButText.get()=='Quit!':
            print("Quitting")
            self.mainWin.destroy()
            sys.exit(1)
            return
        else:
            self.popUp.withdraw()
            self.popUp.grab_release()
        print(self.popButText.get())
        print("Closing popup...")
        self.popUpState=False


    #----Function to change window infomration show popup
    def ShowPopupMessage(self,buttonText,messageText,titleText):
            if titleText=='Correct!':
                messagebox.showinfo(titleText,messageText)
            elif titleText=='WRONG!':
                messagebox.showerror(titleText,messageText)
            else:
                self.popButText.set(buttonText)
                self.popMsgText.set(messageText)
                self.popUp.title(titleText)
                self.popUp.deiconify()
                self.popUp.grab_set()
                self.popUpState=True
            return


    #--------------Event handler for textbox -------------------
    def EnterKeyPressEvent(self,event):
        self.CheckAnswer()
    #-------Break Text onto multiple lines if greater than breaklen chars long    
    def BreakText(self,text,breaklen):
        if len(text)>breaklen:
            breaks=int(len(text)/breaklen)
            for j in range(0, breaks):         #reapeat break if more than 2 lines - multiline
                i=breaklen*(j+1)+j
                while text[i]!=' ':           #find the wight space char before breaklen
                    i-=1
                text=text[:i]+'\n'+text[i:]
        return text
		
    #---randomly set the first question and put in list of questions already asked
    def SetNextRandomQuestion(self):
        while self.nextQuestion in self.questionsAlreadyAsked:
            self.nextQuestion=random.randint(0,self.totalQuestions-1)
        self.questionsAlreadyAsked[self.questionsAnswered]=self.nextQuestion
        return

    def LoadQuestion(self):
        self.textBoxText.set("")
        self.lblPwrMsgText.set("")
        if (self.datalist[self.nextQuestion]['d']=='4') or (self.datalist[self.nextQuestion]['d']=='5'):
            self.lblPwrMsgText.set("This is a hard one - Good Luck")
        print("Loading question:",self.nextQuestion,"Difficulty:",self.datalist[self.nextQuestion]['d'])
        self.lblQuesText.set(self.BreakText("Question {0}:{1}".format(self.questionsAnswered+1,self.datalist[self.nextQuestion]['q']),70))
        if self.questionsAnswered>0:
            self.lblQCntMsgText.set("{0}/{1} Questions answered correctly({2}%).".format(self.questionsCorrect,self.questionsAnswered,self.currentScore))
        else:
            self.lblQCntMsgText.set("No questions answered yet.")
        #self.textBox.focus_set()

    def CheckAnswer(self):
        #-----Dont if theres nothing in the text display a message
        if self.textBoxText.get()=="":
            self.ShowPopupMessage("OK","Please answer the question.","No Answer!")
        else:
            answers=self.datalist[self.nextQuestion]['a']
            self.questionsAnswered+=1
         #if the users answer is in the answers show a message and add to score
            #Else just show the message
            if self.textBoxText.get().lower() in answers:
                self.questionsCorrect+=1
                self.currentScore=int(round(100*self.questionsCorrect/self.questionsAnswered))
                self.ShowPopupMessage("OK","You are correct!","Correct!")

                print("Answered Question:{0}".format(self.nextQuestion))
            else:
                self.ShowPopupMessage("OK","You are WRONG! HA HA HA...","WRONG!")
            #while self.popUpState: pass
        #once the number of questions asked is 5 game over
            if self.questionsAnswered>=5:
                self.lblQCntMsgText.set("{0}/{1} Questions answered correctly({2}%).".format(self.questionsCorrect,self.questionsAnswered,self.currentScore))
                self.ShowPopupMessage("Quit!","GameOver.\nScore:{0}\nThankyou for playing.".format(self.questionsCorrect*2),"Game Over!")    
            else:
                self.currentScore=int(round(100*self.questionsCorrect/self.questionsAnswered,0))
                self.SetNextRandomQuestion()
                self.LoadQuestion()



myApp=Application()

