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
        print("1")
        isValid = True
    if CurrentYear <= yyyy and bMonths <= 1:
        print("2")
        if bMonths > 1:
            print("4")
            isValid = True
        if bMonths == 1:
            print("5")
            days = dd+(lastDayMonth - currentday)
            
            if days >= 30:
                print("6")
                isValid = True
        if bMonths <1:
            print("7")
            print("dd: ", dd)
            if mm != currentMonth:
                days = dd+(lastDayMonth - currentday)
                if days >= 30:
                    print(8)
                    isValid = True
            else:
                print("8")
                if dd >= 30:
                    print("9")
                    isValid = True
                   
                   
    return isValid


valid = checkDate(1,12,2022)

print(valid)
        
            
            
            
    
        
    