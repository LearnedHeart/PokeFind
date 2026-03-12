import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

idx = css.find('/* --- PILL NAV --- */')
if idx != -1:
    css = css[:idx]
    
idx2 = css.find('.pill-nav {')
if idx2 != -1:
    css = css[:idx2]

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css.strip() + '\n')
