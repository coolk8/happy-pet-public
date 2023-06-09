import base64
import os
#import asyncio
import aiohttp
import datetime
import backoff

from config_dataclass.config import Config, load_config

config: Config = load_config()
SD_URL = config.sd.url
SD_TOKEN = config.sd.token


#engine_id = "stable-diffusion-xl-beta-v2-2-2"#"stable-diffusion-512-v2-1" #""#
#api_host = 'https://api.stability.ai/v1/generation/stable-diffusion-xl-beta-v2-2-2/text-to-image'

#from main import SD_URL, SD_TOKEN


#add @backoff.on_exception
@backoff.on_exception(backoff.expo, Exception, max_tries=10)
async def generate_pet_images(user_id, pet_type, samples):
    async with aiohttp.ClientSession() as session:
        async with session.post(SD_URL,
                                headers={
                                    "Content-Type": "application/json",
                                    "Accept": "application/json",
                                    "Authorization": f"Bearer {SD_TOKEN}"
                                    },
                                json={
                                    "text_prompts": [
                                        {
                                            "text": f"3d fluffy {pet_type} looking into camera, cute and adorable, cute big circular reflective eyes, long fuzzy fur, Pixar render, unreal engine cinematic smooth, intricate detail, cinematic"
                                        }
                                    ],
                                    "cfg_scale": 7,
                                    "clip_guidance_preset": "FAST_BLUE",
                                    "height": 512,
                                    "width": 512,
                                    "samples": samples,
                                    "steps": 15,
                                }                               
                                ) as responce:
            if responce.status != 200:
                raise Exception("Non-200 SD response: " + str(responce.text))
            else:
#                   print(responce.status)
                data = await responce.json()
                pet_images_filenames = []
                for i, image in enumerate(data["artifacts"]):

                    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                    filename = f"{user_id}_v1_txt2img_{i}_{current_time}.png"
                    pet_images_filenames.append(filename)
                    os.makedirs("out", exist_ok=True)
                    with open(os.path.join("out", filename), "wb") as f:
                        f.write(base64.b64decode(image["base64"])) 

                return pet_images_filenames
                                                
