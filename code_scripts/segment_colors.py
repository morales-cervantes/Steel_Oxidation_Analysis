import cv2
import numpy as np
from skimage import color

def segment_colors(image, select):
    # Convertir la imagen a espacio de color LAB
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Definir los marcadores de color para el fondo azul en el espacio LAB
    if not select:
        # Usar los valores obtenidos
        lower_blue = np.array([39, 176, 64])
        upper_blue = np.array([65, 186, 71])
    else:
        # Placeholder, ajustar según sea necesario
        lower_blue = np.array([20, 135, 140])  
        upper_blue = np.array([255, 175, 170])  

    # Crear una máscara binaria donde se detecte el fondo azul
    blue_mask = cv2.inRange(lab_image, lower_blue, upper_blue)

    # Crear una imagen con el fondo azul eliminado
    image2 = image.copy()
    image2[blue_mask != 0] = [0, 0, 0]  # Eliminar el fondo azul

    return image2, blue_mask

# Si necesitas realizar pruebas:
if __name__ == "__main__":
    # Código de prueba
    file_name = 't8.tiff'
    img = cv2.imread(file_name)
    image2, blue_mask = segment_colors(img, False)
    cv2.imshow('Imagen Original', img)
    cv2.imshow('Imagen sin Fondo', image2)
    cv2.imshow('Máscara Azul', blue_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


