from dataclasses import dataclass
from environs import Env

@dataclass
class TgConfig:
    token: str
    
@dataclass
class SdConfig:
    token: str
    url: str

@dataclass
class RedisConfig:
    host: str
    password: str
    port: int
    db: int 

@dataclass
class OpenAIConfig:
    api_key: str
    engine: str
    temperature: float
    max_tokens: int

@dataclass
class MongoDBConfig:
    url: str

@dataclass
class AmplitudeConfig:
    api_key: str    

@dataclass
class Config:
    tg: TgConfig
    sd: SdConfig
    redis: RedisConfig
    openai_service: OpenAIConfig
    mongodb: MongoDBConfig
    amplitude: AmplitudeConfig

def load_config():
    env = Env()
    env.read_env()
    return Config(
        tg=TgConfig(
            token=env.str("TG_TOKEN")
        ),
        sd=SdConfig(
            token=env.str("SD_TOKEN"),
            url=env.str("SD_URL")
        ),
        redis=RedisConfig(
            host=env.str("REDIS_HOST"),
            password=env.str("REDIS_PASS"),
            port=env.int("REDIS_PORT"),
            db=env.int("REDIS_DB")
        ),
        openai_service=OpenAIConfig(
            api_key = env.str("OPENAI_API_KEY"),
            engine = "gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=1000 
        ),
        mongodb=MongoDBConfig(
            url=env.str("MONGODB_URL")
        ),
        amplitude=AmplitudeConfig(
            api_key=env.str("AMPLITUDE_API_KEY")
        )                        
    )