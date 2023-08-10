import requests

BASE_URL = "http://localhost:5000"
HEADERS = {
    "Content-Type": "application/json"
}
TOKEN = None

def login(username, password):
    global TOKEN
    response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    if response.status_code == 200:
        TOKEN = response.json().get('access_token')
        print(f"Logged in successfully! Token: {TOKEN}")
    else:
        print(f"Failed to login. Status code: {response.status_code}, Message: {response.text}")

def get_jobs():
    if not TOKEN:
        print("You must login first.")
        return

    headers = {**HEADERS, "Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{BASE_URL}/jobs/", headers=headers)
    print(response.json())

def insert_data(table_name, data):
    if not TOKEN:
        print("You must login first.")
        return

    headers = {**HEADERS, "Authorization": f"Bearer {TOKEN}"}
    response = requests.post(f"{BASE_URL}/insert/{table_name}", headers=headers, json={"data": data})
    print(response.json())

def backup():
    if not TOKEN:
        print("You must login first.")
        return

    headers = {**HEADERS, "Authorization": f"Bearer {TOKEN}"}
    response = requests.post(f"{BASE_URL}/backup", headers=headers)
    print(response.json())

def restore():
    if not TOKEN:
        print("You must login first.")
        return

    headers = {**HEADERS, "Authorization": f"Bearer {TOKEN}"}
    response = requests.post(f"{BASE_URL}/restore", headers=headers)
    print(response.json())

if __name__ == "__main__":
    # Ejemplo de uso:
    login("admin", "1016082760")
    get_jobs()
    # insert_data('hired_employees', [{"name": "John", ...}])
    # backup()
    # restore()
