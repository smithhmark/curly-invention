"""
longest is an interview question that I barfed all over but coded in 3 minutes once off the phone.
"""

def _longest(s):
    t = set()
    idx = 0
    while idx < len(s) and s[idx] not in t:
        t.add(s[idx])
        idx += 1
    return s[:idx]
    
def longest(s):
    max = ""
    for pos in range(len(s)-1):
        seq = _longest(s[pos:])
        if len(seq) > len(max):
            max = seq
    return max

def test_helper(): 
    assert _longest("abcda") == "abcd"
    assert _longest("aa") == "a"
    assert _longest("aba") == "ab"
    assert _longest("ab") == "ab"

def test_longest():
    assert longest("abcdabcdefgabc") == "abcdefg"
    assert longest("abcdabcabcde") == "abcde"
    assert longest("abcabc") == "abc"

