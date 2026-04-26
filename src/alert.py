# Alerting Module
# Sends notifications when automation fails

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AlertSystem:
    def __init__(self, config_loader):
        self.config = config_loader.get_alert_config()
    
    def critical_alert(self, message):
        logger.critical(f"CRITICAL: {message}")
        print(f"\n!!! ALERT: {message} !!!\n")
    
    def info_alert(self, message):
        logger.info(f"INFO ALERT: {message}")
        print(f"[INFO] {message}")