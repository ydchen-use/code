import pymysql


def mysql_connect():
    """
    连接数据库,获取全局禁止的规则sid
    """
    try:
        # db = pymysql.connect(host="192.168.20.33",
        #                     user="reader",
        #                     passwd="Kibo@2020",
        #                     port=3306,
        #                     db = "kb_ids_new",
        #                     charset="utf8")
        db = pymysql.connect(host="192.168.129.1",
                             user="kaibo_user",
                             passwd="kaibo_user_2022",
                             port=3306,
                             db="ZOSDB",
                             charset="utf8")
        return db

    except:
        raise Exception("数据库连接失败！")


def implement_mysql(sql):
    db = mysql_connect()
    cursor = db.cursor()  # 使用cursor()方法获取游标
    for i in range(1):
        try:
            cursor.execute(sql)  # 执行sql语句
            result = cursor.fetchall()
            db.commit()
            return result
        except Exception as e:
            print(e)
            db.rollback()
            print("数据库查询失败！")
    cursor.close()
    db.close()


def get_info_mysql(ip):
    # sql = """SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'kb_ids_new' and TABLE_NAME = 'ids_asset_classify' and ip = ?;"""
    # sql = """SELECT id, updateTime FROM ids_asset_classify WHERE ip = '%s'""" %(ip)
    sql = """SELECT USER_NAME, USER_REAL_NAME FROM ONLINE_USER WHERE USER_IPV4 = '%s'""" % (ip)
    sql1 = """SELECT sid FROM kb_ids_new.ids_suricata_rules_record isrr where alarmFlag = 2;"""
    sql2 = """SELECT sid from kb_ids_new.ids_suricata_rules_classify isrc ;"""

    user_info = implement_mysql(sql)

    print(user_info)
    print(type(user_info))
    # ip_list = []
    # for i in range(len(user_info)):
    #     ip = user_info[i][2]
    #     ip_list.append(ip)
    #
    # print(ip_list)
    # result_dict = {}
    # sid_open = []  # 开启的
    # sids_open = implement_mysql(sql2)
    # for i in range(len(sids_open)):
    #     sid_open = sid_open + [str(sids_open[i][0])]
    #
    # sid_global_ban = []  # 全局禁止的
    # sids_global_ban = implement_mysql(sql1)
    # for i in range(len(sids_global_ban)):
    #     sid_global_ban = sid_global_ban + [str(sids_global_ban[i][0])]
    #
    # result_dict["sid_open_num"] = len(sids_open)
    # result_dict["sid_down_num"] = len(sids_global_ban)
    # result_dict["sid_open"] = sid_open
    # result_dict["sid_down"] = sid_global_ban
    #
    # return result_dict


if __name__ == "__main__":
    get_info_mysql('10.32.64.13')
