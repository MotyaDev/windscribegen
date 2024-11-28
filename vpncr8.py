import random
import string
import requests
import os
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Function to generate a random username
def generate_username():
    username_length = random.randint(8, 12)  # Username length between 8 and 12 characters
    return ''.join(random.choices(string.ascii_letters + string.digits, k=username_length))

# Function to generate a random password
def generate_password():
    password_length = random.randint(7, 15)  # Password length between 7 and 15 characters
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=password_length))

# Generate credentials
username = generate_username()
password = generate_password()

# Print generated credentials with colors
print(f"{Fore.GREEN}Generated Username: {Fore.CYAN}{username}")
print(f"{Fore.GREEN}Generated Password: {Fore.CYAN}{password}")

# Target URL for signup
signup_url = "https://windscribe.com/signup"

# Prepare initial payload
payload = {
    "signup": "1",
    "username": username,
    "password": password,
    "password2": password,  # Confirm password
    "email": "",
    "voucher_code": "",
    "captcha": "",
    "robert_status": "0",
    "unlimited_plan": "0"
}

# Headers
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en;q=0.5",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "_pk_id.3.2e1e=996db2ffaea89280.1732726027.2.1732748765.1732748203.; cpid=app_windows; i_can_has_cookie=1; pcpid=website_post_signup; ref=https%3A%2F%2Fwindscribe.com%2Fsignup%3Fcpid%3Dapp_windows; _pk_id.5.2e1e=167a6e953e021a09.1732726384.1.1732726384.1732726384.; PHPSESSID=daf26423df48fcae85a6cd39fed904aa; _pk_ses.3.2e1e=*",
    "DNT": "1",
    "Host": "windscribe.com",
    "Origin": "https://windscribe.com",
    "Priority": "u=0",
    "Referer": "https://windscribe.com/signup",
    "sec-ch-ua": '"Google Chrome";v="112", "Chromium";v="112", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "TE": "trailers",
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-A037U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 uacq"
}

try:
    # Step 1: Send the initial POST request
    response = requests.post(signup_url, data=payload, headers=headers)
    print(f"Response Status Code: {response.status_code}")
    response_data = response.json()  # Parse JSON response

    # Check if captcha is required
    if response_data.get("errorCode") == 909:
        captcha_url = f"https://windscribe.com{response_data['captcha']}"
        print(f"Captcha URL: {captcha_url}")

        # Step 2: Fetch and save the captcha image
        captcha_response = requests.get(captcha_url, headers=headers)
        if captcha_response.status_code == 200:
            # Save the captcha image in the working directory
            working_directory = os.getcwd()
            captcha_image_path = os.path.join(working_directory, "captcha_image.png")
            with open(captcha_image_path, "wb") as f:
                f.write(captcha_response.content)
            print(f"Captcha image saved as '{captcha_image_path}'.")

            # Step 3: Prompt the user to solve the captcha
            captcha_solution = input("Please view the 'captcha_image.png' and enter the captcha: ")

            # Step 4: Resend the POST request with the solved captcha
            payload["captcha"] = captcha_solution
            final_response = requests.post(signup_url, data=payload, headers=headers)
            print(f"Final Response Status Code: {final_response.status_code}")
            print(f"Final Response Content: {final_response.text}")
        else:
            print("Failed to fetch the captcha image.")
    else:
        print("Captcha not required or unexpected response.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
