from datetime import datetime

AUDIT = []

def log(request_id, event):
    AUDIT.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "request_id": request_id,
        "event": event
    })

def get_logs():
    return AUDIT