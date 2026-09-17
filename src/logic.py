import requests

def sort_by_severity(alerts):
    """Sort alerts from highest to lowest severity score."""
    return sorted(alerts, key=lambda a: a.score, reverse=True)

def check_ip_reputation(ip_address):
    """Look up rough geolocation for an IP via a free API (ip-api.com).

    try/except matters here: if there's no internet or the API is down,
    we return a clear fallback message instead of crashing.
    """
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=3)
        response.raise_for_status()
        data = response.json()
        return data.get("country", "unknown")
    except requests.exceptions.RequestException:
        return "Could not reach the API (check your internet connection)"
