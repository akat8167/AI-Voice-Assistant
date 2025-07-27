import ollama
from livekit.agents import llm

class OllamaSession:
    def __init__(self, model):
        self.model = model
        self.conversation = self
        self.item = self
        self.response = self

    def create(self, msg):
        pass  # LiveKit expects this placeholder

    def create_response(self):
        pass


class OllamaModel:
    def __init__(self, model="mistral", base_url="http://localhost:11434", temperature=0.7, voice=None):
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self.voice = voice
        self._sessions = [OllamaSession(self)]

    def session(self, chat_ctx=None, fnc_ctx=None):
        """Return a new session for LiveKit, accepts chat_ctx and fnc_ctx for compatibility"""
        s = OllamaSession(self)
        self._sessions.append(s)
        return s

    @property
    def sessions(self):
        return self._sessions

    def chat(self, prompt: str) -> str:
        """Simple one-shot chat"""
        res = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return res["message"]["content"]

    def stream_chat(self, prompt: str):
        """Streaming chat generator"""
        stream = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in stream:
            if "message" in chunk and "content" in chunk["message"]:
                yield chunk["message"]["content"]
