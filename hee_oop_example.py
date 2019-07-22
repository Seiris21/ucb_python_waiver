#Python OOP 
import re

#Function to add names to a list after normalization given any number of arguments
def addName(*args):
    namelist=list()
    for name in args:
        #Split into First/Middle(if applicable)/Last
        fullname = name.split(' ')
        #Lowercase
        fullname=[x.lower() for x in fullname]
        #Capitalize
        fullname=[x.capitalize() for x in fullname]
        #Recombine and append to lead list
        namelist.append(' '.join(fullname))
    return namelist #for extend()

#Function to remove every instance of name from list after normalization
def removeName(namelist, *args):
    for name in args:
        #Split into First/Middle(if applicable)/Last
        fullname = name.split(' ')
        #Lowercase
        fullname=[x.lower() for x in fullname]
        #Capitalize
        fullname=[x.capitalize() for x in fullname]
        #remove matching names
        namelist=[y for y in namelist if y!=' '.join(fullname)]
    return namelist 

class Entertainment:
    def __init__(self,name,media,lang,director_name):
        self.name=name
        self.platform=media
        self.genre=list()
        self.language=lang
        self.director=director_name
    def setRating(self, value):
        #Check that rating is within scale
        if value>10:
            print("Score cannot exceed 10/10 rating scale")
            return
        self.rating=value
    def addGenre(self, *args):
        #Add each genre in argument to genre list
        for genre in args:
            #Add after normalizing to lower case
            self.genre.append(str(genre).lower())
    def removeGenre(self, *args):
        #Remove every occurance of each specified genre from list
        for genre in args:
            #remove after normalizing to lower case
            self.genre=[y for y in self.genre if y!=str(genre).lower()]
    def setRuntime(self, XhrYmin):
        #convert from combined format to minutes
        runtime=re.split('\.|hr|min',XhrYmin)
        if len(runtime) != 3:
            print("Incorrect format. Please use #hr#min")
            return
        try:
            self.runtime=(int(runtime[0])*60) + (int(runtime[1]))
        except ValueError:
            print("Incorrect format. Please use #hr#min")

class LiveAction:
    def __init__(self):
        self.leadactor=list()
        self.supportcast=list()
    def addLeadActor(self, *args):
        self.leadactor.extend(addName(*args))
    def addSupportCast(self, *args):
        self.supportcast.extend(addName(*args))
    def removeLA(self, *args):
        #Remove every occurance of each specified genre from list
        self.leadactor=removeName(self.leadactor,*args)
    def removeSC(self, *args):
        #Remove every occurance of each specified genre from list
        self.supportcast=removeName(self.supportcast,*args)

class ComputerGenerated:
    def __init__(self,studio_name):
        self.voiceactor=list()
        self.animator=list()
    def addVoiceActor(self, *args):
        self.voiceactor.extend(addName(*args))
    def removeVA(self, *args):
        for actor in args:
            fullname = actor.split(' ')
            #change to match what is in list
            fullname=[x.capitalize() for x in fullname]
            #remove after normalizing to lower case
            self.voiceactor=[y for y in self.voiceactor if y!=fullname]

class Film(Entertainment,LiveAction):
    def __init__(self,name,media,lang,director_name):
        #super() to merge these __init__
        #Entertainment.__init__(kwargs)
        #LiveAction.__init__(kwargs)
        super().__init__(name,media,lang,director_name)
        self.boxoffice="N/A"
    def updateBoxOffice(self,money):
        try:
            #Convert to millions
            millions=round(int(money)/float(1000000),2)
            self.boxoffice= f"{millions} million dollars"
        except ValueError:
            print("Please enter box_office as a whole number value")

class VideoGame(Entertainment,ComputerGenerated):
    def __init__(self,name,media,lang,director_name,studio_name):
        #super to merge these __init__
        #Entertainment.__init__(kwargs)
        #Animation.__init__(args)
        super().__init__(name,media,lang,director_name)
        self.developer=list()
        self.publisher=list()
        self.studio=studio_name
    def addDeveloper(self, *args):
        self.developer.extend(addName(*args))
    def addPublisher(self, *args):
        self.publisher.extend(addName(*args))
    def removeDeveloper(self, *args):
        self.developer=removeName(self.developer,*args)
    def removePublisher(self, *args):
        self.publisher=removeName(self.publisher,*args)


