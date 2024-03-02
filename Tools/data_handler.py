def split_and_validate_extensions(extensions_string):
    extensions = extensions_string.strip().split(",")
    valid_extensions = []
    for extension in extensions:
        if len(extension) < 2 or extension[0] != ".":
            raise ValueError(f"Invalid extension: '{extension}'. Extensions must start with a dot (.) and cannot be empty.")
        valid_extensions.append(extension[1:])  # Remove the leading dot
    return valid_extensions
