

def read_interface(filename):
    content = ""
    with open(filename, 'r') as f:
        content = f.read()

    try:
        setting = float(content)
        return setting
    except ValueError:
        return "Error"


def write_interface(filename, value):
    with open(filename, 'w') as f:
        f.write(str(value))

