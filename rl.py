#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class YourMod(loader.Module):
    """rules"""  # Translateable due to @loader.tds
    strings = {"cfg_doc": "totka",
               "name": "r",
               "after_sleep": "привет\nпр"
               "rules": "Читы, слив промо - бан навсегда\nОскорбление - мут 1 час\nСпам - мут 3 дня\nПорнография - мут 5 дней\nСпам тегом - мут 4 дня\nПробив участника - бан навсегда\nСлив личных данных - бан навсегда+ жалоба\nРеклама-мут два часа\nСкример- мут день""
              }

    def __init__(self):
        self.config = loader.ModuleConfig("CONFIG_STRING", "hello", lambda m: self.strings("cfg_doc", m))

    @loader.unrestricted  # Security setting to change who can use the command (defaults to owner | sudo)
    async def rlcmd(self, message):
        """Does something when you type .example (hence, named examplecmd)"""
        logger.debug("We logged something!")
        await utils.answer(message, self.config["CONFIG_STRING"])
        await asyncio.sleep(5)  # Never use time.sleep
        await utils.answer(message, self.strings("rules", message))
      
