import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class YourMod(loader.Module):
    """Крутой модуль ещкере"""  # Translateable due to @loader.tds
    strings = {"cfg_doc": "This is what is said, you can edit me with the configurato",
               "name": "amster module",
               "after_sleep": "We have finished sleeping!"}

    def __init__(self):
        self.config = loader.ModuleConfig("CONFIG_STRING", "hello", lambda m: self.strings("cfg_doc", m))

    @loader.unrestricted  # Security setting to change who can use the command (defaults to owner | sudo)
    async def amscmd(self, message):
        """Используй .ams"""
        logger.debug("We logged something!")
        await utils.answer(message, self.config["CONFIG_STRING"])
        await asyncio.sleep(5)  # Never use time.sleep
        await utils.answer(message, self.strings("after_sleep", message))
        await utils.answer(message, "Result")
     
