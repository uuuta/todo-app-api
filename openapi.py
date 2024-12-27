import json

from main import app

if __name__ == "__main__":
    with open("openapi.json", "w", encoding="utf-8") as f:
        api_spec = app.openapi()
        f.write(json.dumps(api_spec, indent=4, ensure_ascii=False))
