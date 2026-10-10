"""Generic synthetic fixture: add one to each number, with optional metadata."""

def transform(values):
    return [value + 1 for value in values]


def attach_metadata(values, metadata):
    return {"values": values, "metadata": metadata}


def prepare(values, metadata=None, use_metadata=False):
    result = transform(values)
    if use_metadata and metadata is not None:
        return attach_metadata(result, metadata)
    return {"values": result, "metadata": None}
