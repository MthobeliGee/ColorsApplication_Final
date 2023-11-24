from datetime import datetime
import calendar


def checkDate(dd, mm, yyyy):
    isValid = False
    
    CurrentYear = datetime.now().year
    currentMonth = datetime.now().month
    currentday = datetime.now().day
    lastDayMonth = calendar.monthrange(datetime.now().year,datetime.now().month)[1]
    bMonths = mm - currentMonth
    bMonths = mm - currentMonth
    bMonths = mm - currentMonth
    
    if CurrentYear < yyyy and bMonths > 1:
        
        isValid = True
    if CurrentYear <= yyyy and bMonths <= 1:
        
        if bMonths > 1:
            
            isValid = True
        if bMonths == 1:
            
            days = dd+(lastDayMonth + currentday)
            
            if days >= 30:
                isValid = True
        if bMonths <1:
            if dd >= 30:
                isValid = True
                   
                   
    return isValid


valid = checkDate(1,12,2022)

print(valid)
        
            
            
            
    
        
    