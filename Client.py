import pygame
from network import Network

pygame.init()
pygame.font.init()

Res = ([1920, 1080] , [1280, 720])

WIDTH, HEIGHT = Res[1]

if WIDTH == 1920:
    imageWidth = 1980 * 2
    imageHeight = 198 * 2
    spriteModifier = 2
    spriteWidth = 869 * spriteModifier
    spriteHeight = 1673 * spriteModifier
    bols = 5
    bols2 = 5
else:
    imageWidth = 1980 * 2 * (2/3)
    imageHeight = 198 * 2 * (2/3)
    spriteModifier = 2 * (2/3)
    spriteWidth = 869 * spriteModifier
    spriteHeight = 1673 * spriteModifier
    bols = 4
    bols2 = 4
    #To bols2 kanonizei poso psila tha einai to send button

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tichu")
BG = pygame.transform.scale(pygame.image.load("Assets/BG.jpg").convert(), (WIDTH, HEIGHT))
cardGiveWidth = 256 * spriteModifier
cardGiveHeight = 121 * spriteModifier
cardWidth = imageWidth/30
cardHeight = imageHeight/2
cardImage = pygame.transform.scale(pygame.image.load("Assets/TichuCards.png"), (imageWidth, imageHeight)).convert_alpha()
sprites = pygame.transform.scale(pygame.image.load("Assets/spritesheet.png"), (spriteWidth, spriteHeight)).convert_alpha()
cardSurface = pygame.Surface((cardWidth, cardHeight), pygame.SRCALPHA)
cardBack = pygame.Surface((cardWidth, cardHeight), pygame.SRCALPHA)
cardBack.blit(cardImage, (cardWidth * (-28), 0))
cardGive = pygame.Surface((cardGiveWidth, cardGiveHeight), pygame.SRCALPHA)
#cardGive = pygame.Surface((0, 0), pygame.SRCALPHA)
cardGive.blit(sprites,(-528*spriteModifier, -1447*spriteModifier))

cardrect = {}

playPos = ((15 * (cardWidth * (2 / 3))) + cardWidth / 2, HEIGHT - cardHeight - 20 * bols)
sendPos = ((15 * (cardWidth * (2 / 3))) + cardWidth / 2, HEIGHT - cardHeight - 20 * bols2)

class Buttons:
    #To posSc einai tou sthn othoni enw to allo sto asset
    def __init__(self, posOnScreen, size, posOnAsset, assets):
        self.ready = False
        self.selected = False
        self.clicked = False
        self.posSc = posOnScreen
        self.posAs = posOnAsset
        self.size = size
        self.assets = assets

def inGame():
    global bols
    global sendPos
    global playPos
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player + 1)
    hand = n.send("Get Hand")
    assign(hand, imageWidth, imageHeight)
    selMode = True
    playAssets = ("Assets/PlayGrey.png", "Assets/PlaySelected.png", "Assets/Play.png")
    sendAssets = ("Assets/Send.png", "Assets/SendSelected.png", "Assets/SendGrey.png", "Assets/SendGreen.png", "Assets/SendGreenSelected.png")
    socketedCards = {}
    playBtn = Buttons(playPos, (WIDTH / 10, HEIGHT / 15), 0, playAssets)
    sendBtn = Buttons(playPos, (WIDTH / 10, HEIGHT / 15), 0, sendAssets)

    while run:
        hand = sortedHand(hand)
        getGame = n.send("Begin")
        #print("Trying to get game")
        if getGame == "Waiting":
            #print("Trying to connect")
            playing = False
        else:
            playing = True
        clock.tick(60)
        x_mouse, y_mouse = pygame.mouse.get_pos()

        PlayerHands = n.send("Get Hands")
        phase = n.send("Get Phase")
        if phase == "Giving":
            for card in hand:
                if card.selected:
                    selMode = False

        if phase == "Giving":
            if len(socketedCards) == 3:
                sendBtn.ready= True
            else:
                sendBtn.ready = False

        socketsHeight = [(HEIGHT - cardHeight - 20 * (bols + 1)) - cardGiveHeight + 12 * spriteModifier,(HEIGHT - cardHeight - 20 * (bols + 1)) - cardGiveHeight + 108 * spriteModifier]
        sockets = [(WIDTH - cardGiveWidth) / 2 + 9 * spriteModifier, (WIDTH - cardGiveWidth) / 2 + 72 * spriteModifier,(WIDTH - cardGiveWidth) / 2 + 93 * spriteModifier,(WIDTH - cardGiveWidth) / 2 + 156 * spriteModifier,(WIDTH - cardGiveWidth) / 2 + 180 * spriteModifier,(WIDTH - cardGiveWidth) / 2 + 243 * spriteModifier]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif  event.type == pygame.MOUSEBUTTONDOWN:
                if phase == "Playing" or selMode:
                    breakIt = False
                    for j in range(3):
                        if sockets[j * 2] < x_mouse < sockets[j * 2 + 1] and socketsHeight[0] < y_mouse < socketsHeight[1] and phase == "Giving":
                            if j in socketedCards:
                                socketedCards[j].socketed = [False, -1]
                                hand.append(socketedCards[j])
                                socketedCards.pop(j)
                                breakIt = True
                    for i in range(len(hand)):
                        if breakIt:
                            break
                        if playing and cardrect[i].collidepoint(x_mouse, y_mouse) and not hand[i].selected:
                            if i > 0 and cardrect[i - 1].collidepoint(x_mouse, y_mouse):
                                hand[i - 1].selected = not hand[i - 1].selected

                            hand[i].selected = True

                            movePlayButton(0, phase, hand)
                        elif playing and cardrect[i].collidepoint(x_mouse, y_mouse) and hand[i].selected:
                            if i > 0 and cardrect[i - 1].collidepoint(x_mouse, y_mouse):
                                hand[i - 1].selected = not hand[i - 1].selected
                            hand[i].selected = False
                            movePlayButton(1, phase, hand)
                else:
                    for i in range(len(hand)):
                        if hand[i].selected:
                            hand[i].selected = False
                            if phase == "Giving":
                                if sockets[0] < x_mouse < sockets[1] and socketsHeight[0] < y_mouse < socketsHeight[1]:
                                    hand[i].socketed = [True, 0]
                                elif sockets[2] < x_mouse < sockets[3] and socketsHeight[0] < y_mouse < socketsHeight[1]:
                                    hand[i].socketed = [True, 1]
                                elif sockets[4] < x_mouse < sockets[5] and socketsHeight[0] < y_mouse < socketsHeight[1]:
                                    hand[i].socketed = [True, 2]
                            for j in range(3):
                                if sockets[j * 2] < x_mouse < sockets[j * 2 + 1] and socketsHeight[0] < y_mouse < socketsHeight[1] and phase == "Giving":
                                    if j in socketedCards:
                                        socketedCards[j].socketed = [False, -1]
                                        hand.append(socketedCards[j])
                                        socketedCards.pop(j)
                                    for card in hand:
                                        if card.socketed[0]:
                                            if card.socketed[1] == j:
                                                socketedCards[j] = card
                                                hand.remove(card)
                            break
                    selMode = True
                if phase == "Giving" and sendBtn.posSc[0] < x_mouse < sendBtn.posSc[0] + sendBtn.size[0] and sendBtn.posSc[1] < y_mouse < sendBtn.posSc[1] + sendBtn.size[1] and sendBtn.ready:
                    sendBtn.clicked = not sendBtn.clicked
                    if sendBtn.clicked:
                        if n.send("Ready To Send") == "Get Cards":
                            receivedCards = n.send("Sent Cards", socketedCards)

                    else:
                        n.send("Not Ready To Send")

        if playBtn.ready:
            if playBtn.posSc[0] < x_mouse < playBtn.posSc[0] + playBtn.size[0] and playBtn.posSc[1] < y_mouse < playBtn.posSc[1] + playBtn.size[1]:
                playBtn.selected = True
            else:
                playBtn.selected = False

        if phase == "Giving" and sendBtn.ready:
            if sendBtn.posSc[0] < x_mouse < sendBtn.posSc[0] + sendBtn.size[0] and sendBtn.posSc[1] < y_mouse < sendBtn.posSc[1] + sendBtn.size[1]:
                sendBtn.selected = True
            else:
                sendBtn.selected = False

        if phase == "Playing" and playing:
            drawGame(hand, PlayerHands, player, playBtn)
        elif phase == "Giving" and playing:
            drawGiving(hand, x_mouse, y_mouse, PlayerHands, player, socketsHeight, sockets, socketedCards, sendBtn)
        else:
            drawWaitingScreen()
    pygame.quit()

def drawGame(hand, length, player, playBtn):
    WIN.blit(BG, (0, 0))
    i = 0
    space = (len(hand)+1) * (cardWidth * (2 / 3))
    for card in hand:
        cardSurface.blit(cardImage, (card.res[0], card.res[1]))
        card.y = HEIGHT - cardHeight - 20
        if card.selected:
            for _ in range(5):
                hand[i].y -= 10
        WIN.blit(cardSurface, ((WIDTH - space)/2 + (cardWidth * (2/3))*i, card.y))
        cardrect[i] = cardSurface.get_rect(topleft=((WIDTH - space)/2 + (cardWidth * (2/3))*i, card.y))
        i+=1
    drawOpponent(length, player)
    if not playBtn.ready:
        playAsset = playBtn.assets[0]
    elif playBtn.ready and playBtn.selected:
        playAsset = playBtn.assets[1]
    else:
        playAsset = playBtn.assets[2]
    play = pygame.transform.scale(pygame.image.load(playAsset), playBtn.size)
    WIN.blit(play, playBtn.posSc)

    pygame.display.update()

def movePlayButton(x, phase, hand):
    global bols
    if x == 0 and phase == "Playing":
        try:
            if hand[13].selected or hand[12].selected or hand[11].selected:
                if bols == 5:
                    bols = 8
                elif bols == 4:
                    bols = 6
        except:
            try:
                if hand[12].selected or hand[11].selected:
                    if bols == 5:
                        bols = 8
                    elif bols == 4:
                        bols = 6
            except:
                try:
                    if hand[11].selected:
                        if bols == 5:
                            bols = 8
                        elif bols == 4:
                            bols = 6
                except:
                    pass

    if x == 1 and phase == "Playing":
        try:
            if not hand[13].selected and not hand[12].selected and not hand[11].selected:
                if bols == 8:
                    bols = 5
                elif bols == 6:
                    bols = 4
        except:
            try:
                if not (hand[12].selected and not hand[11].selected):
                    if bols == 8:
                        bols = 5
                    elif bols == 6:
                        bols = 4
            except:
                try:
                    if not hand[11].selected:
                        if bols == 8:
                            bols = 5
                        elif bols == 6:
                            bols = 4
                except:
                    pass

def drawGiving(hand, x, y, length, player, socketsHeight, sockets, socketedCards, sendBtn):
    WIN.blit(BG, (0, 0))
    drawOpponent(length, player)
    space = (len(hand) + 0.5) * (cardWidth * (2 / 3))
    WIN.blit(cardGive, ((WIDTH - cardGiveWidth) / 2, (HEIGHT - cardHeight - 20 * (bols + 1)) - cardGiveHeight))
    i = 0
    for count in range(3):
        if count in socketedCards:
            cards = socketedCards[count]
            cardSurface.blit(cardImage, (cards.res[0], cards.res[1]))
            for j in range(3):
                if cards.socketed[1] == j:
                    cards.x = sockets[j * 2]
                    cards.y = socketsHeight[0] - 2 * spriteModifier
            WIN.blit(cardSurface, (cards.x, cards.y))
        i += 1
    i = 0
    for card in hand:
        cardSurface.blit(cardImage, (card.res[0], card.res[1]))
        card.y = HEIGHT - cardHeight - 20
        card.x = (WIDTH - space) / 2 + (cardWidth * (2 / 3)) * i
        if card.selected:
            hand[i].x = x - (cardWidth/2)
            hand[i].y = y - (cardHeight / 2)

        WIN.blit(cardSurface, (card.x , card.y))
        cardrect[i] = cardSurface.get_rect(topleft=(card.x, card.y))
        i += 1
    if sendBtn.ready and sendBtn.selected and not sendBtn.clicked:
        sendAsset = sendBtn.assets[1]
    elif sendBtn.ready and not sendBtn.selected and not sendBtn.clicked:
        sendAsset = sendBtn.assets[0]
    elif not sendBtn.ready:
        sendAsset = sendBtn.assets[2]
    elif sendBtn.clicked:
        sendAsset = sendBtn.assets[3]
    else:
        sendAsset = sendBtn.assets[4]
    send = pygame.transform.scale(pygame.image.load(sendAsset), sendBtn.size)
    WIN.blit(send, sendBtn.posSc)
    pygame.display.update()

def drawOpponent(length, player):
    opposite = 0
    left = 0
    right = 0
    if player == 0:
        left = 3
        right = 1
        opposite = 2
    if player == 1:
        left = 0
        right = 2
        opposite = 3
    if player == 2:
        left = 1
        right = 3
        opposite = 0
    if player == 3:
        left = 2
        right = 0
        opposite = 1
    spaceOp = (length[opposite] + 0.5) * (cardWidth * (2 / 3))
    spaceL = ((length[left] + 1) * (cardWidth * (2 / 5)))
    spaceR = ((length[right] + 1) * (cardWidth * (2 / 5)))

    for i in range(length[opposite]):
        back = pygame.transform.rotate(cardBack, 180)
        cardy = 20
        cardx = (WIDTH - spaceOp) / 2 + (cardWidth * (2 / 3)) * i
        WIN.blit(back, (cardx, cardy))
    for i in range(length[left]):
        side = pygame.transform.rotate(cardBack, 90)
        cardy = (HEIGHT - spaceL) / 2 + (cardWidth * (2 / 5)) * i
        cardx = 10
        WIN.blit(side, (cardx, cardy))
    for i in range(length[right]):
        side = pygame.transform.rotate(cardBack, 270)
        cardy = (HEIGHT - spaceR) / 2 + (cardWidth * (2 / 5)) * i
        cardx = WIDTH - 10 - cardHeight
        WIN.blit(side, (cardx, cardy))

def drawWaitingScreen():
    WIN.blit(BG, (0, 0))
    font = pygame.font.SysFont('comicsans', 80)
    text = font.render("Waiting for players", True, ("White"), True)
    WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()

def menu():
    run = True
    clock = pygame.time.Clock()
    start = pygame.transform.scale(pygame.image.load("Assets/StartButtonSelected.png"), (WIDTH / 5, HEIGHT / 5)).convert()

    while run:
        clock.tick(144)
        startPos = WIDTH / 2 - start.get_width() / 2, HEIGHT / 2 - start.get_height() / 2
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and (startPos[0] < mousePos[0] < startPos[0] + start.get_width() and startPos[1] < mousePos[1] < startPos[1] + start.get_height()):
                inGame()

        if startPos[0] < mousePos[0] < startPos[0] + start.get_width() and startPos[1] < mousePos[1] < startPos[1] + start.get_height():
            start = pygame.transform.scale(pygame.image.load("Assets/StartButtonSelected.png"), (WIDTH/5, HEIGHT/5)).convert()
        else:
            start = pygame.transform.scale(pygame.image.load("Assets/StartButton.png"), (WIDTH/5, HEIGHT/5)).convert()

        drawStart(start, startPos)
    pygame.quit()

def drawStart(start, startPos):
    WIN.blit(BG, (0, 0))
    WIN.blit(start, (startPos[0], startPos[1]))
    pygame.display.update()

def assign(hand, W, H):
    for card in hand:
        if card.color == "Red":
            card.res[0] -= W/30
            for _ in range(card.card - 2):
                card.res[0] -= 2 * (W/30)
        elif card.color == "Green":
            for _ in range(card.card - 2):
                card.res[0] -= 2 * (W/30)
        elif card.color == "Blue":
            card.res[0] -= (W/30)
            for _ in range(card.card - 2):
                card.res[0] -= 2 * (W/30)
            card.res[1] -= (H/2)
        elif card.color == "Black":
            for _ in range(card.card - 2):
                card.res[0] -= 2 * (W/30)
            card.res[1] -= (H/2)
        elif card.card == 15:
            card.res[0] += cardWidth * (-26)
            card.res[1] -= (H/2)
        elif card.card == 0.5:
            card.res[0] += cardWidth * (-27)
            card.res[1] -= (H/2)
        elif card.card == 1:
            card.res[0] += cardWidth * (-27)
        elif card.card == -2:
            card.res[0] += cardWidth * (-26)

    return hand

def sortedHand(hand):
    cards = sorted(hand, key=lambda card: card.card, reverse=True)
    return cards

if __name__ == '__main__':
    menu()
