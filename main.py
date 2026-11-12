from pathlib import Path
from pprint import pprint
from tempfile import TemporaryDirectory

from sources import Asura
from utils.download import download
from utils.zip import zip_folder

PARENT = Path(__file__).resolve().parent
OUTPUT_FOLDER = PARENT / "output"
OUTPUT_FOLDER.mkdir(exist_ok=True)


def main():
    series = Asura.search_series(Asura, "star embracing")[0]
    chapters = series.get_chapters()
    latest_ch = chapters[0]
    pages = latest_ch.get_pages()
    
    s_title, ch_name = latest_ch.name()
    
    with TemporaryDirectory() as tempdir:
        temp = Path(tempdir)
        for i, page in enumerate(pages):
            download(page, temp / f"{i+1}.webp")
            
        SERIES_FOLDER = OUTPUT_FOLDER / s_title
        SERIES_FOLDER.mkdir(exist_ok=True)
        zip_folder(temp, SERIES_FOLDER / f"{ch_name}.zip")
    
    print(f"DOWNLOADED: {s_title} {ch_name}")


if __name__ == "__main__":
    main()
