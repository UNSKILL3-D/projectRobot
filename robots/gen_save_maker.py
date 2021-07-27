def compile_generator(filename):
    import numpy as np
    inp = open('generator.py', 'r')
    gen_code = ''
    buf = '+'
    while buf != 'def generate():\n':
        buf = inp.readline()
    while buf:
        gen_code += buf
        buf = inp.readline()
    save = np.array(['dynamic', gen_code, 'default'], dtype=object)
    np.save(filename, save)
