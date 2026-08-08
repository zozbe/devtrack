import logging
import sys

# 1. Logger objesini oluşturuyoruz
logger = logging.getLogger("DevTrackLogger")
logger.setLevel(logging.INFO) # INFO, WARNING, ERROR ve CRITICAL seviyelerini yakalar

# 2. Logların nasıl görüneceğini (Formatını) belirliyoruz
# Örnek çıktı: 2026-08-08 17:45:12,345 - INFO - Görev başarıyla silindi.
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 3. Terminale (Konsola) yazdırmak için Handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 4. Dosyaya (devtrack.log) kaydetmek için Handler
file_handler = logging.FileHandler("devtrack.log", encoding="utf-8")
file_handler.setFormatter(formatter)

# 5. Handler'ları logger'a ekliyoruz (Çift loglamayı önlemek için kontrol yapıyoruz)
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)