from config import *
from main import *
apiKey = API_KEY
secret = SECRET_KEY
url = ENDPOINT
import alpaca_trade_api as tradeapi

api = tradeapi.REST(apiKey,secret,url)

account = api.get_account()
print(account.status)
