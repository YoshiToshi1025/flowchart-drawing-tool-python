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
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        elif self.ai_type == "Gemini":
            from google import genai
            self.gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        elif self.ai_type == "Anthropic":
            from anthropic import Anthropic
            self.anthropic_client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def get_specified_AI_type_and_model(self):
        ai_model = ct.AI_MODEL
        if ai_model is not None and ai_model.startswith("gpt-") and self.defined_openai_api_key():
            ai_type = "OpenAI"
        elif ai_model is not None and ai_model.startswith("gemini-") and self.defined_gemini_api_key():
            ai_type = "Gemini"
        elif ai_model is not None and ai_model.startswith("claude-") and self.defined_anthropic_api_key():
            ai_type = "Anthropic"
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

    def send_message_to_ai(self, user_msg: str, spec_msg: str|None = None):
        # print(f"send_message_to_ai called with user_msg: {user_msg}")
        if not user_msg:
            return None, None

        user_input_msg = ct.AI_INPUT_TEMPLATE.replace("$order", user_msg)
        if spec_msg:
            user_input_msg += ct.AI_SPEC_TEMPLATE.replace("$spec", spec_msg)
        original_filename = f"{user_msg}_{self.ai_model}"
        sanitized_filename = self.sanitize_filename(original_filename)
        args = (user_input_msg, sanitized_filename)
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

    def call_openai_ai(self, args, return_values):
        user_input_msg, filename = args
        try:
            resp = self.openai_client.responses.create(
                model=ct.AI_MODEL,
                instructions=ct.AI_SYSTEM_INSTRUCTIONS,
                input=user_input_msg,
            )
            assistant_text = resp.output_text or ""
            success_flag, mmd_filepath = self.save_mmd_to_file(filename, assistant_text)
            return_values[0] = assistant_text
            return_values[1] = mmd_filepath
            # print(f"OpenAI API call successful. assistant_text: {assistant_text}, mmd_filepath: {mmd_filepath}, return_values: {return_values}")
        except Exception as e:
            # print(e)
            return_values[0] = "OpenAI API Error"
            return_values[1] = None

    def call_gemini_ai(self, args, return_values):
        user_input_msg, filename = args
        from google import genai
        try:
            response = self.gemini_client.models.generate_content(
                model=ct.AI_MODEL,
                config=genai.types.GenerateContentConfig(system_instruction=ct.AI_SYSTEM_INSTRUCTIONS),
                contents=user_input_msg
            )
            assistant_text = response.text or ""
            success_flag, mmd_filepath = self.save_mmd_to_file(filename, assistant_text)
            return_values[0] = assistant_text
            return_values[1] = mmd_filepath
        except Exception as e:
            print(e)
            return_values[0] = "Gemini API Error"
            return_values[1] = None

    def call_anthropic_ai(self, args, return_values):
        user_input_msg, filename = args
        from anthropic import Anthropic
        try:
            response = self.anthropic_client.messages.create(
                model=ct.AI_MODEL,
                max_tokens=20000,
                temperature=1,
                system=ct.AI_SYSTEM_INSTRUCTIONS,
                messages=[{"role": "user", "content": [{"type": "text", "text": user_input_msg}]}],
                thinking={"type": "disabled"},
                output_config={"effort":"high"}
            )
            assistant_text = response.content[0].text or ""
            success_flag, mmd_filepath = self.save_mmd_to_file(filename, assistant_text)
            return_values[0] = assistant_text
            return_values[1] = mmd_filepath
        except Exception as e:
            # print(e)
            return_values[0] = "Anthropic API Error"
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
