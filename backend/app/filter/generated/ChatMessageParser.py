# Generated from C:\Users\hung1\Learn\Sem2_2026\PPL\Chat-room\backend\app\filter\ChatMessage.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\6")
        buf.write("\21\4\2\t\2\4\3\t\3\3\2\7\2\b\n\2\f\2\16\2\13\13\2\3\2")
        buf.write("\3\2\3\3\3\3\3\3\2\2\4\2\4\2\3\3\2\3\6\2\17\2\t\3\2\2")
        buf.write("\2\4\16\3\2\2\2\6\b\5\4\3\2\7\6\3\2\2\2\b\13\3\2\2\2\t")
        buf.write("\7\3\2\2\2\t\n\3\2\2\2\n\f\3\2\2\2\13\t\3\2\2\2\f\r\7")
        buf.write("\2\2\3\r\3\3\2\2\2\16\17\t\2\2\2\17\5\3\2\2\2\3\t")
        return buf.getvalue()


class ChatMessageParser ( Parser ):

    grammarFileName = "ChatMessage.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "WORD", "NUMBER", "WS", "SYMBOL" ]

    RULE_message = 0
    RULE_token = 1

    ruleNames =  [ "message", "token" ]

    EOF = Token.EOF
    WORD=1
    NUMBER=2
    WS=3
    SYMBOL=4

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class MessageContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(ChatMessageParser.EOF, 0)

        def token(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ChatMessageParser.TokenContext)
            else:
                return self.getTypedRuleContext(ChatMessageParser.TokenContext,i)


        def getRuleIndex(self):
            return ChatMessageParser.RULE_message




    def message(self):

        localctx = ChatMessageParser.MessageContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_message)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 7
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << ChatMessageParser.WORD) | (1 << ChatMessageParser.NUMBER) | (1 << ChatMessageParser.WS) | (1 << ChatMessageParser.SYMBOL))) != 0):
                self.state = 4
                self.token()
                self.state = 9
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 10
            self.match(ChatMessageParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TokenContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WORD(self):
            return self.getToken(ChatMessageParser.WORD, 0)

        def NUMBER(self):
            return self.getToken(ChatMessageParser.NUMBER, 0)

        def WS(self):
            return self.getToken(ChatMessageParser.WS, 0)

        def SYMBOL(self):
            return self.getToken(ChatMessageParser.SYMBOL, 0)

        def getRuleIndex(self):
            return ChatMessageParser.RULE_token




    def token(self):

        localctx = ChatMessageParser.TokenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_token)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << ChatMessageParser.WORD) | (1 << ChatMessageParser.NUMBER) | (1 << ChatMessageParser.WS) | (1 << ChatMessageParser.SYMBOL))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





