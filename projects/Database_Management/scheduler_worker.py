# ==============================================================================
# File        : scheduler_worker.py
# Location    : /data/database-management/scheduler_worker.py
# Purpose     : APScheduler background worker - triggers periodic health-check collection for all registered servers.
# Author      : Madan U
# Email       : madan.u@kotak.com
# Created On  : 2026-09-07
# Last Update : 2026-09-07
# ==============================================================================

import time
from app import app
from services.monitoring_service import sweep_all_servers

def run_scheduler():
    with app.app_context():
        print("Scheduler started... Fetching live data.")
        while True:
            try:
                # ಈಗ ಸರಿಯಾದ ಫಂಕ್ಷನ್ ಕರೆಯುತ್ತಿದ್ದೇವೆ
                sweep_all_servers()
                print("Health checks completed successfully.")
            except Exception as e:
                print(f"Error in scheduler: {e}")
            
            # ಪ್ರತಿ 5 ನಿಮಿಷಕ್ಕೊಮ್ಮೆ (300 seconds) ರನ್ ಆಗಲು
            time.sleep(300) 

if __name__ == "__main__":
    run_scheduler()
