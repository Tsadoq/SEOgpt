from abc import ABC, abstractmethod
from typing import List, Dict


class GenerativeModel(ABC):
    @abstractmethod
    async def generate_answer_from_chat_history(self, chat_history: List[Dict[str, str]], output_json=False) -> str:
        pass

    @abstractmethod
    async def generate_answer_from_prompt(self, prompt: str, output_json=False) -> str:
        pass
