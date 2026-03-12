class Thoikhoabieu:
    def __init__(self,row,col, mon_hoc):
        self.row= row
        self.col = col 
        self.mon_hoc = mon_hoc

    def __str__(self):
        return f" {self.mon_hoc} "