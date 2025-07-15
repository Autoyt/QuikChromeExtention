import os
import json
import subprocess

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Get folder path
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

# Choose mode
print("\nChoose mode:\n1 - Conventional\n2 - Inject")
mode = input("Enter choice (1 or 2): ").strip()

# Folder layout
app_dir = os.path.join(path, "app")
src_dir = os.path.join(path, "src")
os.makedirs(app_dir, exist_ok=True)
os.makedirs(src_dir, exist_ok=True)

# Write TypeScript entry
with open(os.path.join(src_dir, "index.ts"), "w") as f:
    f.write('console.log("Hello from TypeScript!");\n')

# Generate tsconfig.json
tsconfig = {
    "compilerOptions": {
        "target": "es2016",
        "module": "esnext",
        "outDir": "./app",
        "strict": True,
        "esModuleInterop": True,
        "skipLibCheck": True,
        "forceConsistentCasingInFileNames": True
    },
    "include": ["src"]
}
with open(os.path.join(path, "tsconfig.json"), "w") as f:
    json.dump(tsconfig, f, indent=2)

# Setup extension files
if mode == "1":
    popup_dir = os.path.join(app_dir, "popup")
    assets_dir = os.path.join(app_dir, "assets")
    os.makedirs(popup_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)

    manifest = {
        "manifest_version": 3,
        "name": extname,
        "version": "1.0",
        "description": extdesc,
        "action": {
            "default_popup": "popup/popup.html",
            "default_icon": "assets/icon.png"
        },
        "background": {
            "service_worker": "background.js"
        },
        "permissions": []
    }

    with open(os.path.join(app_dir, "popup", "popup.html"), "w") as f:
        f.write("""<!DOCTYPE html>
<html>
  <body>
    <h1>Popup</h1>
    <script src="popup.js"></script>
  </body>
</html>
""")

    with open(os.path.join(app_dir, "popup", "popup.js"), "w") as f:
        f.write('console.log("Popup loaded");\n')

    with open(os.path.join(app_dir, "background.js"), "w") as f:
        f.write('console.log("Background script loaded");\n')

elif mode == "2":
    os.makedirs(os.path.join(app_dir, "assets"), exist_ok=True)

    manifest = {
        "manifest_version": 3,
        "name": extname,
        "version": "1.0",
        "description": extdesc,
        "content_scripts": [{
            "matches": ["<all_urls>"],
            "js": ["content.js"]
        }],
        "permissions": ["scripting"]
    }

    with open(os.path.join(app_dir, "content.js"), "w") as f:
        f.write('console.log("Injected script running");\n')

else:
    print("Invalid mode selected.")
    exit(1)

# Write manifest
with open(os.path.join(app_dir, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2)

# Write info.md
with open(os.path.join(path, "info.md"), "w") as f:
    f.write(f"# {extname}\n\n")
    f.write(f"**Description:** {extdesc}\n\n")
    f.write("## Structure\n")
    f.write("- `app/`: Chrome extension files (manifest, js/html)\n")
    f.write("- `src/`: Your TypeScript source code\n")
    f.write("- Run `tsc --watch` to compile to `app/`\n\n")
    f.write("## Adding Icons\n")
    f.write("Put icons in `app/assets/` and update `manifest.json`:\n\n")
    f.write("```json\n\"icons\": {\n"
            "  \"16\": \"assets/icon16.png\",\n"
            "  \"32\": \"assets/icon32.png\",\n"
            "  \"48\": \"assets/icon48.png\",\n"
            "  \"128\": \"assets/icon128.png\"\n"
            "}\n```\n")

# Install TypeScript (local)
print("Installing TypeScript...")
try:
    subprocess.run(["npm", "init", "-y"], cwd=path, check=True)
    subprocess.run(["npm", "install", "--save-dev", "typescript"], cwd=path, check=True)
    print("✅ TypeScript installed.")
except Exception as e:
    print("❌ Failed to install TypeScript. Run manually with:")
    print("   npm install --save-dev typescript")

print(f"\n✅ Extension '{extname}' created at: {path}")
