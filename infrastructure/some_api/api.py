from infrastructure.some_api.base import BaseClient


class MyApi(BaseClient):
    def __init__(self, api_key: str, **kwargs):
        self.api_key = api_key
        self.base_url = "https://some-api.com"
        super().__init__(base_url=self.base_url)

    async def get_something(self, *args, **kwargs):
        # await self._make_request(
        #     ...
        # )
        return
