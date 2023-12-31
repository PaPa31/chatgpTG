from bot.src.utils import config
from bot.src.utils.proxies import db, chat_mode_cache, model_cache, lang_cache, api_cache
from bot.src.utils.constants import constant_db_tokens, constant_db_chat_mode, constant_db_model, constant_db_lang, constant_db_api
from bot.src.utils.misc import ver_modelo_get_tokens, tokenizer

async def putos_tokens(chat, _message):
    try:
        if chat.id in chat_mode_cache and chat.id in model_cache and chat.id in api_cache and chat.id in lang_cache:
            chat_mode = chat_mode_cache.get(chat.id)[0]
            current_model = model_cache[chat.id][0]
            current_api = api_cache[chat.id][0]
            language = lang_cache[chat.id][0]
        else:
            db_args = [constant_db_chat_mode, constant_db_model, constant_db_api, constant_db_lang]
            db_call = await db.get_chat_attributes_dict(chat, db_args)
            
            chat_mode = db_call[constant_db_chat_mode]
            current_model = db_call[constant_db_model]
            current_api = db_call[constant_db_api]
            language = db_call[constant_db_lang]

        max_tokens = await ver_modelo_get_tokens(None, model=current_model, api=current_api)

        dialog_messages = await db.get_dialog_messages(chat, dialog_id=None)
        data, dialogos_tokens = await reconteo_tokens(chat, dialog_messages, max_tokens)
        
        language = config.lang[language]["info"]["name"]
        especificacionlang = config.especificacionlang.format(language=language)
        prompter = config.chat_mode["info"][chat_mode]["prompt_start"].format(language=language)
        injectprompt = """{especificarlang}\n\n{elprompt}\n\n{especificarlang}\n\n{_message}"""
        pre_tokens = injectprompt.format(especificarlang=especificacionlang, elprompt=prompter, _message=_message)
        _, mensaje_tokens = await reconteo_tokens(chat, pre_tokens, max_tokens)

        await db.set_dialog_attribute(chat, f'{constant_db_tokens}', dialogos_tokens + mensaje_tokens)
        completion_tokens = int(max_tokens - dialogos_tokens - mensaje_tokens - (dialogos_tokens * 0.15) - 300)
        while completion_tokens < 0:
            if len(data) > 0:
                data.pop(0)
            data, dialogos_tokens = await reconteo_tokens(chat, data, max_tokens)
            completion_tokens = int(max_tokens - dialogos_tokens - mensaje_tokens - (dialogos_tokens * 0.15) - 300)
        return data, completion_tokens, chat_mode
    except Exception as e:
        raise ValueError(f'<count_tokens.putos_tokens> {e}')

async def reconteo_tokens(chat, input_data, max_tokens):
    data, dialogos_tokens, _ = await tokenizer.handle(input_data, max_tokens)
    if isinstance(data, list):
        await db.set_dialog_messages(
            chat,
            data,
            dialog_id=None
        )
    return data, dialogos_tokens
