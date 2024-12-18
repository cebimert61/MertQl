from src.models.models import User

class BaseService:
    def __init__(self, session):
        self.session = session

# Service classes will be implemented based on your business logic
# Example:
# class YourService(BaseService):
#     def your_method(self):
#         pass
