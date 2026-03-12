import os

for root, dirs, files in os.walk("."):
    for name in files:
        if name.endswith(".html") and "index" not in name and "auth" not in name:
            filepath = os.path.join(root, name)
            with open(filepath, "r") as f:
                content = f.read()
            if "<nav class=\"nav-links\">" in content and "nav-item\">Accueil</a>" not in content:
                depth = len(filepath.split("/")) - 2
                prefix = "../" * depth if depth > 0 else ""
                content = content.replace("<nav class=\"nav-links\">", "<nav class=\"nav-links\">\n                <a href=\"" + prefix + "index.html\" class=\"nav-item\">Accueil</a>")
                with open(filepath, "w") as f:
                    f.write(content)
                print(f"Updated {filepath}")

