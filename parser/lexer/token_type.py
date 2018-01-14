from enum import Enum


class TokenType(Enum):
    # Comment node
    COMMENT = '#.*'
    # AKO/ONDA veznici
    IF = 'AKO'
    THEN = 'ONDA'
    # I/ILI veznici
    OR = 'ILI'
    AND = 'I'
    # je/nije veznici
    IS = 'je'
    NOT = 'nije'
    # Argument predikata
    QUOTE = '\"'
    # WORD
    WORD = '[A-Za-zčćžšđČĆŽŠĐ][a-zčćžpšđ]+'
    # Parametar
    PARAM = '[A-ZČĆŽŠĐ_]+[0-9]*'


if __name__ == "__main__":
    print(TokenType.COMMENT.name, TokenType.COMMENT.value)
