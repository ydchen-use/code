import cv2
import pytesseract as tess

tesseract_version = tess.get_tesseract_version()
tesseract_language = tess.get_languages()


def ocr_test():
    image = cv2.imread("test.png")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    text = tess.image_to_string(image_rgb, lang="chi_sim")
    print(text)
    h, w, c = image.shape
    boxes = tess.image_to_boxes(image)
    for b in boxes.splitlines():
        b = b.split(" ")
        image = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 1)

    cv2.imshow("text detect", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print(tesseract_language)
    print(tesseract_version)

    ocr_test()
