import gradio as gr
import assemblyai as aai

def transcribe_audio(file):
    aai.settings.api_key = open('api_key.txt', 'r').read()
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(file)
    # transcript = transcriber.transcribe("./my-local-audio-file.wav")

    return(transcript.text)



with gr.Blocks() as demo:
    gr.Markdown("# Audio to text")
    with gr.Row():
        file_upload=gr.File(file_types=['.mp3'], type="filepath")
        text=gr.TextArea()
    b_transcribe=gr.Button("Transcribe")
    b_transcribe.click(fn=transcribe_audio, inputs=[file_upload], outputs=[text])

demo.launch(share=False)