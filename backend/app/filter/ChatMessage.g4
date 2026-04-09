grammar ChatMessage;

message: token* EOF;

token: WORD | NUMBER | WS | SYMBOL;

WORD: [a-zA-Z]+;
NUMBER: [0-9]+;
WS: [ \t\r\n]+;
SYMBOL: .;
