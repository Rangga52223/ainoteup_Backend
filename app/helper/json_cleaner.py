import json, sys, re, ast

def safe_json_parse(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # coba perbaiki dengan tambahin } kalau hilang
        fixed = text.strip()
        if fixed.endswith(","):
            fixed = fixed[:-1]
        if not fixed.endswith("}"):
            fixed += "}"
        try:
            return json.loads(fixed)
        except Exception:
            pass

        # coba eval python dict style
        try:
            return ast.literal_eval(fixed)
        except Exception:
            return text  # fallback: balikin string mentah