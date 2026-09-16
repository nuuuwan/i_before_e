from ibe.core.Word import Word

words = Word.list()
n_words = len(words)


def rule(word, s_i, s_e, s_c):
    s_ie = s_i + s_e
    s_ei = s_e + s_i
    s_cie = s_c + s_ie
    s_cei = s_c + s_ei

    if s_ie not in word and s_ei not in word:
        return None

    if s_cie in word:
        return False
    if s_ei in word and not s_cei in word:
        return False
    return True


def analyze(s_i, s_e, s_c):
    n_null = 0
    n_true = 0
    n_false = 0
    for word in words:
        result = rule(word, s_i, s_e, s_c)
        if result is None:
            n_null += 1
            continue

        if result is True:
            n_true += 1
        else:
            n_false += 1

    return n_null, n_true, n_false


LETTERS = "abcdefghijklmnopqrstuvwxyz"
for s_i in LETTERS:
    if s_i != "i":
        continue
    for s_e in LETTERS:
        if s_e != "e":
            continue
        if s_i == s_e:
            continue
        for s_c in LETTERS:

            if s_c == s_i or s_c == s_e:
                continue

            n_null, n_true, n_false = analyze(s_i, s_e, s_c)
            if n_true + n_false > n_words * 0.001:
                if n_true > 2 * n_false:
                    p_true = n_true / (n_true + n_false)
                    print(
                        f"{p_true:.0%} ({n_true + n_false}):"
                        + f" '{s_i}' before '{s_e}' except after '{s_c}'"
                    )
                    print()
