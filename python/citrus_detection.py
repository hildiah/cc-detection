import cv2
import numpy as np
import csv
import os

# Fungsi untuk mengubah gambar dari RGB ke Grayscale
def rgb_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Fungsi untuk meningkatkan kontras gambar menggunakan CLAHE (Contrast Limited Adaptive Histogram Equalization)
def apply_clahe(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(image)

# Fungsi untuk normalisasi gambar
def normalize_image(image):
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)

# Fungsi untuk menerapkan median blur
def apply_median_blur(image):
    return cv2.medianBlur(image, 5)

# Fungsi untuk menerapkan Gaussian blur
def apply_gaussian_blur(image):
    return cv2.GaussianBlur(image, (5, 5), 0)

# Fungsi untuk deteksi tepi Sobel
def apply_sobel(image):
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    sobel_magnitude = cv2.magnitude(sobel_x, sobel_y)
    return np.uint8(np.absolute(sobel_magnitude))

# Fungsi untuk menerapkan thresholding pada gambar
def apply_threshold(image, threshold_value=50):
    _, thresholded = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return thresholded

# Fungsi untuk ekstraksi fitur dari gambar
def extract_features(image):
    mean_r = np.mean(image[:, :, 0])  # R channel
    mean_g = np.mean(image[:, :, 1])  # G channel
    mean_b = np.mean(image[:, :, 2])  # B channel

    # Menghitung kontras menggunakan deviasi standar
    contrast = np.std(image)

    # Untuk menghitung jumlah dan area spot, gunakan deteksi kontur
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    spot_count = len(contours)
    spot_area = sum([cv2.contourArea(contour) for contour in contours])

    return {
        'mean_r': mean_r,
        'mean_g': mean_g,
        'mean_b': mean_b,
        'contrast': contrast,
        'spot_count': spot_count,
        'spot_area': spot_area
    }

# Fungsi untuk menyimpan hasil ekstraksi fitur ke dalam file CSV
def save_features_to_csv(features, filename='results.csv'):
    header = ['File_Name', 'Mean_R', 'Mean_G', 'Mean_B', 'Contrast', 'Spot_Count', 'Spot_Area']
    row = [filename, features['mean_r'], features['mean_g'], features['mean_b'], features['contrast'], features['spot_count'], features['spot_area']]
    
    # Menyimpan data dalam CSV
    file_exists = os.path.exists(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)  # Menambahkan header jika file baru
        writer.writerow(row)

# Fungsi utama untuk menjalankan deteksi
def detect_disease(image_path, output_csv='results.csv'):
    # Membaca gambar
    image = cv2.imread(image_path)
    
    # Proses pengolahan gambar
    grayscale_image = rgb_to_grayscale(image)
    clahe_image = apply_clahe(grayscale_image)
    normalized_image = normalize_image(clahe_image)
    median_blurred_image = apply_median_blur(normalized_image)
    gaussian_blurred_image = apply_gaussian_blur(median_blurred_image)
    sobel_image = apply_sobel(gaussian_blurred_image)
    thresholded_image = apply_threshold(sobel_image)

    # Ekstraksi fitur
    features = extract_features(image)

    # Menyimpan hasil ekstraksi fitur ke CSV
    save_features_to_csv(features, filename=output_csv)

    return thresholded_image  # Mengembalikan gambar yang telah di-threshold
aaaa