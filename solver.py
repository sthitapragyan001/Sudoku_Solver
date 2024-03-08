#Jai Jagannath 🙏🙏
import copy
def blanks(grid):
    blank=[]
    for i in range(9):
        for j in range(9):
            if int(grid[i][j])==0:
                blank.append((i,j))
    return blank

def check(lis):
    cl=[]
    for j in lis:
        if int(j)>9 or int(j)<0:
            return False
        if int(j)!=0:
            if j in cl:return False
            else:cl.append(j)
    return True

def colcheck(grid,col_num):
    col=[]
    for i in range(9):
        col.append(grid[i][col_num])
    return check(col)

def blockcheck(grid,cell):
    i,j=cell
    if i<3:r=0
    elif i<6:r=3
    else:r=6
    if j<3:c=0
    elif j<6:c=3
    else:c=6
    lis=[]
    for s in range(3):
        for t in range(3):
            lis.append(grid[r+s][c+t])
    return check(lis)

def clone(grid):
    clon=copy.deepcopy(grid)
    return clon

def normal_fill(grid):
    poss={}
    blank=blanks(grid)
    if len(blank)==0:return grid,None
    flag=True
    for blnk in blank:
        poss[blnk]=[]
        for j in range(1,10):
            ngrid=clone(grid)
            ngrid[blnk[0]][blnk[1]]=j
            if blockcheck(ngrid,blnk) and colcheck(ngrid,blnk[1]) and check(ngrid[blnk[0]]):
                poss[blnk].append(j)
        if len(poss[blnk])==0:
            return grid,'wrong'
        if len(poss[blnk])==1:
            grid[blnk[0]][blnk[1]]=poss[blnk][0]
            flag=False
    if flag: 
        return grid,poss
    return normal_fill(grid)

def pro_fill(grid,poss):
    blank=blanks(grid)
    ngrid=clone(grid)
    nposs=clone(poss)
    blnk=blank[0]
    for pos in poss[blnk]:
        ngrid[blnk[0]][blnk[1]]=pos
        hngrid,hnposs=clone(ngrid),clone(nposs)
        hngrid,hnposs=fill(hngrid,hnposs)
        if hnposs=='wrong':
            pass
        elif hnposs==None:
            grid,poss=hngrid,hnposs
            return grid,poss
    return grid,'wrong'

def fill(grid,poss):
    grid,poss=normal_fill(grid)
    if poss=='wrong':
        return grid,'wrong'
    if poss==None:
        return grid,poss
    else:
        return pro_fill(grid,poss)

def main(grid):  
    poss={} 
    ans_grid=fill(grid,poss)[0]
    flg=True
    for i in ans_grid:
        for j in i:
            if j==0:
                flg=False
                break
        if not flg:break
    if flg:
        return ans_grid
    else:
        return 'wrong'
    
def display(grid):
    for i in range(9):
        print(grid[i])
    print('\n\n')

if __name__=='__main__':
    grid1=[
        [0,0,0,0,0,0,0,0,0],
        [3,0,0,0,2,0,0,9,0],
        [0,7,0,0,1,0,0,0,5],
        [6,0,0,0,0,0,0,0,8],
        [0,0,3,2,8,0,0,0,7],
        [9,0,0,0,5,0,0,0,2],
        [1,0,0,5,3,2,0,4,0],
        [0,0,6,0,0,1,0,5,0],
        [0,0,0,6,0,8,0,0,0]
        ]
    grid2=[
        [0,0,0,0,0,0,6,0,2],
        [0,2,2,9,0,5,0,0,0],
        [0,0,0,0,0,0,0,7,0],
        [0,0,6,5,0,0,0,0,0],
        [9,4,7,3,0,0,0,1,0],
        [1,0,3,0,0,0,9,0,0],
        [5,6,0,7,2,4,0,0,0],
        [3,0,9,0,0,0,0,4,0],
        [0,0,0,0,0,0,0,0,7]          
        ]
    grid=grid2
    ans_grid=main(grid)

    if ans_grid=='wrong':
        print('---Grid Unsolvable---')
    else:
        display(ans_grid)
    