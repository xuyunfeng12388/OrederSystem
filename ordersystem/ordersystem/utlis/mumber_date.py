

def member_time(times, now_time):
    # now_time = datetime.datetime.now()  # 当前日期
    addmonths = times  # 增加的月份数 往前推 就是负数 -3
    if now_time.month + addmonths > 12:
        year = now_time.year + 1
        month = (now_time.month + addmonths - 1) % 12 + 1
        day = now_time.day
        if month == 2 and now_time.day >= 28:
            day = 28
        elif day >= 30:
            day = 30
            return now_time.replace(month=month, year=year, day=day)
        return now_time.replace(month=month, year=year, day=day)
    else:
        year = now_time.year
        month = (now_time.month + addmonths - 1) % 12 + 1
        day = now_time.day
        if month == 2 and now_time.day >= 28:
            day = 28
        elif day >= 30:
            day = 30
            return now_time.replace(month=month, year=year, day=day)
        return now_time.replace(month=month, year=year, day=day)


