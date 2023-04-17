import requests
import time
import os
import logging
import sys

has_env = all(
    [
    'ZSCALER_API_KEY' in os.environ
    ,'ZSCALER_USR' in os.environ
    ,'ZSCALER_PW' in os.environ
    ]
    )
    
class MissingEnvironmentVariable(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def obfuscateApiKey(api_key:str):
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

# alternatively, we can create a class to keep track of session
class ZSession:
    url = 'https://zsapi.zscalergov.net/api/v1/'
    def __init__(
        self
        ,usr:str=None
        ,pw:str=None
        ,api_key:str=None,
        **kwargs
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
    
    def _set_env_creds(self,usr=None,pw=None,api_key=None):
        """
        Sets the credentials to the environment. Overrides any existing values.
        """
        if not all((usr,pw,api_key)) and not has_env:
            raise MissingEnvironmentVariable('Environment variables must be set if credentials are not passed in as an argument.')
        if all((usr,pw,api_key)):
            if has_env:
                logging.info("Overriding environment credentials w/ arguments.")
            logging.info("Setting credentials to environment.")
            os.environ['ZSCALER_API_KEY'] = api_key
            os.environ['ZSCALER_USR'] = usr
            os.environ['ZSCALER_PW'] = pw
        elif has_env:
            logging.info("No credentials passed as argument. Using credentials applied to environment.")

    def get_auth_session(
        self
        ,usr:str=None
        ,pw:str=None
        ,api_key:str=None
        ):
        """
        Creates an authenticated session. 
        The response returns a cookie in the header called JSESSIONID 
        that must be used in subsequent requests.

        API Reference
        ---
        https://help.zscaler.us/zia/api-authentication
        """
        self._set_env_creds(usr,pw,api_key)
        now, key = obfuscateApiKey(os.environ['ZSCALER_API_KEY'])
        payload = {
        "apiKey": key,
        "username": os.environ['ZSCALER_USR'],
        "password": os.environ['ZSCALER_PW'],
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
        results = []
        if isinstance(url,str):
            url = [url]
        for chunk in chunks(url,100):
            result = self.session.post(
                url=self.url+'urlLookup'
                ,json=chunk
                )
            result.raise_for_status()
            results+=result.json()
        return results
    
    def url_categories(self):
        """
        Gets information about all or custom URL categories. By default, the response includes keywords.
        """
        return self.session.get(
            url=self.url+'urlCategories'
            )
    
if __name__ == '__main__':
    logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)])
    
    z = ZSession()
    
    result = z.status()
    result = z.url_lookup('google.com')
