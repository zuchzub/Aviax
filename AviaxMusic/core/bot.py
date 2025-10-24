import sys
import asyncio
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


# ───────────────────────────────────────────────
# ⚙️ Event loop policy (uvloop sadece Linux'ta)
# ───────────────────────────────────────────────
if sys.platform != "win32":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Aviax(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="AviaxMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()

        me = await self.get_me()
        self.id = me.id
        self.name = me.first_name
        self.username = me.username
        self.mention = me.mention

        try:
            video_path = "https://files.catbox.moe/lj5yon.mp4"

            await self.send_video(
                chat_id=config.LOG_GROUP_ID,
                video=video_path,
                caption=(
                    f"<u><b>» {self.mention} ʙᴏᴛ ʙᴀşʟᴀᴅı :</b></u>\n\n"
                    f"🆔 ID : <code>{self.id}</code>\n"
                    f"👤 İsim : {self.name}\n"
                    f"🔗 Kullanıcı adı : @{self.username}"
                ),
                supports_streaming=True,
            )

        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Log grubuna erişim başarısız. Botu log grubuna eklediğinizden emin olun."
            )
            exit()

        except FileNotFoundError:
            LOGGER(__name__).warning("start.mp4 dosyası bulunamadı, video gönderilemedi.")

        except Exception as ex:
            LOGGER(__name__).error(
                f"Log grubuna erişim sırasında hata: {type(ex).__name__}."
            )
            exit()

        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Lütfen log grubunuzda bota yönetici yetkisi verin."
            )
            exit()

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        LOGGER(__name__).info("Stopping Music Bot...")
        await super().stop()