import io
import os
import pathlib
import re
import typing
from decimal import Decimal
from typing import List, Optional

from ptext.io.transform.types import (
    List,
)
from ptext.pdf.canvas.font.font import Font
from ptext.pdf.canvas.font.font_descriptor import FontDescriptor


class AdobeFontMetrics:
    """
    ASCII text-based font format developed by Adobe; stores font metric data for a Type 1 PostScript file;
    contains the master design of a specific font, which defines the way each character of the font looks.
    """

    _font_cache = {}

    @staticmethod
    def get(name: str) -> Optional[Font]:
        """
        Get the Font (only the metrics will be filled in) with a given name
        """
        # standardize names
        canonical_name = re.sub("[^A-Z]+", "", name.upper())

        # find all available afm files
        parent_dir = pathlib.Path(__file__).parent
        available_font_metrics = [
            (re.sub("[^A-Z]+", "", x.upper()[:-4]), x)
            for x in os.listdir(parent_dir)
            if x.endswith(".afm")
        ]

        # check whether given name is present
        afm_file_name = [x for x in available_font_metrics if x[0] == canonical_name]
        afm_file_name = None if len(afm_file_name) == 0 else afm_file_name[0][1]
        if afm_file_name is None:
            return None

        # read file
        if afm_file_name not in AdobeFontMetrics._font_cache:
            with open(parent_dir / afm_file_name, "r") as afm_file_handle:
                AdobeFontMetrics._font_cache[
                    afm_file_name
                ] = AdobeFontMetrics._read_file(afm_file_handle)

        # read cache
        if afm_file_name in AdobeFontMetrics._font_cache:
            return AdobeFontMetrics._font_cache[afm_file_name]

        # default
        return None

    @staticmethod
    def _read_file(input: io.IOBase) -> Optional[Font]:
        lines = [x for x in input.readlines() if not x.startswith("Comment")]
        lines = [x[:-1] if x.endswith("\n") else x for x in lines]

        # check first/last line
        if not lines[0].startswith("StartFontMetrics") or not lines[-1].startswith(
            "EndFontMetrics"
        ):
            return None

        out_font = Font()

        # FontDescriptor
        out_font_descriptor = FontDescriptor().set_parent(out_font)
        out_font_descriptor["FontName"] = AdobeFontMetrics._find_and_parse_as_string(
            lines, "FontName"
        )
        out_font_descriptor["FontFamily"] = AdobeFontMetrics._find_and_parse_as_string(
            lines, "FamilyName"
        )
        # FontStretch
        # FontWeight
        # Flags
        # FontBBox
        # ItalicAngle
        out_font_descriptor["Ascent"] = AdobeFontMetrics._find_and_parse_as_float(
            lines, "Ascender"
        )
        out_font_descriptor["Descent"] = AdobeFontMetrics._find_and_parse_as_float(
            lines, "Descender"
        )
        # Leading
        out_font_descriptor["CapHeight"] = AdobeFontMetrics._find_and_parse_as_float(
            lines, "CapHeight"
        )
        out_font_descriptor["XHeight"] = AdobeFontMetrics._find_and_parse_as_float(
            lines, "XHeight"
        )
        # StemV
        out_font_descriptor["StemV"] = AdobeFontMetrics._find_and_parse_as_float(
            lines, "StemV"
        )
        # StemH
        out_font_descriptor["StemH"] = AdobeFontMetrics._find_and_parse_as_float(
            lines, "StemH"
        )
        # AvgWidth
        out_font_descriptor["AvgWidth"] = AdobeFontMetrics._find_and_parse_as_float(
            lines, "AvgWidth"
        )
        # MaxWidth
        out_font_descriptor["MaxWidth"] = AdobeFontMetrics._find_and_parse_as_float(
            lines, "MaxWidth"
        )
        # MissingWidth
        out_font_descriptor["MissingWidth"] = AdobeFontMetrics._find_and_parse_as_float(
            lines, "MissingWidth"
        )
        # FontFile
        # FontFile2
        # FontFile3
        out_font_descriptor["CharSet"] = AdobeFontMetrics._find_and_parse_as_integer(
            lines, "Characters"
        )

        # Font
        out_font["Type"] = "Font"
        out_font["Subtype"] = "Type1"
        out_font["Name"] = out_font_descriptor["FontName"]
        out_font["BaseFont"] = out_font_descriptor["FontName"]

        widths = List().set_parent(out_font)
        avg_char_width = 0
        avg_char_width_norm = 0
        first_char = None
        last_char = None

        char_metrics_lines = lines[
            lines.index(
                [x for x in lines if x.startswith("StartCharMetrics")][0]
            ) : lines.index("EndCharMetrics")
            + 1
        ]
        char_metrics_lines = char_metrics_lines[1:-1]
        for cml in char_metrics_lines:
            tmp = {
                y.split(" ")[0]: y.split(" ")[1]
                for y in [x.strip() for x in cml.split(";")]
                if " " in y
            }

            # determine char
            ch = -1
            if "C" in tmp:
                ch = int(tmp["C"])
            if "CH" in tmp:
                ch = int(tmp["CH"][1:-1], 16)

            if (first_char is None or ch < first_char) and ch != -1:
                first_char = ch
            if (last_char is None or ch > last_char) and ch != -1:
                last_char = ch

            w = float(tmp["WX"])
            if ch != -1 and w != 0:
                avg_char_width += w
                avg_char_width_norm += 1

            widths.append(Decimal(w))

        out_font["FirstChar"] = Decimal(first_char)
        out_font["LastChar"] = Decimal(last_char)
        out_font["Widths"] = widths

        if out_font_descriptor["AvgWidth"] is None:
            out_font_descriptor["AvgWidth"] = round(
                Decimal(avg_char_width / avg_char_width_norm), 2
            )
        if out_font_descriptor["MaxWidth"] is None:
            out_font_descriptor["MaxWidth"] = max(widths)
        out_font["FontDescriptor"] = out_font_descriptor

        # return
        return out_font

    @staticmethod
    def _find_line(lines: typing.List[str], key: str) -> Optional[str]:
        relevant_line = [x for x in lines if x.startswith(key)]
        if len(relevant_line) == 0:
            return None
        relevant_line = relevant_line[0][len(key) :]
        # trim white space
        while relevant_line[0] in [" ", "\t"]:
            relevant_line = relevant_line[1:]
        return relevant_line

    @staticmethod
    def _find_and_parse_as_string(lines: typing.List[str], key: str) -> Optional[str]:
        return AdobeFontMetrics._find_line(lines, key)

    @staticmethod
    def _find_and_parse_as_integer(lines: typing.List[str], key: str) -> Optional[int]:
        relevant_line = AdobeFontMetrics._find_line(lines, key)
        return int(relevant_line) if relevant_line is not None else None

    @staticmethod
    def _find_and_parse_as_float(lines: typing.List[str], key: str) -> Optional[float]:
        relevant_line = AdobeFontMetrics._find_line(lines, key)
        return float(relevant_line) if relevant_line is not None else None

    @staticmethod
    def _find_and_parse_as_bool(lines: typing.List[str], key: str) -> Optional[bool]:
        relevant_line = AdobeFontMetrics._find_line(lines, key)
        return (relevant_line.upper() == "TRUE") if relevant_line is not None else None
