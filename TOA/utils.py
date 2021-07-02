import re
from itertools import product


def match_string_from_lang(string, lang):
    lang = sorted(lang, reverse=True)
    regex = re.compile(f'^({"|".join(lang)})*$')
    return re.match(regex, string)


def string_to_letters(string, lang):
    if not match_string_from_lang(string, lang):
        return []

    regex = re.compile(f'({"|".join(lang)})')
    return re.findall(regex, string)


def power_string(string_len, lang):
    combs = list(product(lang, repeat=int(string_len / len(min(lang))),))
    return [''.join(x) for x in combs if len(''.join(x)) == string_len]


def is_palindrome(string, lang):
    letters = string_to_letters(string, lang)
    return letters == letters[::-1]


def power_plindrome_string(string_len, lang):
    return [s for s in power_string(string_len, lang) if is_palindrome(s, lang)]
