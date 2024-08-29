#import requirement libraries
import os
import wget

import json
import string
import pandas as pd

import time
import jdatetime
import pycountry_convert as pc
from datetime import datetime, timezone, timedelta

#import web-based libraries
import html
import socket
import requests
import ipaddress
import geoip2.database
from bs4 import BeautifulSoup
from dns import resolver, rdatatype

#import regex and encoding libraries
import re


# Create the geoip-lite folder if it doesn't exist
if not os.path.exists('./geoip-lite'):
    os.mkdir('./geoip-lite')

if os.path.exists('./geoip-lite/geoip-lite-country.mmdb'):
    os.remove('./geoip-lite/geoip-lite-country.mmdb')

# Download the file and rename it
url = 'https://git.io/GeoLite2-Country.mmdb'
filename = 'geoip-lite-country.mmdb'
wget.download(url, filename)

# Move the file to the geoip folder
os.rename(filename, os.path.join('./geoip-lite', filename))


# Load and read last date and time update
with open('./last update', 'r') as file:
    last_update_datetime = file.readline()
    last_update_datetime = datetime.strptime(last_update_datetime, '%Y-%m-%d %H:%M:%S.%f%z')

# Write the current date and time update
with open('./last update', 'w') as file:
    current_datetime_update = datetime.now(tz = timezone(timedelta(hours = 3, minutes = 30)))
    file.write(f'{current_datetime_update}')

print(f"Latest Update: {last_update_datetime.strftime('%a, %d %b %Y %X %Z')}\nCurrent Update: {current_datetime_update.strftime('%a, %d %b %Y %X %Z')}")


def json_load(path):
    # Open and read the json file
    with open(path, 'r') as file:
        # Load json file content into list
        list_content = json.load(file)
    # Return list of json content
    return list_content


def tg_channel_messages(channel_user):
    try:
        # Retrieve channels messages
        response = requests.get(f"https://t.me/s/{channel_user}")
        soup = BeautifulSoup(response.text, "html.parser")
        # Find all telegram widget messages
        div_messages = soup.find_all("div", class_="tgme_widget_message")
        # Return list of all messages in channel
        return div_messages
    except:
        pass


def find_matches(text_content):
    # Initialize configuration type patterns
    pattern_telegram_user = r'(?:@)(\w{4,})'
    pattern_proxy = r'"(.*?)/proxy?(.*?)"'
    pattern_url = r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))'

    # Find all matches of patterns in text
    matches_usersname = re.findall(pattern_telegram_user, text_content)
    matches_proxy = re.findall(pattern_proxy, text_content)
    matches_url = re.findall(pattern_url, text_content)

    proxies_list = list()
    # Iterate over matches to subtract titles
    for tg_url_class, proxy in matches_proxy:
        proxies_list.append(proxy)

    return matches_usersname, matches_url, proxies_list


def tg_message_time(div_message):
    # Retrieve channel message info
    div_message_info = div_message.find('div', class_='tgme_widget_message_info')
    # Retrieve channel message datetime
    message_datetime_tag = div_message_info.find('time')
    message_datetime = message_datetime_tag.get('datetime')

    # Change message datetime type into object and convert into Iran datetime
    datetime_object = datetime.fromisoformat(message_datetime)
    datetime_object = datetime.astimezone(datetime_object, tz = timezone(timedelta(hours = 3, minutes = 30)))

    # Retrieve now datetime based on Iran timezone
    datetime_now = datetime.now(tz = timezone(timedelta(hours = 3, minutes = 30)))

    # Return datetime object, current datetime based on Iran datetime and delta datetime
    return datetime_object, datetime_now, datetime_now - datetime_object


def tg_message_text(div_message):
    try:
        # Retrieve message text class from telegram messages widget
        div_message_text = div_message.find("div", class_="tgme_widget_message_text")
        div_message_inline_keyboard = div_message.find("div", class_="tgme_widget_message_inline_keyboard")

        text_content = div_message_text.prettify()
        text_inline_keyboard = div_message_inline_keyboard.prettify()

        div_message_text = re.sub(r"amp;amp;", r"", re.sub(r"amp;", r"",re.sub(r" ", "", text_content),),)
        div_message_inline_keyboard = re.sub(r"amp;amp;", r"", re.sub(r"amp;", r"",re.sub(r" ", "", text_inline_keyboard),),)

        div_message_text = ''.join([div_message_text, div_message_inline_keyboard])
        # Return text content
        return div_message_text
    except:
        # Retrieve message text class from telegram messages widget
        div_message_text = div_message.find("div", class_="tgme_widget_message_text")
        text_content = div_message_text.prettify()
        div_message_text = re.sub(r"amp;amp;", r"", re.sub(r"amp;", r"",re.sub(r" ", "", text_content),),)

        # Return text content
        return div_message_text


# Load telegram channels usernames
telegram_channels = json_load('./telegram channels.json')

# Initial channels messages array
channel_messages_array = list()
removed_channel_array = list()
channel_check_messages_array = list()

# Iterate over all public telegram chanels and store twenty latest messages
for channel_user in telegram_channels:
    try:
        print(f'{channel_user}')
        # Iterate over Telegram channels to Retrieve channel messages and extend to array
        div_messages = tg_channel_messages(channel_user)
        
        # Append destroyed Telegram channels
        if len(div_messages) == 0:
            removed_channel_array.append(channel_user)
        # Check configuation Telegram channels
        channel_check_messages_array.append((channel_user, div_messages))
        
        for div_message in div_messages:
            datetime_object, datetime_now, delta_datetime_now = tg_message_time(div_message)
            if datetime_object > last_update_datetime:
                print(f"\t{datetime_object.strftime('%a, %d %b %Y %X %Z')}")
                channel_messages_array.append((channel_user, div_message))
    except:
        continue

# Messages Counter
print(f"\nTotal New Messages From {last_update_datetime.strftime('%a, %d %b %Y %X %Z')} To {current_datetime_update.strftime('%a, %d %b %Y %X %Z')} : {len(channel_messages_array)}\n")


# Initial arrays for proxies
array_usernames = list()
array_url = list()
array_proxies = list()

for channel_user, message in channel_messages_array:
    try:
        # Iterate over channel messages to extract text content
        text_content = tg_message_text(message)
        # Iterate over each message to extract proxies
        matches_usersname, matches_url, matches_proxies = find_matches(text_content)

        # Extend proxies into array
        array_usernames.extend([element.lower() for element in matches_usersname if len(element) >= 5])
        array_proxies.extend(matches_proxies)
        array_url.extend(matches_url)
    except:
        continue


# Initialize Telegram channels list without configuration
channel_without_config = set()

for channel_user, messages in channel_check_messages_array:
    # Initialize Channel Configs Counter
    total_config = 0

    for message in messages:
        try:
            # Iterate over channel messages to extract text content
            text_content = tg_message_text(message)
            # Iterate over each message to extract proxies
            matches_usersname, matches_url, matches_proxies = find_matches(text_content)
            total_config = total_config + len(matches_proxies)

        except Exception as exc:
            continue

    if total_config == 0:
        channel_without_config.add(channel_user)
        

def tg_username_extract(url):
    telegram_pattern = r'((http|Http|HTTP)://|(https|Https|HTTPS)://|(www|Www|WWW)\.|https://www\.|)(?P<telegram_domain>(t|T)\.(me|Me|ME)|(telegram|Telegram|TELEGRAM)\.(me|Me|ME)|(telegram|Telegram|TELEGRAM).(org|Org|ORG)|telesco.pe|(tg|Tg|TG).(dev|Dev|DEV)|(telegram|Telegram|TELEGRAM).(dog|Dog|DOG))/(?P<username>[a-zA-Z0-9_+-]+)'
    matches_url = re.match(telegram_pattern, url)
    return matches_url.group('username')


# Split Telegram usernames and subscription url links
tg_username_list = set()
proxy_list = set()
url_subscription_links = set()

for url in array_url:
    try:
        tg_user = tg_username_extract(url)
        if tg_user not in ['proxy', 'img', 'emoji', 'joinchat'] and '+' not in tg_user and '-' not in tg_user and len(tg_user)>=5:
            tg_user = ''.join([element for element in list(tg_user) if element in string.ascii_letters + string.digits + '_'])
            tg_username_list.add(tg_user.lower())
        if tg_user == 'proxy':
            proxy_list.add(url.split("\"")[0])
    except:
        url_subscription_links.add(url.split("\"")[0])
        continue

for index, tg_user in enumerate(array_usernames):
    tg_user = ''.join([element for element in list(tg_user) if element in string.ascii_letters + string.digits + '_'])
    array_usernames[index] = tg_user


url = 'https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/telegram channels.json'
filename = 'telegram configs channel.json'
wget.download(url, filename)

tg_username_list.update(array_usernames)
telegram_configs_channel = json_load('./telegram configs channel.json')
tg_username_list.update(telegram_configs_channel)
os.remove('./telegram configs channel.json')


# Subtract and get new telegram channels
new_telegram_channels = tg_username_list.difference(telegram_channels)

# Initial channels messages array
new_channel_messages = list()
invalid_array_channels = json_load('invalid telegram channels.json')
invalid_array_channels = set(invalid_array_channels)

# Iterate over all public telegram chanels and store twenty latest messages
for channel_user in new_telegram_channels:
    if channel_user not in invalid_array_channels:
        try:
            print(f'{channel_user}')
            # Iterate over Telegram channels to Retrieve channel messages and extend to array
            div_messages = tg_channel_messages(channel_user)
            channel_messages = list()
            for div_message in div_messages:
                datetime_object, datetime_now, delta_datetime_now = tg_message_time(div_message)
                #print(f"\t{datetime_object.strftime('%a, %d %b %Y %X %Z')}")
                channel_messages.append(div_message)
            new_channel_messages.append((channel_user, channel_messages))
        except:
            continue
    else:
        continue

# Messages Counter
print(f"\nTotal New Messages From New Channels {last_update_datetime.strftime('%a, %d %b %Y %X %Z')} To {current_datetime_update.strftime('%a, %d %b %Y %X %Z')} : {len(new_channel_messages)}\n")


# Initial arrays for protocols
new_array_proxies = list()

# Initialize array for channelswith configuration contents
new_array_channels = set()

for channel, messages in new_channel_messages:
    # Set Iterator to estimate each channel configurations
    total_config = 0
    new_array_url = set()
    new_array_usernames = set()

    for message in messages:
        try:
            # Iterate over channel messages to extract text content
            text_content = tg_message_text(message)
            # Iterate over each message to extract configuration protocol types and subscription links
            matches_username, matches_url, matches_proxy = find_matches(text_content)
            total_config = total_config + len(matches_proxy)

            # Extend protocol type arrays and subscription link array
            new_array_usernames.update([element.lower() for element in matches_username if len(element) >= 5])
            new_array_url.update(matches_url)
            new_array_proxies.extend(matches_proxy)

        except Exception as exc:
            continue
            
    # Append to channels that conatins configurations
    if total_config != 0:
        new_array_channels.add(channel)
    else:
        invalid_array_channels.add(channel)

    # Split Telegram usernames and subscription url links
    tg_username_list_new = set()

    for url in new_array_url:
        try:
            tg_user = tg_username_extract(url)
            if tg_user not in ['proxy', 'img', 'emoji', 'joinchat'] and '+' not in tg_user and '-' not in tg_user and len(tg_user)>=5:
                tg_user = ''.join([element for element in list(tg_user) if element in string.ascii_letters + string.digits + '_'])
                tg_username_list_new.add(tg_user.lower())
            if tg_user == 'proxy':
                proxy_list.add(url.split("\"")[0])
        except:
            url_subscription_links.add(url.split("\"")[0])
            continue

    new_array_usernames = list(new_array_usernames)
    for index, tg_user in enumerate(new_array_usernames):
        tg_user = ''.join([element for element in list(tg_user) if element in string.ascii_letters + string.digits + '_'])
        new_array_usernames[index] = tg_user

    # Subtract and get new telegram channels
    tg_username_list_new.update([element.lower() for element in new_array_usernames])
    tg_username_list_new = tg_username_list_new.difference(telegram_channels)
    tg_username_list_new = tg_username_list_new.difference(new_telegram_channels)
    updated_new_channel = set(list(map(lambda element : element[0], new_channel_messages)))
    tg_username_list_new = tg_username_list_new.difference(updated_new_channel)

    # Iterate over all public telegram chanels and store twenty latest messages
    for channel_user in tg_username_list_new:
        try:
            print(f'{channel_user}')
            # Iterate over Telegram channels to Retrieve channel messages and extend to array
            div_messages = tg_channel_messages(channel_user)
            channel_messages = list()
            for div_message in div_messages:
                datetime_object, datetime_now, delta_datetime_now = tg_message_time(div_message)
                print(f"\t{datetime_object.strftime('%a, %d %b %Y %X %Z')}")
                channel_messages.append(div_message)
            # new_channel_messages.append((channel_user, channel_messages))
        except:
            continue


print("New Telegram Channels Found")
for channel in new_array_channels:
    print('\t{value}'.format(value = channel))

print("Destroyed Telegram Channels Found")
for channel in removed_channel_array:
    print('\t{value}'.format(value = channel))

print("No Config Telegram Channels Found")
for channel in channel_without_config:
    print('\t{value}'.format(value = channel))

    
# Extend new channels into previous channels
telegram_channels.extend(new_array_channels)
telegram_channels = [channel for channel in telegram_channels if channel not in removed_channel_array and channel not in channel_without_config]
telegram_channels = [channel for channel in telegram_channels if channel not in removed_channel_array]
telegram_channels = list(set(telegram_channels))
telegram_channels = list(map(lambda var : var.lower(), telegram_channels))
telegram_channels = sorted(telegram_channels)

invalid_telegram_channels = list(set(invalid_array_channels))
invalid_telegram_channels = sorted(invalid_telegram_channels)


with open('./telegram channels.json', 'w') as telegram_channels_file:
    json.dump(telegram_channels, telegram_channels_file, indent = 4)

with open('./invalid telegram channels.json', 'w') as invalid_telegram_channels_file:
    json.dump(invalid_telegram_channels, invalid_telegram_channels_file, indent = 4)


def html_content(html_address):
    # Retrieve subscription link content
    response = requests.get(html_address, timeout = 5)
    soup = BeautifulSoup(response.text, 'html.parser').text
    return soup


# Load subscription links
subscription_links = json_load('./subscription links.json')

# Initial links contents array decoded content array
array_links_content = list()
array_contents = list()

for url_link in subscription_links:
    try:
        # Retrieve subscription link content
        links_content = html_content(url_link)
        array_links_content.append(links_content)
    except:
        continue

array_links_content.extend(list(proxy_list))

for content in array_links_content:
    try:
        # Split each link contents into array and split by lines
        link_contents = content.splitlines()
        link_contents = [f'"{element}"' for element in link_contents if element not in ['\n','\t','']]
        array_contents.extend(link_contents)
    except:
        continue

# Merge all subscription links content and find all protocols matches base on protocol pattern
content_merged = "\n".join(array_contents)
array_contents = find_matches(content_merged)[2]


# Extend and merge all proxies array
array_proxies.extend(array_contents)
array_proxies.extend(new_array_proxies)

# Remove duplicate proxies and sort
array_proxies = list(set(array_proxies))
array_proxies = sorted(array_proxies)


def proxy_params(proxy):
    # Define pattern for proxy
    pattern = r'(.*?)\?server=(?P<server>[^&]*?)(&|&&)port=(?P<port>[0-9]*?)(&|&&)secret=(?P<secret>[^%#@&()]*)'
    # Find all matches of pattern in proxy string
    matches = re.match(pattern, proxy)

    server = matches.group('server')
    port = matches.group('port')
    port = int(port)
    secret = matches.group('secret')

    return server, port, secret


def is_valid_ip_address(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_ipv6(ip):
    try:
        ipaddress.ip_address(ip)
        if ":" in ip:
            return True
        else:
            return False
    except ValueError:
        return False


def get_ips(node):
    try:
        res = resolver.Resolver()
        res.nameservers = ["8.8.8.8"]

        # Retrieve IPV4 and IPV6
        answers_ipv4 = res.resolve(node, rdatatype.A, raise_on_no_answer=False)
        answers_ipv6 = res.resolve(node, rdatatype.AAAA, raise_on_no_answer=False)

        # Initialize set for IPV4 and IPV6
        ips = set()

        # Append IPV4 and IPV6 into set
        for rdata in answers_ipv4:
            ips.add(rdata.address)

        for rdata in answers_ipv6:
            ips.add(rdata.address)

        return ips
    except Exception:
        return None


def get_country_from_ip(ip):
    try:
        with geoip2.database.Reader("./geoip-lite/geoip-lite-country.mmdb") as reader:
            response = reader.country(ip)
            country_code = response.country.iso_code
        if not country_code is None:
            return country_code
        else:
            # If country code is NoneType, Returns 'NA'
            return "NA"
    except:
        return "NA"


def get_country_flag(country_code):
    if country_code == 'NA':
        return html.unescape("\U0001F3F4\u200D\u2620\uFE0F")

    base = 127397  # Base value for regional indicator symbol letters
    codepoints = [ord(c) + base for c in country_code.upper()]
    return html.unescape("".join(["&#x{:X};".format(c) for c in codepoints]))


def check_port(ip, port, timeout=1):
    """
    Check if a port is open on a given IP address.

    Args:
    ip (str): The IP address.
    port (int): The port number.
    timeout (int, optional): The timeout in seconds. Defaults to 5.

    Returns:
    bool: True if the port is open, False otherwise.
    """
    try:
        sock = socket.create_connection((ip, port), timeout)
        sock.close()
        print("CONNECTION PORT: OPEN")
        return True
    except:
        print("CONNECTION PORT: CLOSED\n")
        return False


def ping_ip_address(ip, port):
    try:
        it = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        ft = time.time()
        sock.close()
        if result == 0:
            return round((ft - it) * 1000, 2)
        else:
            return round(0, 2)
    except:
        return round(0, 2)


# Initialize an array for modified proxies
modified_proxies = list()
duplicate_proxies = list()

ipv6_proxies = list()
ipv4_proxies = list()

# Iterate over proxies array to check out connectivity and modify server address into IP address
for proxy in array_proxies:
    try:
        # Try out to get matches from proxy string
        server, port, secret = proxy_params(proxy)

        # Remove invalid proxies with wrong secret code
        if any([invalid_char_secret in secret for invalid_char_secret in [":","/","\\"]]):
            continue

        ips_list = {server}
        # Try out to retrieve IP adress of server
        if not is_valid_ip_address(server):
            ips_list = get_ips(server)

        if ips_list is None:
            continue

        for ip_address in ips_list:
            # Print out Original Proxy without any modification
            print(f'ORIGINAL PROXY: https://t.me/proxy?server={server}&port={port}&secret={secret}')

            # Ignore proxies with Dns address
            if ip_address in ['1.1.1.1', '1.0.0.1', '8.8.8.8', '8.8.4.4']:
                print('IP ADDRESS: DNS SERVER\n')
                continue

            # Ignore if IP address is version 6
            if is_ipv6(ip_address):
                print('IP ADDRESS: IPV6\n')
                

            server_port_secret = (ip_address, port, secret)
            # Ignore duplicate proxy
            if server_port_secret in duplicate_proxies:
                print('DUPLICATE PROXY\n')
                continue

            # Ignore if IP address is version 6
            # if is_ipv6(ip_address):
            #    print('IP ADDRESS: IPV6\n')
            #    continue
                
            # Append unique proxy into collected duplicate proxies
            duplicate_proxies.append(server_port_secret)

            # Try out to check out server conectivity
            if not is_ipv6(ip_address):
                if not check_port(ip_address, int(port)):
                    continue
                    
            # Retrieve proxy ping of the server
            if not is_ipv6(ip_address):
                proxy_ping = ping_ip_address(ip_address, int(port))
            else:
                proxy_ping = round(0, 2)

            # Retrieve country code and flag based on IP address
            country_code = get_country_from_ip(ip_address)
            country_name = pc.country_alpha2_to_country_name(country_code).upper() if country_code != 'NA' else 'NOT AVAILABLE'
            country_flag = get_country_flag(country_code)

            # Print out modified proxy and append it into modified proxies array
            modified_proxy = f"tg://proxy?server={ip_address}&port={port}&secret={secret}"
            print(f"MODIFIED PROXY: https://t.me/proxy?server={ip_address}&port={port}&secret={secret}\n")

            modified_proxy = (country_flag, country_name, country_code, ip_address, port, proxy_ping, modified_proxy)
            modified_proxies.append(modified_proxy)

            if is_ipv6(ip_address):
                ipv6_proxies.append(modified_proxy[6])
                print('IP ADDRESS: IPV6\n')
            else:
                ipv4_proxies.append(modified_proxy[6])
                print('IP ADDRESS: IPV4\n')

    except:
        continue


# Sort Proxies Based On Country, IP Address,Port And Ping
modified_proxies = sorted(modified_proxies, key = lambda element: (element[1], element[2], element[3], element[4]))


# create country dictionary
def create_country_dict(modified_proxy_list):
    country_dict = dict()

    for index, value in enumerate(modified_proxy_list):
        country_code = value[2].lower()
        country_name = value[1]
        modified_proxy = value[6]

        if country_code in country_dict.keys():
            country_dict[country_code].append(modified_proxy)
        elif country_code not in country_dict.keys():
            country_dict[country_code] = list()
            country_dict[country_code].append(modified_proxy)
    
    return country_dict

# Generate dictionary od countries
country_based_proxies_dict = create_country_dict(modified_proxies)


# Define update date and time based on Iran timezone and calendar
datetime_update = jdatetime.datetime.now(tz = timezone(timedelta(hours = 3, minutes = 30)))
datetime_update_str = datetime_update.strftime("LATEST UPDATE: %a-%d-%B-%Y %H:%M %Z").upper()


for country in country_based_proxies_dict.keys():
    if not os.path.exists('./countries'):
        os.mkdir('./countries')
    if not os.path.exists(f'./countries/{country}'):
        os.mkdir(f'./countries/{country}')
    with open(f'./countries/{country}/proxies', "w") as file:
        file.write(f"{datetime_update_str}\n\n")
    with open(f'./countries/{country}/proxies', "a") as file:
        file.write("\n".join(country_based_proxies_dict[country]))

# create ip version 4 & 6 directories
with open(f'./layers/ipv4', "w") as file:
    file.write(f"{datetime_update_str}\n\n")
with open(f'./layers/ipv4', "a") as file:
    file.write("\n".join(ipv4_proxies))
with open(f'./layers/ipv6', "w") as file:
    file.write(f"{datetime_update_str}\n\n")
with open(f'./layers/ipv6', "a") as file:
    file.write("\n".join(ipv6_proxies))


def create_country_table(country_path):
    # Retrive Country List
    country_code_list = os.listdir(country_path)

    # Counvert country code into country name
    country_url_pattern = '[Subscription Link](https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/{country_code}/proxies)'
    country_code_name_url = sorted(list(map(lambda element : (element.upper(), pc.country_alpha2_to_country_name(element.upper()) if element.upper() != 'NA' else 'Not Available', country_url_pattern.format(country_code = element)), country_code_list)), key = lambda element : element[1])

    for index, element in enumerate(country_code_name_url):
        tail_string = ' | '.join(element)
        country_code_name_url[index] = tail_string

    chunks = list()
    for i in range(0, len(country_code_name_url), 2):
        chunk = country_code_name_url[i : i + 2]
        chunks.append(chunk)

    tail_srtring_list = list()
    for element in chunks:
        start = '| '
        tail_string = ' | '.join(element)
        end = ' |'
        tail_string = start + tail_string + end
        tail_srtring_list.append(tail_string)

    tail_srtring_list = '\n'.join(tail_srtring_list)
    table_hedar = '''| **Code** | **Country Name** | **Subscription Link** | **Code** | **Country Name** | **Subscription Link** |\n|:---:|:---:|:---:|:---:|:---:|:---:|'''
    table = table_hedar + '\n' + tail_srtring_list

    return table

readme = '''## Introduction
The script aggregates MTProto proxies from public Telegram channels. It cleans up proxies based on the open and closed ports, removes duplicate ones and resolves proxies addresses based on IP addresses.

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/soroushmirzaei/telegram-proxies-collector?label=Last%20Commit&color=%2338914b)
![GitHub](https://img.shields.io/github/license/soroushmirzaei/telegram-proxies-collector?label=License&color=yellow)
![GitHub Repo stars](https://img.shields.io/github/stars/soroushmirzaei/telegram-proxies-collector?label=Stars&color=red&style=flat)
![GitHub forks](https://img.shields.io/github/forks/soroushmirzaei/telegram-proxies-collector?label=Forks&color=blue&style=flat)
[![Execute On Schedule](https://github.com/soroushmirzaei/telegram-proxies-collector/actions/workflows/schedule.yml/badge.svg)](https://github.com/soroushmirzaei/telegram-proxies-collector/actions/workflows/schedule.yml)
[![Execute On Push](https://github.com/soroushmirzaei/telegram-proxies-collector/actions/workflows/push.yml/badge.svg)](https://github.com/soroushmirzaei/telegram-proxies-collector/actions/workflows/push.yml)

## Subscription Links
MTProto Proxies subscription links
| **Subscription Link Type** | **Subscription Links** |
|:---:|:---:|
| **Proxies Subscription Link** | [Subscription Link](https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/proxies) |
| **User Interface Subscription Link** | [Subscription Link](https://soroushmirzaei.github.io/telegram-proxies-collector) |

## Internet Protocol Type Subscription Links
MTProto Proxies subscription links based on internet protocol type
| **Internet Protocol Type** | **Subscription Links** |
|:---:|:---:|
| **Internet Protocol Version 4 (IPV4)** | [Subscription Link](https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/layers/ipv4) |
| **Internet Protocol Version 6 (IPV6)** | [Subscription Link](https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/layers/ipv6) |

## Country Subscription Links
MTProto proxies subscription links based on country'''

stats = '''## Stats
[![Stars](https://starchart.cc/soroushmirzaei/telegram-proxies-collector.svg?variant=adaptive)](https://starchart.cc/soroushmirzaei/telegram-proxies-collector)
## Activity
![Alt](https://repobeats.axiom.co/api/embed/150be6bfa1829ba8ec007b139002968bedad293e.svg "Repobeats analytics image")'''

with open('./readme.md', 'w') as file:
    file.write(readme + '\n' + create_country_table('./countries') + '\n' + stats)
    

html_string = '''<html>
  <head><title>Telegram Proxy - Soroush Mirzaei</title></head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
  {style}
  </style>
  <body>
    {table}
  </body>
</html>'''

style_string = '''body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
      background-color: #f4f7fa;
      color: #333;
      margin: 0;
      padding: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }
    table {
      width: 100%;
      max-width: 800px;
      border-collapse: collapse;
      background-color: #ffffff;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      border-radius: 8px;
      overflow: hidden;
    }
    th, td {
      padding: 15px;
      text-align: center;
      border-bottom: 1px solid #eeeeee;
    }
    th {
      background-color: #f9fafc;
      font-weight: 600;
      color: #555;
    }
    tr:hover {
      background-color: #f1f4f9;
    }
    td:last-child a button {
      padding: 10px 20px;
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 14px;
      transition: background-color 0.3s ease;
    }
    td:last-child a button:hover {
      background-color: #0056b3;
    }
    @media screen and (max-width: 600px) {
      table {
        width: 100%;
        display: block;
        overflow-x: auto;
        box-shadow: none;
        border-radius: 0;
      }
      th, td {
        padding: 10px;
        font-size: 14px;
      }
      td:last-child a button {
        padding: 8px 16px;
        font-size: 12px;
      }
    }'''

# Create dataframe based on proxies list
proxy_dataframe = pd.DataFrame(modified_proxies, columns = ['Flag', 'Country', 'Code', 'Server', 'Port', 'Ping', 'Proxy'])
proxy_dataframe['Ping'] = proxy_dataframe['Ping'].apply(lambda var : f"{var:06.2f}")

# Modify hyper-text github page
html_codes = proxy_dataframe.to_html(render_links = True, bold_rows = False, border = False, justify = 'match-parent',
                                     formatters={'Proxy': lambda x: f'<a href="{x}"><button>Connect Proxy</button></a>'}, escape = False)

# Output html file
with open('index.html', 'w') as html_file:
    html_file.write(html_string.format(style = style_string, table = html_codes))


# Clean up country file and append latest update time and proxies
with open('./proxies', 'w') as country_file:
    country_file.write(f"{datetime_update_str}\n\n")

with open("./proxies", "a", encoding="utf-8") as proxies_file:
    for index, elemenet in enumerate(modified_proxies):
        country_flag, country_name, country_code, ip_address, port, ping, proxy = elemenet
        proxies_file.write(f"{proxy}\n")
