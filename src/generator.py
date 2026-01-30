import torch
from diffusers import FluxPipeline
from config import settings
import time

class ImageGenerator:
    def __init__(self):
        print("🔌 Loading Local FLUX Pipeline (This typically takes 30s)...")
        # Load the model in bfloat16 to save VRAM (even with 48GB, it's faster)
        self.pipe = FluxPipeline.from_pretrained(
            settings.IMAGE_MODEL_PATH,
            torch_dtype=torch.bfloat16
        )
        # Move to your GPU
        self.pipe.to(settings.DEVICE)
        
        # Optional: Enable CPU offload if you run other heavy things, 
        # but with A6000 you probably don't need it.
        # self.pipe.enable_model_cpu_offload() 

    def generate_image(self, news_title, style_prompt):
        print(f"🎨 Generating Image locally on {settings.DEVICE.upper()}...")
        
        # CHANGED: PROMPT ENGINEERING FOR TEXT
        # 1. We wrap the title in double quotes which helps Flux understand it's text.
        # 2. We explicitly ask for "typography" and "poster".
        prompt = f'A high-quality poster featuring the text "{news_title}" written in large, bold, clear typography. {style_prompt}. High resolution, 8k, cinematic lighting.'
        
        print(f"   ▶ Prompt: {prompt}") # Print to see what we are sending
        
        seed = int(time.time())
        generator = torch.Generator("cuda").manual_seed(seed)
        
        image = self.pipe(
            prompt,
            output_type="pil",
            num_inference_steps=30, # Increased slightly for better text sharpness
            generator=generator,
            height=720,
            width=1280,
            guidance_scale=3.5,
            max_sequence_length=512 # Flux Dev supports up to 512 tokens (fixes the 77 token warning!)
        ).images[0]
        
        filename = f"local_render_{seed}.jpg"
        image.save(filename)
        print(f"✅ Local Image Saved: {filename}")
        return filename