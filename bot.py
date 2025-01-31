import logging
import asyncio
from binance.client import AsyncClient
from binance.streams import BinanceSocketManager

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('bot_logs.txt'), logging.StreamHandler()])

class CryptoBot:
    def __init__(self):
        self.client = None
        self.symbols = ['BTCUSDT', 'ETHUSDT']  # Liste des paires à surveiller

    async def handle_socket(self, ts):
        try:
            async for message in ts:
                logging.info(f"Message reçu pour {ts}: {message}")
                # Ajoute ton traitement ici (extraction de données, prises de décisions, etc.)
        except asyncio.CancelledError:
            logging.warning(f"WebSocket annulé pour {ts}")
        except Exception as e:
            logging.error(f"Erreur dans le WebSocket {ts}: {e}")

    async def run_bot(self):
        try:
            logging.info("🔌 Connexion à Binance...")
            self.client = await AsyncClient.create('BINANCE_API_KEY', 'BINANCE_SECRET')  # Remplace par tes clés API
            logging.info("✅ Connecté à Binance!")
            
            bm = BinanceSocketManager(self.client)
            sockets = []
            tasks = []
            
            # Test avec une seule paire d'actifs pour vérifier la connexion
            for symbol in self.symbols:
                ts = bm.depth_socket(symbol)
                sockets.append(ts)
                task = asyncio.create_task(self.handle_socket(ts))
                tasks.append(task)
            
            logging.info("👂 En écoute des données...")
            await asyncio.gather(*tasks)
            
        except asyncio.CancelledError:
            logging.warning("⛔ Tâches annulées.")
        except Exception as e:
            logging.error(f"Erreur dans le bot : {e}")
        finally:
            logging.info("🔒 Fermeture de la connexion...")
            if self.client:
                await self.client.close_connection()
                logging.info("✅ Connexion fermée.")

async def main():
    bot = CryptoBot()
    try:
        logging.info("🚀 Démarrage du bot...")
        await bot.run_bot()
    except KeyboardInterrupt:
        logging.info("\n🛑 Arrêt demandé...")
    finally:
        if bot.client:
            await bot.client.close_connection()
        logging.info("✅ Bot arrêté proprement.")

if __name__ == "__main__":
    asyncio.run(main())
