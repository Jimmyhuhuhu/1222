from transformers import AutoProcessor, MusicgenForConditionalGeneration

#模型名稱
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")    #處理器
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small") #模型

#文字敘述
inputs = processor(
    text=["80s pop track with bassy drums and synth", "90s rock song with loud guitars and heavy drums"],
    padding=True,
    return_tensors="pt",
)
print(input)
audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=256)

#save to wav
import scipy

sampling_rate = model.config.audio_encoder.sampling_rate
scipy.io.wavfile.write("musicgen_out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())