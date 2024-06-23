import gradio as gr
import assemblyai as aai
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
# from transformers import pipeline

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
    
    prompt = ChatPromptTemplate.from_messages([("human", "Summarize this text: \n"+text)])
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



with gr.Blocks() as demo:
    gr.Markdown("# Audio to text")
    with gr.Row():
        file_upload=gr.File(file_types=['.mp3'], type="filepath")
        text_result=gr.TextArea()
    text_summ=gr.TextArea()
    b_transcribe=gr.Button("Transcribe")
    b_summarize=gr.Button("Summarizer")
    b_transcribe.click(fn=transcribe_audio, inputs=[file_upload], outputs=[text_result])
    b_summarize.click(fn=summarize, inputs=[text_result], outputs=[text_summ])

demo.launch(share=False)