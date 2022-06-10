from pydantic import BaseModel
import json
import redis
from fastapi import FastAPI, status
from pprint import pprint
import httpx


app = FastAPI()

r = redis.Redis()

class usersgame(BaseModel):
   	
   user_id : str
   game_id : str 
   word : str 

class userstate(BaseModel):
   user_id : str
   game_id : str
	



@app.post("/create")
def creategame(u : userstate):
    u=dict(u)
    uid=u["user_id"]
    gid=u["game_id"]
    
    usersbytes = r.get("track_user")
    userstr = usersbytes.decode("utf-8")
    userdict = json.loads(userstr)
   
	
    val=userdict[uid]['games'].get(gid)
    i=1    
    temp = {1: '', 2: '',3: '',4: '',5: '',6 : '', 'Remaining':6}  
    
    #User is playing game for the first time
    if gid not in userdict[uid]['games']:
            userdict[uid]['games'][gid]=temp
            (r.set("track_user", json.dumps(userdict)))
            
    return "Game created"             
	
@app.post("/recordguess")
def checkgameplayed(ug : usersgame):
	u=dict(ug)

	uid=u["user_id"]
	gid=u["game_id"]
	word=u["word"]
	 
	usersbytes = r.get("track_user")
	userstr = usersbytes.decode("utf-8")
	userdict = json.loads(userstr)
	    
	checkword = {}
	checkword["word"]=word
	checkword_dict = json.dumps(checkword)
	rcheckvalid = httpx.post("http://127.0.0.1:5300/checkvalidword", data=checkword_dict)
	    	
	val=userdict[uid]['games'].get(gid)
	i=1    
	    
	#Recording the word guesses for game ID
	if userdict[uid]['games'][gid]['Remaining']!=0 :
        
        
		if rcheckvalid.json()["status"] == "Valid Word" :
			x=7-userdict[uid]['games'][gid]['Remaining']
			userdict[uid]['games'][gid][str(x)]=word
			userdict[uid]['games'][gid]['Remaining']-=1
			(r.set("track_user", json.dumps(userdict)))
			return userdict[uid]['games'][gid]
		else:
			return {'status' : 'Enter a Valid Word'}
		
        
        
    #User has already played the game
	else:
		return {'status' : 'Game Already Played'}

	 
        
#Upon request, the user should be able to retrieve an object containing the current state of a game, including the words guessed so far and the number of guesses remaining.
@app.post("/stateofgame")
def stategame(ug: userstate):
    u=dict(ug)

    uid=u["user_id"]
    gid=u["game_id"]

    usersbytes = r.get("track_user")
    userstr = usersbytes.decode("utf-8")
    userdict = json.loads(userstr)
    
	
    val=userdict[uid]['games'].get(gid)
    return val

@app.post("/Setremainingtozero")
def settozero(ug: userstate):
    u=dict(ug)

    uid=u["user_id"]
    gid=u["game_id"]
    
    usersbytes = r.get("track_user")
    userstr = usersbytes.decode("utf-8")
    userdict = json.loads(userstr)
    
    userdict[uid]['games'][gid]['Remaining']=0
    (r.set("track_user", json.dumps(userdict)))
    
    return {'status' : 'Set to 0'}
