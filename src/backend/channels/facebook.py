from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount


my_app_id = 'your-app-id'
my_app_secret = 'your-appsecret'
my_access_token = 'your-page-access-token'
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
my_account = AdAccount('act_<your-adaccount-id>')
campaigns = my_account.get_campaigns()
print(campaigns)


print(my_account)
#{'account_id': u'17842443', 'id': u'act_17842443'}
my_account = my_account.api_get(fields=[AdAccount.Field.amount_spent])
print(my_account[AdAccount.Field.amount_spent])
#{'amount_spent': 21167, 'account_id': u'17842443', 'id': u'act_17842443'}