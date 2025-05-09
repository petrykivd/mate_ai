from abc import ABC, abstractmethod


class BaseLLMClient(ABC):

    @abstractmethod
    async def send_message(
        self,
        system_prompt: str,
        message: str
    ):
        pass
