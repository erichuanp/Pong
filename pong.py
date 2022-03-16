import random
import turtle
import winsound

# 变量
openAI = False  # AI 开关
gameStart = False  # 游戏开关
gameEnd = False
gameProcess = 0  # 游戏次数
mapWidth = 800  # 地图宽度
mapHeight = 600  # 地图高度
mapEdgeUP = (mapHeight - 10) // 2  # 地图上边界
mapEdgeDN = -mapEdgeUP  # 地图下边界
mapEdgeRT = (mapWidth - 10) // 2  # 地图左边界
mapEdgeLT = -mapEdgeRT  # 地图右边界

paddleSpeed = 10  # 球拍速度
paddleHeight = mapHeight // 100  # 球拍长度
paddleWidth = 0.2  # 球拍厚度
paddleLInitialPos = -(mapWidth - 100) // 2  # 左球拍初始位置
paddleLSpeed = 0.1  # 左球拍速度
paddleLAcceleration = 0.007  # 左球拍成长性
paddleRInitialPos = -paddleLInitialPos  # 右球拍初始位置

ballSpeed = mapWidth / 10000  # 小球速度
ballSize = 0.5  # 小球大小
ballRandMinSpeed = 1.01  # 小球速度随机最小浮点数
ballRandMaxSpeed = 1.1  # 小球速度随机最大浮点数
ballMaxXSpeed = 0.5  # 小球在X轴最大速度
ballMaxYSpeed = 0.3  # 小球在Y轴最大速度

# 游戏框架
pong = turtle.Screen()
pong.title('Pong by erichuanp')
pong.bgcolor('black')
pong.setup(width=mapWidth, height=mapHeight)

pong.tracer(0)

# 左球拍
L = turtle.Turtle()
L.speed(0)
L.shape('square')
L.color('white')
L.shapesize(stretch_wid=paddleHeight, stretch_len=paddleWidth)
L.penup()
L.goto(paddleLInitialPos, 0)
L.shapesize()
L.dy = 0.1  # 移动速度

# 右球拍
R = turtle.Turtle()
R.speed(0)
R.shape('square')
R.color('white')
R.shapesize(stretch_wid=paddleHeight, stretch_len=paddleWidth)
R.penup()
R.goto(paddleRInitialPos, 0)

# 球
B = turtle.Turtle()
B.speed(0)
B.shape('circle')
B.color('white')
B.shapesize(stretch_wid=ballSize, stretch_len=ballSize)
B.penup()
B.goto(0, 0)
B.dx = ballSpeed
B.dy = -ballSpeed

# UI绘制
scoreL = 0
scoreR = 0
pen = turtle.Turtle()
pen.speed(0)
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(0, mapHeight // 2 - 40)
pen.write('玩家 L: {}  玩家 R: {}'.format(scoreL, scoreR), align='center', font=('Courier', 24, 'normal'))

info = turtle.Turtle()
info.speed(0)
info.color('white')
info.penup()
info.hideturtle()
info.goto(0, 0)


# 移动方法
def move(pos, UpOrDown):
    if UpOrDown:
        pos += paddleSpeed * (2 + B.dy * 2)
    else:
        pos -= paddleSpeed * (2 + B.dy * 2)
    return pos


# 移动 L 的方法
def LUP():
    if gameStart and not openAI:
        L.sety(move(L.ycor(), True))


def LDN():
    if gameStart and not openAI:
        L.sety(move(L.ycor(), False))


# 移动 R 的方法
def RUP():
    if gameStart:
        R.sety(move(R.ycor(), True))


def RDN():
    if gameStart:
        R.sety(move(R.ycor(), False))


def start():
    global gameStart
    gameStart = not gameStart


# 小球回到中心
def back():
    B.goto(0, 0)
    winsound.PlaySound('SystemHand', winsound.SND_ASYNC)
    if B.dx > ballMaxXSpeed:
        B.dx = ballSpeed
    if B.dy > ballMaxYSpeed:
        B.dy = ballSpeed
    B.dx *= -1


# 小球被球拍打中
def hit():
    winsound.PlaySound('bounce.wav', winsound.SND_ASYNC)
    B.dx = B.dx * -random.uniform(ballRandMinSpeed, ballRandMaxSpeed)
    B.dy = B.dy * random.uniform(ballRandMinSpeed, ballRandMaxSpeed)


# 更新分数
def updateScore():
    global scoreR, scoreL, gameProcess
    pen.clear()
    pen.write('玩家 L: {}  玩家 R: {}'.format(scoreL, scoreR),
              align='center', font=('Courier', 24, 'normal'))
    gameProcess += 1


# AI是否打开
def ai():
    global openAI
    openAI = not openAI

def esc():
    global gameEnd
    gameEnd = True

pong.listen()
pong.onkeypress(LUP, 'w')
pong.onkeypress(LDN, 's')
pong.onkeypress(RUP, 'Up')
pong.onkeypress(RDN, 'Down')
pong.onkeypress(start, 'space')
pong.onkeypress(ai, 'c')
pong.onkeypress(esc, 'Escape')

# 持续更新游戏
while not gameEnd:
    pong.update()
    # 球移动
    if gameStart:
        B.setx(B.xcor() + B.dx)
        B.sety(B.ycor() + B.dy)
        info.clear()
    else:
        info.write('按下 Space 键开始/暂停游戏\n  按下 C 键开启/关闭人机\n   按下 Esc 键退出游戏', align='center', font=('Courier', 24, 'normal'))

    # 检测球边界且弹回
    if B.ycor() > mapEdgeUP:
        B.sety(mapEdgeUP)
        winsound.PlaySound('bounce.wav', winsound.SND_ASYNC)
        B.dy *= -1
    if B.ycor() < mapEdgeDN:
        B.sety(mapEdgeDN)
        winsound.PlaySound('bounce.wav', winsound.SND_ASYNC)
        B.dy *= -1
    if B.xcor() > mapEdgeRT:
        back()
        scoreL += 1
        updateScore()
    if B.xcor() < mapEdgeLT:
        back()
        scoreR += 1
        updateScore()

    # 检测球拍边界
    if L.ycor() > mapEdgeUP:
        L.sety(mapEdgeUP)
    if L.ycor() < mapEdgeDN:
        L.sety(mapEdgeDN)
    if R.ycor() > mapEdgeUP:
        R.sety(mapEdgeUP)
    if R.ycor() < mapEdgeDN:
        R.sety(mapEdgeDN)

    # 检测球拍击球
    if (paddleRInitialPos - 10 < B.xcor() < paddleRInitialPos) and \
            (R.ycor() + (paddleHeight * 20) // 2 > B.ycor() > R.ycor() - (paddleHeight * 20) // 2):
        B.setx(paddleRInitialPos - 10)
        hit()
    if (paddleLInitialPos + 10 > B.xcor() > paddleLInitialPos) and \
            (L.ycor() + (paddleHeight * 20) // 2 > B.ycor() > L.ycor() - (paddleHeight * 20) // 2):
        B.setx(paddleLInitialPos + 10)
        hit()

    # AI
    if openAI:
        L.dy = paddleLSpeed + gameProcess * paddleLAcceleration
        if L.ycor() != B.ycor() and B.dx < 0 and gameStart:
            if B.ycor() - L.ycor() > 0:
                L.dy = abs(L.dy)
            else:
                L.dy = -L.dy
            L.sety(L.ycor() + L.dy)
