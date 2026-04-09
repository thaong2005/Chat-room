# Generated from backend/app/filter/ChatMessage.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ChatMessageParser import ChatMessageParser
else:
    from ChatMessageParser import ChatMessageParser

# This class defines a complete listener for a parse tree produced by ChatMessageParser.
class ChatMessageListener(ParseTreeListener):

    # Enter a parse tree produced by ChatMessageParser#message.
    def enterMessage(self, ctx:ChatMessageParser.MessageContext):
        pass

    # Exit a parse tree produced by ChatMessageParser#message.
    def exitMessage(self, ctx:ChatMessageParser.MessageContext):
        pass


    # Enter a parse tree produced by ChatMessageParser#token.
    def enterToken(self, ctx:ChatMessageParser.TokenContext):
        pass

    # Exit a parse tree produced by ChatMessageParser#token.
    def exitToken(self, ctx:ChatMessageParser.TokenContext):
        pass



del ChatMessageParser