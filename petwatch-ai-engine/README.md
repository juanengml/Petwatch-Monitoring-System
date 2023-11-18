# Petwatch API Engine

----

## Contexto
O conjunto de dados para detecção computacional aplicado ao reconhecimento facial de gatos é projetado para treinar e avaliar algoritmos de detecção de objetos específicos para identificar rostos de gatos em imagens. Este conjunto de dados geralmente incluiria uma variedade de imagens que abrangem diversas condições, como diferentes posições dos gatos, iluminações, fundos e expressões faciais.

**Objetivo**: Treinar modelos de detecção de objetos para identificar e localizar rostos de gatos em imagens.

### 1. Dataset
**Formato das Anotações**: Cada imagem é acompanhada por anotações que indicam as coordenadas das bounding boxes que envolvem os rostos de gatos.

| dataset | quantidade | labels |
|---------|------------|--------|
| gatos   | 100        | lora|
| gatos   | 100        | uly|

|  |  |  |
|---------|------------|--------|
| ![](imagens_gatos/dataset.png)   | ![](imagens_gatos/dataset_2.png)        | 






### 2. Escolher Modelo

![](https://raw.githubusercontent.com/ultralytics/assets/main/yolov8/yolo-comparison-plots.png)

O Ultralytics YOLOv8 é um modelo de ponta, estado-da-arte (SOTA) que se baseia no sucesso das versões anteriores do YOLO e introduz novos recursos e melhorias para impulsionar ainda mais o desempenho e a flexibilidade. O YOLOv8 é projetado para ser rápido, preciso e fácil de usar, tornando-o uma excelente escolha para uma ampla gama de tarefas, como detecção e rastreamento de objetos, segmentação de instâncias, classificação de imagens e estimativa de pose.

Esperamos que os recursos aqui ajudem você a obter o máximo do YOLOv8. Por favor, consulte a documentação do YOLOv8 para obter detalhes, abra um problema no GitHub para suporte e junte-se à nossa comunidade no Discord para perguntas e discussões!

Para solicitar uma Licença Corporativa, por favor, preencha o formulário em Ultralytics Licensing.

### 3. Notebook Train
 <a href="https://colab.research.google.com/gist/juanengml/cff5786316bfbd78d994ac732ee3d4d7/train-yolov8-object-detection-on-custom-dataset.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

 <a href="notebooks/train_model_yolov8.ipynb"><img src="https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white" alt="Open In Colab"></a>

![](imagens_gatos/trainModel.png)

### 4. Tests

### 5. Deploy


