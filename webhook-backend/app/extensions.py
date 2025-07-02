from pymongo import MongoClient

client = MongoClient("replace this with mongodb atlas string", tlsAllowInvalidCertificates=True)
db = client["github_events"]
collection = db["events"]

