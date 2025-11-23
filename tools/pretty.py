import json

def pretty_json(data):
    """Return beautifully formatted JSON text."""
    try:
        return json.dumps(data, indent=4, ensure_ascii=False)
    except Exception:
        # If printing fails for some reason, fallback to string
        return str(data)
