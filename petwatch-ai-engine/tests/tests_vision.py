import unittest
from lmodel import vision
import cv2, base64


class TestVisionFunctions(unittest.TestCase):

    def test_inference_yolo(self):
        # Simule um frame para teste
        frame = cv2.imread("imagens_gatos/uly.jpeg")
        result = vision.inference_yolo(frame)

        # Verifique se o resultado contém as chaves esperadas
        self.assertIn('label', result)
        self.assertIn('bbox', result)
        self.assertIn('confidence', result)

    def test_decode_base64_to_byarray(self):
        # Simule uma imagem codificada em base64 para teste
        frame = cv2.imread("imagens_gatos/uly.jpeg")
        _, buffer = cv2.imencode('.jpeg', frame)
        foto_base64 = base64.b64encode(buffer).decode('utf-8')
        image = vision.decode_base64_to_byarray(foto_base64)

        # Verifique se o resultado é uma instância de numpy array
        self.assertIsInstance(image, vision.np.ndarray)

class TestPrecision(unittest.TestCase):

    def test_precision(self):
        # Simule um frame para teste
        frame = cv2.imread("imagens_gatos/uly.jpeg")
        result = vision.inference_yolo(frame)

        # Verifique se o resultado contém as chaves esperadas
        self.assertEqual('uly', result['label'])
        
        # Verifique as coordenadas da bounding box
        expected_bbox = {'x': 19, 'y': 66, 'x2': 866, 'y2': 890}
        self.assertDictEqual(expected_bbox, result['bbox'])

        # Verifique a confiança
        expected_confidence = 0.5
        self.assertEqual(expected_confidence, result['confidence'])



if __name__ == '__main__':
    unittest.main()
