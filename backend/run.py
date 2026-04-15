import os
import subprocess
import sys

from antlr4 import CommonTokenStream, FileStream, Token
from antlr4.error.ErrorListener import ErrorListener


DIR = os.path.dirname(__file__)
ANTLR_JAR = "C:/antlr/antlr4-4.9.2-complete.jar"
CPL_DEST = os.path.join(DIR, "app", "filter", "generated")
SRC = os.path.join(DIR, "app", "filter", "ChatMessage.g4")
TESTS_DIR = os.path.join(DIR, "tests")


def print_usage() -> None:
    print("python backend/run.py gen")
    print("python backend/run.py test [filename]")


def print_break() -> None:
    print("-----------------------------------------------")


def generate_antlr_to_python() -> None:
    print("Antlr4 is running...")
    subprocess.run(
        [
            "java",
            "-jar",
            ANTLR_JAR,
            "-o",
            CPL_DEST,
            "-no-listener",
            "-Dlanguage=Python3",
            SRC,
        ],
        check=True,
    )
    print("Generate successfully")


def run_test(filename: str = "001.txt") -> None:
    print("Running testcases...")

    from app.filter.generated.ChatMessageLexer import ChatMessageLexer
    from app.filter.generated.ChatMessageParser import ChatMessageParser

    class CustomErrorListener(ErrorListener):
        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            print(f"Input rejected: {msg}")
            raise SystemExit(1)

    input_file = os.path.join(TESTS_DIR, filename)
    if not os.path.exists(input_file):
        print(f"Test file not found: {input_file}")
        raise SystemExit(1)

    print("List of token:")
    lexer = ChatMessageLexer(FileStream(input_file, encoding="utf-8"))
    tokens = []
    token = lexer.nextToken()
    while token.type != Token.EOF:
        tokens.append(token.text)
        token = lexer.nextToken()
    tokens.append("<EOF>")
    print(",".join(tokens))

    input_stream = FileStream(input_file, encoding="utf-8")
    lexer = ChatMessageLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ChatMessageParser(stream)
    tree = parser.message()
    print(tree.toStringTree(recog=parser))

    lexer = ChatMessageLexer(FileStream(input_file, encoding="utf-8"))
    token_stream = CommonTokenStream(lexer)
    parser = ChatMessageParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(CustomErrorListener())

    try:
        parser.message()
        print("Input accepted")
    except SystemExit:
        pass

    print_break()
    print("Run tests completely")


def main(argv: list[str]) -> None:
    print("Complete jar file ANTLR  :  " + str(ANTLR_JAR))
    print("Length of arguments      :  " + str(len(argv)))
    print_break()

    if len(argv) < 1:
        print_usage()
    elif argv[0] == "gen":
        generate_antlr_to_python()
    elif argv[0] == "test":
        filename = argv[1] if len(argv) > 1 else "001.txt"
        run_test(filename)
    else:
        print_usage()


if __name__ == "__main__":
    main(sys.argv[1:])
