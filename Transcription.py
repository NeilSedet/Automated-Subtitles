import speech_recognition as sr
import os
from os import path
from pydub import AudioSegment
from pydub.silence import split_on_silence 
import glob
import audioread
import shutil

def transcribeAudioFile(filePath, fileType):
    # file which needs to be transcribed
    AUDIO_FILES_PATH=path.join(path.dirname(path.realpath(__file__)), filePath)
    # converts all files of that type into a new wav file which will then be transcribed
    AUDIO_FILES = AudioConversion(AUDIO_FILES_PATH, fileType)
    
    # transcribes all wav files within that folder
    for AUDIO_FILE in AUDIO_FILES:
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), AUDIO_FILE)
        splitAudio(AUDIO_FILE, filePath, 45, 15)

# takes a live transcription of the microphone which is used
def transcribeLive():
    r=sr.Recognizer()
    mic=sr.Microphone()

    # checking recognizer to see if it's set properly
    if not isinstance(r, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    # checking microphone to see if it's set properly
    if not isinstance(mic, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # starts recording, then transcribes and prints transcription from microphone (will continue to record until long silence)
    print("Please Talk")
    with mic as source:
        for i in range(15):
            try:
                audio = r.record(source, duration = 2)
                text=r.recognize_google(audio)
                print(text)
            except:
                pass

# converts audio file in folder
def AudioConversion(path, fileType):
    originalFiles = glob.glob(os.path.join(path, '*.' + fileType))
    audioFiles = []
    
    # working with multiple file types to convert them to .wav
    for new_file in originalFiles:
        wav_file = os.path.splitext(new_file)[0] + '.wav'
        sound = AudioSegment.from_file(new_file, format = fileType)
        sound.export(wav_file, format="wav")
        audioFiles.append(wav_file)
    return audioFiles

# splits audio file every 30 seconds into intervals which allows the an entire file to be transcribed
def splitAudio(audioFile, filepath, time, delay):
    
    #originalFiles = glob.glob(os.path.join(path, '*.wav'))
    with audioread.audio_open(audioFile) as f:
        duration = f.duration

    dotSpot = findLast(audioFile, '.', 0)
    split_foldername = audioFile[:dotSpot] + '_split_audiofiles'
    split_foldername = replaceAll (split_foldername, " ", "_")
    folder_name = replaceAll (split_foldername, "\\", "/")
    print("The folder name is: " + folder_name)
    folder_path = folder_name
    print("Folder path is: " + folder_path)

    # create file, if file has already been created pass
    try:
        os.mkdir(split_foldername)
    except(FileExistsError):
        pass
    
    os.chdir(split_foldername)
    for i in range (int(duration/time)):
        split_filename = audioFile[:dotSpot] + '_chunk' + str(i) + '.wav'
        t1 = i * 1000 * (time - delay)
        t2 = (i + 1) * 1000 * time

        split_audio = AudioSegment.from_file(audioFile, format = "wav")
        split_audio = split_audio[t1:t2]
        split_audio.export(split_filename, format="wav")

        newFile = path.join(folder_path, split_filename)
        print(newFile)
        #recordSplits(audioFile, split_filename)

# splits recordings into smaller parts to then transcribe the file
def recordSplits (originalFile, filename):
    r = sr.Recognizer()
    text_file = open(str(originalFile) + "_transcribed.txt","a+")

    # checking recognizer to see if it's set properly
    if not isinstance(r, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    # starts recording, then transcribes and prints transcription
    with sr.AudioFile(filename) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)

    try:
        text = r.recognize_google(audio)
        text_file.write(text + "\n\n")
        print("\n" + text + "\n")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


    text_file.close()

# finds last character of a string
def findLast (name, character, start):
    dot = name.find(character, start, len(name))
    if (dot == -1):
        return dot
    else:
        temp = findLast(name, character, dot+1)
        if (temp == -1):
            return dot
        else:
            return temp

# replaces all of one character with another character which is specified
def replaceAll (name, characterTaken, characterReplace):
    found = name.find(characterTaken, 0, len(name))
    if (found == -1):
        return name
    else:
        name = name[:found] + characterReplace + name[found+1:]
        new_name = replaceAll(name, characterTaken, characterReplace)
        return new_name