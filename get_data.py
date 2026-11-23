"""Download the Olist dataset from Kaggle into data/raw/."""
import shutil
from pathlib import Path

import kagglehub

DEST = Path("data/raw")


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    src = Path(kagglehub.dataset_download("olistbr/brazilian-ecommerce"))
    for csv in sorted(src.glob("*.csv")):
        shutil.copy2(csv, DEST / csv.name)
        print(f"copied {csv.name}")


if __name__ == "__main__":
    main()