def pretty_print(string, minlen=10):
    if type(string) in [type(0), type(0.0)]:
        string = str(int(string))
    else:
        string = string[:2] + ';'.join(string.split(' ')[1:])
    return string+' '*(minlen-len(string))
