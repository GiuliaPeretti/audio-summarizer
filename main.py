import gradio as gr
import assemblyai as aai
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import speech_recognition as sr
from pydub import AudioSegment
import os
import multiprocessing as mp

# from transformers import pipeline S

def transcribe_audio(file):
    aai.settings.api_key = open('api_key.txt', 'r').read()
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(file)
    # transcript = transcriber.transcribe("./my-local-audio-file.wav")

    return(transcript.text)

def summarize(text):
    client = Groq(
        api_key='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'
    )
    chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mixtral-8x7b-32768")
    
    prompt = ChatPromptTemplate.from_messages([("human", "Riassumi questo testo: \n"+text)])
    chain = prompt | chat
    print()
    result=""
    # return(chain.json())
    for chunk in chain.stream({"topic": "box"}):
        result=result+chunk.content
        # str_alias=str_alias+(chunk.content)
    # print()
    # str_alias=str_alias.replace('"',' ')
    # str_alias=str_alias.replace('-',' ')
    # str_alias=str_alias.split("\n")
    # new_aliases=[]
    # for i in range (len(str_alias)):
    #     e=str_alias[i].split(" ")
    #     a=""
    #     for x in e[1:]:
    #         a=a+x
    #     new_aliases.append(a)
    # return(new_aliases[len(new_aliases)-10:])
    return(result)

def summ_part(i, parts, length, sound, results):
    if i==parts:
        p = sound[i*length:]
    p = sound[i*length:(i+1)*length]
    print(i*length,(i+1)*length)
# create a new file "first_half.mp3":
    p.export("current_part"+str(1)+".wav", format="wav")

    recognizer_instance = sr.Recognizer() # Crea una istanza del recognizer
    wav = sr.AudioFile("current_part"+str(1)+".wav") # formati riconosciuti: .aiff .flac .wav

    with wav as source:
        recognizer_instance.pause_threshold = 3.0
        audio = recognizer_instance.listen(source)
        print("Ok! sto ora elaborando il messaggio!")
    try:
        text = recognizer_instance.recognize_google(audio, language="it-IT")
        print(text)
        result=+(text)+"\n"
    except Exception as e:
        print(e)
    results[i]=result




def prova(file):
    dim=os.path.getsize(file)
    print(dim)
    parts=(dim//10000000)+1
    sound = AudioSegment.from_file(file)
    length = len(sound) // parts

    p=[]
    manager = mp.Manager()
    results=manager.list()

    for i in range (parts+1):
        p.append(mp.Process(target=summ_part, args=(i,parts,length,sound, results)))
        results.append("")
        p[i].start()

    for i in range(0,3):
        p[i].join()
        

    return(results)


if __name__=='__main__':

    with gr.Blocks() as demo:
        gr.Markdown("# Audio to text")
        with gr.Row():
            file_upload=gr.File(file_types=['audio'], type="filepath")
            text_result=gr.TextArea()
        text_summ=gr.TextArea()
        b_transcribe=gr.Button("Transcribe")
        b_summarize=gr.Button("Summarizer")
        b_transcribe.click(fn=prova, inputs=[file_upload], outputs=[text_result])
        b_summarize.click(fn=summarize, inputs=[text_result], outputs=[text_summ])

    demo.launch(share=False)