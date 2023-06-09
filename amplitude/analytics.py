import aiohttp

from config_dataclass.config import Config, load_config

config: Config = load_config()
AMPLITUDE_API_KEY = config.amplitude.api_key

async def post_analytic_event(event):
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api2.amplitude.com/2/httpapi',
                                headers={
                                    'Content-Type': 'application/json',
                                    'Accept': '*/*'
                                },
                                json={
                                    "api_key": f"{AMPLITUDE_API_KEY}",
                                    "events": [event]
                                }                              
                                ) as responce:
            if responce.status != 200:
                raise Exception("Non-200 Analytics response: " + str(responce.text))    


