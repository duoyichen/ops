#!/usr/bin/env python
# encoding: utf-8
'''
@author: duoyichen
@email: duoyichen@qq.com
@date:  
'''
import sys


def get_mail_list_from_mysql():
    import pymysql
    conn = pymysql.connect(host='122.11.50.35', user='emidc',db='easymonitord',password='dja9sdhasdasndoia)asdjaisd9)sa_fxsajs',port=3306,use_unicode=True, charset="utf8")
    cur = conn.cursor()
    sql = "select custName,linkEmails from easy_idc_custEmail where custName like '%send' group by linkEmails"
    cur.execute(sql)
    if cur.rowcount==0:
        sys.exit("sql return no customer emails!")
    mail_list = []
    for row in cur.fetchall():
        cust,email=(row[0],row[1].replace(';',',').replace(' ',''
                                                           ))
        # print(type(email))
        # print(email)
        mail_list += email.split(',')
    conn.close()
    mail_list2 = list(set(mail_list))
    # print(len(mail_list))
    # print(len(mail_list2))
    # for i in mail_list2:
    #     print(i)

    return mail_list2

# get_mail_list_from_mysql()


# 在匹配 机房名称 与 客户名称 的时候，一定要手动处理，确保二者不能同时匹配上
def get_mail_list_from_excel(excel):
    import xlrd
    workbook = xlrd.open_workbook(excel)
    # sheet_1 = workbook.sheet_by_index(0)
    # print('sheet_1: ', sheet_1)
    sheet_name_list = workbook.sheet_names()

    mail_dic = {}
    # sheet_index = 0
    mail_list = []
    for i in sheet_name_list:
        sheet_obj = workbook.sheet_by_name(i)
        num_rows = sheet_obj.nrows
        sheet00_value = sheet_obj.cell_value(0, 0).strip()
        if '机房名称' in sheet00_value:
            mail_dic[i] = {}
            # mail_dic[sheet_index] = {}
            for j in range(num_rows):
                if j == 0:
                    continue
                # print(j)
                # print(sheet_obj.cell_value(j,0),sheet_obj.cell_value(j,5))
                mail_dic[i][sheet_obj.cell_value(j,1)] = {}
                mail_dic[i][sheet_obj.cell_value(j,1)]['idc_name'] = sheet_obj.cell_value(j,0)
                mail_dic[i][sheet_obj.cell_value(j,1)]['start_time'] = sheet_obj.cell_value(j,2)
                mail_dic[i][sheet_obj.cell_value(j,1)]['end_time'] = sheet_obj.cell_value(j,3)
                mail_dic[i][sheet_obj.cell_value(j,1)]['mail_list'] = sheet_obj.cell_value(j,4)
        elif '客户名称' in sheet00_value:
            # print(i,'（sheet）: ')
            sheet_list = []
            for j in range(num_rows):
                if j == 0:
                    continue
                # print(sheet_obj.cell_value(j,1))
                sheet_list += sheet_obj.cell_value(j,1).replace(';',',').split(',')
            # print(sheet_list)
            # mail_list.extend(sheet_list)
            mail_list.append(sheet_list)
            # print(mail_list)
        else:
            continue


    if len(mail_list) != 0:
        # print(mail_list)
        # 将返回一个二层嵌套的列表
        mails = mail_list
    else:
        # print(mail_dic)
        # for k, v in mail_dic.items():
        #     print('')
        #     print('#' * 36)
        #     print(k, ':', )
        #     for k2, v2 in v.items():
        #         print('    ', k2, ': ', )
        #         for k3, v3 in v2.items():
        #             print('        ', k3, ': ', v3)
        # 将返回一个三层嵌套的字典
        mails =  mail_dic

    return mails




    # return mail_dic

# excel = '机房.xlsx'
# excel = '2019春节封网&祝福邮箱统计.xlsx'
# l = get_mail_list_from_excel(excel)
# for i in l:
#     print('去重之前：',len(i))
#     mail_list = list(set(i))
#     print('去重之后：',len(mail_list))
#     for j in i:
#         print(j)