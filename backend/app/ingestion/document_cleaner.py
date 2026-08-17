from __future__ import annotations

import re
import unicodedata


class DocumentCleaner:
    """
    Cleans extracted document text before chunking.
    """

    def clean(
        self,
        text: str,
    ) -> str:

        if not text:
            return ""

        # Normalize Unicode.
        text = unicodedata.normalize(
            "NFKC",
            text,
        )

        # Normalize line endings.
        text = text.replace(
            "\r\n",
            "\n",
        )

        text = text.replace(
            "\r",
            "\n",
        )

        # Remove null characters.
        text = text.replace(
            "\x00",
            "",
        )

        # Remove excessive spaces/tabs.
        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        # Remove spaces at the beginning/end of lines.
        text = re.sub(
            r"^[ \t]+|[ \t]+$",
            "",
            text,
            flags=re.MULTILINE,
        )

        # Reduce excessive blank lines.
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        return text.strip()