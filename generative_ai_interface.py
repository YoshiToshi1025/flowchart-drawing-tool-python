import os
import threading
import constants as ct
import re
from threading import Thread
from pathlib import Path

class Generative_AI_interface:

    def __init__(self):
        self.ai_type, self.ai_model = self.get_specified_AI_type_and_model()
        if self.ai_type == "OpenAI":
            if self.defined_openai_api_key():
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
                openai_ai_models = self.get_openai_ai_models()
                print(f"Available OpenAI models: {openai_ai_models}")
                if self.ai_model not in openai_ai_models:
                    print(f"Specified OpenAI model '{self.ai_model}' is not available.")
            # else:
            #    print("OpenAI API key is not defined.")
        elif self.ai_type == "Gemini":
            if self.defined_gemini_api_key():
                from google import genai
                self.gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
                gemini_ai_models = self.get_gemini_ai_models()
                print(f"Available Gemini models: {gemini_ai_models}")
                if self.ai_model not in gemini_ai_models:
                    print(f"Specified Gemini model '{self.ai_model}' is not available.")
            # else:
            #    print("Gemini API key is not defined.")
        elif self.ai_type == "Anthropic":
            if self.defined_anthropic_api_key():
                from anthropic import Anthropic
                self.anthropic_client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
                anthropic_ai_models = self.get_anthropic_ai_models()
                print(f"Available Anthropic models: {anthropic_ai_models}")
                if self.ai_model not in anthropic_ai_models:
                    print(f"Specified Anthropic model '{self.ai_model}' is not available.")
            # else:
            #    print("Anthropic API key is not defined.")
        elif self.ai_type == "MoonshotAI":
            if self.defined_moonshot_api_key():
                from openai import OpenAI
                self.moonshot_client = OpenAI(base_url=ct.MOONSHOT_BASE_URL, api_key=os.environ["MOONSHOT_API_KEY"])
                moonshot_ai_models = self.get_moonshot_ai_models()
                print(f"Available MoonshotAI models: {moonshot_ai_models}")
                if self.ai_model not in moonshot_ai_models:
                    print(f"Specified MoonshotAI model '{self.ai_model}' is not available.")
            # else:
            #    print("MoonshotAI API key is not defined.")
        elif self.ai_type == "SpaceXAI":
            if self.defined_spacexai_api_key():
                from openai import OpenAI
                self.spacexai_client = OpenAI(base_url=ct.XAI_BASE_URL, api_key=os.environ["XAI_API_KEY"])
                spacexai_ai_models = self.get_spacexai_ai_models()
                print(f"Available SpaceXAI models: {spacexai_ai_models}")
                if self.ai_model not in spacexai_ai_models:
                    print(f"Specified SpaceXAI model '{self.ai_model}' is not available.")
            # else:
            #    print("SpaceXAI API key is not defined.")
        elif self.ai_type == "LMStudio":
            if ct.LMSTUDIO_BASE_URL is not None:
                from openai import OpenAI
                self.lmstudio_client = OpenAI(base_url=ct.LMSTUDIO_BASE_URL, api_key="not-needed")
                lmstudio_ai_models = self.get_lmstudio_ai_models()
                print(f"Available LMStudio models: {lmstudio_ai_models}")
                if len(lmstudio_ai_models):
                      print(f"Specified LMStudio AI model is not available.")
            # else:
            #    print("LMStudio base URL is not defined.")
        elif self.ai_type == "Unsloth":
            if self.defined_unsloth_api_key() and ct.UNSLOTH_BASE_URL is not None:
                from openai import OpenAI
                self.unsloth_client = OpenAI(base_url=ct.UNSLOTH_BASE_URL, api_key=os.environ["UNSLOTH_API_KEY"])
                unsloth_ai_models = self.get_unsloth_ai_models()
                print(f"Available Unsloth models: {unsloth_ai_models}")
                if len(unsloth_ai_models) == 0:
                    print(f"Specified Unsloth AI model is not available.")
            # else:
            #    print("Unsloth API key or base URL is not defined.")

    def get_specified_AI_type_and_model(self):
        ai_model = ct.AI_MODEL
        if ai_model is not None and ai_model.startswith("gpt-"):
            ai_type = "OpenAI"
        elif ai_model is not None and ai_model.startswith("gemini-"):
            ai_type = "Gemini"
        elif ai_model is not None and ai_model.startswith("claude-"):
            ai_type = "Anthropic"
        elif ai_model is not None and ai_model.startswith("kimi-"):
            ai_type = "MoonshotAI"
        elif ai_model is not None and ai_model.startswith("grok-"):
            ai_type = "SpaceXAI"
        elif ai_model is not None and ai_model=="lmstudio":
            ai_type = "LMStudio"
        elif ai_model is not None and ai_model=="unsloth":
            ai_type = "Unsloth"
        else:
            if ai_model is None or ai_model == "":
                print(ct.NOT_SPECIFIED_AI_MODEL_MESSAGE)
            else:
                print(ct.UNSUPPORTED_AI_MODEL_MESSAGE)
            ai_type = None
            ai_model = None
        
        return ai_type, ai_model

    def defined_openai_api_key(self):
        if "OPENAI_API_KEY" in os.environ and len(os.environ["OPENAI_API_KEY"].strip()) > 0:
            return True
        else:
            print(ct.OPENAI_API_KEY_NOT_SET_MESSAGE)
            return False

    def defined_gemini_api_key(self):
        if "GEMINI_API_KEY" in os.environ and len(os.environ["GEMINI_API_KEY"].strip()) > 0:
            return True
        else:
            print(ct.GEMINI_API_KEY_NOT_SET_MESSAGE)
            return False

    def defined_anthropic_api_key(self):
        if "ANTHROPIC_API_KEY" in os.environ and len(os.environ["ANTHROPIC_API_KEY"].strip()) > 0:
            return True
        else:
            print(ct.ANTHROPIC_API_KEY_NOT_SET_MESSAGE)
            return False

    def defined_spacexai_api_key(self):
        if "XAI_API_KEY" in os.environ and len(os.environ["XAI_API_KEY"].strip()) > 0:
            return True
        else:
            print(ct.SPACEXAI_API_KEY_NOT_SET_MESSAGE)
            return False

    def defined_moonshot_api_key(self):
        if "MOONSHOT_API_KEY" in os.environ and len(os.environ["MOONSHOT_API_KEY"].strip()) > 0:
            return True
        else:
            print(ct.MOONSHOT_API_KEY_NOT_SET_MESSAGE)
            return False

    def defined_unsloth_api_key(self):
        if "UNSLOTH_API_KEY" in os.environ and len(os.environ["UNSLOTH_API_KEY"].strip()) > 0:
            return True
        else:
            print(ct.UNSLOTH_API_KEY_NOT_SET_MESSAGE)
            return False

    def get_openai_ai_models(self):
        if not self.defined_openai_api_key():
            return []
        try:
            models = self.openai_client.models.list()
            model_names = []
            for model in models.data:
                if model.id.startswith("gpt-") and "image" not in model.id and "codex" not in model.id \
                        and "audio" not in model.id and "realtime" not in model.id and "tts" not in model.id \
                        and "whisper" not in model.id and "transcribe" not in model.id and "search" not in model.id \
                        and "chat" not in model.id and "live" not in model.id:
                    model_names.append(model.id)
            model_names.sort(reverse=True)
            return model_names
        except Exception as e:
            print(f"Error fetching OpenAI models: {e}")
            return []

    def get_gemini_ai_models(self):
        if not self.defined_gemini_api_key():
            return []
        try:
            from google import genai
            models = self.gemini_client.models.list()
            model_names = []
            for model in models:
               model_name = model.name.removeprefix("models/")
               if model_name.startswith("gemini-") and "audio" not in model_name and "translate" not in model_name \
                       and "embedding" not in model_name and "robotics" not in model_name and "omni" not in model_name \
                       and "image" not in model_name and "tts" not in model_name and "live" not in model_name \
                       and "computer-use" not in model_name and "customtools" not in model_name and "transcribe" not in model_name:
                   model_names.append(model_name)
            model_names.sort(reverse=True)
            return model_names
        except Exception as e:
            print(f"Error fetching Gemini models: {e}")
            return []

    def get_anthropic_ai_models(self):
        if not self.defined_anthropic_api_key():
            return []
        try:
            from anthropic import Anthropic
            models = self.anthropic_client.models.list()
            model_names = [model.id for model in models]
            return model_names
        except Exception as e:
            print(f"Error fetching Anthropic models: {e}")
            return []

    def get_spacexai_ai_models(self):
        if not self.defined_spacexai_api_key():
            return []
        try:
            models = self.spacexai_client.models.list()
            model_names = []
            for model in models.data:
                if model.id.startswith("grok-") and "image" not in model.id and "video" not in model.id \
                        and "agent" not in model.id and "reasoning" not in model.id and "build" not in model.id:
                    model_names.append(model.id)
            model_names.sort(reverse=True)
            return model_names
        except Exception as e:
            print(f"Error fetching SpaceXAI models: {e}")
            return []

    def get_moonshot_ai_models(self):
        if not self.defined_moonshot_api_key():
            return []
        try:
            models = self.moonshot_client.models.list()
            model_names = []
            for model in models.data:
                if model.id.startswith("kimi-") and "code" not in model.id:
                    model_names.append(model.id)
            model_names.sort(reverse=True)
            return model_names
        except Exception as e:
            print(f"Error fetching MoonshotAI models: {e}")
            return []

    def get_lmstudio_ai_models(self):
        #if not self.defined_lmstudio_api_key():
        #    return []
        try:
            models = self.lmstudio_client.models.list(timeout=5)
            model_names = []
            for model in models.data:
                if "embedding" not in model.id:
                    model_names.append(model.id)
            model_names.sort(reverse=True)
            return model_names
        except Exception as e:
            print(f"Error fetching LMStudio models: {e}")
            return []

    def get_unsloth_ai_models(self):
        if not self.defined_unsloth_api_key():
            return []
        try:
            models = self.unsloth_client.models.list(timeout=5)
            model_names = []
            for model in models.data:
                model_names.append(model.id)
            model_names.sort(reverse=True)
            return model_names
        except Exception as e:
            print(f"Error fetching Unsloth models: {e}")
            return []

    def send_message_to_ai(self, user_msg: str, spec_msg: str|None = None):
        # print(f"send_message_to_ai called with user_msg: {user_msg}")
        if not user_msg:
            return None, None

        user_input_msg = ct.AI_INPUT_TEMPLATE.replace("$order", user_msg)
        if spec_msg:
            user_input_msg += "\n" + ct.AI_SPEC_TEMPLATE.replace("$spec", spec_msg)
        original_filename = f"{user_msg}_{self.ai_model}"
        sanitized_filename = self.sanitize_filename(original_filename)
        args = (user_input_msg, sanitized_filename, user_msg, spec_msg)
        return_values = [None, None]
        if self.ai_type == "OpenAI":
            # print("Calling OpenAI API...")
            thread = Thread(target=self.call_openai_ai, args=(args, return_values), daemon=True)
        elif self.ai_type == "Gemini":
            # print("Calling Gemini API...")
            thread = Thread(target=self.call_gemini_ai, args=(args, return_values), daemon=True)
        elif self.ai_type == "Anthropic":
            # print("Calling Anthropic API...")
            thread = Thread(target=self.call_anthropic_ai, args=(args, return_values), daemon=True)
        elif self.ai_type == "MoonshotAI":
            # print("Calling MoonshotAI API...")
            thread = Thread(target=self.call_moonshot_ai, args=(args, return_values), daemon=True)
        elif self.ai_type == "SpaceXAI":
            # print("Calling SpaceXAI API...")
            thread = Thread(target=self.call_spacexai_ai, args=(args, return_values), daemon=True)
        elif self.ai_type == "LMStudio":
            # print("Calling LMStudio API...")
            thread = Thread(target=self.call_lmstudio_ai, args=(args, return_values), daemon=True)
        elif self.ai_type == "Unsloth":
            # print("Calling Unsloth API...")
            thread = Thread(target=self.call_unsloth_ai, args=(args, return_values), daemon=True)
        else:
            print(ct.UNSUPPORTED_AI_MODEL_MESSAGE)
            return_text = ct.UNSUPPORTED_AI_MODEL_MESSAGE
            mmd_filepath = None
            return return_text, mmd_filepath
        thread.start()
        thread.join()
        return_text = return_values[0]
        mmd_filepath = return_values[1]
        # print(f"AI response received: {return_text}, mmd_filepath: {mmd_filepath}")

        return return_text, mmd_filepath

    # AIが生成したテキストに、依頼したプロンプトを強制的に埋め込む
    def insert_prompt_into_output(self, ai_output_text: str, title_prompt: str, spec_prompt: str) -> str:
        search_text = "bx: 0, by: 0"

        title_phrase = ct.AI_PROMPT_TITLE
        spec_phrase = ct.AI_PROMPT_SPEC
        spec_prompt = spec_prompt.replace("\n", "\\n")

        if title_prompt is not None and title_prompt != "":
            if spec_prompt is None or spec_prompt == "":
                repalce_text = f"{search_text}, details: \"{title_phrase}{title_prompt}\""
            else:
                repalce_text = f"{search_text}, details: \"{title_phrase}{title_prompt}\\n{spec_phrase}\\n{spec_prompt}\""

            if search_text in ai_output_text:
                ai_output_text = ai_output_text.replace(search_text, repalce_text, 1)

        return ai_output_text

    def call_openai_ai(self, args, return_values):
        user_input_msg, filename, user_msg, spec_msg = args
        try:
            resp = self.openai_client.responses.create(
                model=ct.AI_MODEL,
                instructions=ct.AI_SYSTEM_INSTRUCTIONS,
                input=user_input_msg,
            )
            assistant_text = resp.output_text or ""
            assistant_text = self.insert_prompt_into_output(assistant_text, user_msg, spec_msg)

            success_flag, mmd_filepath = self.save_mmd_to_file(filename, assistant_text)
            return_values[0] = assistant_text
            return_values[1] = mmd_filepath
            # print(f"OpenAI API call successful. assistant_text: {assistant_text}, mmd_filepath: {mmd_filepath}, return_values: {return_values}")
        except Exception as e:
            print(e)
            return_values[0] = "OpenAI API Error"
            return_values[1] = None

    def call_gemini_ai(self, args, return_values):
        user_input_msg, filename, user_msg, spec_msg = args
        from google import genai
        try:
            response = self.gemini_client.models.generate_content(
                model=ct.AI_MODEL,
                config=genai.types.GenerateContentConfig(system_instruction=ct.AI_SYSTEM_INSTRUCTIONS),
                contents=user_input_msg
            )
            assistant_text = response.text or ""
            assistant_text = self.insert_prompt_into_output(assistant_text, user_msg, spec_msg)
            success_flag, mmd_filepath = self.save_mmd_to_file(filename, assistant_text)
            return_values[0] = assistant_text
            return_values[1] = mmd_filepath
        except Exception as e:
            print(e)
            return_values[0] = "Gemini API Error"
            return_values[1] = None

    def call_anthropic_ai(self, args, return_values):
        user_input_msg, filename, user_msg, spec_msg = args
        from anthropic import Anthropic
        try:
            response = self.anthropic_client.messages.create(
                model=ct.AI_MODEL,
                max_tokens=20000,
                temperature=1,
                system=ct.AI_SYSTEM_INSTRUCTIONS,
                messages=[{"role": "user", "content": [{"type": "text", "text": user_input_msg}]}],
                # thinking={"type": "adaptive"},
                # output_config={"effort":"max"}     # "effort": "low", "medium", "high", "xhigh", "max"
            )
            # print(response)
            assistant_text = ""
            for message in response.content:
                if message.type == "text":
                    assistant_text = message.text or ""
                    break
            assistant_text = self.insert_prompt_into_output(assistant_text, user_msg, spec_msg)
            success_flag, mmd_filepath = self.save_mmd_to_file(filename, assistant_text)
            return_values[0] = assistant_text
            return_values[1] = mmd_filepath
        except Exception as e:
            print(e)
            return_values[0] = "Anthropic API Error"
            return_values[1] = None

    def call_spacexai_ai(self, args, return_values):
        user_input_msg, filename, user_msg, spec_msg = args
        try:
            resp = self.spacexai_client.responses.create(
                model=ct.AI_MODEL,
                instructions=ct.AI_SYSTEM_INSTRUCTIONS,
                input=user_input_msg,
            )
            assistant_text = resp.output_text or ""
            assistant_text = self.insert_prompt_into_output(assistant_text, user_msg, spec_msg)

            success_flag, mmd_filepath = self.save_mmd_to_file(filename, assistant_text)
            return_values[0] = assistant_text
            return_values[1] = mmd_filepath
            # print(f"SpaceXAI API call successful. assistant_text: {assistant_text}, mmd_filepath: {mmd_filepath}, return_values: {return_values}")
        except Exception as e:
            print(e)
            return_values[0] = "SpaceXAI API Error"
            return_values[1] = None

    def call_moonshot_ai(self, args, return_values):
        user_input_msg, filename, user_msg, spec_msg = args
        try:
            resp = self.moonshot_client.chat.completions.create(
                model=ct.AI_MODEL,
                messages=[
                    {"role": "system", "content": ct.AI_SYSTEM_INSTRUCTIONS},
                    {"role": "user", "content": user_input_msg}
                ],
            )
            assistant_text = resp.choices[0].message.content or ""
            assistant_text = self.insert_prompt_into_output(assistant_text, user_msg, spec_msg)
            success_flag, mmd_filepath = self.save_mmd_to_file(filename, assistant_text)
            return_values[0] = assistant_text
            return_values[1] = mmd_filepath
            # print(f"Moonshot API call successful. assistant_text: {assistant_text}, mmd_filepath: {mmd_filepath}, return_values: {return_values}")
        except Exception as e:
            print(e)
            return_values[0] = "Moonshot API Error"
            return_values[1] = None

    def call_lmstudio_ai(self, args, return_values):
        user_input_msg, filename, user_msg, spec_msg = args
        try:
            resp = self.lmstudio_client.responses.create(
                model=ct.AI_MODEL,
                instructions=ct.AI_SYSTEM_INSTRUCTIONS,
                input=user_input_msg,
            )
            assistant_text = resp.output_text or ""
            assistant_text = self.insert_prompt_into_output(assistant_text, user_msg, spec_msg)

            success_flag, mmd_filepath = self.save_mmd_to_file(filename, assistant_text)
            return_values[0] = assistant_text
            return_values[1] = mmd_filepath
            # print(f"LMStudioAI API call successful. assistant_text: {assistant_text}, mmd_filepath: {mmd_filepath}, return_values: {return_values}")
        except Exception as e:
            print(e)
            return_values[0] = "LMStudioAI API Error"
            return_values[1] = None

    def call_unsloth_ai(self, args, return_values):
        user_input_msg, filename, user_msg, spec_msg = args
        try:
            resp = self.unsloth_client.responses.create(
                model=ct.AI_MODEL,
                instructions=ct.AI_SYSTEM_INSTRUCTIONS,
                input=user_input_msg,
            )
            assistant_text = resp.output_text or ""
            assistant_text = self.insert_prompt_into_output(assistant_text, user_msg, spec_msg)

            success_flag, mmd_filepath = self.save_mmd_to_file(filename, assistant_text)
            return_values[0] = assistant_text
            return_values[1] = mmd_filepath
            # print(f"Unsloth AI API call successful. assistant_text: {assistant_text}, mmd_filepath: {mmd_filepath}, return_values: {return_values}")
        except Exception as e:
            print(e)
            return_values[0] = "Unsloth AI API Error"
            return_values[1] = None

    # -----------------------------
    # ファイル保存（work/[roder].md に追記）
    # -----------------------------
    def save_mmd_to_file(self, order: str, answer: str):
        # 保存先（実行フォルダ直下の work/test.md）
        success_flag = False
        SAVE_DIR = Path(ct.WORK_DIR_NAME)
        filename = self.sanitize_filename(order)
        OUT_FILE = SAVE_DIR / f"{filename}.md"
 
        # answer = self.strip_triple_quotes(answer) # AI回答の前後の ``` をそのまま残す

        try:
            SAVE_DIR.mkdir(parents=True, exist_ok=True)  # work が無ければ作る
            with OUT_FILE.open("w", encoding="utf-8") as f:
                f.write(f"{answer}\n")
            success_flag = True
        except Exception as e:
            success_flag = False

        return success_flag, OUT_FILE

    def sanitize_filename(self, filename: str) -> str:
        # Windowsで使用禁止の文字
        forbidden = r'[\\/:*?"<>|]'
        return re.sub(forbidden, '_', filename)

    def strip_triple_quotes(self, text: str) -> str:
        return_text = text.strip()
        if return_text.startswith("```"):
            return_text = return_text[3:]
        if return_text.endswith("```"):
            return_text = return_text[:-3]
        return return_text
