import string
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import names
from unidecode import unidecode

print("Loading proxies from file...")
with open("http_proxies.txt") as f:
    proxies = f.readlines()


proxies = [x.strip() for x in proxies]
num = 0
while True:
    print("Selecting a random proxy number...")
    proxy = random.choice(proxies)

    print(f"Checking proxy {proxy}")
    try:
        response = requests.get("https://obchod-vsb.cz/", proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code != 200:
            raise Exception("Invalid response code from server")
    except:
        continue

    print(f"Setting up web driver with proxy {proxy}...")
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % proxy)
    options.add_argument('--ignore-ssl-errors=yes')

    try:
        num = num+1
        driver = webdriver.Chrome(options=options)
        print('Executing login sequence number', num)
        time.sleep(4)
        print("Navigating to website and logging in...")
        driver.get("https://obchod-vsb.cz/")

        wait = WebDriverWait(driver, 15)

        print("Generating username...")
        time.sleep(1)
        def generate_last_name():
            vowels = "aeiouy"
            consonants1 = "bcdfghjklmnprstz"
            consonants = "bcdfghjklmnprstvz"
            return random.choice(consonants1) + random.choice(vowels) + random.choice(consonants)


        def generate_username():
            last_name = generate_last_name()

            first_three_letters = last_name[:3].upper() if random.random() < 0.25 else last_name[:3].lower()

            rand_num = random.randint(1, 100)

            if rand_num <= 50:
                num = random.randint(26, 149)
            elif rand_num <= 75:
                num = random.randint(150, 200)
            elif rand_num <= 90:
                num = random.randint(201, 399)
            else:
                num = random.randint(400, 499)

            num_str = "{:04d}".format(num)

            username = first_three_letters + num_str

            return username


        username = generate_username()

        import random
        import string

        print("Generating password...")
        time.sleep(1)
        def generate_password():
            with open('/usr/share/dict/words', 'r') as f:
                words = [word.strip() for word in f.readlines()]
            random.shuffle(words)
            num_words = random.randint(3, 5)
            phrase = " ".join(words[:num_words])
            password = "".join(word[0] for word in phrase.split())
            password = password.replace("o", "0")
            password = password.replace("s", "$")
            password = password.lower()
            password = list(password)
            length = len(password)
            uppercase_chance = 0.5
            if random.random() < uppercase_chance:
                num_uppercase = max(1, int(length * 0.25))
                uppercase_indices = random.sample(range(length), num_uppercase)
                for i in uppercase_indices:
                    password[i] = password[i].upper()
            password.insert(random.randint(0, length), str(random.randint(0, 9)))
            if random.random() < 0.2:
                password.insert(random.randint(0, length), '-')
            length = random.randint(7, 11)
            if len(password) > length:
                password = password[:length]
            else:
                password += "".join(
                    random.choice(string.ascii_letters + string.digits) for i in range(length - len(password)))
            return "".join(c for c in password if c.isalnum())

        password = generate_password()

        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#username")))
        username_input.send_keys(username)
        username_input.send_keys(Keys.RETURN)
        password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#password")))
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        print("Login successful, exiting web driver...")
        time.sleep(2)
        driver.quit()

    except Exception as e:
        print(f"An error occurred: {e}")
        continue

    if len(proxies) == 0:
        print("All proxies used, reloading list...")
        with open("http_proxies.txt") as f:
            proxies = f.readlines()
        proxies = [x.strip() for x in proxies]
