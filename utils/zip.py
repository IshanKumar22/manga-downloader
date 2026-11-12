from os import path, walk
from zipfile import ZIP_DEFLATED, ZipFile


def zip_folder(folder_path, output_zip_path):
  # ZIP_DEFLATED is required to actually compress the files (default is ZIP_STORED)
    with ZipFile(output_zip_path, "w", ZIP_DEFLATED) as zipf:
        for root, dirs, files in walk(folder_path):
            for file in files:
                file_path = path.join(root, file)
                # Preserve relative folder structure inside the zip
                arcname = path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)
