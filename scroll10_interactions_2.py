import pygame
pygame.init()
import time
import pickle

wn = pygame.display.set_mode((500, 500))
font1 = pygame.font.Font("AFont.ttf", 100)
font2 = pygame.font.Font("AFont.ttf", 50)

#######################################################################################################################################################################

p1 = pygame.image.load("scr10\ch1.bmp")
p2 = pygame.image.load("scr10\ch2.bmp")
p3 = pygame.image.load("scr10\ch3.bmp")
p4 = pygame.image.load("scr10\ch4.bmp")
extwin = pygame.image.load("scr10/extwin2.bmp")
chlist = [p1,p2,p3,p4]
lever1 = pygame.image.load("scr10/img_lever/lever1.png")
lever2 = pygame.image.load("scr10/img_lever/lever2.png")
ap_img = pygame.image.load("scr10/pick_item/apple.png")
trdor = pygame.image.load("scr10\crdor.bmp")
dim1 = "scr10\img_dimension1\gr"
dim2 = "scr10\img_dimension2\gr"
dim3 = "scr10\img_dimension3\gr"
dim4 = "scr10\img_dimension4\gr"
exten = ".bmp"

#######################################################################################################################################################################

'''_________________________________________________________________________LISTS___________________________________________________________________________________'''


#clever = []                                        #levers are stored in this
#oblist = []                                        #obstacles are stored in this
#inter = []                                         #interactible objects(press space to interact)
#sclist = []                                        #portals/doors are stored in this
#biglist = []                                       #big obstacles(ones with inbuilt images) are stored in this
#imglist = []                                       #free images, not bound to any particular element in the code
dimes = []                                         #dimension objects
fclist = [[50,0],[0,50],[-50,0],[0,-50]]           #used in checking where you are facing  
price_dict = {"apple":30, "orange":50}


#######################################################################################################################################################################

'''_____________________________________________________________________IMAGE LOADER FUNCTION_______________________________________________________________________'''

def imgloader(prefix, exted, ro, co):
    lis = []
    count = 1
    for m in range(ro):
        atlas = []
        for n in range(co):
            stryng = pygame.image.load((str(prefix)+str(count)+str(exted)))
            atlas.append(stryng)
            count += 1
        lis.append(atlas)
    return lis

#######################################################################################################################################################################
'''_________________________________________________________________________SAVE TRIAL______________________________________________________________________________'''

'''
def sa_for_now(filename, charei):
    print("saving...", charei)
    with open(filename, mode='wb') as f:
        pickle.dump(charei, f)

def lo_for_now(filename):
    global ma_char_in
    f = open(filename, mode='rb')
    clist = pickle.load(f)
    f.close()
    ma_char_in = character(clist[0],clist[1],clist[2],clist[3],clist[4])
'''

def sa_for_now(filename, charei):
    #charei = ma_char_in.send_savedata()
    print("saving...", charei)
    with open(filename, mode='wb') as f:
        char_info = [charei]
        save_data = [char_info]
        save_data.append(dime1.send_savedata())
        pickle.dump(save_data, f)

def lo_for_now(filename):
    global ma_char_in
    with open(filename, mode='rb') as f:
        load_data = f.readlines()
        clist = pickle.loads(load_data)[0]
    ma_char_in = character(clist[0],clist[1],clist[2],clist[3])
    


#######################################################################################################################################################################

'''______________________________________________________________________TWO BASIC CLASSES__________________________________________________________________________'''


class dimension:
    def __init__(self, pre, suf, row, col, num):
        self.pre = pre
        self.suf = suf
        self.row = row
        self.col = col
        self.num = num
        self.piclist = imgloader(self.pre, self.suf, self.row, self.col)

        self.clever = []
        self.oblist = []
        self.biglist = []
        self.sclist = []
        self.inter = []
        self.imglist = []
        
        dimes.append(self)

    def send_savedata(self):
        svlist = [self.clever,self.oblist,self.biglist,self.sclist,self.inter,self.imglist]
        return svlist

    def use_loaddata(self, lddata):
        self.clever = ldlist[0]
        self.oblist = ldlist[1]
        self.biglist = ldlist[2]
        self.sclist = ldlist[3]
        self.inter = ldlist[4]
        self.imglist = ldlist[5]
        

class character:
    def __init__(self, scroll_tup=(0,0), direction=1, progress=0, inventory={}, money=800):
        self.scrollx = scroll_tup[0]
        self.scrolly = scroll_tup[1]
        self.xpos = 250
        self.ypos = 250
        self.img = p1
        self.dir = direction
        self.dim = cur_dim.num
        self.progress = progress
        self.inventory = inventory
        self.money = money
    def mv1(self):
        if self.dir != 1:
            self.dir = 1            
        else:
            self.dir = 1
            self.scrollx += 50
            if self.scrollx > ((cur_dim.col - 1)*500) or collide():
                self.scrollx -= 50
    def mv2(self):
        if self.dir != 2:
            self.dir = 2            
        else:
            self.dir = 2
            self.scrolly += 50
            if self.scrolly > ((cur_dim.row - 1)*500) or collide():
                self.scrolly -= 50
    def mv3(self):
        if self.dir != 3:
            self.dir = 3            
        else:
            self.dir = 3
            self.scrollx -= 50
            if self.scrollx < 0 or collide():
                self.scrollx += 50
    def mv4(self):
        if self.dir != 4:
            self.dir = 4            
        else:
            self.dir = 4
            self.scrolly -= 50
            if self.scrolly < 0 or collide():
                self.scrolly += 50
    def drawbody(self):
        self.img = chlist[self.dir - 1]
        wn.blit(self.img, (225, 225))
    def facing(self):
        newx = self.scrollx + fclist[self.dir - 1][0]
        newy = self.scrolly + fclist[self.dir - 1][1]
        return (newx, newy)
    def is_facing(self):
        for some in dimes[self.dim-1].inter:
            some.actu()
            if (some.scx, some.scy) == self.facing():
                some.perf()
    def send_savedata(self):
        svlist = [(self.scrollx,self.scrolly), self.dir, self.progress, self.inventory, self.money]
        return svlist
    
dime1 = dimension(dim1, exten, 3, 3, 1)
dime2 = dimension(dim2, exten, 3, 3, 2)
dime3 = dimension(dim3, exten, 2, 2, 3)
dime4 = dimension(dim4, exten, 2, 2, 4)
cur_dim = dime1

ma_char_in = character()


#####################################################################___________________________#######################################################################

#####################################################################     FUNCTION DEFINIIONS   #######################################################################

#####################################################################___________________________#######################################################################


def change_dim(dimnum):
    global cur_dim
    if dimnum <= len(dimes):
        ma_char_in.dim = dimnum
        cur_dim = dimes[dimnum-1]

def collide():
    a = 0
    for i in cur_dim.oblist:
        i.actu()
        if (i.actx, i.acty) == (250, 250):
            a += 1
    if a > 0:    
        return True        
    else:    
        return False

def say(dialogue):
    wn.blit(extwin, (3,353))
    for line in range(len(dialogue)):
        text = font2.render(dialogue[line], True, (0,0,0), (100,100,100))
        textRect=text.get_rect()
        textRect.topleft=(5,((line*60)+355))
        wn.blit(text, textRect)
    pygame.display.update()
    cond = True
    while cond:
        for hap in pygame.event.get():
            if hap.type == pygame.QUIT:
                pygame.quit()
            if hap.type == pygame.KEYDOWN:
                if hap.key == pygame.K_RETURN:
                    cond = False

def mastersay(things):
    for i in things:
        say(i)

def xsay(dialogue):
    wn.blit(extwin, (3,353))
    for line in range(len(dialogue)):
        text = font2.render(dialogue[line], True, (0,0,0), (100,100,100))
        textRect=text.get_rect()
        textRect.topleft=(5,((line*60)+355))
        wn.blit(text, textRect)
    pygame.display.update()

def blit_cho(array,sel):
    for chno in range(len(array)):
        if chno == sel:
            colour = (255,128,0)
        else:
            colour = (0,0,0)
        text = font1.render(array[chno], True, colour, (100,100,100))
        textRect=text.get_rect()
        textRect.topright=(500,(chno*100))
        wn.blit(text, textRect)
    pygame.display.update()
    
def bloat_up(string_list):
    len_list = [len(i) for i in string_list]
    full_len = max(len_list)
    add_list = [(full_len - i) for i in len_list]
    bloated = [(string_list[i].upper() + (add_list[i]*' ')) for i in range(len(string_list))]
    return bloated
        
def bloat_b(string, till):
    len_gth = len(str(string))
    add_space = till - len_gth
    bloated = (add_space*' ') + str(string)
    return bloated

def bloat_f(string, till):
    len_gth = len(str(string))
    add_space = till - len_gth
    bloated =str(string) + (add_space*' ')
    return bloated
        
    
def present_choice(choice_array):
    choice_array = bloat_up(choice_array)
    selected = 0
    blit_cho(choice_array, selected)
    cond = True
    while cond:
        for hap in pygame.event.get():
            if hap.type == pygame.QUIT:
                pygame.quit()
            if hap.type == pygame.KEYDOWN:
                if hap.key == pygame.K_RETURN:
                    cond = False
                if hap.key == pygame.K_UP:
                    selected -= 1
                    if selected < 0:
                        selected = (len(choice_array)-1)
                    blit_cho(choice_array, selected)
                if hap.key == pygame.K_DOWN:
                    selected += 1
                    if selected >= len(choice_array):
                        selected = 0
                    blit_cho(choice_array, selected)
    return selected

def blit_count(sel, base, blo):
    sel = str(sel)
    colour = (0,0,0)
    text1 = font1.render(sel, True, colour, (100,100,100))
    textRect1=text1.get_rect()
    textRect1.topright=(500,0)
    wn.blit(text1, textRect1)
    if base != None:
        text2 = font1.render(bloat_f(int(sel)*int(base), blo), True, colour, (100,100,100))
        textRect2=text2.get_rect()
        textRect2.topleft=(0,0)
        wn.blit(text2, textRect2)
    pygame.display.update()
    

def counter_type(range_tup, allowed, base_price=None):    #if no price ascociated/given, default is None. None not 0
    i_val = range_tup[0]
    f_val = range_tup[1]
    cost = base_price
    selected = i_val
    bloat_no = len(str(cost*f_val))
    blit_count(bloat_b(selected,2), cost, bloat_no)
    cond = True
    while cond:
        for hap in pygame.event.get():
            if hap.type == pygame.QUIT:
                pygame.quit()
            if hap.type == pygame.KEYDOWN:
                if hap.key == pygame.K_RETURN:
                    cond = False
                if hap.key == pygame.K_UP:
                    if selected != f_val:
                        selected += 1                        
                        blit_count(bloat_b(selected,2), cost, bloat_no)
                        break
                        
                if hap.key == pygame.K_DOWN:
                    if selected != i_val:
                        selected -= 1
                        blit_count(bloat_b(selected,2), cost, bloat_no)
                        break

                if allowed:
                    if hap.key == pygame.K_x:
                        selected = "back"
                        cond = False
                        break
    return selected, cost
    

def performer(name):
    if name == "":
        pass
    elif name == 1:       #lever1 state1
        ownport.dim = 234173105
        dime1.sclist.remove(ownport)
    elif name == 2:       #lever1 state2
        ownport.dim = 1
        dime1.sclist.append(ownport)
    elif name == 3:       #apple giver man
        rec_item(0,1)
    elif name == 4:       #apple giver man takes apple
        rem_item(0,1)
    else:
        print(f"{name} is not a valid parameter for performer")


def rec_item(item_id, amount):
    if item_id in ma_char_in.inventory:
        ma_char_in.inventory[item_id] += amount
    else:
        ma_char_in.inventory[item_id] = amount

def rem_item(item_id, amount):
    if item_id in ma_char_in.inventory:
        if ma_char_in.inventory[item_id] >= amount:
            ma_char_in.inventory[item_id] -= amount



#####################################################################___________________________#######################################################################

#####################################################################     CLASS_DEFINITIONS     #######################################################################

#####################################################################___________________________#######################################################################


class obstacle:
    def __init__(self, scroll_tup, dim, image):
        self.scx = scroll_tup[0]
        self.scy = scroll_tup[1]
        self.dim = dim
        self.img = image
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
        if self.dim != 234173105:
            dimes[self.dim-1].oblist.append(self)

    def actu(self):
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
    def dec(self):
        self.actu()
        if -25<self.actx<525 and -25<self.acty<525:
            if self.img != None:
                wn.blit(pygame.image.load(self.img), (self.actx - 25, self.acty - 25))

'''/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''

class sign:
    def __init__(self, allargs):
        scroll_tup = allargs[0]                                                      #           REDUNDANT CLASS           #
        dim = allargs[1]
        content = allargs[2]
        image = allargs[3]
        self.cond = allargs[4]
        self.if_not_cond = allargs[5]
        self.scx = scroll_tup[0]
        self.scy = scroll_tup[1]
        self.dim = dim
        self.img = image
        self.con = content
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
        if self.dim != 234173105:
            dimes[self.dim-1].inter.append(self)
            dimes[self.dim-1].oblist.append(self)

    def actu(self):
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
    def dec(self):
        self.actu()
        if -25<self.actx<525 and -25<self.acty<525:
            if self.img != None:
                wn.blit(pygame.image.load(self.img), (self.actx - 25, self.acty - 25))
    def perf(self):
        if self.cond():
            say([self.con])
        else:
            say([self.if_not_cond])

'''/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''

#[flow_id <--not an argument(use index value instead), type, (options/dialogue(s)), [(condition,href)]]

class person:
    def __init__(self, scroll_tup, dim, content, image):
        self.scx = scroll_tup[0]
        self.scy = scroll_tup[1]
        self.dim = dim
        self.con = content
        self.img = image
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
        if self.dim != 234173105:
            dimes[self.dim-1].inter.append(self)
            dimes[self.dim-1].oblist.append(self)

    def actu(self):
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
    def dec(self):
        self.actu()
        if -25<self.actx<525 and -25<self.acty<525:
            if self.img != None:
                wn.blit(pygame.image.load(self.img), (self.actx - 25, self.acty - 25))
    def perf(self, node=0):
        cur_st = node
        convo = True
        while convo:
            if self.con[cur_st][0] == 1:                                                      #saying stuff
                mastersay(self.con[cur_st][1])
                if self.con[cur_st][2] == "end":
                    convo = False
                else:
                    cur_st = self.con[cur_st][2]

            elif self.con[cur_st][0] == 2:                                                    #present a choice
                xsay([self.con[cur_st][1][0]])
                href_index = present_choice(self.con[cur_st][1][1:len(self.con[cur_st][1])])
                if self.con[cur_st][2][href_index] == "end":
                    convo = False
                else:
                    draw_screen(False)
                    cur_st = self.con[cur_st][2][href_index]

            elif self.con[cur_st][0] == 3:                                                    #check condition and pass control accordingly
                for i in self.con[cur_st][1]:
                    if i():
                        if self.con[cur_st][2][self.con[cur_st][1].index(i)] == "end":
                            convo = False
                        else:
                            cur_st = self.con[cur_st][2][self.con[cur_st][1].index(i)]
                        break

            elif self.con[cur_st][0] == 4:                                                    #do stuff and then pass control
                performer(self.con[cur_st][1])
                if self.con[cur_st][2] == "end":
                    convo = False
                else:
                    cur_st = self.con[cur_st][2]

        
'''/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''

class pick_up_item:
    def __init__(self, scroll_tup, dim, item_id, image):
        self.item_id = item_id
        self.scx = scroll_tup[0]
        self.scy = scroll_tup[1]
        self.dim = dim
        self.img = image
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
        if self.dim != 234173105:
            dimes[self.dim-1].inter.append(self)
            dimes[self.dim-1].oblist.append(self)

    def actu(self):
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
    def dec(self):
        self.actu()
        if -25<self.actx<525 and -25<self.acty<525:
            if self.img != None:
                wn.blit(self.img, (self.actx-25,self.acty-25))
    def perf(self):
        xsay(["do you want to pick it up"])
        seltd = present_choice(['yes', 'no'])
        if seltd == 0:
            draw_screen()
            say(["You picked up a " + item_dict[self.item_id][0]])
            self.dim = 234173105
            if self.item_id in ma_char_in.inventory:
                ma_char_in.inventory[self.item_id] += 1
            else:
                ma_char_in.inventory[self.item_id] = 1
            cur_dim.oblist.remove(self)
            cur_dim.inter.remove(self)
                
        

'''/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''

class lever:
    def __init__(self, scroll_tup, dim ,state, dopara):
        self.scx = scroll_tup[0]
        self.scy = scroll_tup[1]
        self.dim = dim
        self.state = state
        self.img = lever1
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
        self.dopara = dopara
        if self.dim != 234173105:
            dimes[self.dim-1].clever.append(self)
            dimes[self.dim-1].inter.append(self)
            dimes[self.dim-1].oblist.append(self)

    def actu(self):
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
    def dec(self):
        self.actu()
        if -25<self.actx<525 and -25<self.acty<525:
            wn.blit(self.img, (self.actx-25,self.acty-25))
    def perf(self):
        time.sleep(0.15)
        if self.state == 1:
            self.state = 2
            self.img = lever2
            self.callownfunc()
        else:
            self.state = 1
            self.img = lever1
            self.callownfunc()

    def callownfunc(self):
        performer(self.dopara + self.state - 1)

'''/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''

class portal:
    def __init__(self, scroll_tup, fut_scroll_tup, od, td, image):
        self.scx = scroll_tup[0]
        self.scy = scroll_tup[1]
        self.tdx = fut_scroll_tup[0]
        self.tdy = fut_scroll_tup[1]
        self.dim = od
        self.transdim = td
        self.img = image
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify    
        if self.dim != 234173105:
            dimes[self.dim-1].sclist.append(self)

    def actu(self):
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
    def dec(self):
        self.actu()
        if -25<self.actx<525 and -25<self.acty<525:
            if self.img != None:
                wn.blit(pygame.image.load(self.img), (self.actx - 25, self.acty - 25))
    def perf(self):
        #time.sleep(1)
        change_dim(self.transdim)
        ma_char_in.scrollx = self.tdx
        ma_char_in.scrolly = self.tdy

'''/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''

class bigstacle:
    def __init__(self, scroll_tup, fut_scroll_tup, dim, rowcol_tup, door_tup, imh, td):
        self.scx = scroll_tup[0]
        self.scy = scroll_tup[1]
        self.tdx = fut_scroll_tup[0]
        self.tdy = fut_scroll_tup[1]
        self.dpx = door_tup[0]
        self.dpy = door_tup[1]
        self.nr = rowcol_tup[0]
        self.nc = rowcol_tup[1]
        self.dim = dim
        self.img = imh
        for i in range(self.nr): #150, 300
            for bs in range(self.nc):
                wex = self.scx + (bs * 50)
                wey = self.scy + (i * 50)
                if (i,bs) == (self.dpx,self.dpy):
                    door = portal((wex,wey), (self.tdx,self.tdy), self.dim, td,None)
                else:
                    childs = obstacle((wex,wey),self.dim,None)                
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify

        if self.dim != 234173105:
            dimes[self.dim-1].biglist.append(self)

    def actu(self):
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
    def dec(self):
        self.actu()
        if -500<self.actx<525 and -500<self.acty<525:
            wn.blit(pygame.image.load(self.img), (self.actx-25,self.acty-25))

'''/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''

class freemage:
    def __init__(self, scroll_tup, dim, image):
        self.scx = scroll_tup[0]
        self.scy = scroll_tup[1]
        self.dim = dim
        self.img = image
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
        if self.dim != 234173105:
            dimes[self.dim-1].imglist.append(self)

    def actu(self):
        difx = ma_char_in.scrollx - self.scx
        self.actx = (250) - difx
        dify = ma_char_in.scrolly - self.scy
        self.acty = (250) - dify
    def dec(self):
        self.actu()
        if -500<self.actx<525 and -500<self.acty<525:
            if self.img != None:
                wn.blit(pygame.image.load(self.img), (self.actx - 25, self.acty - 25))

'''/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''

class train_route:
    def __init__(self, start, end):
        pass



#######################################################################################################################################################################
'''_________________________________________________________________PERMANENT DEFINITIONS___________________________________________________________________________'''


#perma_signs = [((200,200),1,"Try Flicking the lever", None, lambda: 0 in ma_char_in.inventory, "sign is unreadable")]
    
item_dict = {
    0:('apple', 1),
    1:('orange',1),
    2:('decipher-er',2)
}



#######################################################################################################################################################################
#for ulfric in perma_signs:
#    sign(ulfric)

bsasd = portal((500, 1000), (150,250), 2, 1, "c.bmp")
ownport = portal((150, 200), (500,950), 234173105, 2, None)
plopa = lever((300,250), 1, 1, 1)
bom = bigstacle((100, 100),(250,450),1,(3,4),(2,1),"scr10\house.gif",3)
inc = bigstacle((200, 150),(150,400),3,(3,4),(2,1),"scr10\house.gif",1)
bom = bigstacle((0, 500),(150,250),3,(1,11),(0,5),"scr10\lack.bmp",1)
bar = freemage((250,500), 3, "scr10\doors\carrow.bmp")

zesin = person((200,200), 1,
              [[3, [lambda:not(0 in ma_char_in.inventory), lambda: ma_char_in.inventory[0]==0, lambda: True], [2, 2, 1]],
               [1, [["Try Flicking the lever"]], "end"],
               [1, [["Sign is unreadable"]], "end"]
              ],
              None)  

               
tlk = person((0,300),1,
             [[1, [["hello, I am a new object"], ["made using flowcharts!!"]],1],
              [2, ("do you like apples?", "yes", "no"), [2,6]],
              [3, [lambda:not(0 in ma_char_in.inventory), lambda: ma_char_in.inventory[0]<=10, lambda: True], [3, 3, 5]],
              [1, [["Here", "I'll give you one"], ["Recieved apple from", "stranger"]], 4],
              [4, 3, "end"],
              [1, [["That explains why you", "have so many"]], "end"], 
              [3, [lambda:not(0 in ma_char_in.inventory), lambda: ma_char_in.inventory[0]==0, lambda: True], [9, 9, 7]],
              [1, [["What?!", "I'll take one away for"], ["that"], ["Stranger took one apple", "from you"]], 8],
              [4, 4, "end"],
              [1, [["That's why you have none", "eh?"]], "end"] 
               ],
             "c.bmp")


app2 = pick_up_item((200,350), 1, 0, ap_img)

trprt = portal((200,450), (0,0), 1, 4, "scr10\crdor.bmp")
wall1 = obstacle((0,100), 4, None)
wall2 = obstacle((50,100), 4, None)
wall3 = obstacle((100,100), 4, None)
wall4 = obstacle((150,100), 4, None)
wall5 = obstacle((200,0), 4, None)
wall6 = obstacle((200,50), 4, None)
#final_p = counter_type((1,10), True, 10)
#######################################################################################################################################################################

def play_animation():
    for i in range(600):
        pygame.draw.circle(wn, (0,0,0), (250,250), i+50)
        pygame.draw.circle(wn, (255,255,255), (250,250), i)
        pygame.display.update()

def telepoort():
    for gohn in cur_dim.sclist:
        if (gohn.scx, gohn.scy) == (ma_char_in.scrollx, ma_char_in.scrolly):
            time.sleep(0.2)
            play_animation()
            gohn.perf()

def dosomestuff():
    telepoort()
            


def draw_screen(updoot_screen=True):
    for j in range(cur_dim.row):
        bly = (j*500) - ma_char_in.scrolly
        for k in range(cur_dim.col):
            blx = (k*500) - ma_char_in.scrollx
            wn.blit(cur_dim.piclist[j][k], (blx, bly))
    for kl in cur_dim.oblist:
        kl.dec()
    for lk in cur_dim.inter:
        lk.dec()
    for fa in cur_dim.sclist:
        fa.dec()
    for da in cur_dim.biglist:
        da.dec()
    for sl in cur_dim.imglist:
        sl.dec()
    ma_char_in.drawbody()
    if updoot_screen:
        pygame.display.update()

#######################################################################################################################################################################

draw_screen()
pygame.display.update()
clock = pygame.time.Clock()
loop = True

while loop:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        ma_char_in.mv4()
    if keys[pygame.K_DOWN]:
        ma_char_in.mv2()
    if keys[pygame.K_LEFT]:
        ma_char_in.mv3()
    if keys[pygame.K_RIGHT]:
        ma_char_in.mv1()
    if keys[pygame.K_SPACE]:
        ma_char_in.is_facing()
    if keys[pygame.K_s]:
        sa_for_now("scr10/saves/nice.txt", ma_char_in.send_savedata())
        time.sleep(0.5)
    if keys[pygame.K_l]:
        lo_for_now("scr10/saves/nice.txt")
        time.sleep(0.5)
    draw_screen()
    dosomestuff()
    draw_screen()
pygame.quit()
