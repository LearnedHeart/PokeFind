with open('style.css', 'a', encoding='utf-8') as f:
    f.write("""

/* --- PILL NAV --- */
.pill-nav {
    display: flex;
    gap: 16px;
    align-items: center;
}

.nav-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-decoration: none;
    transition: all 0.2s ease;
}

.pill-red {
    background: #fdf2f2;
    border: 1px solid #fae8e8;
    color: #b91c1c;
}
.pill-red:hover {
    background: #fae8e8;
}
.pill-red .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #dc2626;
    box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.15);
}

""")
