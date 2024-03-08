from diffusers import AudioLDM2Pipeline
import torch
import gradio as gr
# import intel_extension_for_pytorch as ipex

model_id = "cvssp/audioldm2"

pipe = AudioLDM2Pipeline.from_pretrained(
    model_id,
    #torch_dtype = torch.float16,
).to("cpu")

prompt = "A cheerful ukulele strumming in a beachside jam."

generator = torch.Generator("cpu").manual_seed(0)

def create_music(prompt):
  negative_prompt = "Low quality"
  audio = pipe(
    prompt,
    negative_prompt = negative_prompt,
    audio_length_in_s = 10.24,
    generator = generator,
  ).audios[0]
  return 16000, audio

interface = gr.Interface(
    title = "Music Generation App",
    examples = ["A cheerful ukulele strumming in a beachside jam."],
    fn = create_music,
    inputs = gr.Textbox(),
    outputs = "audio",
).launch(debug=True, share=True)