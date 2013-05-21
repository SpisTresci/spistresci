#!/usr/bin/python
# -*- coding: utf-8 -*-

substitution_table = [(u"CH", u"H"),
                      (u"TRZ", u"C"), (u"TCZ", u"C"), (u"CZ", u"C"), (u"SZ", u"C"),
                      (u"RZ", u"Ż"), (u"DZ", u"Ż"), (u"DŻ", u"Ż"), (u"DŹ", u"Ż"),
                      (u"CI", u"Ć"),
                      (u"NI", u"Ń"), (u"MI", u"Ń"),
                      (u"SI", u"Ś"),
                      (u"ZI", u"Ź"),
                      (u"ON", u"Ą"), (u"OM", u"Ą"),
                      (u"KS", u"X"), (u"KŚ", u"X")
]

code_table = [(u"A", u"0"), (u"E", u"0"), (u"I", u"0"), (u"J", u"0"), (u"O", u"0"), (u"U", u"0"), (u"Y", u"0"), (u"Ą", u"0"), (u"Ę", u"0"), (u"Ó", u"0"),
              (u"B", u"1"), (u"F", u"1"), (u"P", u"1"), (u"V", u"1"), (u"W", u"1"),
              (u"C", u"2"), (u"S", u"2"), (u"Z", u"2"), (u"Ć", u"2"), (u"Ś", u"2"), (u"Ż", u"2"), (u"Ź", u"2"),
              (u"D", u"3"), (u"T", u"3"),
              (u"L", u"4"), (u"Ł", u"4"),
              (u"M", u"5"), (u"N", u"5"), (u"Ń", u"5"),
              (u"R", u"6"),
              (u"G", u"7"), (u"H", u"7"), (u"K", u"7"), (u"Q", u"7"), (u"X", u"7")
]

reduce_codes_table = [('00', '0'), ('11', '1'), ('22', '2'), ('33', '3'), ('44', '4'), ('55', '5'), ('66', '6'), ('77', '7')]

def strtr(word, table):
    old_word = word
    while True:
        for sub in table:
            if sub[0] in word:
                word = word.replace(sub[0], sub[1])
        if old_word == word:
            break
        else:
            old_word = word

    return word

def removeNotLetters(word):
    return ''.join([letter if ord(letter) >= ord("A") and ord(letter) <= ord("Z") else "" for letter in word])

def soundexPL(word):
    word = word.upper()
    word = removeNotLetters(word)
    word = strtr(word, substitution_table)
    word = strtr(word, code_table)
    word = strtr(word, reduce_codes_table)
    word = strtr(word, [('0', '')])
    word = word[:4] + ('0' * (4 - len(word)))
    return int(word)

def main():
    print soundexPL(u"Wróżka")

if __name__ == '__main__':
    main()
