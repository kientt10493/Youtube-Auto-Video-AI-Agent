import json
import os
from typing import Type, TypeVar, Optional, List, Dict, Any
from pydantic import BaseModel
from openai import OpenAI

T = TypeVar("T", bound=BaseModel)

# Cấu hình kết nối tới Gateway Gemini Web API / 9Router
GEMINI_API_BASE = os.getenv("GEMINI_API_URL", "http://localhost:4981/openai/v1")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "dummy-key")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-3.8-flash")

client = OpenAI(
    base_url=GEMINI_API_BASE,
    api_key=GEMINI_API_KEY,
)

class BaseAgent:
    def __init__(
        self,
        name: str,
        role: str,
        system_instruction: str,
        response_model: Optional[Type[T]] = None,
        model: str = DEFAULT_MODEL,
    ):
        self.name = name
        self.role = role
        self.system_instruction = system_instruction
        self.response_model = response_model
        self.model = model

    def run(self, prompt: str, schema_instruction: bool = True) -> Any:
        sys_prompt = (
            f"You are {self.name}, working as {self.role} in a professional YouTube media studio.\n"
            f"Instructions:\n{self.system_instruction}\n"
            f"Note: All output content, narratives, scripts, titles, and factual texts must be written naturally in Vietnamese.\n"
        )
        
        if self.response_model and schema_instruction:
            schema_json = json.dumps(self.response_model.model_json_schema(), ensure_ascii=False, indent=2)
            sys_prompt += (
                f"\nCRITICAL INSTRUCTIONS FOR JSON OUTPUT:\n"
                f"- You MUST respond with ONLY a valid JSON object matching the schema below.\n"
                f"- Do NOT wrap in python code (DO NOT write import json or print).\n"
                f"- Return raw JSON starting with '{{' and ending with '}}'.\n"
                f"Pydantic JSON Schema:\n{schema_json}\n"
            )

        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"Task instructions (Produce all content in Vietnamese):\n{prompt}"},
        ]

        create_kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
        }

        try:
            response = client.chat.completions.create(**create_kwargs)
            raw_content = response.choices[0].message.content or "{}"
            raw_content = raw_content.strip()
            # Bỏ dấu nháy đơn bao bọc '{"..."}' hoặc '''{"..."}'''
            while (raw_content.startswith("'") and raw_content.endswith("'")) or (raw_content.startswith('"') and raw_content.endswith('"')):
                raw_content = raw_content[1:-1].strip()
            while raw_content.endswith("'''") or raw_content.endswith('"""'):
                raw_content = raw_content[:-3].strip()
            
            # Tìm kiếm vị trí '{' đầu tiên trong toàn bộ văn bản trả về
            text = raw_content
            # Nếu model trả về ```python?code_reference... hoặc ```...```
            import re
            blocks = re.findall(r"```(?:[a-zA-Z0-9_\-\?&=]+)?\s*([\s\S]*?)\s*```", text)
            for b in blocks:
                s_idx = b.find("{")
                if s_idx != -1:
                    try:
                        decoder = json.JSONDecoder()
                        data, _ = decoder.raw_decode(b[s_idx:])
                        if self.response_model:
                            return self.response_model.model_validate(data)
                        return data
                    except Exception:
                        pass

            start_idx = text.find("{")
            if start_idx != -1:
                try:
                    decoder = json.JSONDecoder()
                    data, _ = decoder.raw_decode(text[start_idx:])
                    if self.response_model:
                        return self.response_model.model_validate(data)
                    return data
                except Exception:
                    pass

            # Thử tìm substring giữa '{' đầu tiên và '}' cuối cùng
            e_idx = text.rfind("}")
            if start_idx != -1 and e_idx != -1 and e_idx > start_idx:
                try:
                    data = json.loads(text[start_idx : e_idx + 1])
                    if self.response_model:
                        return self.response_model.model_validate(data)
                    return data
                except Exception:
                    pass

            if self.response_model:
                return self.response_model.model_validate_json(text.strip())
            return raw_content
        except Exception as e:
            raise RuntimeError(f"[{self.name}] Lỗi khi gọi Gemini: {e}")
