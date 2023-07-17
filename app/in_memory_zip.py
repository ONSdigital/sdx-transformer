from io import BytesIO
from typing import Any, Self
from zipfile import ZIP_DEFLATED, ZipFile


class InMemoryZip:
    """Class for creating in memory Zip objects using BytesIO."""
    def __init__(self):
        self._in_memory_zip = BytesIO()

    def append(self, filename_in_zip: str, file_contents: Any) -> Self:
        """Appends a file with name filename_in_zip and contents of
        file_contents to the in-memory zip."""
        # Get a handle to the in-memory zip in append mode
        zf = ZipFile(self._in_memory_zip, "a", ZIP_DEFLATED, False)

        # Write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)
        zf.close()
        return self

    def get(self) -> BytesIO:
        """Rewind current file position to the start of in memory file"""
        self._in_memory_zip.seek(0)
        return self._in_memory_zip

    def get_filenames(self) -> list[str]:
        """Returns a list of filenames currently in the zipfile"""
        zf = ZipFile(self._in_memory_zip, "r", ZIP_DEFLATED, False)
        file_names = zf.namelist()
        zf.close()
        return file_names
