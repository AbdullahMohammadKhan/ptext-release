import json
import logging
import unittest
from pathlib import Path

from ptext.action.text.stop_words import ENGLISH_STOP_WORDS
from ptext.action.text.tf_idf_keyword_extraction import (
    TFIDFKeywordExtraction,
)
from ptext.pdf.pdf import PDF
from test.base_test import BaseTest

logging.basicConfig(filename="test_extract_keywords.log", level=logging.DEBUG)


class TestExtractKeywords(BaseTest):
    """
    This test attempts to extract the keywords (TF-IDF)
    from each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("keywords")

    def test_single_document(self):
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = TFIDFKeywordExtraction(ENGLISH_STOP_WORDS)
            doc = PDF.loads(pdf_file_handle, [l])

            # export txt
            output_file = self.output_dir / (file.stem + ".json")
            with open(output_file, "w") as json_file_handle:
                json_file_handle.write(
                    json.dumps(
                        [x.__dict__ for x in l.get_keywords_per_page(0, 5)], indent=4
                    )
                )


if __name__ == "__main__":
    unittest.main()
