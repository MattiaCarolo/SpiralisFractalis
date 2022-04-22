import numpy as np

## Built-In Transformations
def Scale(s:float):
    return np.array([[s, 0, 0],[0, s, 0],[0, 0, 1]], dtype=np.float64)
def Translate(a:float, b:float):
    return np.array([[1, 0, a],[0, 1, b],[0, 0, 1]], dtype=np.float64)
def Rotate(theta:float):
    return np.array([[np.cos(theta), -np.sin(theta), 0],[np.sin(theta), np.cos(theta), 0],[0, 0, 1]], dtype=np.float64)
def ShearX(t:float):
    return np.array([[1, t, 0],[0,1, 0],[0, 0, 1]], dtype=np.float64)
def ShearY(t:float):
    return np.array([[1, 0, 0],[t,1, 0],[0, 0, 1]], dtype=np.float64)
def ScaleX(s:float):
    return np.array([[s, 0, 0],[0, 1, 0],[0, 0, 1]], dtype=np.float64)
def ScaleY(s:float):
    return np.array([[1, 0, 0],[0, s, 0],[0, 0, 1]], dtype=np.float64)
def ScaleXY(s:float, t:float):
    return np.array([[s, 0, 0],[0,t, 0],[0, 0, 1]], dtype=np.float64)