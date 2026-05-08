from pathlib import Path

from utils.logger import logger


def write_file(path: str, content: str):
    """
    Write content to a file.
    Creates parent directories automatically.
    """

    try:
        file_path = Path(path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"File written successfully: {path}")

        return True

    except Exception as e:
        logger.error(f"Failed to write file {path}: {e}")

        return False
