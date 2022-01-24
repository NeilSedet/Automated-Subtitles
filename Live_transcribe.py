# X 1. Transcribe from microphone
# 2. Transcribe from audio files
# X  a. Transcribe audio files
#   b. Transcribe long audio files
#       -Split longer files into shorter files and combine the text to allow for an entire transcription
#       -Plug text into punctuator to get punctuation in sentences
#       -Use that punctuation to get 
# 3. Show transcription in real time rather than waiting for silence
# X 4. Convert any file into a .wav file
# X   a. Need to identify what type of file it is
# X   b. Convert file 
# 5. Store and handle files as necessary (display title, length of audio file, shows transcription when clicked)
#   a. Variables needed:
#       -Title (String)
#       -Length in seconds (int)
#       -Transcription (string array)
#       -Time stamps (int array)
#   b. Transcription
#       -Hold a string in each segment of the array for the sentence within it
#           -Needs to be able to identify sentence then place it into correct position in array
#   c. Time Stamps
#       -Holds the time stamp of the start of each sentence, so when user clicks sentence automatically goes to stored time stamp
# 6. Allow for the upload of voice recordings and transcriptions in to google drive and drop box

from pydub import AudioSegment
import Transcription

def menu():
    choice = 0
    while (choice != -1):
        print("\nWelcome to the Task Program: please select a task or type '-1' to quit:")
        print("1. Live transcription with mic")
        print("2. Transcribe audio file")
        choice = input()
        choice = int(choice)
        if (choice == 1):
            Transcription.transcribeLive()
        elif (choice == 2):
            Transcription.transcribeAudioFile('./Audiofiles', 'm4a')
    print("Thank you for using my program")

menu()