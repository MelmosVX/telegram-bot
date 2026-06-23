import asyncio
import logging
import json
import aiohttp

# Configuración
BOT_TOKEN = "8908437704:AAE_nHs_dtr9-P8cjj9CrMZKcgex2Zx88Qk"
CHANNEL_ID = -1003965172753
INTERVALO_SEGUNDOS = 60
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def api_call(session, method, params=None):
    url = f"{BASE_URL}/{method}"
    async with session.post(url, json=params or {}) as resp:
        text = await resp.text()
        try:
            return json.loads(text)
        except:
            logger.error(f"No se pudo parsear respuesta: {text[:200]}")
            return {"ok": False}

async def auto_aprobar():
    logger.info("✅ Bot iniciado. Comprobando solicitudes cada 60 segundos...")
    async with aiohttp.ClientSession() as session:

        # Verificar que el bot tiene acceso al canal
        me = await api_call(session, "getMe")
        if me.get("ok"):
            logger.info(f"Bot conectado: @{me['result']['username']}")
        else:
            logger.error(f"❌ Token inválido: {me}")
            return

        chat = await api_call(session, "getChat", {"chat_id": CHANNEL_ID})
        if chat.get("ok"):
            logger.info(f"Canal encontrado: {chat['result'].get('title', 'Sin título')}")
        else:
            logger.error(f"❌ No se puede acceder al canal: {chat}")
            return

        while True:
            try:
                result = await api_call(session, "getChatJoinRequests", {
                    "chat_id": CHANNEL_ID,
                    "limit": 100
                })

                if result.get("ok"):
                    requests = result.get("result", [])
                    if requests:
                        for req in requests:
                            user = req.get("from", {})
                            user_id = user.get("id")
                            name = user.get("first_name", "Desconocido")
                            if user_id:
                                approve = await api_call(session, "approveChatJoinRequest", {
                                    "chat_id": CHANNEL_ID,
                                    "user_id": user_id
                                })
                                if approve.get("ok"):
                                    logger.info(f"✅ Aprobado: {name} (ID: {user_id})")
                                else:
                                    logger.warning(f"⚠️ Error aprobando {name}: {approve}")
                    else:
                        logger.info("Sin solicitudes pendientes.")
                else:
                    logger.error(f"❌ Error API: {result}")

            except Exception as e:
                logger.error(f"❌ Error inesperado: {e}")

            await asyncio.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    asyncio.run(auto_aprobar())
