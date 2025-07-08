import pandas as pd
import requests
import random
import string
from tqdm import tqdm

# === CONFIGURATION ===
EXCEL_FILE = "users.xlsx"
OUTPUT_FILE = "created_users.csv"
API_URL = "<humhub_api_url>"
BEARER_TOKEN = "<token>"  # https://marketplace.humhub.com/module/rest/manual


def generate_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choices(chars, k=length))


def generate_username(first, last, index):
    base = f"{first}.{last}".lower().replace(" ", "").replace("'", "")
    return base if base else f"user{index}"


headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
}

df = pd.read_excel(EXCEL_FILE)
results = []


for idx, row in tqdm(df.iterrows(), total=len(df), desc="Creating users"):
    first = str(row.get("First Name [Required]", "")).strip()
    last = str(row.get("Last Name [Required]", "")).strip()
    email = str(row.get("Email Address [Required]", "")).strip()
    phone = str(row.get("Recovery Phone [MUST BE IN THE E.164 FORMAT]", "")).strip()

    if not (first and last and email):
        results.append(
            {
                "username": "",
                "email": email,
                "firstname": first,
                "lastname": last,
                "generated_password": "",
                "mobile": phone,
                "status": "FAIL",
                "error": "Missing required fields",
            }
        )
        continue

    password = generate_password()
    username = generate_username(first, last, idx)

    payload = {
        "account": {
            "username": username,
            "email": email,
            "visibility": 1,
            "status": 1,
            "tagsField": [],
            "language": "ru",
            "authclient": "local",
            "authclient_id": None,
        },
        "profile": {
            "firstname": first,
            "lastname": last,
            "title": "",
            "gender": "",
            "street": "",
            "zip": None,
            "city": "",
            "country": None,
            "state": None,
            "birthday_hide_year": 0,
            "birthday": "1990-01-01",
            "about": None,
            "phone_private": None,
            "phone_work": None,
            "mobile": phone if phone else None,
            "fax": None,
            "im_skype": None,
            "im_xmpp": None,
            "url": None,
            "url_facebook": None,
            "url_linkedin": None,
            "url_xing": None,
            "url_youtube": None,
            "url_vimeo": None,
            "url_flickr": None,
            "url_myspace": None,
            "url_twitter": None,
            "image_url": None,
            "banner_url": None,
            "image": "https://teamspace.narxoz.kz/static/img/default_user.jpg",
            "banner": "https://teamspace.narxoz.kz/static/img/default_banner.jpg",
        },
        "password": {"newPassword": password, "mustChangePassword": True},
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        if res.status_code == 200:
            results.append(
                {
                    "username": username,
                    "email": email,
                    "firstname": first,
                    "lastname": last,
                    "generated_password": password,
                    "mobile": phone,
                    "status": "OK",
                    "error": "",
                }
            )
        else:
            results.append(
                {
                    "username": username,
                    "email": email,
                    "firstname": first,
                    "lastname": last,
                    "generated_password": password,
                    "mobile": phone,
                    "status": "FAIL",
                    "error": res.text,
                }
            )
    except Exception as e:
        results.append(
            {
                "username": username,
                "email": email,
                "firstname": first,
                "lastname": last,
                "generated_password": password,
                "mobile": phone,
                "status": "FAIL",
                "error": str(e),
            }
        )

df_result = pd.DataFrame(results)
df_result.to_csv(OUTPUT_FILE, index=False)
