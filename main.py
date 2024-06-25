import gradio as gr
import assemblyai as aai
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import speech_recognition as sr
from pydub import AudioSegment
import os
import multiprocessing as mp

def english(file):
    aai.settings.api_key = open('api_key.txt', 'r').read()
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file)
    return(transcript.text)

def summarize(text, check):
    if(len(check)!=1):
        return("Please choose one language")
    elif(text==""):
        return("Please transcribe something first")
    else:
        key=open('groq_key.txt', 'r').read()
        client = Groq(
            api_key=key
        )
        chat = ChatGroq(temperature=0, groq_api_key=key, model_name="mixtral-8x7b-32768")
        prompt = ChatPromptTemplate.from_messages([("human", "Riassumi questo testo: \n"+text)])
        chain = prompt | chat
        result=""
        for chunk in chain.stream({"topic": "box"}):
            result=result+chunk.content
        return(result)

def summ_part(i, parts, length, sound, results,recognizer_instance):
    if i==parts:
        p = sound[i*length:]
    p = sound[i*length:(i+1)*length]
    p.export("current_part"+str(1)+".wav", format="wav")

    wav = sr.AudioFile("current_part"+str(1)+".wav") # formati riconosciuti: .aiff .flac .wav

    with wav as source:
        recognizer_instance.pause_threshold = 3.0
        audio = recognizer_instance.listen(source)
    try:
        text = recognizer_instance.recognize_google(audio, language="it-IT")
        result=(text)+"\n"
    except Exception as e:
        print(e)
    results[i]=result

def speech_to_text(file, choice):
    if(len(choice)!=1):
        return("Please choose one language")
    if(choice[0]=="English"):
        return(english(file))
    else:
        sound = AudioSegment.from_file(file)
        recognizer_instance = sr.Recognizer() # Crea una istanza del recognizer
        dim=os.path.getsize(file)
        if (dim>10000000):
            parts=(dim//10000000)
            length = len(sound) // parts

            p=[]
            manager = mp.Manager()
            results=manager.list()

            for i in range (parts+1):
                p.append(mp.Process(target=summ_part, args=(i,parts,length,sound, results,recognizer_instance)))
                results.append("")
                p[i].start()

            tot_result=""
            for i in range (parts+1):
                p[i].join()
                tot_result=tot_result+results[i]
        else:
            sound.export("current_part.wav", format="wav")
            wav = sr.AudioFile("current_part.wav") # formati riconosciuti: .aiff .flac .wav

            with wav as source:
                recognizer_instance.pause_threshold = 3.0
                audio = recognizer_instance.listen(source)
            try:
                text = recognizer_instance.recognize_google(audio, language="it-IT")
                tot_result=(text)+"\n"
            except Exception as e:
                print(e)

        return(tot_result)

if __name__=='__main__':

    with gr.Blocks() as demo:
        # gr.Markdown("# Audio to text")
        # with gr.Row():
        #     with gr.Column():
        #         check=gr.CheckboxGroup(choices=["Italiano", "English"], label="Language: ")
        #         file_upload=gr.File(file_types=['audio'], type="filepath", label="File: ")
        #     text_result=gr.TextArea(label="Speech to text")
        # text_summ=gr.TextArea(label="Summary")
        # with gr.Row():
        #     b_transcribe=gr.Button("Transcribe")
        #     b_summarize=gr.Button("Summarizer")
        # b_transcribe.click(fn=speech_to_text, inputs=[file_upload, check], outputs=[text_result])
        # b_summarize.click(fn=summarize, inputs=[text_result, check], outputs=[text_summ])

        gr.Markdown("# Audio to text")
        with gr.Row():
            with gr.Column():
                check=gr.CheckboxGroup(choices=["Italiano", "English"], label="Language: ")
                file_upload=gr.File(file_types=['audio'], type="filepath", label="File: ")
                text_summ=gr.TextArea(label="Summary")
            text_result=gr.TextArea(label="Speech to text")
        
        with gr.Row():
            b_transcribe=gr.Button("Transcribe")
            b_summarize=gr.Button("Summarizer")
        b_transcribe.click(fn=speech_to_text, inputs=[file_upload, check], outputs=[text_result])
        b_summarize.click(fn=summarize, inputs=[text_result, check], outputs=[text_summ])

    demo.launch(share=True)