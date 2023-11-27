from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tkinter import simpledialog
import os
import time


_SYLL_XPATH = ".//html//body//div[@class='main page']//div[@class='middle']//div[@class='canvasArea']//div[@class='round']//div[@class='syllable']"
_INPT_XPATH = ".//html//body//div[@class='main page']//div[@class='bottom']//div[@class='round']//div[@class='selfTurn']//form//input"
_CD_PATH =os.path.dirname(__file__)
_LETTERS = set(list("abcdefghijklmnopqrstuvwy"))


os.chdir(_CD_PATH)
print("CD SET TO :",_CD_PATH,"\n")

print("Starting browser!")
os.system("chromeprofgen.bat")

words=[]
with open('words.txt','r') as f:
   for lines in f:
    word = f.readline()
    words.append(word.rstrip())    
words.pop()


opts = Options()
opts.add_experimental_option('debuggerAddress','localhost:6969')
drv = webdriver.Chrome(options=opts )
roomcode  = str(simpledialog.askstring("Boombot","Enter jklm.fun roomcode"))
URL ="https://jklm.fun/"+roomcode
drv.delete_all_cookies()
drv.get(URL)

hasSwitched = False

def iframeSwitch():
   try:
    gameFrame = drv.find_element(By.TAG_NAME,"iframe")
    if "bomb" in str(gameFrame.get_attribute("src")):
                print("Iframe switched!")
                drv.switch_to.frame(gameFrame)
                global hasSwitched
                hasSwitched =True
                return True
    
   except:
       return hasSwitched
def isMyTurn():
    try:
        return drv.find_element(By.XPATH,_INPT_XPATH).is_displayed()
                
    except:
        return False       
def enterWord(syll):
    global _LETTERS
    best = 0
    toSend = ""
    backup=""
    count = 0
    for word in words:
        if syll.lower() in word:

            count+=1
            if len(_LETTERS.intersection(set(list(word)))) > best:
                best = len(_LETTERS.intersection(set(list(word))))
                toSend = word
            backup = word
        
                            
    try:
        if toSend =="":
            toSend = backup
        print("Possible words: ",count,"words")
        print("Trying",toSend)
        print("Letters eliminated:",best,_LETTERS.intersection(set(list(toSend))))
        drv.find_element(By.XPATH,_INPT_XPATH).send_keys(toSend)    
        drv.find_element(By.XPATH,_INPT_XPATH).send_keys(Keys.ENTER)
        time.sleep(1)
        if isMyTurn():
            print("Rejected",toSend)
            words.remove(toSend)
            print("Words in bank: ",len(words))   
            enterWord(syll)
        else:
            words.remove(toSend)   
            print("Words in bank: ",len(words))   
            print("Accepted",toSend)
            _LETTERS.difference_update(set(list(toSend)))
            if len(_LETTERS) ==0:
                print("All letters completed!")
                print("Letters have been reset!")
                _LETTERS = set(list("abcdefghijklmnopqrstuvwy"))
            else:
                print("Letters remaining for bonus:",len(_LETTERS),_LETTERS)

            print("--------------------","\n")

    except:
        time.sleep(1)
        pass

prev_syll = "none"

while drv.service.is_connectable:
 if URL in drv.current_url and iframeSwitch() and isMyTurn():
    syll = drv.find_element(By.XPATH,_SYLL_XPATH).text
    if prev_syll != syll:
        print("--------------------")
        print("Current syllable:",syll)
        enterWord(syll)
        prev_syll = syll    
drv.quit()  