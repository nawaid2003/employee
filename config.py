from dotenv import load_dotenv
import os

# Load environment variables to simulate Key Vault
load_dotenv()

class MockKeyVault:
    @staticmethod
    def get_secret(key, default):
        return os.getenv(key, default)