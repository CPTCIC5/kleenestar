from django.shortcuts import get_object_or_404
from app_channels.models import Channel
from users.models import User
from oauth import check_refresh
from oauth.exceptions import RefreshException

def get_channel(channel_type_num, subspace_id):
    return get_object_or_404(Channel, channel_type=channel_type_num, subspace=subspace_id)

def create_channel(channel_type_num, subspace_id):
    try:
        
        new_channel = Channel.objects.create(
           channel_type=channel_type_num, subspace_id=subspace_id
        )
        return new_channel
    except Exception as e:
        print(str(e), "Error in creating channel object")
        return Channel.objects.get(channel_type=channel_type_num, subspace=subspace_id)
    

def refresh_credentials(channel):
    print("refresh function called")

    channel_types = {
        1: check_refresh.check_update_google_credentials,
        2: check_refresh.check_update_facebook_credentials,
        3: check_refresh.check_update_twitter_credentials,
        4: check_refresh.check_update_linkedin_credentials,
        5: check_refresh.check_update_tiktok_credentials,
        6: check_refresh.check_update_reddit_credentials,
        7: check_refresh.check_update_shopify_credentials,
        8: check_refresh.check_update_google_credentials,
        9: check_refresh.check_update_mailchimp_credentials,
        # 10: check_refresh.check_update_instagram_credentials,
        11: check_refresh.check_update_bing_credentials
    }

    try:

        get_refresh_function = channel_types.get(channel.channel_type)
        
        try:
            if get_refresh_function:
                credentials = channel.credentials
                if channel.channel_type == 1:
                    data = get_refresh_function(credentials.key_1, credentials.key_2)
                    if(data[0]): # Update Access token If the new access token is generated
                        channel.credentials.key_2 = data[1]

                elif channel.channel_type == 2: # No Refresh token passed
                    get_refresh_function(credentials.key_1)

                elif channel.channel_type == 3: # No Refresh token passed
                    get_refresh_function(credentials.key_3, credentials.key_4)
                
                elif channel.channel_type == 4: # Update Access token If the new access token is generated
                    data = get_refresh_function(credentials.key_1, credentials.key_2)
                    if(data[0]):
                        channel.credentials.key_1 = data[1]

                elif channel.channel_type == 5: # No Refresh token passed
                    get_refresh_function(credentials.key_1)
                
                elif channel.channel_type == 6: # Update Access token If the new access token is generated
                    data = get_refresh_function(credentials.key_1, credentials.key_2)
                    if(data[0]):
                        channel.credentials.key_1 = data[1]
                
                elif channel.channel_type == 7: # No Refresh token passed
                    get_refresh_function(credentials.key_1,credentials.key_2)
                
                elif channel.channel_type == 8:
                    data = get_refresh_function(credentials.key_1, credentials.key_2)
                    if(data[0]): # Update Access token If the new access token is generated
                        channel.credentials.key_2 = data[1]
                        
                elif channel.channel_type == 9: # No Refresh token passed
                    get_refresh_function(credentials.key_1,credentials.key_2)
                
                # elif channel.channel_type == 10: # No Refresh token passed
                #     get_refresh_function(credentials.key_1,credentials.key_2)

                elif channel.channel_type == 11: # Update Access token If the new access token is generated
                    data = get_refresh_function(credentials.key_1, credentials.key_2)
                    if(data[0]):
                        channel.credentials.key_1 = data[1]
                     
                channel.credentials.save()
            
            channel.save()

        except RefreshException as e:
            print(f"channel - {channel.channel_type} credentials are removed (expired) - channel disabled")
            channel.delete()


    except Exception as e:
        print("Error in refresh function:" + str(e))
        return None

