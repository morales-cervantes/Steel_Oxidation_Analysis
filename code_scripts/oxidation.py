import cv2
import numpy as np

def oxidation(i, offset=1, sens=5):
    # Aplicar un filtro Gaussiano para reducir el ruido
    i_blur = cv2.GaussianBlur(i, (5, 5), 0)
    
    # Convertir la imagen a escala de grises
    i_gray = cv2.cvtColor(i_blur, cv2.COLOR_BGR2GRAY)
    
    # Aplicar binarización adaptativa para resaltar manchas
    bin_image = cv2.adaptiveThreshold(i_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 11, 2)
    
    # Obtener las dimensiones de la imagen
    m, n = i_gray.shape
    
    # Inicializar dos matrices vacías para almacenar resultados
    image = np.zeros((m, n, 3), dtype=np.uint8)
    i2 = np.zeros((m, n, 3), dtype=np.uint8)
    
    # Encontrar componentes conectados en la imagen binarizada
    num_labels, labels_im = cv2.connectedComponents(bin_image)
    
    # Iterar sobre cada componente conectado
    for label in range(1, num_labels):  # Ignorar el fondo
        mask = (labels_im == label)
        if np.mean(i_gray[mask]) < 255:
            # Clasificar los valores en función de su variación respecto a la media
            image[mask] = i[mask]  # Óxido (alta variación)
            # Establecer las primeras 5 filas y las últimas 5 filas de image a cero
            image[:5, :] = 0
            image[-5:, :] = 0
    
    # Crear una máscara para los valores de óxido
    mask_oxido_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask_oxido = cv2.cvtColor(mask_oxido_gray, cv2.COLOR_GRAY2BGR)
    

    
    # Restar la imagen de óxido de la imagen original para obtener la imagen sin óxido
    i2 = cv2.subtract(i, mask_oxido)
    
    # Calcular el porcentaje de píxeles clasificados como óxido, sin contar las primeras 5 filas superiores e inferiores
    oxido_pixels = np.sum(image[5:-5, :] > 0)
    total_pixels = (m - 10) * n  # Restamos 10 filas (5 superiores y 5 inferiores)
    oxido_percentage = (oxido_pixels / total_pixels) * 100
    
    # Devolver las dos imágenes resultantes y el porcentaje de óxido
    return image, i2, oxido_percentage

# Si necesitas realizar pruebas:
if __name__ == "__main__":
    # Código de prueba
    file_name = 't8.tiff'
    img = cv2.imread(file_name)
    image, i2, oxido_percentage = oxidation(img, offset=1, sens=5)
    cv2.imshow('Óxido', image)
    cv2.imshow('Sin óxido', i2)
    print(f'Porcentaje de óxido: {oxido_percentage:.2f}%')
    cv2.waitKey(0)
    cv2.destroyAllWindows()


