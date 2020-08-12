

def read_interface(filename):
    """
    :param filename: file to read content of.
    :return float value of content.
    """
    with open(filename, 'r') as f:
        content = f.read()

    try:
        return float(content)
    except ValueError:
        return 0.0


def write_interface(filename, value):
    """
    :param filename to write to
    :param value to be written
    :return: None.
    """
    with open(filename, 'w') as f:
        f.write(str(value))

