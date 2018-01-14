import re

from parser.lexer.lexer_err import LexerException
from parser.lexer.token import Token

from parser.lexer.token_type import TokenType


class Lexer:
    def __init__(self, text):
        self.data = re.finditer('|'.join([t_type.value for t_type in TokenType]) + str('|[^\s]+'), text.strip())
        self.token = None

    def tokens(self):
        for matched in self.data:
            char = matched.group()
            t_type = self.get_token_type(char)
            self.token = Token(t_type, char)
            yield self.token

    def get_token(self):
        return self.token

    @staticmethod
    def get_token_type(char):
        for t_type in TokenType:
            if re.match(t_type.value, char):
                return t_type
        raise LexerException("Character " + str(char) + " cannot be parsed!")


if __name__ == "__main__":
    rule = "AKO L_1 je \"Kritično blizu ILI Blizu\" I LK je \"Kritično daleko\" ONDA K je \"Oštro desno\"\n #fefefefefe\n " \
           "AKO L " \
           "nije \"blizu ONDA K je lijevo\""
    l = Lexer(rule)
    for c in l.tokens():
        print(c)
