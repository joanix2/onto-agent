from slugify import slugify

def to_snake_case(text: str) -> str:
    return slugify(text, separator="_")