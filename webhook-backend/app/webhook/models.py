from datetime import datetime, timezone

def format_push(data):
    return {
        "type": "push",
        "author": data["pusher"]["name"],
        "to_branch": data["ref"].split("/")[-1],
        "timestamp": datetime.utcnow()
    }

def format_pull_request(data):
    pr = data["pull_request"]
    return {
        "type": "pull_request",
        "author": pr["user"]["login"],
        "from_branch": pr["head"]["ref"],
        "to_branch": pr["base"]["ref"],
        "timestamp": datetime.utcnow()
    }

def format_merge(data):
    pr = data["pull_request"]
    if pr.get("merged"):
        return {
            "type": "merge",
            "author": pr["user"]["login"],
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": datetime.utcnow()
        }
