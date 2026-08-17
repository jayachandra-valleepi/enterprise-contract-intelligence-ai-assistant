from __future__ import annotations

from typing import Any


class MetadataFilterBuilder:
    """
    Builds Pinecone metadata filters.

    Example:

        filter_builder = MetadataFilterBuilder()

        metadata_filter = (
            filter_builder
            .country("France")
            .document_type("contract")
            .build()
        )

    Result:

        {
            "$and": [
                {"country": {"$eq": "France"}},
                {"document_type": {"$eq": "contract"}}
            ]
        }
    """

    def __init__(self) -> None:

        self.conditions: list[dict[str, Any]] = []

    def country(
        self,
        country: str,
    ) -> "MetadataFilterBuilder":

        if country:
            self.conditions.append(
                {
                    "country": {
                        "$eq": country
                    }
                }
            )

        return self

    def region(
        self,
        region: str,
    ) -> "MetadataFilterBuilder":

        if region:
            self.conditions.append(
                {
                    "region": {
                        "$eq": region
                    }
                }
            )

        return self

    def document_type(
        self,
        document_type: str,
    ) -> "MetadataFilterBuilder":

        if document_type:
            self.conditions.append(
                {
                    "document_type": {
                        "$eq": document_type
                    }
                }
            )

        return self

    def document_id(
        self,
        document_id: str,
    ) -> "MetadataFilterBuilder":

        if document_id:
            self.conditions.append(
                {
                    "document_id": {
                        "$eq": document_id
                    }
                }
            )

        return self

    def s3_key(
        self,
        s3_key: str,
    ) -> "MetadataFilterBuilder":

        if s3_key:
            self.conditions.append(
                {
                    "s3_key": {
                        "$eq": s3_key
                    }
                }
            )

        return self

    def add(
        self,
        field: str,
        value: Any,
    ) -> "MetadataFilterBuilder":

        if not field:
            raise ValueError(
                "Metadata field is required."
            )

        self.conditions.append(
            {
                field: {
                    "$eq": value
                }
            }
        )

        return self

    def build(self) -> dict[str, Any]:
        """
        Build a Pinecone-compatible metadata filter.
        """

        if not self.conditions:
            return {}

        if len(self.conditions) == 1:
            return self.conditions[0]

        return {
            "$and": self.conditions
        }

    def clear(
        self,
    ) -> "MetadataFilterBuilder":

        self.conditions.clear()

        return self