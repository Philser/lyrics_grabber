

import sys
import lyricsGrabber

class App:

    def __init__(self):
        self.parameterMap = {"-a": "artist", "-l": "location"}


    ################################
    # process given user input
    ################################
    def processUserInput(self, userInput):
        arguments = {}
        currentFlag = ""

        #
        #skip 0 since we don't need the called file's name
        #
        userInput.pop(0)

        parameterMap = self.parameterMap

        #
        # insert all args into a dict
        #
        for arg in userInput:



            if arg[0] == "-":
                currentFlag = arg

                #
                # raise exception if given parameter is unknown
                #
                mappedParameter = parameterMap.get(currentFlag, "")
                if mappedParameter == "":
                    raise AttributeError("Parameter " + arg + " not recognized")

                arguments[mappedParameter] = ""
            else:
                if(currentFlag == ""):
                    raise AttributeError('Usage instructions: Bla Bla')
                else:
                    arguments[mappedParameter] += " " + arg

        #
        # validate dict by checking if all parameters have values
        #
        for parameter in arguments:
            if(arguments.get(parameter, "") == ""):
                raise AttributeError("Missing value for parameter " + parameter)
            else:
                arguments[parameter] = arguments[parameter].strip()

        #
        # make sure the file location has a trailing slash at the end
        # TODO: Linux and Windows differences !
        #
        locationLength = len(arguments["location"])
        if(arguments["location"][locationLength-1] != "\\"):
            arguments["location"] += "\\"

        return arguments

    ################################
    # main procedure
    ################################
    def grab(self, userInput):
        try:
            arguments = self.processUserInput(userInput)
            grabber = lyricsGrabber.LyricsGrabber(arguments)
            grabber.getSongList()
        except AttributeError as e:
            print(e)


app = App()
app.grab(sys.argv)