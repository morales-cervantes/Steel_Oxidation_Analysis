import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import color, filters
from segment_colors import segment_colors
from limites_probeta import limites_probeta
from oxidation import oxidation
import pandas as pd

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

def seleccionar_puntos(imagen):
    puntos = []
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            puntos.append((x, y))
            cv2.circle(imagen, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow('Selecciona puntos', imagen)

    cv2.imshow('Selecciona puntos', imagen)
    cv2.setMouseCallback('Selecciona puntos', mouse_callback)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return puntos

def crear_mascara(puntos, shape):
    mask = np.zeros(shape[:2], dtype=np.uint8)
    puntos_np = np.array(puntos, dtype=np.int32)
    cv2.fillPoly(mask, [puntos_np], 1)
    return mask

def seleccionar_multiples_poligonos(imagen):
    mascaras = []
    while True:
        print("Selecciona un polígono. Presiona 'q' para terminar.")
        puntos = seleccionar_puntos(imagen.copy())
        if not puntos:
            break
        mascara = crear_mascara(puntos, imagen.shape)
        mascaras.append(mascara)
        key = cv2.waitKey(0)
        if key == ord('q'):
            break
    if mascaras:
        mascara_total = np.bitwise_or.reduce(mascaras)
    else:
        mascara_total = np.zeros(imagen.shape[:2], dtype=np.uint8)
    return mascara_total

def calcular_métricas(mascara_manual, mascara_automatica):
    TP = np.sum((mascara_manual == 1) & (mascara_automatica == 1))
    TN = np.sum((mascara_manual == 0) & (mascara_automatica == 0))
    FP = np.sum((mascara_manual == 0) & (mascara_automatica == 1))
    FN = np.sum((mascara_manual == 1) & (mascara_automatica == 0))
    
    precision = TP / (TP + FP) if (TP + FP) != 0 else 0
    recall = TP / (TP + FN) if (TP + FN) != 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
    dice = 2 * TP / (2 * TP + FP + FN) if (2 * TP + FP + FN) != 0 else 0
    iou = TP / (TP + FP + FN) if (TP + FP + FN) != 0 else 0
    tnr = TN / (TN + FP) if (TN + FP) != 0 else 0
    accuracy = (TP + TN) / (TP + FP + TN + FN) if (TP + FP + TN + FN) != 0 else 0
    
    return {
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1_score,
        "Dice Coefficient": dice,
        "IoU": iou,
        "True Negative Rate": tnr,
        "Accuracy": accuracy
    }

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

# Elegir un umbral adecuado (esto lo puedes ajustarlo según la visualización de la matriz)
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

# Seleccionar manualmente la probeta
print("Selecciona manualmente la probeta.")
puntos_probeta = seleccionar_puntos(image3.copy())
mascara_probeta_manual = crear_mascara(puntos_probeta, image3.shape)

# Determinar puntos de oxidación
image_oxido, image_sin_oxido, oxido_percentage = oxidation(image3, offset=1, sens=5)

# Calcular las métricas de la probeta
metricas_probeta = calcular_métricas(mascara_probeta_manual, cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY) > 0)
print("Métricas de la probeta:")
for metrica, valor in metricas_probeta.items():
    print(f'{metrica}: {valor:.2f}')

# Mostrar la selección manual de la probeta
mostrar_imagen('Máscara Manual de Probeta', mascara_probeta_manual * 255, cmap='gray')

# Seleccionar manualmente el óxido
print("Selecciona manualmente el óxido. Presiona 'q' para terminar cada polígono.")
mascara_oxido_manual = seleccionar_multiples_poligonos(image3.copy())

# Calcular las métricas del óxido
image_oxido_bin = cv2.cvtColor(image_oxido, cv2.COLOR_BGR2GRAY) > 0
metricas_oxido = calcular_métricas(mascara_oxido_manual, image_oxido_bin)
print("Métricas del óxido:")
for metrica, valor in metricas_oxido.items():
    print(f'{metrica}: {valor:.2f}')

# Mostrar la selección manual del óxido
mostrar_imagen('Máscara Manual de Óxido', mascara_oxido_manual * 255, cmap='gray')

# Guardar las métricas en un archivo Excel
df_metricas_probeta = pd.DataFrame([metricas_probeta])
df_metricas_oxido = pd.DataFrame([metricas_oxido])

with pd.ExcelWriter('metricas_evaluacion.xlsx') as writer:
    df_metricas_probeta.to_excel(writer, sheet_name='Probeta', index=False)
    df_metricas_oxido.to_excel(writer, sheet_name='Oxido', index=False)

# Mostrar las imágenes y el porcentaje de óxido
mostrar_imagen('Sin óxido', image_sin_oxido)
mostrar_imagen('Óxido', image_oxido)
print(f'Porcentaje de óxido: {oxido_percentage:.2f}%')

