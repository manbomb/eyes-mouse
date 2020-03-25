# Eyes Mouse
## Excuse me. I will translate this Readme into English soon.

A virtual mouse controled by the eyes.

## Propósito

Fazer com que pessoas que não podem ou não conseguem utilizar o mouse ou mouse pad consigam usar seus computadores da maneira mais natural possível.

## O que foi utilizado ?

### Python

A escolha do python se deu pelo seu alto nível e devido as bibliotecas que este possui disponíveis. Além da comunidade também, muitos projetos de visão computacional e machine learning são feitos em Python, o que faz com que o número de fontes e o apoio da comunidade seja muito grande.

### OpenCV e Haarcascade

Foi utilizada a biblioteca OpenCV para poder detectar as faces na imagem, utilizando para isso a técnica de Haarcascade. A biblioteca OpenCV é de longe a que possui a maior comunidade e a mais completa na área, além de ser muito intuitiva, por isso foi a escolhida para este projeto.

### PyAutoGUI

Esta biblioteca permite controlar várias funções do mouse, arrastar, clicar, mover e outras do teclado também. Ela foi a escolhida pois aparentemente suporta diversos sistemas operacionais, ao contrário de outras que foram desenvolvidas unicamente para o Windows 32 bits.

### Numpy

Esta biblioteca é de longe indipensável para uma gama enorme de projetos em Python, pois disponibiliza diversos objetos matematicamente úteis, sendo o mais usado o array de zeros e o método mean (média aritmética).

## Algo interessante neste projeto ?

### Equalização de Histograma com quatro zonas

Quando o primeiro haarcascade (o do rosto) encontra uma ROI (region of interest) o segundo haarcascede (o dos olhos) é aplicado somente nesta ROI encontrada. Para melhorar o acerto, diminuir o número de falsos negativos, foi dividida esta ROI única em 4 ROI's menores, sendo feita assim a equalização de histograma sobre cada uma separadamente. Isto diminuiu considerévelmente o número de falsos negativos.

### Escolha dos 'melhores olhos'

Devido a tecnologia Haarcascade não ser algo muito preciso, muito menos exata, por vezes o sistema detecta mais de dois olhos por face, um absurdo. Para tentar evitar isso, o sistema lista todos os olhos encontrados e ordena estes por distância ao ponto inicial da face (que é o ponto superior esquerdo), os dois mais próximos são os escolhidos para o cálculo.

### Posições utilizando médias móveis

Devido ao fato de existirem falsos negativos, quando o olho não é detectado, foi pensado um jeito de diminuir a influência destes sobre o resultado final. Para isso, o ponto (mx,my) que é o ponto médio dos olhos (ou caso apenas um olho tenha sido detectado, este é a posição deste) passou a ser plotado e utilizado como a média dos seus útimos quatro valores. Ou seja, cada novo ponto que é calculado toma a posição 0 desta lista, e os outros itens pulam para a próxima posição cada um, sendo o último descartado. E ao final é calculado o ponto médio destes pontos da lista, ou se preferir, a média móvel das coordenadas destes.

## Problemas do projeto:

- **Precisa de uma boa iluminação**: caso não haja uma boa iluminação, horizontal e à frente do rosto, pode ser que o sistema falhe em encontrar a face ou os olhos.
- **Objetos muito claros**: objetos muito claros atrapalham também, pois, a equalização de histograma que é feita em todas as etapas de detecção tende a escurecer as partes 'menos claras' quando existe algo muito claro e grande na imagem. De preferência, o seu rosto tem de ser a parte mais clara da imagem.

## O que ainda falta ser feito:

- **Click**: ainda falta ser feito o comando de click que vai ser dado por um piscar com os dois olhos.
- **Limitar o número de faces**: não foi feito o teste com mais de uma face em frente a webcam, mas deve ser limitado no código para que apenas uma face controle o mouse, e esta seja a maior que está na tela.
- **Testes práticos**: tentar controlar o computador unicamente com este sistema durante algum tempo, em situações diárias e corriqueiras.
