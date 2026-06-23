import asyncio
import logging
from telegram import Bot
from telegram.error import TelegramError

# Configuración
BOT_TOKEN = "8908437704:AAE_nHs_dtr9-P8cjj9CrMZKcgex2Zx88Qk"
CHANNEL_ID = -1003965172753
INTERVALO_SEGUNDOS = 60  # cada 60 segundos

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def auto_aprobar():
    bot = Bot(token=BOT_TOKEN)
    logger.info("✅ Bot iniciado. Comprobando solicitudes cada 60 segundos...")

    while True:
        try:
            requests = await bot.get_chat_join_requests(chat_id=CHANNEL_ID)
            if requests:
                for req in requests:
                    await bot.approve_chat_join_request(
                        chat_id=CHANNEL_ID,
                        user_id=req.from_user.id
                    )
                    logger.info(f"✅ Aprobado: {req.from_user.first_name} (ID: {req.from_user.id})")
            else:
                logger.info("Sin solicitudes pendientes.")
        except TelegramError as e:
            logger.error(f"❌ Error de Telegram: {e}")
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}")

        await asyncio.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    asyncio.run(auto_aprobar())
