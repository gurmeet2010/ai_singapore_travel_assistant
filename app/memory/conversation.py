from collections import defaultdict, deque
from threading import Lock


class ConversationMemory:
    def __init__(self, max_messages: int = 12):
        self._messages: dict[str, deque[dict[str, str]]] = defaultdict(
            lambda: deque(maxlen=max_messages)
        )
        self._lock = Lock()

    def add(self, session_id: str, role: str, content: str) -> None:
        with self._lock:
            self._messages[session_id].append(
                {"role": role, "content": content}
            )

    def get(self, session_id: str) -> list[dict[str, str]]:
        with self._lock:
            return list(self._messages[session_id])

    def as_text(self, session_id: str) -> str:
        messages = self.get(session_id)
        if not messages:
            return "No previous conversation."

        return "\n".join(
            f"{message['role'].upper()}: {message['content']}"
            for message in messages
        )


memory = ConversationMemory()
