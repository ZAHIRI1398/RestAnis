import requests

BASES = {
    "BE (www.restofourchette.be)": "https://www.restofourchette.be",
    "RAIL (web-production-85f59)": "https://web-production-85f59.up.railway.app",
}

for label, base in BASES.items():
    s = requests.Session()
    # login
    r = s.post(base + "/admin/login",
               data={"username": "admin", "password": "password123"},
               allow_redirects=False, timeout=30)
    print(f"\n=== {label} ===")
    print("login status:", r.status_code, "->", r.headers.get("location"))

    # fetch reservations list page
    r2 = s.get(base + "/admin/reservations", timeout=30)
    print("reservations page status:", r2.status_code, "len:", len(r2.text))

    # count table rows referencing RES- references
    txt = r2.text
    n_res = txt.count("RES-")
    n_grp = txt.count("GRP-")
    print("occurrences 'RES-':", n_res, "| 'GRP-':", n_grp)

    # look for the known reservation from the altaria DB
    print("contains 'Zahiri':", "Zahiri" in txt)
    print("contains 'RES-05TNYLBL':", "RES-05TNYLBL" in txt)
