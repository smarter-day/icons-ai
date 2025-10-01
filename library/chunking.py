"""Chunking and batching helper functions."""

from typing import Any, Callable


def next_chunk_size(
    items: list, fits_context: Callable[[list], bool]
) -> int:
    """
    Determines the maximum number of items that can be processed without
    exceeding constraints.

    Args:
        items: List of items to process
        fits_context: Callable that takes a list and returns True if it fits
                     within constraints

    Returns:
        Maximum number of items that can be processed together
    """
    chunk: list[Any] = []
    for item in items:
        test_chunk = chunk + [item]
        if not fits_context(test_chunk):
            break
        chunk = test_chunk
    return len(chunk)
