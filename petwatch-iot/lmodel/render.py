import cv2

def draw_bbox(frame, result):
    frame_bbox_drawed = frame.copy()

    bbox = result['bbox']
    x, x2, y, y2 = bbox['x'], bbox['x2'], bbox['y'], bbox['y2']

    label = result['nome']
    confidence = result['confidence']

    label_full = f"{label} ({confidence})"
    color = (0, 255, 0)  # Cor verde para o rótulo
    thickness = 2

    # Desenhe a caixa delimitadora
    cv2.rectangle(frame_bbox_drawed, (x, y), (x2, y2), color, thickness)

    # Configure o tamanho e a cor da fonte para o rótulo
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 0, 0)  # Cor verde

    # Desenhe o texto
    text_size = cv2.getTextSize(label_full, font, font_scale, thickness)[0]
    cv2.rectangle(frame_bbox_drawed, (x, y - 20), (x + text_size[0], y), color, thickness=cv2.FILLED)
    cv2.putText(frame_bbox_drawed, label_full, (x, y - 10), font, font_scale, font_color, thickness, lineType=cv2.LINE_AA)

    return frame_bbox_drawed
