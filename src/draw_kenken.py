import pygame

# initialise the pygame font
pygame.font.init()

# # Total window
screen = pygame.display.set_mode((600, 600))

# Load test fonts for future use
font1 = pygame.font.SysFont("comicsans", 25)
font2 = pygame.font.SysFont("comicsans", 10)

class kenken_draw():
    def __init__(self,size=3):
        self.colors ={
            0:(44, 235, 232 ),
            1:(125, 206, 160),
            2:(249, 231, 159),
            3:(175, 122, 197),
            4:(51, 252, 255),
            5:(245, 183, 177),
            6:(213, 245, 227),
            7:(245, 176, 65),
            8:(52, 73, 94 ),
            9:(100, 149, 237),
            10:(246, 221, 204),
            11:(222, 49, 99),
            12:(255,0,0),
            13:(22, 160, 133),
            14:(255, 160, 122),
            15:(72, 201, 176),
            16:(250, 219, 216),
            17:(91, 235, 44 ),
            18:(208, 236, 231 ),
            19:(155, 89, 182 ),
        }
        self.dif=500 / 9
        self.size=size

    def draw_board(self,cliques,shift):
        screen.fill((0, 0, 0))
        # dif = 500 / 9
        c=1
        for group in cliques:
            # print(group)
            members,op,target = group
            for member in members:
                # print(member)
                xm=member[0]
                ym=member[1]

                # print("(",xm,ym,")")
                pygame.draw.rect(screen, self.colors[c%20], pygame.Rect(xm* self.dif +shift, ym* self.dif,  self.dif + 1, self.dif + 1))
                pygame.display.flip()
                # pygame.display.flip() 
            # print("------------------------------")
            c+=1

    def draw_grid(self,shift):
        # dif = 500 / 9
        for i in range(self.size):
            for j in range(self.size):
                # (242, 243, 244) or (166, 172, 175)
                pygame.draw.rect(screen,(242, 243, 244) , ((i+1) * self.dif +shift, (j+1) * self.dif, self.dif + 1, self.dif + 1),1)
                pygame.display.flip()

    # Fill value entered in cell	
    def draw_rule(self,cliques,shift):
        # dif = 500 / 9
        for group in cliques:
                m=1
                members,op,target = group
                for member in members:
                    if m==1:
                        # print(member)
                        xm=member[0]
                        ym=member[1]
                        txt=str(abs(target))+op
                        text1 = font2.render(txt, 1, (0,0,0))
                        # print(text1)
                        screen.blit(text1, (xm * self.dif + 5+shift, ym * self.dif + 5))
                        pygame.display.flip()
                    m +=1

    def draw_sol(self,assignemnt,shift):
        # dif = 500 / 9
        val = 0
        for group in assignemnt:
            m=0
            # print("----------------") 
            # print(group)
            for member in group:
                # print(member)
                # print("value= ",assignemnt[group][m])
                xm=member[0]
                ym=member[1]
                val= assignemnt[group][m]
                # txt=str(abs(target))+op
                text1 = font1.render(str(val), 1, (0,0,0))
                # # print(text1)
                screen.blit(text1, (xm * self.dif + 25 +shift, ym * self.dif + 20))
                pygame.display.flip()
                m+=1

    def draw(self,assignment,cages):
        # dif = 500 / 9
        shift=int((600/2)-((self.dif*(self.size/2))+self.dif))
        # print("shift= ",shift)
        kenken_draw.draw_board(self,cages,shift)
        kenken_draw.draw_grid(self,shift)
        kenken_draw.draw_rule(self,cages,shift)
        kenken_draw.draw_sol(self,assignment,shift)
