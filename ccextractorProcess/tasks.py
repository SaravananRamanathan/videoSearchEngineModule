from time import sleep
from urllib import response
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django import conf
from .models import video
from django.core.files import File
import wave
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
from .word import Word as custom_Word
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
import boto3
from decimal import Decimal
"""  @shared_task(bind=True)
def ProgressBarUploadHandler(self,response):
    ""
"""

@shared_task(bind=True)
def go_to_sleep(self,duration):
    ""
    progress_recorder= ProgressRecorder(self) #testing progress bar
    for i in range(10):
        sleep(duration)
        progress_recorder.set_progress(i+1,10,f"status: {i} done")
    return 'done'

@shared_task(bind=True)
def videoProcessing(self,file,fileName):
    "gettting the uploaded video and converting in into audio."
    progress_recorder= ProgressRecorder(self)
    audioclip = AudioFileClip(file)
    audioclip.write_audiofile("transcribed_speech.wav")
    progress_recorder.set_progress(1,2,f"result: Video->Audio done.")
    #task_audioProcessing=audioProcessing.delay()
    #done_audioProcessing=task_audioProcessing.get() 
    #return "video->audio done."
                

#@shared_task(bind=True)
#def audioProcessing(self):
    #
    #
    #just add your model_path here
    #
    #vosk model_path*
    model_path = "vosk-model-en-us-0.22-lgraph"#"vosk-model-en-us-0.22" 
    audio_filename = "transcribed_speech.wav"
    sound = AudioSegment.from_wav(audio_filename)
    sound = sound.set_channels(1)
    sound.export(audio_filename, format="wav")

    wf=wave.open(audio_filename,"rb")

    """
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)
    """
    #model = Model(lang="en-us")

    # You can also init model by name or with a folder path
    model = Model(model_path)
    # model = Model("models/en")

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    #rec.SetPartialWords(True)

    results=[]

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            #print(rec.Result())
            part_result = json.loads(rec.Result())
            results.append(part_result)
            #progress_recorder.set_progress(1,2,f"result: {part_result}")
        #else:
            #print(rec.PartialResult())
            #partial_result = json.loads(rec.Result())
            #results.append(partial_result)
            #progress_recorder.set_progress(1,2,f"result: {partial_result}")
    #print(rec.FinalResult())
    part_result = json.loads(rec.FinalResult())
    results.append(part_result)
    wf.close()  # close audiofile

    

    #DynamoDb setup
    dynamodb = boto3.resource('dynamodb',
        region_name='ap-south-1', 
        aws_access_key_id='<your-access-key-id>', 
        aws_secret_access_key='<your-access-key-secret>')
    table = dynamodb.Table("wordsList")


    #testing put_item on DynamoDb
    """#testing was ok.
    result = table.put_item(
        Item={
            "fileName":fileName,
            "startTime":Decimal("0.33"),
            "endTime":Decimal("0.99"),
            "word":"hello",
            "confidence":"100%"
        }
    )
    print(result["ResponseMetadata"]["HTTPStatusCode"]) #200 as result =OK. 
    """

    sno=1;#this is the dynamodb sort key ---- making primary key as non unique and making sort_key as unique.
    #weir choice , but this is what is best for the currect project. #trust me on this xd

    # convert list of JSON dictionaries to list of 'Word' objects
    list_of_Words = []
    for sentence in results:
        if len(sentence) == 1:
            # sometimes there are bugs in recognition 
            # and it returns an empty dictionary
            # {'text': ''}
            continue
        for obj in sentence['result']:
            w = custom_Word(obj)  # create custom Word object
            #tested before saing to aws dynamoDB.
            """
            print("****************************")
            print(w.conf)
            print(w.end)
            print(w.start)
            print(w.word)
            print("****************************")
            """

            #testing decimal values
            """#test ok.
            print("*********************")
            print(round(Decimal(w.start),2))
            print(w.start)
            print("*********************")
            """

            #round(Decimal(w.start),2)   #testing : Decimal(str(w.start)) #testing: json.loads(json.dumps(w.start), parse_float=Decimal) 
            #round(Decimal(w.end),2)
            #todo : need make this ^ work as a decimal , for now using a string in pace.
            #adding into dynamoDB

            #testing type: test ok.
            """print("***********")
            print(type((Decimal(w.end),2)))
            print(type(w.end))
            print("***********")"""


            result = table.put_item(
            Item={
            "fileName":fileName,
            "sNo":sno,
            "word":w.word,
            "startTime": str(w.start), 
            "endTime": str(w.end),
            "confidence": str(w.conf)
            }
            )
            #print(result["ResponseMetadata"]["HTTPStatusCode"]) #test ok 200==ok.
            sno+=1
            list_of_Words.append(w)  # and add it to list
            
    wordsList=f""
    for word in list_of_Words:
        #print(word.to_string())
        wordsList+="<p>"
        wordsList+='<span style="color:green">'
        all_words = word.to_string().split()
        first_word= all_words[0]
        wordsList+= first_word#word.to_string()
        wordsList+='</span>'
        wordsList+=': '
        wordsList+=' '.join(word.to_string().split()[1:])
        wordsList+="</p>"
        #wordsList+="\n"
    print(results)
    print("testing wordslist: ")
    print(wordsList)
    return wordsList