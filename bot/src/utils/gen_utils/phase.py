from bot.src.utils import proxies
import openai
import asyncio
from . import make_transcription, make_image
from bot.src.utils.constants import constant_db_api, constant_db_tokens
from bot.src.utils.gen_utils.make_completion import _make_api_call
from bot.src.utils.preprocess.parse_headers import parse_values_to_json
class ChatGPT:
    def __init__(self, chat, lang="es", model="gpt-3.5-turbo"):
        self.chat = chat
        self.model = model
        self.lang = lang
        self.answer = None
        self.proxies = proxies.config.apisproxy
        assert self.model in proxies.config.model["available_model"], f'{proxies.config.lang[self.lang]["errores"]["utils_modelo_desconocido"]}: {self.model}'
        self.api=(proxies.api_cache[self.chat.id][0] if self.chat.id in proxies.api_cache else asyncio.run(proxies.db.get_chat_attribute(self.chat, f'{constant_db_api}')))
        self.diccionario = {}
        self.diccionario.clear()
        self.diccionario.update(proxies.config.completion_options)
        self.diccionario["stream"] = proxies.config.usar_streaming
        from bot.src.utils.gen_utils import middleware
        asyncio.ensure_future(middleware.resetip(self))

    async def send_message(self, _message, dialog_messages=[], chat_mode="assistant"):
        while self.answer is None:
            try:
                async for status, self.answer in self._prepare_request(_message, dialog_messages, chat_mode):
                    yield status, self.answer
            except openai.error.InvalidRequestError as e:  # too many tokens
                if len(dialog_messages) == 0:
                    raise IndexError(f'{proxies.config.lang[self.lang]["errores"]["utils_dialog_messages_0"]} [{self.api}]: {e}') from e
                # forget first message in dialog_messages
                dialog_messages = dialog_messages[1:]
            except Exception as e:
                self._handle_exception(f'send_message: {e}')
        yield "finished", self.answer

    async def _prepare_request(self, _message, dialog_messages, chat_mode):
        from bot.src.utils.preprocess.make_messages import handle as mms
        from bot.src.utils.preprocess.make_prompt import handle as mpm
        try:
            messages, prompt = (await mms(self, _message, dialog_messages, chat_mode), None) if self.model not in proxies.config.model["text_completions"] else (None, await mpm(self, _message, dialog_messages, chat_mode))
            kwargs = {
                "prompt": prompt,
                "messages": messages
            }

            #if proxies.config.api["info"][self.api].get("headers"):
                #kwargs["headers"] = parse_values_to_json(proxies.config.api["info"][self.api]["headers"])
                #print(f'{kwargs}')

            from bot.src.utils.misc import ver_modelo_get_tokens, tokenizer

            max_tokens = await ver_modelo_get_tokens(None, model=self.model)
            tokens_actual = await proxies.db.get_dialog_attribute(self.chat, f'{constant_db_tokens}')

            #pre_tokens = f'{proxies.config.chat_mode["info"][chat_mode]["prompt_start"]}\n\n{_message}'
            #mensaje_tokens = await tokenizer.pre_message(input_data=pre_tokens)
            max_tokens = (max_tokens - tokens_actual - 1000)
            print(max_tokens)
            self.diccionario["max_tokens"] = max_tokens

            async for status, self.answer in _make_api_call(self, **kwargs):
                yield status, self.answer

            self.answer = await self._postprocess_answer()
            
        except Exception as e: raise BufferError(f'_prepare_request: {e}')

    async def _handle_invalid_request_error(self, error, dialog_messages):
        try:
            if len(dialog_messages) == 0:
                raise IndexError(f'{proxies.config.lang[self.lang]["errores"]["utils_dialog_messages_0"]} [{self.api}]: {error}') from error
            dialog_messages = dialog_messages[1:]
        except Exception as e: raise ValueError(f'_handle_invalid_request_error: {e}')

    def _handle_exception(self, error):
        raise ValueError(f'{self.api}: {error}')

    async def _postprocess_answer(self):
        try:
            return "" if self.answer == None else self.answer.strip()
        except Exception as e: raise ValueError(f'_postprocess_answer: {e}')

    async def transcribe(self, audio_file):
        try:
            return await make_transcription.write(self, audio_file)
        except Exception as e: raise RuntimeError(f"phase.transcribe > {e}")
    
    async def imagen(self, prompt, current_api, style, ratio, model, seed=None, negative=None):
        try:
            images, seed = await make_image.gen(self, prompt, current_api, style, ratio, model, seed, negative)
            return images, seed
        except Exception as e:
            raise RuntimeError(f"phase.imagen > {e}")

    async def busqueduck(self, query):
        try:
            from bot.src.apis.duckduckgo import search
            formatted_results_backend, formatted_results_string = await search(self, query)
            return formatted_results_backend, formatted_results_string
        except Exception as e: raise RuntimeError(f"phase.busqueduck > {e}")