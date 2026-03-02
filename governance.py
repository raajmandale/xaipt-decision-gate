import uuid
from datetime import datetime

class Request:
    def __init__(self, action_text):
        self.request_id = str(uuid.uuid4())[:8]
        self.action_text = action_text
        self.status = "HOLD"
        self.token = str(uuid.uuid4())[:6].upper()
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.approved_at = None
        self.executed_at = None

    def approve(self, token_input):
        if token_input.strip().upper() == self.token:
            self.status = "APPROVED"
            self.approved_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True
        return False

    def execute(self):
        if self.status == "APPROVED":
            self.status = "EXECUTED"
            self.executed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True
        return False