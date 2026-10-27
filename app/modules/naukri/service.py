class NaukriService:
    def __init__(self):
        self._connected = False

    async def connect(self):
        # Placeholder until authorized integration is available
        return {
            "status": "not_connected",
            "message": "Naukri integration requires authorized access",
        }

    async def get_status(self):
        return {
            "connected": self._connected,
            "provider": "naukri",
        }

    async def disconnect(self):
        self._connected = False

        return {
            "status": "disconnected",
        }


naukri_service = NaukriService()