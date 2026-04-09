from __future__ import annotations

from pathlib import Path

from antlr4 import CommonTokenStream, InputStream
from antlr4.Token import Token

from .generated.ChatMessageLexer import ChatMessageLexer


def load_bad_words(file_path: Path) -> set[str]:
    if not file_path.exists():
        return set()

    words: set[str] = set()
    for line in file_path.read_text(encoding="utf-8").splitlines():
        cleaned = line.strip().lower()
        if cleaned and not cleaned.startswith("#"):
            words.add(cleaned)

    return words


class AntlrWordFilter:
    def __init__(self, bad_words: set[str], mask_char: str = "*") -> None:
        self.bad_words = {word.lower() for word in bad_words}
        self.mask_char = mask_char

    def sanitize(self, text: str) -> tuple[str, bool]:
        filtered = False
        sanitized_parts: list[str] = []

        for token in self._tokenize(text):
            token_text = token.text or ""
            if token.type == ChatMessageLexer.WORD and token_text.lower() in self.bad_words:
                sanitized_parts.append(self.mask_char * len(token_text))
                filtered = True
            else:
                sanitized_parts.append(token_text)

        return "".join(sanitized_parts), filtered

    def find_invalid_words(self, text: str) -> list[str]:
        found: list[str] = []
        seen: set[str] = set()

        for token in self._tokenize(text):
            token_text = (token.text or "").lower()
            if token.type == ChatMessageLexer.WORD and token_text in self.bad_words:
                if token_text not in seen:
                    seen.add(token_text)
                    found.append(token_text)

        return found

    def _tokenize(self, text: str) -> list[Token]:
        lexer = ChatMessageLexer(InputStream(text))
        token_stream = CommonTokenStream(lexer)
        token_stream.fill()
        return [token for token in token_stream.tokens if token.type != Token.EOF]
