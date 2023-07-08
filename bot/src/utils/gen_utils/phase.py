from bot.src.utils import proxies
from asyncio import create_task
from . import make_transcription, make_image
from bot.src.utils.constants import constant_db_api
from bot.src.utils.gen_utils.make_completion import _make_api_call

class ChatGPT:
    def __init__(self, chat, lang="es", model="gpt-3.5-turbo"):
        self.chat = chat
        self.model = model
        self.lang = lang
        self.answer = None
        self.proxies = proxies.config.apisproxy
        assert self.model in proxies.config.model["available_model"], f'{proxies.config.lang[self.lang]["errores"]["utils_modelo_desconocido"]}: {self.model}'
        self.diccionario = {}
        self.diccionario.clear()
        self.diccionario.update(proxies.config.completion_options)
        self.diccionario["stream"] = proxies.config.usar_streaming
        from bot.src.utils.gen_utils import middleware
        create_task(middleware.resetip(self))

    @classmethod
    async def create(cls, chat, lang="es", model="gpt-3.5-turbo"):
        self = ChatGPT(chat, lang, model)
        self.api = proxies.api_cache[self.chat.id][0] if self.chat.id in proxies.api_cache else await proxies.db.get_chat_attribute(self.chat, f'{constant_db_api}')
        return self

    async def send_message(self, _message, chat_mode="assistant"):
        while self.answer is None:
            try:
                async for status, self.answer in self._prepare_request(_message, chat_mode):
                    yield status, self.answer
            except Exception as e:
                self._handle_exception(f'send_message: {e}')
        yield "finished", self.answer

    async def _prepare_request(self, _message, chat_mode):
        from bot.src.utils.preprocess.make_messages import handle as mms
        from bot.src.utils.preprocess.make_prompt import handle as mpm
        try:
            from bot.src.utils.preprocess import count_tokens
            data, completion_tokens, _ = await count_tokens.putos_tokens(self.chat, _message)
            self.diccionario["max_tokens"] = completion_tokens
            messages, prompt = (await mms(self, _message, data, chat_mode), None) if self.model not in proxies.config.model["text_completions"] else (None, await mpm(self, _message, data, chat_mode))
            kwargs = {
                "prompt": prompt,
                "messages": messages,
                "_message": _message
            }

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
            raise RuntimeError(f"phase.imagen > {current_api}: {e}")

    async def busqueduck(self, query):
        try:
            from bot.src.apis.duckduckgo import search
            formatted_results_backend, formatted_results_string = await search(self, query)
            return formatted_results_backend, formatted_results_string
        except Exception as e: raise RuntimeError(f"phase.busqueduck > {e}")