import io
import typing
from typing import Union, Any, Optional

from ptext.io.transform.base_transformer import BaseTransformer, TransformerContext
from ptext.io.transform.types import List, AnyPDFType
from ptext.pdf.canvas.event.event_listener import EventListener


class DefaultArrayTransformer(BaseTransformer):
    """
    This implementation of BaseTransformer converts a PDFArray to a List
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return isinstance(object, List)

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[TransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        # create root object
        tmp = List().set_parent(parent_object)

        # add listener(s)
        for l in event_listeners:
            tmp.add_event_listener(l)

        # transform child(ren)
        for i in range(0, len(object_to_transform)):
            tmp.append(
                self.get_root_transformer().transform(
                    object_to_transform[i], tmp, context, []
                )
            )

        # return
        return tmp
