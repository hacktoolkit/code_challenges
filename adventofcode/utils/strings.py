def base_anagram(word):
    letters = [c for c in word]
    anagram = ''.join(sorted(letters))
    return anagram
