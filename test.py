from pymongo import MongoClient
import ssl

client = MongoClient('mongodb://web:almafa@aws-us-east-1-portal.22.dblayer.com:16806,aws-us-east-1-portal.23.dblayer.com:16806/admin?ssl=true',ssl_cert_reqs=ssl.CERT_NONE)

print client.config.config.find_one({})['key']