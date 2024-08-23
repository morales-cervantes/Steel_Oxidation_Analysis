import numpy as np

def limites_probeta(bw, image):
    m, n = bw.shape

    print(f'bw shape: {bw.shape}')
    print(f'bw non-zero count: {np.count_nonzero(bw)}')

    # Calculos para determinar el limite inferior
    cont = 0
    lowlim = 0
    for i in range(m-10, 0, -1):
        if cont < 20:
            cont = 0
            for j in range(n):
                if bw[i, j] == 1:
                    cont += 1
                    lowlim = i

    # Calculos para determinar el limite superior
    cont = 0
    uplim = 0
    for i in range(5, lowlim - 1):
        if cont < 20:
            cont = 0
            for j in range(n):
                if bw[i, j] == 1:
                    cont += 1
                    uplim = i

    # Calculos para determinar los limites izquierdo y derecho
    izqlim = n
    derlim = 0
    for i in range(uplim, lowlim):
        for j in range(5, n - 5):
            if bw[i, j] == 1:
                if izqlim > j:
                    izqlim = j
                if derlim < j:
                    derlim = j

    print(f'uplim: {uplim}, lowlim: {lowlim}, izqlim: {izqlim}, derlim: {derlim}')

    # Se recorta la imagen filtrada del termograma original
    if uplim < lowlim and izqlim < derlim:
        image2 = image[uplim:lowlim, izqlim:derlim, :]
        m, n, p = image2.shape
    else:
        image2 = np.zeros_like(image)
        m, n, p = image2.shape

    return image2, m, n, p

