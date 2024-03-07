'''Used to watch the work directory for new files and process them'''

import os
import threading
import time
from mgxhub.config import cfg
from mgxhub.handler import FileHandler, DBHandler
from mgxhub.logger import logger


class RecordWatcher:
    '''Watches the work directory for new files and processes them'''

    def __init__(self):
        self.work_dir = cfg.get('system', 'uploaddir')
        os.makedirs(self.work_dir, exist_ok=True)

        if self.work_dir and os.path.isdir(self.work_dir):
            logger.info(f"[Watcher] Monitoring directory: {self.work_dir}")
            self.thread = threading.Thread(target=self._watch, daemon=True)
            self.thread.start()

    def _watch(self):
        '''Watch the work directory for new files and process them'''

        thread_db = DBHandler()
        while True:
            for filename in os.listdir(self.work_dir):
                file_path = os.path.join(self.work_dir, filename)
                logger.info(f"[Watcher] Found file: {file_path}")
                file_handler = FileHandler(file_path, delete_after=True, db_handler=thread_db)
                try:
                    file_handler.process()
                    time.sleep(0.05)
                except Exception as e:
                    logger.error(f"[Watcher] Error processing file [{file_path}]: {e}")
                    time.sleep(5)
                    continue
                else:
                    logger.debug(f"[Watcher] Processed file [{file_path}]")
            time.sleep(1)
