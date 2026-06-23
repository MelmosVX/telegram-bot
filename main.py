import asyncio
import logging
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

async def get_join_requests(session):
    url = f"{BASE_URL}/getChatJoinRequests"
    params = {"chat_id": CHANNEL_ID, "limit": 100}
    async with session.get(url, params=params) as resp:
        text = await resp.text()
        import json
        data = json.loads(text)
        if data.get("ok"):
            return data.get("result", [])
        else:
            logger.error(f"Error obteniendo solicitudes: {data}")
            return []

async def approve_request(session, user_id):
    url = f"{BASE_URL}/approveChatJoinRequest"
    params = {"chat_id": CHANNEL_ID, "user_id": user_id}
    async with session.post(url, params=params) as resp:
        import json
        text = await resp.text()
        data = json.loads(text)
        return data.get("ok", False)

async def auto_aprobar():
    logger.info("✅ Bot iniciado. Comprobando solicitudes cada 60 segundos...")
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                requests = await get_join_requests(session)
                if requests:
                    for req in requests:
                        user = req.get("from", {})
                        user_id = user.get("id")
                        name = user.get("first_name", "Desconocido")
                        if user_id:
                            ok = await approve_request(session, user_id)
                            if ok:
                                logger.info(f"✅ Aprobado: {name} (ID: {user_id})")
                            else:
                                logger.warning(f"⚠️ No se pudo aprobar: {name}")
                else:
                    logger.info("Sin solicitudes pendientes.")
            except Exception as e:
                logger.error(f"❌ Error inesperado: {e}")

            await asyncio.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    asyncio.run(auto_aprobar())
