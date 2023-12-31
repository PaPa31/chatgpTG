from bot.src.utils import config
from bot.src.utils.constants import continue_key

def get_resources_texts(dialog_messages, key):
    texts = []
    for dialog_message in dialog_messages:
        if len(dialog_message.get(key, "")) >= 5:
            texts = dialog_message.get(key, "").strip()
    if texts:
        return "\n".join(texts)
    return ""
def append_resources_texts(self, documento_texts, url_texts, search_texts, prompt):
    resources = ""
    if documento_texts:
        resources += f'{config.lang[self.lang]["metagen"]["documentos"]}: {documento_texts}\n\n'
    if url_texts:
        resources += f'{config.lang[self.lang]["metagen"]["urls"]}: {url_texts}\n\n'
    if search_texts:
        resources += f'{config.lang[self.lang]["metagen"]["busquedaweb"]}: {search_texts}\n\n'
    if len(resources) > 4:
        prompt += resources
        prompt += f'^{config.lang[self.lang]["metagen"]["mensaje"]}: {prompt}][{config.lang[self.lang]["metagen"]["contexto"]}^\n\n'
    return prompt

def get_prompt_lines(dialog_messages, chat_mode, lang):
    prompt_lines = []
    for dialog_message in dialog_messages:
        user_text = dialog_message.get("user", "").strip()
        if user_text:
            if chat_mode != "nada":
                prompt_lines.append(f'{config.lang[lang]["metagen"]["usuario"]}: {user_text}\n\n')
            else:
                prompt_lines.append(f' {user_text}')
        bot_text = dialog_message.get("bot", "").strip()
        if bot_text:
            if chat_mode != "nada":
                prompt_lines.append(f'{config.chat_mode["info"][chat_mode]["name"][lang]}: {bot_text}\n\n')
            else:
                prompt_lines.append(f' {bot_text}')
    return "".join(prompt_lines)

def get_injectprompt(language, prompter):
    especificacionlang = config.especificacionlang.format(language=language)
    injectprompt = """{especificarlang}\n\n{elprompt}\n\n{especificarlang}\n\n"""
    return injectprompt.format(especificarlang=especificacionlang, elprompt=prompter)
    
def append_chat_mode(self, chat_mode):
    language = config.lang[self.lang]["info"]["name"]
    if chat_mode in ["imagen", "translate"]:
        return f'{config.chat_mode["info"][chat_mode]["prompt_start"].format(language=language)}'
    elif chat_mode != "nada":
        prompter = config.chat_mode["info"][chat_mode]["prompt_start"].format(language=language)
        if chat_mode != "translate":
            return get_injectprompt(language, prompter)
        else:
            return prompter
    return ""

def continue_or_append_latest_message(self, _message, prompt, chat_mode):
    if _message == continue_key:
        _message = ""
        #if prompt.endswith(".") or prompt.endswith("?"):
        #prompt = prompt[:-1]
        prompt = f'{prompt} '
    else:
        if chat_mode != "nada":
            prompt += f'\n\n{config.lang[self.lang]["metagen"]["usuario"]}: {_message}'
            prompt += f'\n\n{config.chat_mode["info"][chat_mode]["name"][self.lang]}:'
        else:
            prompt += f' {_message}'
    return prompt

async def handle(self, _message="", dialog_messages=[], chat_mode="nada"):
    try:
        prompt = ""
        documento_texts = ""
        url_texts = ""
        search_texts = ""
        documento_texts = get_resources_texts(dialog_messages, "documento")
        url_texts = get_resources_texts(dialog_messages, "url")
        search_texts = get_resources_texts(dialog_messages, "search")
        prompt = append_resources_texts(self, documento_texts, url_texts, search_texts, prompt)
        prompt += append_chat_mode(self, chat_mode)
        if chat_mode != "nada":
            prompt += f'{config.lang[self.lang]["metagen"]["log"]}:\n\n'
        prompt += get_prompt_lines(dialog_messages, chat_mode, lang=self.lang)
        prompt = continue_or_append_latest_message(self, _message, prompt, chat_mode)
        return prompt
    except Exception as e:
        e = f'_generate_prompt: {e}'
        raise ValueError(e)