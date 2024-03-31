from google.ads.googleads.client import GoogleAdsClient
import os

os.environ["GOOGLE_ADS_CONFIGURATION_FILE_PATH"] = "path/to/google-ads.yaml"
from google.ads.googleads.client import GoogleAdsClient
client = GoogleAdsClient.load_from_storage()

client = GoogleAdsClient.load_from_storage("path/to/google-ads.yaml")