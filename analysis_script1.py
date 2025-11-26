import csv #Used to read CSV files (My Autopsy exports) and convert into dictionaries
import json #Used only to format the print statements to make them look nice
import glob #USed to check if hive files like sam, software, system exist by matching file names

# Helper: load first CSV that matches a pattern

def load_first_csv(pattern):
    matches = glob.glob(pattern)
    if not matches:
        print(f"File not found for pattern: {pattern}")
        return []
    path = matches[0]
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def section(title, data):
    print()
    print(f"--- {title} ---")
    print(json.dumps(data, indent=4))
    print()

#1. Installed applications (from Installed Programs CSV)

apps = load_first_csv("Installed Programs*.csv")

#2. User accounts (from OS Accounts CSV)

os_accounts = load_first_csv("Results*.csv")
usernames = []

if os_accounts:
    #Try to detect the "Login Name" column automatically
    first_row = os_accounts[0]
    keys = list(first_row.keys())
    login_keys = [k for k in keys if "login" in k.lower() and "name" in k.lower()]
    name_field = login_keys[0] if login_keys else keys[0]

    for row in os_accounts:
        name = row.get(name_field, "").strip()
        if name:
            usernames.append(name)

user_info = {
    "usernames": usernames,
    "user_count": len(usernames),
}

#3. Registry info – presence of SAM / SOFTWARE / SYSTEM hives

sam_info = {"SAM Hive Loaded": bool(glob.glob("SAM"))}
software_info = {"SOFTWARE Hive Loaded": bool(glob.glob("SOFTWARE"))}
system_info = {"SYSTEM Hive Loaded": bool(glob.glob("SYSTEM"))}

#4. USB history (from USB Device Attached CSV)

usb_history = load_first_csv("USB Device Attached*.csv")

#5. Command history / running programs history

run_programs = load_first_csv("Run Programs*.csv")

#OUTPUT

section("Installed applications (first 10)", apps[:10])
section("User accounts", user_info)
section("Registry info SAM hive", sam_info)
section("Registry info SOFTWARE hive", software_info)
section("Registry info SYSTEM hive", system_info)
section("USB history", usb_history)
section("Command / run history (first 10 entries)", run_programs[:10])
