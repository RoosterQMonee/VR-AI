from compile import cmake, obj, import_library

cmake("./lib","cpy")
lib = import_library("./lib/cpy.so")

mn = obj(lib)
fin = mn.exc()
