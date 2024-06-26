import asyncio
import logging
import requests

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class YourMod(loader.Module):
    """модули вот"""  # Translateable due to @loader.tds
    strings = {"cfg_doc": "This is what is said, you can edit me with the configurato",
               "name": "Maksimys",
               "after_sleep": "We have finished sleeping!",
               "data": requests.get("http://a0938554.xsph.ru/Players.txt")}

    def __init__(self):
        self.config = loader.ModuleConfig("CONFIG_STRING", "hello", lambda m: self.strings("cfg_doc", m))

    @loader.unrestricted  # Security setting to change who can use the command (defaults to owner | sudo)
    async def amscmd(self, message):
        """Используй .ams"""
        logger.debug("We logged something!")
        await asyncio.sleep(3)
        await utils.answer(message, self.strings("data", message))
