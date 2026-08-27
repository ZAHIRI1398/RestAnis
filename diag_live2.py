import re
import requests

BASES = {
    "BE": "https://www.restofourchette.be",
    "RAIL": "https://web-production-85f59.up.railway.app",
}

for label, base in BASES.items():
    s = requests.Session()
    s.post(base + "/admin/login",
           data={"username": "admin", "password": "password123"},
           allow_redirects=False, timeout=30)
    r = s.get(base + "/admin/reservations", timeout=30)
    txt = r.text

    # Extract table rows
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", txt, re.DOTALL)
    print(f"\n=== {label} : {len(rows)} <tr> trouvées ===")
    for i, row in enumerate(rows):
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.DOTALL)
        cells = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
        cells = [re.sub(r"\s+", " ", c) for c in cells]
        if cells:
            print(f"  row{i}: {cells}")
