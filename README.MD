# zscaller
This module utilizes the [zscaler APIs](https://help.zscaler.com/zia/getting-started-zia-api).

## Installation
You can install this module by...
```sh
pip install .
```
or

```sh
python -m pip install .
```

## Usage
Set your API credentials to these environment variables:
* ZSCALER_USR
* ZSCALER_PW
* ZSCALER_API_KEY

```py
from zscaller.caller import ZSession
z = ZSession()
domains = ["google.com","youtube.com","facebook.com","baidu.com"]
result = z.url_lookup(domains)
print(result.json())
```

Alternatively, you can directly set the credentials to Zsession:

```py
from zscaller.caller import ZSession
z = ZSession(
    usr='someUsrID'
    ,pw='somePassword'
    ,api_key='someAPIKey'
    )
domains = ["google.com","youtube.com","facebook.com","baidu.com"]
result = z.url_lookup(domains)
print(result.json())
```

