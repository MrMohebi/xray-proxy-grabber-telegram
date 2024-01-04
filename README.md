# Xray Proxy Grabber

###### **See more:** also explore this project; the best solution to use these collected proxies : [clash-meta-iran-bridge-config](https://github.com/MrMohebi/clash-meta-iran-bridge-config) :)

###### **See more:** And also this project for xray-core: [xray-iran-bridge-configs](https://github.com/MrMohebi/xray-iran-bridge-configs) :)


## Quick access

|            | all                                                                                                                                  | active all                                                                                                                                | active ping less than 1000ms                                                                                                                          | active ping less than 1500ms                                                                                                                          | active ping less than 1000ms and No google 403                                                                                                            |
|------------|--------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Row URLs   | [subscription link](https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/all.txt) | [subscription link](https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/actives.txt)  | ask me to provide if u need                                                                                                                           | ask me to provide if u need                                                                                                                           | ask me to provide if u need                                                                                                                               |
| Xray JSON  | ask me to provide if u need                                                                                                          | [json configs](https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/xray-json/actives_all.txt) | [json configs](https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/xray-json/actives_under_1000ms.txt)    | [json configs](https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/xray-json/actives_under_1500ms.txt)    | [json configs](https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/xray-json/actives_no_403_under_1000ms.txt) |
| Clash Meta | [provider link](https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/clash-meta/all.yaml) | ask me to provide if u need                                                                                                               | [provider link](https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/clash-meta/actives_under_1000ms.yaml) | [provider link](https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/clash-meta/actives_under_1500ms.yaml) | ask me to provide if u need                                                                                                                               |



## Explanation
This project is aimed at grabbing fresh proxies from Telegram channels and testing them by real-delay ping.
A Telegram bot will listen on provided channels (even private ones), then parse new proxies and commit them to ur repo.

The main differences between this project and others are:
- creating xray json config from urls (I'll explain what this is for :) )
- can grab proxies from private channels or even PVs (with some little changes).
- AND to-dos that will be added :)

### Telegram grabber:
Uses the Telegram MTProto API Framework and acts exactly like ur real account. After first running,
It will ask u to sign in to your account. then listens to the provided channel in [`env`](./.env.example#L12).

Because of that, it can grab proxies everywhere that u join them with ur real account, even PVs :)
To get started with the MTProto API, u should get `app_id` and `api_hash` which I couldn't get them easily.
###### *Note:* Telegram detects u'r using a VPN and throws an error while creating `app_id` :|. Ask someone to create it for u.(God bless Telegram.)

On each new message that contains a proxy URL, [`proxies_row_url.txt`](collected-proxies/row-url/all.txt) will be updated real-time.

###### *Tip:* u can use [`proxies_row_url.txt`](collected-proxies/row-url/all.txt) as subscription link in ur clients app (V2rayNG, V2rayN, etc):)


### Xray URL Decoder
This [part of project](./xray_url_decoder) aimed to decode and convert proxy URL to python class witch can be played with.
Because of this part I only support `vless` 

I couldn't find it anywhere. Really nobody wrote it before !? :| 

If u know any repo done this before, notify me, tnx.


### Xray ping
To test grabbed proxies, be only relied on ping of server on that port is not a correct approach.

In [this part](./xray_ping) I run a xray-core temporarily, witch trys to GET a simple html page by real connection throw proxy.

Also, nobody wrote it before. Come on guys.

### Auto Run Jobs 
[`checkProxies.py`](./checkProxies.py) will be run every 1 hour by the GitHub runner and check for grabbed proxies to be active.
Next, sort these proxies by real delay ping and save them as JSON type in [`proxies_active.txt`](collected-proxies/xray-json/actives_all.txt)
###### *Note:* GitHub runners aren't in Iran, So proxy checker can't detect censored proxies. U can run it on ur server from Iran by cron jobs.


[`cleanProxiesRowUrl.py`](./cleanProxiesRowUrl.py) will be run each 12 hours by GitHub runner and remove all URL proxies witch are not present in [`proxies_active.txt`](collected-proxies/xray-json/actives_all.txt).
So the url list will be clean always
###### *Note:* It means only supported protocols will remain, and all others will be deleted.



## Env-File:
To commit new proxies in ur repo, u should get [GitHub token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#personal-access-tokens-classic)So the bot will be able to commit new changes, such as new proxies.

Also, I explained How to get `api_id` [here](#telegram-grabber)

## ToDo
- [x] vless protocol support
- [x] reality security support
- [x] vmess protocol support
- [x] trojan protocol support
- [x] connect to iran bridge
- [x] update iran bridge with actives
- [x] tcp security support
- [ ] server less grabber (no telegram or server needed)
