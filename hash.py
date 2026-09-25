def your_function(...):
    """..."""
    sha256 = ...  # compute the file's SHA-256 using the section 2.5 pattern
    port_status_result = port_status(...)  # use Technique 8's helper

    return {
        "sha256": sha256,
        "port_status": port_status_result,
    }
