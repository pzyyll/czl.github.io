import sys
import datetime, time

DIR = '_posts/'

input_date = None
if len(sys.argv) > 2:
    input_date = sys.argv[2]

title = sys.argv[1]

with open(DIR+'zztemplate.md', 'r') as f:
    content_title = f.read()

    if not input_date:
        day_title = datetime.date.today()
        today_detail = datetime.datetime.today()
    else:
        day_title = input_date
        today_detail = "{date} 00:00:00".format(date=day_title)
        
    out_file_name = DIR + "{}-{}.md".format(day_title, title)
    content = content_title.format(time=today_detail)

    with open(out_file_name, 'w') as out_stearm:
        out_stearm.write(content)

    print("out_file_name: ", out_file_name)
    print("content: ")
    print(content)