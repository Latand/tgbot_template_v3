from __future__ import annotations

import asyncio
import logging
import ssl
from typing import TYPE_CHECKING, Any

import backoff
from aiohttp import ClientError, ClientSession, TCPConnector, FormData
from ujson import dumps, loads

if TYPE_CHECKING:
    from collections.abc import Mapping

    from yarl import URL


# Taken from here: https://github.com/Olegt0rr/WebServiceTemplate/blob/main/app/core/base_client.py
class BaseClient:
    """Represents base API client."""

    def __init__(self, base_url: str | URL) -> None:
        self._base_url = base_url
        self._session: ClientSession | None = None
        self.log = logging.getLogger(self.__class__.__name__)

    async def _get_session(self) -> ClientSession:
        """Get aiohttp session with cache."""
        if self._session is None:
            ssl_context = ssl.SSLContext()
            connector = TCPConnector(ssl_context=ssl_context)
            self._session = ClientSession(
                base_url=self._base_url,
                connector=connector,
                json_serialize=dumps,
            )

        return self._session

    @backoff.on_exception(
        backoff.expo,
        ClientError,
        max_time=60,
    )
    async def _make_request(
        self,
        method: str,
        url: str | URL,
        params: Mapping[str, str] | None = None,
        json: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        data: FormData | None = None,
    ) -> tuple[int, dict[str, Any]]:
        """Make request and return decoded json response."""
        session = await self._get_session()

        self.log.debug(
            "Making request %r %r with json %r and params %r",
            method,
            url,
            json,
            params,
        )
        async with session.request(
            method, url, params=params, json=json, headers=headers, data=data
        ) as response:
            status = response.status
            if status != 200:
                s = await response.text()
                raise ClientError(f"Got status {status} for {method} {url}: {s}")
            try:
                result = await response.json(loads=loads)
            except Exception as e:
                self.log.exception(e)
                self.log.info(f"{await response.text()}")
                result = {}

        self.log.debug(
            "Got response %r %r with status %r and json %r",
            method,
            url,
            status,
            result,
        )
        return status, result

    async def close(self) -> None:
        """Graceful session close."""
        if not self._session:
            self.log.debug("There's not session to close.")
            return

        if self._session.closed:
            self.log.debug("Session already closed.")
            return

        await self._session.close()
        self.log.debug("Session successfully closed.")

        # Wait 250 ms for the underlying SSL connections to close
        # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        await asyncio.sleep(0.25)
