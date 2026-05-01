import requests

url = "https://uselessfacts.jsph.pl/api/v2/facts/category/Science?language=en"

def get_random_history_fact():
    response = requests.get(url)
    if response.status_code == 200:
        fact_data = response.json()
        print(f"Did you know? {fact_data['text']}")
        
    else:
        print("Failed to fetch a random history fact.")

while True:
    user_input = input("Press Enter to get a random science fact or 'q' to exit: ").strip().lower()
    if user_input == 'q':
        break
    get_random_history_fact()        