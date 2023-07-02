from bot.src.utils import config
import asyncio
import aiohttp
from .openai_completion import _openai

async def _make_api_call(self, **kwargs):
    self.answer = ""
    api_functions = {
        "chatbase": _chatbase,
        "g4f": _g4f,
        "you": _you,
        "evagpt4": _evagpt4
    }
    api_function = api_functions.get(self.api, _openai)
    for attempt in range(1, (config.max_retries) + 1):
        try:
            # Crea un iterador asincrónico
            api_iterator = api_function(self, **kwargs).__aiter__()

            # Espera el primer paquete con un tiempo de espera
            first_packet = await asyncio.wait_for(api_iterator.__anext__(), timeout=config.request_timeout)

            # Si el primer paquete se recibe con éxito, continúa con el resto de la respuesta
            yield first_packet
            async for status, self.answer in api_iterator:
                yield status, self.answer
            break # Si la llamada a la API fue exitosa, salimos del bucle
        except (aiohttp.client_exceptions.ClientConnectionError, asyncio.exceptions.TimeoutError, asyncio.TimeoutError): None
        except Exception as e:
            if attempt < config.max_retries: await asyncio.sleep(1.75)
            else: # Si hemos alcanzado el máximo número de reintentos, lanzamos la excepción
                error = f'{config.lang[self.lang]["errores"]["reintentos_alcanzados"].format(reintentos=config.max_retries)}'
                yield "error", f'{error}'
                raise ConnectionError(f"_make_api_call. {error}: {e}")

async def _you(self, **kwargs):
    try:
        from bot.src.apis.gpt4free.foraneo import you
        r = you.Completion.create(
            prompt=kwargs['messages'],
            detailed=False,
            include_links=False
        )
        for chunk in r.text.encode('utf-16', 'surrogatepass').decode('utf-16'):
            self.answer += chunk
            if "Unable to fetch the response, Please try again." in self.answer:
                raise RuntimeError(self.answer)
            yield "not_finished", self.answer
    except Exception as e:
        e = f'_get_you_answer: {e}'
        raise ConnectionError(e)
        
async def _chatbase(self, **kwargs):
    try:
        from bot.src.apis.opengpt import chatbase
        r = chatbase.GetAnswer(self, messages=kwargs['messages'], model=self.model)
        for chunk in r:
            self.answer += chunk
            if "API rate limit exceeded" in self.answer:
                raise RuntimeError(config.lang[self.lang]["errores"]["utils_chatbase_limit"])
            yield "not_finished", self.answer
    except Exception as e:
        e = f'_get_chatbase_answer: {e}'
        raise ConnectionError(e)
async def _evagpt4(self, **kwargs):
    try:
        from bot.src.apis.opengpt import evagpt4
        r = evagpt4.Model(model=self.model, proxy=self.proxies).ChatCompletion(messages=kwargs['messages'])
        for chunk in r:
            self.answer += chunk
            yield "not_finished", self.answer
    except Exception as e:
        e = f'_get_evagpt4_answer: {e}'
        raise ConnectionError(e)
    
async def _g4f(self, **kwargs):
    try:
        from bot.src.apis.gpt4free import g4f
        provider_name = config.model['info'][self.model]['name']
        provider = getattr(g4f.Providers, provider_name)
        r = g4f.ChatCompletion.create(provider=provider, model='gpt-3.5-turbo', messages=kwargs['messages'])
        for chunk in r:
            self.answer += chunk
            yield "not_finished", self.answer
    except Exception as e:
        e = f'_get_g4f_answer: {e}'
        raise ConnectionError(e)