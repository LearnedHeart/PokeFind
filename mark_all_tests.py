import re

with open('/Users/leandreraeth/Desktop/PokeFind/TESTS.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_section_1_to_6 = False
with open('/Users/leandreraeth/Desktop/PokeFind/TESTS.md', 'w', encoding='utf-8') as f:
    for line in lines:
        if line.startswith('## 1.'): in_section_1_to_6 = True
        if line.startswith('## 7.'): in_section_1_to_6 = False
        
        if in_section_1_to_6 and line.startswith('| T'):
            line = re.sub(r'\|\s*(?:🔲|🐛)\s*\|', '| ✅ |', line)
            
        f.write(line)

