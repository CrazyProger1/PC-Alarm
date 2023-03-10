def join_by(*parts, by='.'):
    result = ''

    for part in parts:
        part: str = part.strip().removesuffix(by).removeprefix(by)
        result += part + by

    return result.removesuffix(by)


