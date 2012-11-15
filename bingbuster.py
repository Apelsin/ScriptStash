'''
    Bing Buster 0002
    
    Get your Bing Rewards in a snap!
    
    Copyright Vincent Brubaker-Gianakos
    Some Rights Reserved
    
    This work is licensed under a Creative Commons Attribution 3.0 United States License.
    
    http://creativecommons.org/licenses/by/3.0/us/
    
    THE WORK (AS DEFINED BELOW) IS PROVIDED UNDER THE TERMS OF THIS CREATIVE COMMONS PUBLIC LICENSE ("CCPL" OR "LICENSE").
    THE WORK IS PROTECTED BY COPYRIGHT AND/OR OTHER APPLICABLE LAW.
    ANY USE OF THE WORK OTHER THAN AS AUTHORIZED UNDER THIS LICENSE OR COPYRIGHT LAW IS PROHIBITED.
    
    BY EXERCISING ANY RIGHTS TO THE WORK PROVIDED HERE, YOU ACCEPT AND AGREE TO BE BOUND BY THE TERMS OF THIS LICENSE.
    TO THE EXTENT THIS LICENSE MAY BE CONSIDERED TO BE A CONTRACT, THE LICENSOR GRANTS YOU THE RIGHTS CONTAINED HERE IN
    CONSIDERATION OF YOUR ACCEPTANCE OF SUCH TERMS AND CONDITIONS.
'''














'''                                 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                    !!! TO BE USED SOLELY AS PROOF OF CONCEPT !!!
                                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''














import sys
import mechanize
import cookielib
import itertools
import urllib
import time
from getpass import getpass
import re

#Ridiculous queries:
stupid_shit = (
"I love buns",
"buns are awesome",
"yes, rabbits",
"wow, get a load of these buns",
"these search queries are fake",
"bune bune a bun bun",
"Wonderbuns",
"Bunning it up",
"gonna get binged",
"bingin' it up in this bing",
"hit the binger after a workout",
"the party's gonna be bingin' tonight",
"BINGO? more like BINGNO!",
"all my nope",
"some binging would do you good",
"everybingy does the bupple bop bun bun boopity boo",
"I wonder how Microsoft will use this search query information",
"I wonder if anyone will ever read this",
"Bill Gates is my waifu",
"clogging the M$ pipes!",)

# How many times to cycle the query strings:
how_stupid = 2

# Griefy stuff:
bingmagic = "http://www.bing.com/fd/auth/signin?action=interactive&provider=facebook&sig=F11487C67626411BBF7DDB06EDC209D7&return_url=http%3a%2f%2fwww.bing.com%2f&src=EXPLICIT"

# Cheap shot:
faker = [('Content-Type', 'application/x-www-form-urlencoded'),
         ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')]

cookie_jar_file_name = "bb_cookies.txt"

browser = mechanize.Browser()
jar = cookielib.LWPCookieJar()
browser.set_cookiejar(jar)

try:
    jar.load(cookie_jar_file_name, ignore_discard=False, ignore_expires=False)
except IOError, e:
    print "Unable to open bb_cookies.txt"
    if hasattr(e, 'code'):
        print "Error code:", e.code
        
class Facebook():
    def __init__(self, email, password, browser):
        self.email = email
        self.password = password
        self.browser = browser
        
    def prompt_credentials(self):
        self.email = raw_input("Facebook email: ")
        self.password = getpass("Facebook password: ")
           
    def login(self):
        resp = self.browser.open('http://www.facebook.com')
        if "Logout" in resp.read():
            print "(Already) logged in to Facebook :)"
        else:
            if(self.name == None or self.password == None):
                self.prompt_credentials()
            url = 'https://login.facebook.com/login.php?login_attempt=1'
            data = "locale=en_US&non_com_login=&email=" + self.email + "&pass=" + self.password + "&lsd=20TOl&persistent=1"
            resp = self.browser.open(url, data)
            if "Logout" in resp.read():
                print "Logged in to Facebook :)"
            else:
                print "Failed logging in to Facebook :("
                print resp.read()
                print "Once again, failed logging in to Facebook :("
                return -1
        return 0
        
facebook = Facebook(None, None, browser) # Supplying none invokes prompt

browser.set_handle_robots(False) # Very naughty ;;;)))
browser.addheaders = [('Referer', 'http://login.facebook.com/login.php')] + faker

if(facebook.login() == 0):
    browser.addheaders = [('Referer', 'http://bing.com')] + faker
    resp = browser.open(bingmagic)
    if re.search('Bing Rewards', resp.read(), re.IGNORECASE):
        for i in range(how_stupid):
            for crap in stupid_shit:
                print "Searching \"" + crap + "\""
                browser.open("http://www.bing.com/search?q=" + urllib.quote(crap))
                time.sleep(1)
                
jar.save(cookie_jar_file_name, ignore_discard=False, ignore_expires=False)
print "Fin!"