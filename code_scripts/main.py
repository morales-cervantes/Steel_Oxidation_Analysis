import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import color, filters
from segment_colors import segment_colors
from limites_probeta import limites_probeta
from oxidation import oxidation

def mostrar_imagen(titulo, imagen, cmap=None):
    plt.figure(figsize=(10, 8))
    if cmap:
        plt.imshow(imagen, cmap=cmap)
    else:
        plt.imshow(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
    plt.title(titulo)
    plt.axis('off')
    plt.show()

def mostrar_matriz(matriz, titulo):
    plt.figure(figsize=(10, 8))
    plt.imshow(matriz, cmap='gray')
    plt.title(titulo)
    plt.colorbar()
    plt.show()

# Limpiar datos y cerrar ventanas (equivalente en Python no necesario)

# Abrir archivo desde nombre dado
file_name = 't8.tiff'
img = cv2.imread(file_name)
mostrar_imagen('Imagen original', img)

# Detección de bordes
h = np.ones((3, 3), np.float32) / 9  # mascara para filtro promedio
image = cv2.filter2D(img, -1, h)  # se filtra la imagen original
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # se convierte a escala de grises
edges = filters.sobel(gray_image)  # se aplica sobel para segmentar

# Normalizar la matriz de edges para que esté en el rango 0-255
edges_normalized = (edges - edges.min()) / (edges.max() - edges.min())
edges_scaled = (edges_normalized * 255).astype(np.uint8)

# Mostrar la matriz resultante de Sobel normalizada
mostrar_matriz(edges_scaled, 'Matriz Resultante de Sobel (Normalizada)')

# Elegir un umbral adecuado (esto lo puedes ajustar según la visualización de la matriz)
umbral = 70  # Este valor puedes ajustarlo después de ver los resultados

# Convertir edges a una matriz binaria utilizando el umbral elegido
bw = (edges_scaled > umbral).astype(np.uint8)
mostrar_imagen('Bordes Binarios', bw, cmap='gray')

# Calculos para determinar limites de la probeta
image2, m, n, p = limites_probeta(bw, image)

if image2.shape[0] > 0 and image2.shape[1] > 0:
    mostrar_imagen('Área de interés', image2)
else:
    print("Recorte inválido de la imagen.")

# Segmentar fondo en CIE L*a*b
image3, fondo = segment_colors(image2, False)
mostrar_imagen('Área de interés sin fondo', image3)
mostrar_imagen('Fondo', fondo)

# Determinar puntos de oxidación
image_oxido, image_sin_oxido, oxido_percentage = oxidation(image3, offset=1, sens=5)


mostrar_imagen('Sin óxido', image_sin_oxido)
mostrar_imagen('Óxido', image_oxido)
print(f'Porcentaje de óxido: {oxido_percentage:.2f}%')



