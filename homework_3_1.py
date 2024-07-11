from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s' )
logger = logging.getLogger(__name__)

def create_extension_dir(extension, target_dir):
    extension_dir = target_dir / extension
    if not extension_dir.exists():
        extension_dir.mkdir(parents=True)
        logger.info(f"Створено директорію: {extension_dir}")
    return extension_dir

def copy_file(item, target_dir, extension_dirs):
    try:
        extension = item.suffix[1:] if item.suffix.startswith('.') else item.suffix
        if extension not in extension_dirs:
            extension_dirs[extension] = create_extension_dir(extension, target_dir)
        target_file_path = extension_dirs[extension] / item.name
        shutil.copy(item, target_file_path)
        logger.info(f"Скопійовано файл {item} до {target_file_path}")
    except Exception as e:
        logger.error(f"Помилка під час копіювання файлу {item}: {e}")

def process_directory(source_dir, target_dir, extension_dirs):
    try:
        with ThreadPoolExecutor() as executor:
            futures = []
            for item in source_dir.iterdir():
                if item.is_file():
                    futures.append(executor.submit(copy_file, item, target_dir, extension_dirs))
                elif item.is_dir():
                    logger.info(f"Обробка директорії: {item}")
                    futures.append(executor.submit(process_directory, item, target_dir, extension_dirs))
            for future in as_completed(futures):
                future.result()
    except Exception as e:
        logger.error(f"Помилка під час обробки директорії {source_dir}: {e}")

def sort_dir(source_dir, target_dir='dist'):
    source_dir = Path(source_dir)
    target_dir = Path(target_dir)
    
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
        logger.info(f"Створено директорію: {target_dir}")
    
    extension_dirs = {}
    
    try:
        process_directory(source_dir, target_dir, extension_dirs)
    except Exception as e:
        logger.error(f"Помилка під час сортування директорії: {e}")

sort_dir('./pictures')
