from pathlib import Path

import zipfile
import requests

from loguru import logger
from tqdm import tqdm
import typer

from ml_model.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    # ----------------------------------------------
):
    # Create directories if they don't exist
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensured directories exist: {RAW_DATA_DIR} and {PROCESSED_DATA_DIR}")
    
    # Download and extract dataset from Google Drive
    google_drive_id = "1FLaTRGOXZ1Nz3H7npW2Sq5c4vzgEt3aE"
    download_url = f"https://drive.google.com/uc?export=download&id={google_drive_id}"
    zip_file_path = RAW_DATA_DIR / "dataset.zip"
    
    logger.info("Downloading dataset from Google Drive...")
    
    try:
        # Download the file with progress bar
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        with open(zip_file_path, 'wb') as file, tqdm(
            desc="Downloading",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))
        
        logger.info(f"Downloaded dataset to: {zip_file_path}")
        
        # Extract the zip file
        logger.info("Extracting zip file...")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(RAW_DATA_DIR)
        
        logger.success(f"Dataset extracted to: {RAW_DATA_DIR}")
        
        # Optionally remove the zip file after extraction
        zip_file_path.unlink()
        logger.info("Removed zip file after extraction")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading file: {e}")
        raise
    except zipfile.BadZipFile as e:
        logger.error(f"Error extracting zip file: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Processing dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Processing dataset complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
