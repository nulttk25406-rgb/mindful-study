class Deadline:
    def __init__(self, ten, ngay_gio):
        self.ten = ten
        self.ngay_gio = ngay_gio
 
    def __str__(self):
        return f"🎯 {self.ten} (Hạn chót: {self.ngay_gio})"
    
    
   