import re

tests_to_mark = ["T04", "T12", "T15", "T27", "T28", "T32", "T33", "T37", "T42", "T43", "T44", "T48", "T49", "T63", "T68", "T70", "T72", "T73", "T75", "T78"]

with open('/Users/leandreraeth/Desktop/PokeFind/TESTS.md', 'r') as f:
    text = f.read()

for t in tests_to_mark:
    # regex to find "| TXX | ... | 🐛 |" or "| TXX | ... | 🔲 |" and change to ✅
    # find lines starting with "| {t} |"
    pattern = r"(\| " + t + r" \|(?:(?!\|).)*\|(?:(?!\|).)*\|) (?:🐛|🔲) (\|)"
    text = re.sub(pattern, r"\1 ✅ \2", text)

with open('/Users/leandreraeth/Desktop/PokeFind/TESTS.md', 'w') as f:
    f.write(text)

