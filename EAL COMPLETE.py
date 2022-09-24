import random
import pygame
import csv
import math
from datetime import date

GridSize = 5
BraidSeverity = 0.1

class Block:
    def __init__(self):
        self.Row = -1
        self.Column = -1
        self.North = 1
        self.South = 1
        self.West = 1
        self.East = 1
        self.Visited = 0
        self.Distance = 0
        self.SpeedMultiplier = 1


LOB = [Block() for block in range(GridSize**2)]

def BinaryTree(GridSize, LOB):
    Index = -1
    for Row in range(GridSize):
        for Column in range(GridSize):
            Index += 1
            LOB[Index].Row = Row
            LOB[Index].Column = Column
            Decider = random.randint(0, 1)  # 0 is north, 1 is east
            if Row == 0 and Column == GridSize - 1:
                continue
            elif Row == 0:
                Decider = 1
            elif Column == GridSize - 1:
                Decider = 0
            if Decider == 0:
                LOB[Index].North = 0
                LOB[Index - GridSize].South = 0
            elif Decider == 1:
                LOB[Index].East = 0
                LOB[Index + 1].West = 0
            DeciderSpeed = random.randint(1, 20)
            if DeciderSpeed < 3:
                LOB[Index].SpeedMultiplier = 0.5
            elif DeciderSpeed > 18:
                LOB[Index].SpeedMultiplier = 2
    return LOB

def Sidewinder(GridSize, LOB):
    Index = -1
    Run = []
    for Row in range(GridSize):
        for Column in range(GridSize):
            Index += 1
            Run.append(Index)
            LOB[Index].Row = Row
            LOB[Index].Column = Column
            Decider = random.randint(0, 1)  # 0 is north, 1 is east
            if Row == 0 and Column == GridSize - 1:
                continue
            elif Row == 0:
                Decider = 1
            elif Column == GridSize - 1:
                Decider = 0
            if Decider == 1:
                LOB[Index].East = 0
                LOB[Index + 1].West = 0
                if (Index + 1) not in Run:
                    Run.append(Index + 1)
            elif Decider == 0:
                DeciderRun = random.randint(0, len(Run) - 1)
                IndexRun = Run[DeciderRun]
                LOB[IndexRun].North = 0
                LOB[IndexRun - GridSize].South = 0
                Run = []
            DeciderSpeed = random.randint(1, 20)
            if DeciderSpeed < 3:
                LOB[Index].SpeedMultiplier = 0.5
            elif DeciderSpeed > 18:
                LOB[Index].SpeedMultiplier = 2
    for Index in range(GridSize):
        LOB[Index].North = 1
        LOB[Index + (GridSize**2 - GridSize)].South = 1
    return LOB

def AldousBroder(GridSize, LOB):
    for Block in LOB:
        Block.Visited = 0
    UnvisitedCount = GridSize ** 2
    Index = 0
    Row = Column = 0
    while UnvisitedCount != 0:
        Decider = random.randint(0, 3)
        LOB[Index].Row = Row
        LOB[Index].Column = Column
        if LOB[Index].Visited == 0:
            LOB[Index].Visited = 1
            UnvisitedCount = UnvisitedCount - 1
            DeciderSpeed = random.randint(1, 20)
            if DeciderSpeed < 3:
                LOB[Index].SpeedMultiplier = 0.5
            elif DeciderSpeed > 18:
                LOB[Index].SpeedMultiplier = 2
        if Row == 0:  # 0 is north, 1 is east, 2 is south, 3 is west
            if Column == 0:
                Decider = random.randint(1, 2)
            elif Column == GridSize - 1:
                Decider = random.randint(2, 3)
            else:
                Decider = random.randint(1, 3)
        elif Row == GridSize - 1:
            if Column == 0:
                Decider = random.randint(0, 1)
            elif Column == GridSize - 1:
                while Decider in [1, 2]:
                    Decider = random.randint(0, 3)
            else:
                while Decider == 2:
                    Decider = random.randint(0, 3)
        elif Column == 0:
            Decider = random.randint(0, 2)
        elif Column == GridSize - 1:
            while Decider == 1:
                Decider = random.randint(0, 3)

        AdjacentIndex = 0
        if Decider == 0:
            AdjacentIndex = Index - GridSize
            NewRow = Row - 1
            if LOB[AdjacentIndex].Visited == 0:
                LOB[Index].North = 0
                LOB[AdjacentIndex].South = 0
            Row = NewRow
        elif Decider == 1:
            AdjacentIndex = Index + 1
            NewColumn = Column + 1
            if LOB[AdjacentIndex].Visited == 0:
                LOB[Index].East = 0
                LOB[AdjacentIndex].West = 0
            Column = NewColumn
        elif Decider == 2:
            AdjacentIndex = Index + GridSize
            NewRow = Row + 1
            if LOB[AdjacentIndex].Visited == 0:
                LOB[Index].South = 0
                LOB[AdjacentIndex].North = 0
            Row = NewRow
        elif Decider == 3:
            AdjacentIndex = Index - 1
            NewColumn = Column - 1
            if LOB[AdjacentIndex].Visited == 0:
                LOB[Index].West = 0
                LOB[AdjacentIndex].East = 0
            Column = NewColumn
        Index = AdjacentIndex
    return LOB

def Braid(GridSize, LOB, BraidSeverity):
    Decider = 1 / BraidSeverity

    for Index in range(0, GridSize**2):
        Ends = []
        if Index % Decider == 0:
            continue
        if LOB[Index].North == 1:
            Ends.append('N')
        if LOB[Index].East == 1:
            Ends.append('E')
        if LOB[Index].South == 1:
            Ends.append('S')
        if LOB[Index].West == 1:
            Ends.append('W')

        if LOB[Index].Row == 0:
            Ends.remove('N')
        if LOB[Index].Row == GridSize - 1:
            Ends.remove('S')
        if LOB[Index].Column == 0:
            Ends.remove('W')
        if LOB[Index].Column == GridSize - 1:
            Ends.remove('E')

        if len(Ends) == 3:
            Choice = random.choice(Ends)
        else:
            continue

        if Choice == 'N':
            LOB[Index].North = 0
            LOB[Index - GridSize].South = 0
        elif Choice == 'E':
            LOB[Index].East = 0
            LOB[Index + 1].West = 0
        elif Choice == 'S':
            LOB[Index].South = 0
            LOB[Index + GridSize].North = 0
        elif Choice == 'W':
            LOB[Index].West = 0
            LOB[Index - 1].East = 0
    return LOB

def Dijkstra(LOB, GridSize, sRow, sColumn, gRow, gColumn):
    #print("Player is currently in:", sRow, sColumn) ------- Used for testing
    #print("Treasure is currently in:", gRow, gColumn) ------- Used for testing
    for Block in LOB:
        Block.Visited = 0
        Block.Distance = (GridSize**2) * 2
    VisitedCount = 1
    Index = (sRow * GridSize) + sColumn
    Frontier = []
    Frontier.append(Index)
    LOB[Index].Distance = 0
    LOB[Index].Visited = 1
    while VisitedCount < len(LOB):
        ToVisit = []
        for Index in Frontier:
            if LOB[Index].North == 0:
                ToVisit.append([Index - GridSize, LOB[Index].Distance])
            if LOB[Index].East == 0:
                ToVisit.append([Index + 1, LOB[Index].Distance])
            if LOB[Index].South == 0:
                ToVisit.append([Index + GridSize, LOB[Index].Distance])
            if LOB[Index].West == 0:
                ToVisit.append([Index - 1, LOB[Index].Distance])

        Frontier = []
        for IndexList in ToVisit:
            if LOB[IndexList[0]].SpeedMultiplier == 2:
                Weight = 0.5
                if LOB[IndexList[0]].Distance > (IndexList[1] + Weight):
                    Frontier.append(IndexList[0])
                    LOB[IndexList[0]].Distance = IndexList[1] + Weight
                    if LOB[IndexList[0]].Visited == 0:
                        VisitedCount += 1
                        LOB[IndexList[0]].Visited = 1
                    if LOB[IndexList[0]].Row == gRow and LOB[IndexList[0]].Column == gColumn:
                        #DisplayMazeAscii(GridSize, LOB)# ------- Used for testing
                        return LOB[IndexList[0]].Distance
        for IndexList in ToVisit:
            if LOB[IndexList[0]].SpeedMultiplier == 1:
                Weight = 1
                if LOB[IndexList[0]].Distance > (IndexList[1] + Weight):
                    Frontier.append(IndexList[0])
                    LOB[IndexList[0]].Distance = IndexList[1] + Weight
                    if LOB[IndexList[0]].Visited == 0:
                        VisitedCount += 1
                        LOB[IndexList[0]].Visited = 1
                    if LOB[IndexList[0]].Row == gRow and LOB[IndexList[0]].Column == gColumn:
                        #DisplayMazeAscii(GridSize, LOB)# ------- Used for testing
                        return LOB[IndexList[0]].Distance
        for IndexList in ToVisit:
            if LOB[IndexList[0]].SpeedMultiplier == 0.5:
                Weight = 2
                if LOB[IndexList[0]].Distance > (IndexList[1] + Weight):
                    Frontier.append(IndexList[0])
                    LOB[IndexList[0]].Distance = IndexList[1] + Weight
                    if LOB[IndexList[0]].Visited == 0:
                        VisitedCount += 1
                        LOB[IndexList[0]].Visited = 1
                    if LOB[IndexList[0]].Row == gRow and LOB[IndexList[0]].Column == gColumn:
                        #DisplayMazeAscii(GridSize, LOB)# ------- Used for testing
                        return LOB[IndexList[0]].Distance
    DisplayMazeAscii(GridSize, LOB)
    return LOB[(gRow * GridSize) + gColumn].Distance

def DisplayMazeAscii(GridSize, LOB): #Used for testing
    Index = -1
    for Row in range(GridSize):
        Rows1, Rows2, Rows3, Rows4 = '', '', '', ''
        for Column in range(GridSize):
            Index += 1
            if Column == 0:
                Rows1 = '#'
                Rows2 = '#'
                Rows3 = '#'
                Rows4 = '#'
            Spaces = (6 - len(str(LOB[Index].Distance))) * ' '
            if LOB[Index].East == 1:  # 6 spaces before #
                Rows2 = Rows2 + '      #'
                Rows3 = Rows3 + str(LOB[Index].Distance) + Spaces + '#'
                Rows4 = Rows4 + '      #'
            elif LOB[Index].East == 0:
                Rows2 = Rows2 + '       '
                Rows3 = Rows3 + str(LOB[Index].Distance) + Spaces + ' '
                Rows4 = Rows4 + '       '
            if LOB[Index].North == 1:
                Rows1 = Rows1 + '#######'
            elif LOB[Index].North == 0:
                Rows1 = Rows1 + '      #'
        print(Rows1)
        print(Rows2)
        print(Rows3)
        print(Rows4)
        if Row == GridSize - 1:
            print('#' * ((GridSize * 7) + 1))

def LoadMaze(c, hStart, vStart, LOB, GridSize):
    for Index in range(0, GridSize ** 2):
        if LOB[Index].North == 1:
            WallObj = Wall(c + 1, 1, hStart, vStart)
        if LOB[Index].West == 1:
            WallObj = Wall(1, c, hStart, vStart)
        if Index >= (GridSize**2 - GridSize):
            WallObj = Wall(c + 1, 1, hStart, vStart + c)
        if LOB[Index].SpeedMultiplier == 0.5:
            ModifierObj = Modifier(40, hStart + 5, vStart + 5, 'Slow')
        elif LOB[Index].SpeedMultiplier == 2:
            ModifierObj = Modifier(40, hStart + 5, vStart + 5, 'Fast')
        hStart += c
        if (Index + 1) % GridSize == 0:
            WallObj = Wall(1, c, hStart, vStart)
            hStart = 0
            vStart += c

# PYGAME ------------------------------------------------

pygame.init()
pygame.font.init()

def Menu():
    print("----------MENU----------")
    print("1. Play Game")
    print("2. View Highscores")
    print("3. Exit")
    Choice = input("Select option using number")
    return Choice

def ShowHighscores():
    with open('highscores.txt') as CsvFile:
        SpamReader = csv.DictReader(CsvFile, delimiter = ',')
        Counter = 1
        for Row in SpamReader:
            print(Counter, Row['Name'], ':', Row['Score'], ':', Row['Date'])
            if Counter == 10:
                break
            Counter += 1

def AddScore(Name, Score):
    with open('highscores.txt','r+') as CsvFile:
        SpamReader = csv.DictReader(CsvFile, delimiter = ',')
        Highscores = [[int(Score), Name, str(date.today())]]
        for Row in SpamReader:
            if Row['Score'] == 'Score':
                continue
            Highscores.append([int(Row['Score']), Row['Name'], str(Row['Date'])])
        Highscores.sort(reverse = True)
    with open('highscores.txt','w') as CsvFile:
        CsvFile.write('Score,Name,Date\n')
        for Entry in Highscores:
            CsvFile.write(str(Entry[0]))
            CsvFile.write(',')
            CsvFile.write(Entry[1])
            CsvFile.write(',')
            CsvFile.write(str(Entry[2]))
            CsvFile.write('\n')

LOS = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([c / 3, c / 3])
        self.rect = self.image.get_rect()
        self.xMoved = 0
        self.yMoved = 0
        self.Speed = c/12.5
        self.Modified = ''
        pygame.sprite.Sprite.__init__(self, LOS)

    def RecordMove(self, xChange, yChange):
        self.xMoved += xChange
        self.yMoved += yChange

    def UpdatePos(self, Walls, Treasure, Modifiers, Collision, sPath, Score, GridSize, BraidSeverity, TreasureL):
        CollisionList = pygame.sprite.spritecollide(self, Modifiers, False)
        ModifierSum = 0
        SpeedModifier = ''
        for Modifier in CollisionList:
            if Modifier.Type == 'Fast':
                ModifierSum += 1
            elif Modifier.Type == 'Slow':
                ModifierSum -= 1
        if ModifierSum > 0:
            SpeedModifier = 'Fast'
        elif ModifierSum < 0:
            SpeedModifier = 'Slow'
        elif ModifierSum == 0:
            SpeedModifier = 'Normal'

        if SpeedModifier == 'Fast' and self.Modified == '':
            self.RecordMove(self.xMoved, self.yMoved)
            self.Modified = 'Faster'
            self.Speed = self.Speed * 2
        elif SpeedModifier == 'Slow' and self.Modified == '':
            self.RecordMove(-(self.xMoved/2),-(self.yMoved/2))
            self.Modified = 'Slower'
            self.Speed = self.Speed / 2

        if SpeedModifier == 'Normal':
            if self.Modified == 'Slower':
                self.RecordMove(self.xMoved, self.yMoved)
                self.Speed = self.Speed * 2
            elif self.Modified == 'Faster':
                self.RecordMove(-self.xMoved/2, -self.yMoved/2)
                self.Speed = self.Speed / 2
            self.Modified = ''

        self.rect.x += self.xMoved

        CollisionList = pygame.sprite.spritecollide(self, Walls, False)
        for wall in CollisionList:
            if self.xMoved > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right

        self.rect.y += self.yMoved

        CollisionList = pygame.sprite.spritecollide(self, Walls, False)
        for wall in CollisionList:
            if self.yMoved > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom

        CollisionList = pygame.sprite.spritecollide(self, Treasure, False)
        if len(CollisionList) > 0 or Collision == True:
            if len(CollisionList) > 0:
                Score += 1
                if GridSize <= c/2.5:
                    GridSize += 1
                if BraidSeverity < 1:
                    BraidSeverity += 0.1
            else:
                if BraidSeverity > 0.1:
                    BraidSeverity -= 0.1
                if GridSize > 2:
                    GridSize -= 1
                Score -= 1
            #Checks if player is within boundary, if not, player co-ordinates adjusted
            if Collision == True:
                if self.rect.x > c:
                    self.rect.x -= c
                if self.rect.y > c:
                    self.rect.y -= c
            #rect.x and rect.y give the position of the top left corner of player sprite, so a half of
            #player sprite size must be added to each co-ordinate to obtain centre of player
            Collision = True
            TreasureL.UpdatePosT(GridSize, TreasureL.Row, TreasureL.Column)
            PlayerColumn = math.floor((self.rect.x + (c / 6)) / c)
            PlayerRow = math.floor((self.rect.y + (c / 6)) / c)

            Walls.empty()
            Modifiers.empty()
            LOB = [Block() for block in range(GridSize**2)]

            if Score < 5:
                LOB = BinaryTree(GridSize, LOB)

            if Score >=5 and Score < 10:
                LOB = Sidewinder(GridSize, LOB)

            elif Score >= 10:
                LOB = AldousBroder(GridSize, LOB)

            LOB = Braid(GridSize, LOB, BraidSeverity)
            LoadMaze(c, hStart, vStart, LOB, GridSize)
            try:
                sPath = Dijkstra(LOB, GridSize, PlayerRow, PlayerColumn, TreasureL.Row, TreasureL.Column)
            except IndexError:
                return self.UpdatePos(Walls, Treasure, Modifiers, Collision, sPath, Score, GridSize, BraidSeverity,
                          TreasureL)

        return Score, Collision, sPath, GridSize, BraidSeverity

LOT = pygame.sprite.Group()
class Treasure(pygame.sprite.Sprite):
    def __init__(self):
        Image = pygame.image.load("treasure.png")
        Image.convert_alpha()
        self.Row = random.randint(0, GridSize - 1)
        self.Column = random.randint(0, GridSize - 1)
        self.image = pygame.transform.scale(Image, (c // 3, c // 3))
        self.rect = self.image.get_rect()
        self.rect.x = (self.Column * c) + c // 3
        self.rect.y = (self.Row * c) + c // 3
        pygame.sprite.Sprite.__init__(self, LOT)

    def UpdatePosT(self, GridSize, OldRow, OldColumn):
        self.Row = random.randint(0, GridSize-1)
        self.Column = random.randint(0, GridSize-1)
        while self.Row == OldRow:
            self.Row = random.randint(0, GridSize - 1)
        while self.Column == OldColumn:
            self.Column = random.randint(0, GridSize - 1)
        self.rect.x = (self.Column * c) + c // 3
        self.rect.y = (self.Row * c) + c // 3

LOW = pygame.sprite.Group()
class Wall(pygame.sprite.Sprite):
    def __init__(self, Width, Height, xVertice, yVertice):
        self.image = pygame.Surface([Width, Height])
        self.Width = Width
        self.Height = Height
        self.rect = self.image.get_rect()
        self.rect.x = xVertice
        self.rect.y = yVertice
        pygame.sprite.Sprite.__init__(self, LOW)

LOM = pygame.sprite.Group()
class Modifier(pygame.sprite.Sprite):
    def __init__(self, Size,  xVertice, yVertice, Type):
        self.image = pygame.Surface([Size, Size]) #Square so width = height
        self.Type = Type
        if Type == 'Slow':
            self.image.fill((255,204,153))
        elif Type == 'Fast':
            self.image.fill((153,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = xVertice
        self.rect.y = yVertice
        pygame.sprite.Sprite.__init__(self, LOM)

# c is used to to calculate distances - ensures scale of different objects is always the same.
c = 50
hStart = 0
vStart = 0

def Game():

    GridSize = 5
    BraidSeverity = 0.1
    Difficulty = 'Easy'

    LOB = [Block() for block in range(GridSize ** 2)]
    if Difficulty == 'Easy':
        LOB = BinaryTree(GridSize, LOB)

    elif Difficulty == 'Medium':
        LOB = Sidewinder(GridSize, LOB)

    elif Difficulty == 'Hard':
        LOB = AldousBroder(GridSize, LOB)

    LOB = Braid(GridSize, LOB, BraidSeverity)
    LoadMaze(c, hStart, vStart, LOB, GridSize)


    Name = input("Enter Player Name:")
    FPS = 60
    Frame = 0
    Clock = pygame.time.Clock()
    Width = Height = GridSize * c
    Display = pygame.display.set_mode((Width, Height))
    PlayerL = Player()
    TreasureL = Treasure()
    PlayerL.rect.x = (GridSize * c / 2) + 1
    PlayerL.rect.y = (GridSize * c / 2) + 1

    Row = Column = GridSize // 2
    sPath = Dijkstra(LOB, GridSize, Row, Column, TreasureL.Row, TreasureL.Column)
    TimeFrames = (sPath * c) / PlayerL.Speed
    TimeSeconds = TimeFrames / FPS
    Ease = 5
    TargetFrame = (Frame + TimeFrames) + Ease * FPS
    SecondsRemaining = str(math.floor((TargetFrame - Frame) / FPS))
    CollisionFrame = 0
    CollisionCheck = False
    Score = Completed = 0
    Lives = 3

    Running = True
    while Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
            # Game Logic
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    PlayerL.RecordMove(0, -PlayerL.Speed)
                elif event.key == pygame.K_RIGHT:
                    PlayerL.RecordMove(PlayerL.Speed, 0)
                elif event.key == pygame.K_DOWN:
                    PlayerL.RecordMove(0, PlayerL.Speed)
                elif event.key == pygame.K_LEFT:
                    PlayerL.RecordMove(-PlayerL.Speed, 0)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    PlayerL.RecordMove(0, PlayerL.Speed)
                elif event.key == pygame.K_RIGHT:
                    PlayerL.RecordMove(-PlayerL.Speed, 0)
                elif event.key == pygame.K_DOWN:
                    PlayerL.RecordMove(0, -PlayerL.Speed)
                elif event.key == pygame.K_LEFT:
                    PlayerL.RecordMove(PlayerL.Speed, 0)

        Score, CollisionCheck, sPath, GridSize, BraidSeverity = PlayerL.UpdatePos(LOW, LOT, LOM, CollisionCheck, sPath, Score, GridSize, BraidSeverity, TreasureL)
        if CollisionCheck:
            Completed += 1
            if Completed % 10 == 0:
                Lives += 1
            CollisionFrame = Frame
            TimeFrames = (sPath * c) / PlayerL.Speed
            TimeSeconds = TimeFrames % FPS
            TargetFrame = (Frame + TimeFrames) + Ease * FPS
            if Ease > 1:
                Ease = Ease - 0.5
            Width = Height = GridSize * c
            Display = pygame.display.set_mode((Width, Height))
            CollisionCheck = False
        if (Frame - CollisionFrame) % FPS == 0:
            SecondsRemaining = str(math.floor((TargetFrame - Frame) / FPS))
        if TargetFrame < Frame:
            Lives -= 1
            if Lives == 0:
                Running = False
            CollisionCheck = True
            Score, CollisionCheck, sPath, GridSize, BraidSeverity = PlayerL.UpdatePos(LOW, LOT, LOM, CollisionCheck, sPath, Score, GridSize, BraidSeverity, TreasureL)
            CollisionFrame = Frame
            TimeFrames = (sPath * c) / PlayerL.Speed
            TimeSeconds = TimeFrames % FPS
            TargetFrame = (Frame + TimeFrames) + Ease * FPS
            if Ease < 3:
                Ease += 0.5
            Width, Height = GridSize * c, GridSize * c
            Display = pygame.display.set_mode((Width, Height))
            CollisionCheck = False
        # Drawing
        Display.fill((255, 255, 255))

        LOW.draw(Display)
        LOM.draw(Display)
        #Double digit time needs to be displayed with different dimensions to remain centred on screen
        if len(SecondsRemaining) >= 2:
            TFont = pygame.font.SysFont('calibri', (c * GridSize))
        else:
            TFont = pygame.font.SysFont('calibri', (c * GridSize) + c)
        Timer = TFont.render(SecondsRemaining, False, (0,0,0))
        Timer.set_alpha(80)
        if len(SecondsRemaining) >= 2:
            Display.blit(Timer, (0, 0))
        else:
            Display.blit(Timer, (c * GridSize / 4, 0))
        LFont = pygame.font.SysFont('calibri', (c * 2))
        LivesCounter = LFont.render(str(Lives), False, (255, 0, 0))
        LivesCounter.set_alpha(40)
        Display.blit(LivesCounter, (0, 0))
        LOT.draw(Display)
        LOS.draw(Display)
        Frame += 1
        pygame.display.flip()
        Clock.tick(FPS)
    LOS.empty()
    LOW.empty()
    LOT.empty()
    LOM.empty()

    AddScore(Name, Score)

Choice = ''
while Choice != '3':
    Choice = Menu()
    if Choice == '1':
        Game()
    elif Choice == '2':
        ShowHighscores()

    # python "EAL.py"

