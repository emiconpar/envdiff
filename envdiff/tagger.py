"""Tag environment variables with user-defined labels or categories."""

from typing import Dict, List, Optional


def tag_keys(
    env: Dict[str, str],
    tag_map: Dict[str, List[str]],
) -> Dict[str, List[str]]:
    """Return a mapping of key -> list of tags assigned to it.

    Args:
        env: The environment dict whose keys will be tagged.
        tag_map: A dict of {tag_name: [key1, key2, ...]} defining which keys
                 belong to each tag.

    Returns:
        A dict of {key: [tag, ...]} for every key that appears in *env*.
        Keys with no matching tags receive an empty list.
    """
    result: Dict[str, List[str]] = {key: [] for key in env}
    for tag, keys in tag_map.items():
        for key in keys:
            if key in result:
                result[key].append(tag)
    return result


def keys_for_tag(
    tagged: Dict[str, List[str]],
    tag: str,
) -> List[str]:
    """Return all keys that carry *tag*."""
    return [key for key, tags in tagged.items() if tag in tags]


def all_tags(tagged: Dict[str, List[str]]) -> List[str]:
    """Return a sorted, deduplicated list of every tag present in *tagged*."""
    seen: set = set()
    for tags in tagged.values():
        seen.update(tags)
    return sorted(seen)


def filter_by_tag(
    env: Dict[str, str],
    tagged: Dict[str, List[str]],
    tag: str,
) -> Dict[str, str]:
    """Return a subset of *env* containing only keys that carry *tag*."""
    matching = set(keys_for_tag(tagged, tag))
    return {k: v for k, v in env.items() if k in matching}


def untagged_keys(
    tagged: Dict[str, List[str]],
) -> List[str]:
    """Return keys that have no tags assigned."""
    return [key for key, tags in tagged.items() if not tags]
