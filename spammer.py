import time
import itertools
from discord_webhook import DiscordWebhook
import os

from colorama import Style, init

init(autoreset=True) 

def generate_gradient_color(start_rgb, end_rgb, step, total_steps):
    denominator = max(1, total_steps)
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (step / denominator))
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (step / denominator))
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (step / denominator))
    return (r, g, b)

def print_gradient_text(text, start_rgb, end_rgb):
    clean_text = text.replace('\n', '')
    total_steps = len(clean_text)
    output = []
    i_clean = 0
    
    for char in text:
        if char == '\n':
            output.append(char)
            continue
        if char.strip() == "":
            output.append(char)
            continue

        r, g, b = generate_gradient_color(start_rgb, end_rgb, i_clean, total_steps)
        ansi_color_code = f"\033[38;2;{r};{g};{b}m"
        output.append(ansi_color_code + Style.BRIGHT + char)
        i_clean += 1
    
    print("".join(output) + Style.RESET_ALL) 
    print()

ASCII_ART = """
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓█████████████▓▒░░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
                                                                                               
"""

start_color = (255, 0, 0)
end_color = (0, 0, 255)

WEBHOOK_URL = 'link' 

delay = 0.05
monitordelay = 3.0
namestxt = 'names.txt'

used_names = set() 

def getname(filename, sent_names_set):
    if not os.path.exists(filename):
        return []
    new_names = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            name = line.strip()
            if name and name not in sent_names_set:
                new_names.append(name)
                sent_names_set.add(name)
    return new_names

def send_message_with_name(username):
    content = f"test"
    
    webhook = DiscordWebhook(
        url=WEBHOOK_URL, 
        content=content,
        username=username
    )
    
    try:
        webhook.execute(remove_embeds=True)
    except Exception as e:
        pass

print_gradient_text(ASCII_ART, start_color, end_color)

try:
    while True:
        new_usernames = getname(namestxt, used_names)
        
        if new_usernames:
            for name in new_usernames:
                send_message_with_name(name)
                time.sleep(delay)

        time.sleep(monitordelay)

except KeyboardInterrupt:
    print("stopped")
except Exception as e:
    exit(0)
