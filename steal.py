__version__ = (1, 0, 0)

# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# Code is licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka
# 🔑 https://creativecommons.org/licenses/by-nc-nd/4.0/
# + attribution
# + non-commercial
# + no-derivatives

# You CANNOT edit this file without direct permission from the author.
# You can redistribute this file without any changes.

# meta pic: https://ton.org/download/ton_symbol.png
# meta banner: https://mods.hikariatama.ru/badges/cryptosteal.jpg

# meta developer: @hikarimods
# scope: hikka_only
# scope: hikka_min 1.6.3

import asyncio
import contextlib
import logging
import re

from hikkatl.tl.functions.messages import StartBotRequest
from hikkatl.tl.types import Message

from .. import loader

logger = logging.getLogger(__name__)


@loader.tds
class CryptoSteal(loader.Module):
    """Steals checks for CupMeterBot"""

    strings = {"name": "CupSteal"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "delay",
                100,
                "Delay before claiming the check in ms",
                validator=loader.validators.Integer(minimum=10),
            ),
            loader.ConfigValue(
                "bots",
                ["cryptobot", "cupmeterbot", "cryptotestnetbot"],
                "Bots from which the checks should be captured",
                validator=loader.validators.Series(loader.validators.String()),
                on_change=lambda: asyncio.ensure_future(self._process_config()),
            ),
            loader.ConfigValue(
                "only_inline",
                False,
                (
                    "Capture only checks sent through inline mode of the bots, not just"
                    " links"
                ),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "token_length_limit",
                32,
                "To avoid database overflow",
                validator=loader.validators.Integer(minimum=1),
            ),
        )

        self._acquired = []
        self._regex: str = None
        self._id_regex: str = None
        self._username_id_map = {}
        self._regex_ready = asyncio.Event()

    async def _process_config(self):
        self._regex_ready.clear()

        whitelist = []
        whitelist_ids = []
        for entity in self.config["bots"]:
            with contextlib.suppress(Exception):
                entity = await self._client.get_entity(
                    f"@{entity.strip('@')}" if not entity.isdigit() else int(entity),
                    exp=0,
                )
                if entity.username:
                    whitelist.append(re.escape(entity.username.lower()))
                    self._username_id_map[entity.username.lower()] = entity.id

                for username in entity.usernames or []:
                    if re.escape(username.username.lower()) not in whitelist:
                        whitelist.append(re.escape(username.username.lower()))

                    self._username_id_map[username.username.lower()] = entity.id

                if entity.id not in whitelist_ids:
                    whitelist_ids.append(str(entity.id))

        self._regex = f"t\\.me\\/(?i:(?P<bot>{'|'.join(whitelist)}))\\?start=GCA_(?P<token>[a-zA-Z0-9+/_-]+)"
        self._id_regex = f"({'|'.join(whitelist_ids)})"
        self._regex_ready.set()

    async def _acquire(self, bot: str, token: str):
        if (
            token.lower() in self._acquired
            or len(token) > self.config["token_length_limit"]
        ):
            return

        self._acquired.append(token.lower())

        await asyncio.sleep(self.config["delay"] / 1000)

        await self._client(
            StartBotRequest(
                bot=self._username_id_map[bot.lower()],
                peer=self._username_id_map[bot.lower()],
                start_param=token,
            )
        )

    @loader.watcher("in", "only_messages")
    async def watcher(self, message: Message):
        await self._regex_ready.wait()

        if re.search(str(message.via_bot_id), self._id_regex):
            await asyncio.sleep(3)
            message = (
                await self._client.get_messages(message.peer_id, ids=[message.id])
            )[0]

        if not self.config["only_inline"] and (
            match := re.search(
                self._regex,
                message.text,
            )
        ):
            await self._acquire(match.group("bot"), match.group("token"))

        if (
            message.reply_markup
            and (url := getattr(message.reply_markup.rows[0].buttons[0], "url", None))
            and (
                match := re.search(
                    self._regex,
                    url,
                )
            )
        ):
            await self._acquire(match.group("bot"), match.group("token"))
