from lmodel.model import Model
from cv2 import VideoCapture, imencode, INTER_LINEAR, putText, rectangle, LINE_AA
from os import getenv
from flask_opencv_streamer.streamer import Streamer
from lmodel.render import draw_bbox
import cv2
import base64

def main():
    # Obtém a câmera da variável de ambiente "CAMERA"
    port = 3030
    require_login = False
    streamer = Streamer(port, require_login)

    camera = "/home/juannascimento/Documentos/Uly.mp4"
    cap = VideoCapture(camera)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    out = cv2.VideoWriter(f"output/output_{camera}", cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))


    # Inicializa a captura de vídeo


    # Inicializa o reconhecimento de faces
    model = Model()

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            image_bytes = imencode('.jpg', frame)[1].tobytes()
            magem_base64 = base64.b64encode(image_bytes).decode('utf-8')
            try:
              result = model.recognize(magem_base64)
              frame = draw_bbox(frame, result)            
            except Exception as error:
              print(error)  

        
    
        out.write(frame)    
        streamer.update_frame(frame)
        if not streamer.is_streaming:
            streamer.start_streaming()

    # Libera a captura de vídeo quando o loop terminar
    out.release()
    cap.release()

if __name__ == "__main__":
    main()

