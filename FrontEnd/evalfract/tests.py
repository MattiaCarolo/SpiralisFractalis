from django.test import TestCase

# Create your tests here.
def transformation_to_string(transformations):
    t = []
    for ts in transformations:
        t.append(f"{str(ts)[1:-1]}")
    return ';'.join(t)

def string_to_transformations(string):
    res = []
    for s in string.split(';'):
        res.append([float(x) for x in s.split(',')])
    return res

print(transformation_to_string([[1,2,3],[5,6,7],[8, 9, 10]]))
print(string_to_transformations("1, 2, 3;5, 6, 7;8, 9, 10"))