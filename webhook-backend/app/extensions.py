from pymongo import MongoClient

client = MongoClient("mongodb+srv://vpratap419:rpkrLY3ozH2Q7jmv@cluster0.ou78g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tlsAllowInvalidCertificates=True)
db = client["github_events"]
collection = db["events"]

