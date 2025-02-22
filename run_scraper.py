import subprocess
import datetime

# Générer un fichier de log avec la date du jour
log_file = f"logs/scraper_{datetime.datetime.now().strftime('%Y-%m-%d')}.log"

# Exécuter Scrapy et stocker les logs
with open(log_file, "w") as f:
    subprocess.run(["scrapy", "crawl", "ceetiz"], stdout=f, stderr=f)