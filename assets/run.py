import os
import json

# Go one level up from "assets/run.py"
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ask for location
path = input("Location (folder name or full path): ").strip()
if not os.path.isabs(path):
    path = os.path.join(base_dir, path)

confirm = input(f"{path} | Location correct? (Y/N): ").strip().lower()
if confirm == "n":
    new_path = input("New location: ").strip()
    path = new_path if os.path.isabs(new_path) else os.path.join(base_dir, new_path)

# Extension info
extname = input("Extension name: ").strip()
extdesc = input("Extension description: ").strip()

# Mode
print("\nChoose mode:\n1 - Conventional\n2 - Inject")
mode = input("Enter choice (1 or 2): ").strip()

os.makedirs(path, exist_ok=True)

# Setup files
if mode == "1":
    os.makedirs(os.path.join(path, "popup"), exist_ok=True)
    os.makedirs(os.path.join(path, "assets"), exist_ok=True)
    manifest = {
        "manifest_version": 3,
        "name": extname, "version": "1.0", "description": extdesc,
        "action": {
            "default_popup": "popup/popup.html",
            "default_icon": "assets/icon.png"
        },
        "background": {"service_worker": "background.js"},
        "permissions": []
    }
    with open(os.path.join(path, "popup", "popup.html"), "w") as f:
        f.write("""<!DOCTYPE html>
<html>
  <body>
    <h1>Popup</h1>
    <script src="popup.js"></script>
  </body>
</html>
""")
    with open(os.path.join(path, "popup", "popup.js"), "w") as f:
        f.write('console.log("Popup loaded");\n')
    with open(os.path.join(path, "background.js"), "w") as f:
        f.write('console.log("Background script loaded");\n')

elif mode == "2":
    os.makedirs(os.path.join(path, "assets"), exist_ok=True)
    manifest = {
        "manifest_version": 3,
        "name": extname, "version": "1.0", "description": extdesc,
        "content_scripts": [{"matches": ["<all_urls>"], "js": ["content.js"]}],
        "permissions": ["scripting"]
    }
    with open(os.path.join(path, "content.js"), "w") as f:
        f.write('console.log("Injected script running");\n')
else:
    print("Invalid mode selected.")
    exit(1)

# Write manifest.json
with open(os.path.join(path, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2)

# Write info.md
with open(os.path.join(path, "info.md"), "w") as f:
    f.write(f"# {extname}\n\n")
    f.write(f"**Description:** {extdesc}\n\n")
    f.write("## Adding Icons\n")
    f.write("Place PNG icon files in `assets/` with these sizes:\n\n")
    f.write("```json\n\"icons\": {\n"
            "  \"16\": \"assets/icon16.png\",\n"
            "  \"32\": \"assets/icon32.png\",\n"
            "  \"48\": \"assets/icon48.png\",\n"
            "  \"128\": \"assets/icon128.png\"\n"
            "}\n```")
    f.write("\n\n- 16×16 for toolbar/favicon\n- 48×48 for extensions page\n- 128×128 for installation and Chrome Web Store :contentReference[oaicite:1]{index=1}\n\n")
    f.write("## General Info\n")
    f.write("- 128×128 for installation and Chrome Web Store\n\n")
    f.write("- Use PNG format (supports transparency)\n")
    f.write("- Optional runtime icon change via `chrome.action.setIcon()`\n")


print(f"\n✅ Extension '{extname}' + info.md created at: {path}")
