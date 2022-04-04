import sqlite3
import time
import datetime

SQLITE3_DB_PATH = '/usr/lib/kbids/common/ndr.db'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect(SQLITE3_DB_PATH)
conn.row_factory = dict_factory
c = conn.cursor()

now = datetime.datetime.now()
now_time = now.strftime('%Y-%m-%d %H:%M:%S')
before_two_hour = (now - datetime.timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S')

print(now_time, before_two_hour)


check_sql = f"""select ip from main.t_active_scan_results;"""

# where createTime between '{before_two_hour}' and '{now_time}'

infos = c.execute(check_sql)

final_infos = infos.fetchall()

i = 0
ip_list = []
for info in final_infos:
    if i < 10:
        ip_list.append(info.get("ip"))
        print(info)
        # break

print(len(ip_list))
c.close()
