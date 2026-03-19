from copy import deepcopy


def deepMerge(originalTheme, newTheme):
    if not isinstance(originalTheme, dict) or not isinstance(newTheme, dict):
        return deepcopy(newTheme)

    merged = deepcopy(originalTheme)
    for key, value in newTheme.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deepMerge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged
