from thefuck.utils import memoize, get_alias

target_layout = '''qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?'''
# any new keyboard layout must be appended

greek = ''';ςερτυθιοπ[]ασδφγηξκλ΄ζχψωβνμ,./:΅ΕΡΤΥΘΙΟΠ{}ΑΣΔΦΓΗΞΚΛ¨"ΖΧΨΩΒΝΜ<>?'''
korean = '''ㅂㅈㄷㄱㅅㅛㅕㅑㅐㅔ[]ㅁㄴㅇㄹㅎㅗㅓㅏㅣ;'ㅋㅌㅊㅍㅠㅜㅡ,./ㅃㅉㄸㄲㅆㅛㅕㅑㅒㅖ{}ㅁㄴㅇㄹㅎㅗㅓㅏㅣ:"ㅋㅌㅊㅍㅠㅜㅡ<>?'''

source_layouts = ['''йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,''',
                  '''йцукенгшщзхїфівапролджєячсмитьбю.ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ,''',
                  '''ضصثقفغعهخحجچشسیبلاتنمکگظطزرذدپو./ًٌٍَُِّْ][}{ؤئيإأآة»«:؛كٓژٰ‌ٔء><؟''',
                  '''/'קראטוןםפ][שדגכעיחלךף,זסבהנמצתץ.QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?''',
                  greek,
                  korean]

source_to_target = {
    greek: {';': "q", 'ς': "w", 'ε': "e", 'ρ': "r", 'τ': "t", 'υ': "y",
            'θ': "u", 'ι': "i", 'ο': "o", 'π': "p", '[': "[", ']': "]",
            'α': "a", 'σ': "s", 'δ': "d", 'φ': "f", 'γ': "g", 'η': "h",
            'ξ': "j", 'κ': "k", 'λ': "l", '΄': "'", 'ζ': "z", 'χ': "x",
            'ψ': "c", 'ω': "v", 'β': "b", 'ν': "n", 'μ': "m", ',': ",",
            '.': ".", '/': "/", ':': "Q", '΅': "W", 'Ε': "E", 'Ρ': "R",
            'Τ': "T", 'Υ': "Y", 'Θ': "U", 'Ι': "I", 'Ο': "O", 'Π': "P",
            '{': "{", '}': "}", 'Α': "A", 'Σ': "S", 'Δ': "D", 'Φ': "F",
            'Γ': "G", 'Η': "H", 'Ξ': "J", 'Κ': "K", 'Λ': "L", '¨': ":",
            '"': '"', 'Ζ': "Z", 'Χ': "X", 'Ψ': "C", 'Ω': "V", 'Β': "B",
            'Ν': "N", 'Μ': "M", '<': "<", '>': ">", '?': "?", 'ά': "a",
            'έ': "e", 'ύ': "y", 'ί': "i", 'ό': "o", 'ή': 'h', 'ώ': "v",
            'Ά': "A", 'Έ': "E", 'Ύ': "Y", 'Ί': "I", 'Ό': "O", 'Ή': "H",
            'Ώ': "V"},
}

'''Lists used for decomposing korean letters.'''
HEAD_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ',
             'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
BODY_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ',
             'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
TAIL_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ',
             'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ',
             'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
DOUBLE_LIST = ['ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ', 'ㄳ', 'ㄵ', 'ㄶ', 'ㄺ',
               'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㅀ', 'ㅄ']
DOUBLE_MOD_LIST = ['ㅗㅏ', 'ㅗㅐ', 'ㅗㅣ', 'ㅜㅓ', 'ㅜㅔ', 'ㅜㅣ', 'ㅡㅣ', 'ㄱㅅ',
                   'ㄴㅈ', 'ㄴㅎ', 'ㄹㄱ', 'ㄹㅁ', 'ㄹㅂ', 'ㄹㅅ', 'ㄹㅌ', 'ㄹㅎ', 'ㅂㅅ']


@memoize
def _get_matched_layout(command):
    # don't use command.split_script here because a layout mismatch will likely
    # result in a non-splitable script as per shlex
    cmd = command.script.split(' ')
    for source_layout in source_layouts:
        is_all_match = True
        for cmd_part in cmd:
            if not all([ch in source_layout or ch in '-_' for ch in cmd_part]):
                is_all_match = False
                break

        if is_all_match:
            return source_layout


def _switch(ch, layout):
    if ch in layout:
        return target_layout[layout.index(ch)]
    return ch


def _switch_command(command, layout):
    # Layouts with different amount of characters than English
    if layout in source_to_target:
        return ''.join(source_to_target[layout].get(ch, ch)
                       for ch in command.script)

    return ''.join(_switch(ch, layout) for ch in command.script)


def _decompose_korean(command):
    def _change_double(ch):
        if ch in DOUBLE_LIST:
            return DOUBLE_MOD_LIST[DOUBLE_LIST.index(ch)]
        return ch

    hg_str = ''
    for ch in command.script:
        if '가' <= ch <= '힣':
            ord_ch = ord(ch) - ord('가')
            hd = ord_ch // 588
            bd = (ord_ch - 588 * hd) // 28
            tl = ord_ch - 588 * hd - 28 * bd
            for ch in [HEAD_LIST[hd], BODY_LIST[bd], TAIL_LIST[tl]]:
                if ch != ' ':
                    hg_str += _change_double(ch)
        else:
            hg_str += _change_double(ch)
    return hg_str


def match(command):
    if 'not found' not in command.output:
        return False
    if any('ㄱ' <= ch <= 'ㅎ' or 'ㅏ' <= ch <= 'ㅣ' or '가' <= ch <= '힣'
            for ch in command.script):
        return True

    matched_layout = _get_matched_layout(command)
    return (matched_layout and
            _switch_command(command, matched_layout) != get_alias())


def get_new_command(command):
    if any('ㄱ' <= ch <= 'ㅎ' or 'ㅏ' <= ch <= 'ㅣ' or '가' <= ch <= '힣'
            for ch in command.script):
        command.script = _decompose_korean(command)
    matched_layout = _get_matched_layout(command)
    return _switch_command(command, matched_layout)
