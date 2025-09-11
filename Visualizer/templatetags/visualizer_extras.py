from django import template

register = template.Library()


@register.filter(name="split")
def split_filter(value, delimiter=","):
    """
    Split a string into a list for template iteration.

    - Default delimiter is comma.
    - Trims whitespace around parts.
    - Ignores empty parts.
    - If value is None, returns an empty list.
    - If value is an iterable like list/tuple, return a cleaned version.
    """
    if value is None:
        return []

    if isinstance(value, (list, tuple)):
        return [str(x).strip() for x in value if str(x).strip() != ""]

    try:
        s = str(value)
        if delimiter is None:
            parts = [s]
        else:
            parts = s.split(delimiter)
        cleaned = [p.strip() for p in parts]
        return [p for p in cleaned if p != ""]
    except Exception:
        return []

@register.filter(name="has_number_all")
def has_number_filter(value, lotto_numbers):
    if str(value) in lotto_numbers.split(","):
        return True
    else:
        return False

@register.filter(name="has_number_exclude_special")
def has_number_filter(value, lotto_numbers):
    if str(value) in lotto_numbers.split(",")[:-1]:
        return True
    else:
        return False

@register.filter(name="has_special_number")
def has_special_number_filter(value, lotto_numbers):
    if str(value) == lotto_numbers.split(",")[-1]:
        return True
    else:
        return False