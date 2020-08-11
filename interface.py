

def read_interface(filename):

    with open(filename, 'r') as f:
        content = f.read()

    try:
        return float(content)
    except ValueError:
        return 0.0


def write_interface(filename, value):
    print(filename, value)
    with open(filename, 'w') as f:

        f.write(str(value))

