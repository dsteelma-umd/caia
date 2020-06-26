import json
import logging
from typing import Dict, List

from caia.core.step import Step, StepResult
from caia.items.source_items import SourceItems

logger = logging.getLogger(__name__)


def parse_item(item_from_source: Dict[str, str], suppress_null_values: bool) -> Dict[str, str]:
    """
    Converts source map into a destination map, sending all keys in the source
    to the destination.

    If "suppress_nulls" is True, any keys with null values will _not_ be
    sent in the destination request.
    """

    # The source (Alephh) may send undocumented keys to the destination
    # (CaiaSoft), so include all keys from the source to the destinatble
    item_map = {}
    for source_key in item_from_source:
        source_value = item_from_source[source_key]
        if suppress_null_values and source_value is None:
            continue

        item_map[source_key] = item_from_source[source_key]

    return item_map


class CreateDestNewItemsRequest(Step):
    """
    Constructs the POST request body to send to the destination
    """
    def __init__(self, source_items: SourceItems):
        self.source_items = source_items
        self.errors: List[str] = []

    def execute(self) -> StepResult:
        items_array = []

        new_items = self.source_items.get_new_items()
        for item in new_items:
            items_array.append(parse_item(item, False))

        request_body = {"incoming": items_array}
        json_str = json.dumps(request_body)

        step_result = StepResult(True, json_str)
        return step_result

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"


class CreateDestUpdatedItemsRequest(Step):
    """
    Constructs the POST request body to send to the destination
    """
    def __init__(self, source_items: SourceItems):
        self.source_items = source_items
        self.errors: List[str] = []

    def execute(self) -> StepResult:
        items_array = []

        new_items = self.source_items.get_updated_items()
        for item in new_items:
            items_array.append(parse_item(item, False))

        request_body = {"items": items_array}
        json_str = json.dumps(request_body)

        step_result = StepResult(True, json_str)
        return step_result

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
