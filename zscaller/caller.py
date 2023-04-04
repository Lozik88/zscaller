import requests
import time
import os

# you might want to set these as environment variables
# you can use os.environ['YOUR_ENV_VARIABLE'] to retrieve the variable value. 
# if you do, just make sure you import os
# if using linux style OS, these can be added to the $HOME/.profile or $HOME/.bashrc file 
z_api_key=''
z_usr=''
z_pw=''
if 'ZSCALER_API_KEY' in os.environ:
    z_api_key = os.environ['ZSCALER_API_KEY']
if 'ZSCALER_USR' in os.environ:
    z_usr = os.environ['ZSCALER_USR']
if 'ZSCALER_PW' in os.environ:
    z_pw = os.environ['ZSCALER_PW']

# setting up initial requests.Session to keep authenticated session alive. 
# Zscaller requires us to authenticate 
session = requests.session()

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def obfuscateApiKey(api_key:str=z_api_key):
    """
    This is used to obfuscate the api key. This is required by zscaler for the initial authorization.
    api_key : str
        - API key to be obfuscated
    
    References
    ---
    https://help.zscaler.com/zia/getting-started-zia-api#CreateSession
    """
    now = int(time.time() * 1000)
    n = str(now)[-6:]
    r = str(int(n) >> 1).zfill(6)
    key = ""
    for i in range(0, len(str(n)), 1):
        key += api_key[int(str(n)[i])]
    for j in range(0, len(str(r)), 1):
        key += api_key[int(str(r)[j])+2]
    # print("Timestamp:", now, "\tKey", key)
    return now, key

def get_auth_session(
    url='https://zsapi.zscalergov.net/api/v1/authenticatedSession'
    ,usr:str=z_usr
    ,pw:str=z_pw
    ,api_key:str=z_api_key
    ):
    """
    Creates an authenticated session. 
    The response returns a cookie in the header called JSESSIONID 
    that must be used in subsequent requests.

    API Reference
    ---
    https://help.zscaler.us/zia/api-authentication
    """
    now, key = obfuscateApiKey(api_key)
    payload = {
    "apiKey": key,
    "username": usr,
    "password": pw,
    'timestamp':now
    }
    result = session.post(
        url
        ,json=payload
        )
    # raise an error if the API was not authenticated successfully
    result.raise_for_status()
    return result

def url_lookup(url):
    """
    Look up the categorization of the given set of URLs, e.g., ['abc.com', 'xyz.com']. 
    Up to 100 URLs can be looked up per request, and a URL cannot exceed 1024 characters.

    API Reference
    ---
    https://help.zscaler.us/zia/url-categories#/urlLookup-post
    """
    if isinstance(url,str):
        url = [url]
    result = session.post(
        url='https://zsapi.zscalergov.net/api/v1/urlLookup'
        ,json=url
        )
    return result

# alternatively, we can create a class to keep track of session
class ZSession:
    url = 'https://zsapi.zscalergov.net/api/v1/'
    def __init__(
        self
        ,usr:str=z_usr
        ,pw:str=z_pw
        ,api_key:str=z_api_key
        ) -> None:
        """
        This is the class constructor. All code in this method is run upon class instantiation.
        """
        self.session = requests.session()
        self.get_auth_session(
            usr=usr
            ,pw=pw
            ,api_key=api_key
            )
        
    def get_auth_session(
        self
        ,usr:str
        ,pw:str
        ,api_key:str
        ):
        """
        Creates an authenticated session. 
        The response returns a cookie in the header called JSESSIONID 
        that must be used in subsequent requests.

        API Reference
        ---
        https://help.zscaler.us/zia/api-authentication
        """
        now, key = obfuscateApiKey(api_key)
        payload = {
        "apiKey": key,
        "username": usr,
        "password": pw,
        'timestamp':now
        }
        result = self.session.post(
            self.url+'authenticatedSession'
            ,json=payload
            )
        # raise an error if the API was not authenticated successfully
        result.raise_for_status()
        return result

    def status(self):
        """
        Gets the activation status for the saved configuration changes. 

        API Reference
        ---
        https://help.zscaler.com/zia/activation#/status-get
        """
        return self.session.get(
            url=self.url+'status'
            )


    def url_lookup(self,url):
        """
        Look up the categorization of the given set of URLs, e.g., ['abc.com', 'xyz.com']. 
        Up to 100 URLs can be looked up per request, and a URL cannot exceed 1024 characters.

        API Reference
        ---
        https://help.zscaler.us/zia/url-categories#/urlLookup-post
        """
        if isinstance(url,str):
            url = [url]
        result = self.session.post(
            url=self.url+'urlLookup'
            ,json=url
            )
        return result
    
    def url_categories(self):
        """
        Gets information about all or custom URL categories. By default, the response includes keywords.
        """
        return self.session.get(
            url=self.url+'urlCategories'
            )
    
if __name__ == '__main__':
    # ################
    # # Method Usage #
    # ################
    # # authenticate zscaler session
    # get_auth_session()

    # urls = [  
    # "google.com","youtube.com","facebook.com","baidu.com","wikipedia.org","yahoo.com","reddit.com","google.co.in","qq.com","taobao.com","amazon.com","tmall.com","twitter.com","google.co.jp","sohu.com","live.com","vk.com","instagram.com","sina.com","360.cn","google.de","jd.com","google.co.uk","linkedin.com","weibo.com","google.fr","google.ru","yahoo.co.jp","yandex.ru","netflix.com","t.co","hao123.com","imgur.com","google.it","ebay.com","pornhub.com","google.es","detail.tmall.com","WordPress.com","msn.com","aliexpress.com","bing.com","tumblr.com","google.ca","livejasmin.com","microsoft.com","stackoverflow.com","twitch.tv","Soso.com","blogspot.com","ok.ru","apple.com","Naver.com","mail.ru","imdb.com","popads.net","tianya.cn","office.com","google.co.kr","github.com","pinterest.com","paypal.com","diply.com","amazon.de","microsoftonline.com","onclckds.com","amazon.co.uk","txxx.com","adobe.com","wikia.com","cnzz.com","xhamster.com","coccoc.com","bongacams.com","fc2.com","pixnet.net","google.pl","dropbox.com","googleusercontent.com","gmw.cn","whatsapp.com","google.co.th","soundcloud.com","google.nl","xvideos.com","Booking.com","rakuten.co.jp","nytimes.com","alibaba.com","bet365.com","ebay.co.uk","quora.com","avito.ru","dailymail.co.uk","globo.com","uol.com","nicovideo.jp","walmart.com","redtube.com","go2cloud.org"
    # ,'extra.com'
    # ]
    # # run zscaler's urlLookup api
    # urls = list(chunks(urls,100))
    # result = url_lookup(urls)

    ###############
    # Class Usage #
    ###############
    z = ZSession()
    result = z.status()
    result = z.url_lookup('google.com')
