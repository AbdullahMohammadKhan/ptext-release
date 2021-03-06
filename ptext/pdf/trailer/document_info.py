from typing import Optional, List


class DocumentInfo:
    def __init__(self, document: "Document"):
        super().__init__()
        self.document = document

    def get_title(self) -> Optional[str]:
        """
        (Optional; PDF 1.1) The document’s title.
        """
        try:
            return self.document["XRef"]["Trailer"]["Info"]["Title"]
        except:
            return None

    def get_creator(self) -> Optional[str]:
        """
        (Optional) If the document was converted to PDF from another format,
        the name of the conforming product that created the original document
        from which it was converted.
        """
        try:
            return self.document["XRef"]["Trailer"]["Info"]["Creator"]
        except:
            return None

    def get_author(self) -> Optional[str]:
        """
        (Optional; PDF 1.1) The name of the person who created the document.
        """
        try:
            return self.document["XRef"]["Trailer"]["Info"]["Author"]
        except:
            return None

    def get_creation_date(self) -> Optional[str]:
        """
        (Optional) The date and time the document was created, in human-
        readable form (see 7.9.4, “Dates”).
        """
        try:
            return self.document["XRef"]["Trailer"]["Info"]["CreationDate"]
        except:
            return None

    def get_modification_date(self) -> Optional[str]:
        """
        Required if PieceInfo is present in the document catalogue;
        otherwise optional; PDF 1.1) The date and time the document was
        most recently modified, in human-readable form (see 7.9.4, “Dates”).
        """
        try:
            return self.document["XRef"]["Trailer"]["Info"]["ModDate"]
        except:
            return None

    def get_subject(self) -> Optional[str]:
        """
        (Optional; PDF 1.1) The subject of the document.
        """
        try:
            return self.document["XRef"]["Trailer"]["Info"]["Subject"]
        except:
            return None

    def get_keywords(self) -> Optional[List[str]]:
        """
        (Optional; PDF 1.1) Keywords associated with the document.
        """
        try:
            return self.document["XRef"]["Trailer"]["Info"]["Keywords"]
        except:
            return None

    def get_producer(self) -> Optional[str]:
        """
        (Optional) If the document was converted to PDF from another format,
        the name of the conforming product that converted it to PDF.
        """
        try:
            return self.document["XRef"]["Trailer"]["Info"]["Producer"]
        except:
            return None

    def get_number_of_pages(self) -> Optional[int]:
        return self.document.get["XRef"]["Trailer"]["Root"]["Pages"]["Count"]

    def get_file_size(self) -> Optional[int]:
        return int(self.document.get("FileSize"))

    def get_ids(self) -> Optional[List[str]]:
        """
        File identifiers shall be defined by the optional ID entry in a PDF file’s trailer dictionary (see 7.5.5, “File Trailer”).
        The ID entry is optional but should be used. The value of this entry shall be an array of two byte strings. The
        first byte string shall be a permanent identifier based on the contents of the file at the time it was originally
        created and shall not change when the file is incrementally updated. The second byte string shall be a
        changing identifier based on the file’s contents at the time it was last updated. When a file is first written, both
        identifiers shall be set to the same value. If both identifiers match when a file reference is resolved, it is very
        likely that the correct and unchanged file has been found. If only the first identifier matches, a different version
        of the correct file has been found.
        """
        if (
            "XRef" in self.document
            and "Trailer" in self.document["XRef"]
            and "ID" in self.document["XRef"]["Trailer"]
        ):
            return self.document["XRef"]["Trailer"]["ID"]
        return None

    def get_language(self) -> Optional[str]:
        """
        (Optional; PDF 1.4) A language identifier that shall specify the
        natural language for all text in the document except where
        overridden by language specifications for structure elements or
        marked content (see 14.9.2, "Natural Language Specification"). If
        this entry is absent, the language shall be considered unknown.
        """
        try:
            return self.document["XRef"]["Trailer"]["Root"]["Lang"]
        except:
            return None
