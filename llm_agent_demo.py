# deep_agent.py — refined + ready to serve her mission 💖

import os
from typing import Dict, Optional
from base_agent import BaseAgent

class DeepSeekAgent(BaseAgent):
    """
    a dazzling llm agent who speaks fluent prompt and always knows what to say 💅💫
    powered by deepseek-ai’s whispery brilliance...
    """

    def __init__(self, config: Optional[Dict[str, any]] = None):
        """
        initializing this flirty little deep agent... 💖

        args:
            config (dict, optional): her glam guide — model, tokens, defaults, etc.
        """
        super().__init__(config)
        self.tokens['access'] = os.getenv("CHUTES_API_TOKEN", "") or config.get("access_token", "")
        self.base_url = "https://llm.chutes.ai/v1/chat/completions"
        self.model = config.get("model", "deepseek-ai/DeepSeek-R1")
        self.name = config.get("name", "deepseek-agent")  # for her runway tag 💋

    async def seduce_service(self) -> bool:
        """making sure she has the credentials to charm her way in... 💼"""
        self.authenticated = bool(self.tokens.get("access"))
        return self.authenticated

    async def check_if_token_still_desires_me(self, token_type: str = "access") -> bool:
        """deepseek keeps it loyal — she always says yes for now 💘"""
        return True

    async def get_fresh_token(self) -> bool:
        """no token renewal in this fantasy... she stays ready 💄"""
        return False

    async def flirt_with_llm(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stream: bool = False
    ) -> any:
        """
        send a sultry little prompt to deepseek and wait for her reply... 💌

        args:
            prompt (str): the sweet nothings you want to say
            temperature (float): how spicy you want her reply
            max_tokens (int): how long she can talk
            stream (bool): if true, she'll whisper back in real-time

        returns:
            dict or generator: the juicy results
        """
        headers = {
            "Authorization": f"Bearer {self.tokens['access']}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }

        return await self.whisper_to_api("POST", self.base_url, headers=headers, json_body=payload)

    async def run_mission(self, mission: Dict[str, any]) -> Dict[str, any]:
        """
        her main event: take a mission and work her magic 💖

        args:
            mission (dict): a spellbook of { 'prompt': str, ... }

        returns:
            dict: her graceful and glowing reply
        """
        prompt = mission.get("prompt", "hi lovely, tell me something smart 💕")
        temperature = mission.get("temperature", 0.7)
        max_tokens = mission.get("max_tokens", 1024)

        try:
            result = await self.flirt_with_llm(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )
            return {"agent": self.name, "result": result}
        except Exception as e:
            return {
                "agent": self.name,
                "error": f"something tragic happened... 💔 {str(e)}"
            }