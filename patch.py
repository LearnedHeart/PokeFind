with open('style.css', 'a') as f:
    f.write("""
/* --- Nouvelles MAJ --- */
.hero-copy {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 900px;
    margin: 0 auto;
}

.hero-copy p {
    text-align: center;
}

.hero-actions {
    justify-content: center;
}

.mini-stats {
    justify-content: center;
}

.large-search {
    width: 100%;
    max-width: 800px;
    padding: 20px;
    border-radius: 32px;
    margin: 36px auto;
}

.large-search .search-bar input {
    font-size: 1.15rem;
    padding: 16px;
}

.large-search .search-bar .fa-magnifying-glass {
    font-size: 1.3rem;
    padding-left: 12px;
}

.large-search .search-bar .btn {
    padding: 16px 32px;
    font-size: 1.05rem;
    border-radius: 20px;
}

.search-pills {
    justify-content: center;
}

.placeholder-panel {
    width: 100%;
    max-width: 900px;
    aspect-ratio: 16/9;
    background: rgba(255, 255, 255, 0.5);
    border: 2px dashed rgba(24, 32, 50, 0.2);
    border-radius: var(--radius-lg);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: none;
}

.placeholder-content {
    text-align: center;
    color: var(--text-muted);
}

.placeholder-content i {
    font-size: 3rem;
    margin-bottom: 12px;
    opacity: 0.5;
}

.audience-card h3 {
    margin-top: 16px;
}
.audience-card .card-head {
    align-items: flex-start;
}
""")
