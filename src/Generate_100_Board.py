from csp_algorithms import kenken_solver
from KenKen_Game import kenken_data,kenken_generator
from time import time
import xlwt
from xlwt import Workbook

workbook = Workbook()
sheet = workbook.add_sheet('Comparison_100_Board')
header_style = xlwt.easyxf('font: bold 1; align: horiz center')
data_style = xlwt.easyxf('font: bold 1, color blue;align: horiz center')

sheet.write(0,0,'Board Number',header_style)
sheet.write(0,1,'Board Size',header_style)
sheet.write(0,2,'Backtracking Time',header_style)
sheet.write(0,3,'Forward Checking Time',header_style)
sheet.write(0,4,'Arc Consistency Time',header_style)

board_size = 3 # start of board size = 3 
row = 1 # start writing from row = 1
board_count = 1 # Board Counter 

for i in range(7):
    for j in range(15):
        sheet.write(row,0,f'{board_count}',header_style)
        sheet.write(row,1,f'{board_size}*{board_size}',data_style)

       #Generator of board
        ken = kenken_generator(board_size)
        gen_cages = ken.generate_kenken()
        ken_data = kenken_data()
        domains = ken_data.kenken_domains(board_size, gen_cages)
        neighbors_cages = ken_data.get_neighbors_cages(gen_cages)
        variables = ken_data.get_variables(gen_cages)
        ken_solver = kenken_solver()

        #backward tracking
        Time_of_BK = time()
        assignment_bk = ken_solver.backtracking_search(variables,domains,neighbors_cages)
        Time_of_BK = time()-Time_of_BK
        sheet.write(row,2,Time_of_BK,data_style)
    
        #forward checking
        Time_of_FC = time()
        assignment_fc = ken_solver.backtracking_search(variables,domains,neighbors_cages, inference="fc")
        Time_of_FC = time()-Time_of_FC
        sheet.write(row,3,Time_of_FC,data_style)
        
        #Arc Consistency
        Time_of_ARC_C= time()
        assignment_arc = ken_solver.backtracking_search(variables,domains,neighbors_cages, inference="arc")
        Time_of_ARC_C= time()-Time_of_ARC_C
        sheet.write(row,4,Time_of_ARC_C,data_style)
        
        print(f'board : {board_count} is completed')
        row = row + 1
        board_count = board_count + 1
        gen_cages = []
        variables = []
        domains = []
        neighbors_cages = []
        if(board_count == 101):
            break
        
    print(f'board size = {board_size} is completed')
    board_size = board_size + 1

workbook.save('Comparison_100_Board.xls')