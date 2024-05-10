import logging
from typing import Dict, List

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI


load_dotenv(find_dotenv())


class OpenAIModel:
    def __init__(
            self,
            model_name: str = 'gpt-4-turbo',
            temperature: float = 0.0,
            max_tokens: int = 4096,
    ):
        """
        Class that wraps OpenAI API to generate answers from chat history or prompt
        :param model_name: Model name to use for generating answers
        :param temperature: Temperature to use for generating answers, 0.0 is (almost) deterministic
        :param max_tokens: Maximum number of tokens to generate in the response
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenAI()
        self.seed = 42

    def generate_answer_from_chat_history(self, chat_history: List[Dict[str, str]]) -> str:
        """
        Generate answer from chat history
        :param chat_history: List of chat history where each element is a dictionary with keys 'role' and 'content'
        :return: Generated answer
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=chat_history,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            seed=self.seed,
        )
        logging.info(f'Generated response. #N Completion Tokens={response.usage.completion_tokens} -'
                     f' #N Prompt Tokens={response.usage.prompt_tokens}')
        if response.choices[0].finish_reason != 'stop':
            logging.warning(f'Response did not finish due to {response.choices[0].finish_reason} reason')
        return response.choices[0].message.content

    def generate_answer_from_prompt(self, prompt: str) -> str:
        """
        Generate answer from prompt
        :param prompt: Prompt to generate answer from
        :return: Generated answer
        """
        fake_history = [{'role': 'system', 'content': prompt}]
        answer = self.generate_answer_from_chat_history(
            chat_history=fake_history
        )
        return answer

