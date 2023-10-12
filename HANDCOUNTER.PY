import cv2
import mediapipe as mp
import serial
import time

video = cv2.VideoCapture(0)#CONECTAR COM A WEBCAM, CASO 0 SE N FUNCIONAR TENTE 1 OU 2

arduino = serial.Serial('COM4',9600)#PORTA DE ENTRADA DO ARDUINO

hands = mp.solutions.hands
Hands = hands.Hands(max_num_hands=1)
mpDwaw = mp.solutions.drawing_utils
pTime = 0
while True:
    success, img = video.read()
    frameRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = Hands.process(frameRGB)
    handPoints = results.multi_hand_landmarks
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(200,200),cv2.FONT_HERSHEY_PLAIN,3,(205,112,80),2)

    h, w, _ = img.shape
    pontos = []
    if handPoints:
        for points in handPoints:
            mpDwaw.draw_landmarks(img, points,hands.HAND_CONNECTIONS)
            for id, cord in enumerate(points.landmark):#IDENTIFICAÇÃO DAS COORDENADAS DOS PONTOS PRESENTES
                cx, cy = int(cord.x * w), int(cord.y * h)
                #cv2.putText(img, str(id), (cx, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                pontos.append((cx,cy))
            dedos = [8,12,16,20]#ARRAY COM UMA P.A DE RAZÃO 4 PARA IDENTIFICAR OS DEDOS
            contador = 0
            if pontos:

                '''hand_center = (sum([p[0] for p in pontos]) // 21, sum([p[1] for p in pontos]) // 21)
                hand_radius = max([int(1.2 * ((p[0] - hand_center[0])**2 + (p[1] - hand_center[1])**2)**0.5) for p in pontos])
                cv2.circle(img,hand_center,hand_radius,(0,0,255),2)'''#DESENHAR UM CÍRCULO EM TORNO DA MÃO COM BASE NO RAIO E CENTRO

                if pontos[4][0] < pontos[3][0]:
                    contador += 1
                for x in dedos:
                   if pontos[x][1] < pontos[x-2][1]:
                       contador +=1
                       arduino.write(str(contador).encode())#O NÚMERO PRESENTE NO CONTADOR É MANDADO PARA O ARDUINO E ACENDENDENDO UM DETERMINADO LED

            cv2.rectangle(img, (80, 10), (200,110), (255, 0, 0), -1)
            cv2.putText(img,str(contador),(100,100),cv2.FONT_HERSHEY_SIMPLEX,4,(255,255,255),5)

    cv2.imshow('Imagem',img)
    cv2.waitKey(1)