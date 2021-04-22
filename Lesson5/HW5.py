
def translate(string):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

    TRANS = {}
    for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):    
        TRANS[ord(c)]= t
        TRANS[ord(c.upper())] = t.upper()
    
    translated_string = string.translate(TRANS)

    return translated_string

def normalize(string):
    import re
    normalized_string = translate(string)
    normalized_string = re.sub(r'[^0-9a-zA-Z ]', '_', normalized_string, flags=re.ASCII)

    return normalized_string


def main():
    print (normalize('HANNA АННА ХОДЫКА?% МОЛОКО90 аб&в гдз я_к עִבְרִית'))


if __name__ == '__main__':
    main()