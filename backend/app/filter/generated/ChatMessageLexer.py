# Generated from C:\Users\hung1\Learn\Sem2_2026\PPL\Chat-room\backend\app\filter\ChatMessage.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\6")
        buf.write("\34\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\3\2\6\2\r\n\2")
        buf.write("\r\2\16\2\16\3\3\6\3\22\n\3\r\3\16\3\23\3\4\6\4\27\n\4")
        buf.write("\r\4\16\4\30\3\5\3\5\2\2\6\3\3\5\4\7\5\t\6\3\2\5\4\2C")
        buf.write("\\c|\3\2\62;\5\2\13\f\17\17\"\"\2\36\2\3\3\2\2\2\2\5\3")
        buf.write("\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\3\f\3\2\2\2\5\21\3\2\2")
        buf.write("\2\7\26\3\2\2\2\t\32\3\2\2\2\13\r\t\2\2\2\f\13\3\2\2\2")
        buf.write("\r\16\3\2\2\2\16\f\3\2\2\2\16\17\3\2\2\2\17\4\3\2\2\2")
        buf.write("\20\22\t\3\2\2\21\20\3\2\2\2\22\23\3\2\2\2\23\21\3\2\2")
        buf.write("\2\23\24\3\2\2\2\24\6\3\2\2\2\25\27\t\4\2\2\26\25\3\2")
        buf.write("\2\2\27\30\3\2\2\2\30\26\3\2\2\2\30\31\3\2\2\2\31\b\3")
        buf.write("\2\2\2\32\33\13\2\2\2\33\n\3\2\2\2\6\2\16\23\30\2")
        return buf.getvalue()


class ChatMessageLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    WORD = 1
    NUMBER = 2
    WS = 3
    SYMBOL = 4

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
 ]

    symbolicNames = [ "<INVALID>",
            "WORD", "NUMBER", "WS", "SYMBOL" ]

    ruleNames = [ "WORD", "NUMBER", "WS", "SYMBOL" ]

    grammarFileName = "ChatMessage.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


