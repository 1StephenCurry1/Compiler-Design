k = ['do', 'end', 'for', 'if', 'printf', 'scanf', 'then', 'while']  # 关键字表 1
s = ['+', '-', '*', '/', '++', '--', '-=', '+=', '%']  # 算术运算符：+、-、*、/；   3
r = [';', ',', '(', ')', '[', ']', '']  # 分界符： ；、，、（、）、[、]； 2
t = ['<', '<=', '=', '>', '>=', '<>']  # 关系运算符： <、<=、= 、>、>=、<>； 4
u = []  # 常数表         5
v = []  # 标识符表       6
tep = ' '  # 用于控制输出信息之间的距离
hang = 1  # 保存当前单词的行数
lie = 1  # 保存当前单词的列数
output = []  # 用于保存输出信息
jud1 = 0  # 判断当前内容是否为注释，为1表示为注释的内容
for line in open("test.txt", 'r', encoding="utf-8"):
    str = line  #每次读一行内容
    i = 0
    while i < len(str):  #遍历当前行
        if jud1 != 1:    #如果不是注释
            if str[i].isdigit():  # 字符为数字
                jud = 1  # 用于判断该单词是不是纯数字
                str1 = ''  # 用于暂时存储单词
                while i < len(str):
                    if str[i].isdigit() or str[i] == '.':
                        str1 += str[i]
                        i += 1
                    elif str[i].isalpha():
                        str1 += str[i]
                        i += 1
                        jud = 0
                    else: break  #非字母或者数字(空格或者换行)就退出当前循环
                if jud == 1:  # 全为数字，构建输出
                    if str1 not in u: u.append(str1) #为常数表添加新的元素
                    mes = [str1, f'(1,{str1})', '常数', f'({hang},{lie})']
                else:  # 夹杂有字母(错误情况,不满足标识符的要求)
                    mes = [str1, 'Error', 'Error', f'({hang},{lie})']
                lie += 1
                message = tep.join(mes) #以tep为分隔符创建一个字符串
                output.append(message)
            elif str[i].isalpha():  # 字符为字母
                str1 = ""
                while i < len(str):
                    if str[i].isdigit() or str[i].isalpha() or str[i] == '_':
                        str1 += str[i]
                        i += 1
                    else:
                        break #不满足标识符要求
                if str1 in k:   #如果在关键字表中
                    mes = [str1, f'(1,{k.index(str1)})', '关键字', f'({hang},{lie})']
                elif str1 not in v: # 标识符
                    v.append(str1)
                    mes = [str1, f'(6,{str1})', '标识符', f'({hang},{lie})']
                else:
                    mes = [str1, f'(6,{str1})', '标识符', f'({hang},{lie})']
                lie += 1
                message = tep.join(mes)
                output.append(message)
            elif (str[i] in s):  # 字符为算术运算符
                str1 = ""
                # 判断当前是否是注释
                if str[i] == '/' and i != len(str)-1 and str[i+1] == '/':
                    i = len(str)
                elif str[i] == '/' and i != len(str)-1 and str[i+1] == '*':
                    jud1 = 1
                else:
                    while i < len(str):
                        if str[i] in s:
                            str1 += str[i]
                            i += 1
                        else: break
                    if str1 in s:   # 字符为算数运算符
                        mes = [str1, f'(3,{s.index(str1)})', '算术运算符', f'({hang},{lie})']
                    else:
                        mes = [str1, 'Error', 'Error', f'({hang},{lie})']
                    lie += 1
                    message = tep.join(mes)
                    output.append(message)
            elif (str[i] in t):  # 字符为关系运算符
                str1 = ""
                while i < len(str):
                    if str[i] in t:
                        str1 += str[i]
                        i += 1
                    else: break
                if str1 in t: mes = [str1, f'(4,{t.index(str1)})', '关系运算符', f'({hang},{lie})']
                else: mes = [str1, 'Error', 'Error', f'({hang},{lie})']
                lie += 1
                message = tep.join(mes)
                output.append(message)
            elif (str[i] in r):  # 字符为分界符
                str1 = str[i]
                i += 1
                mes = [str1, f'(2,{r.index(str1)})', '分界符', f'({hang},{lie})']
                lie += 1
                message = tep.join(mes)
                output.append(message)
            elif (str[i] == ' '): i += 1  #字符为空格
            elif (str[i] == '\n'): #字符为换行
                hang += 1
                i += 1
                continue
            else: # 收尾工作(以奇怪字符开头)
                str1 = str[i]
                i += 1

                mes = [str1, 'Error', 'Error', f'({hang},{lie})']
                lie += 1
                message = tep.join(mes)
                output.append(message)
        else:   #如果当前是注释
            while str[i] != '*' or str[i+1] != '/':
                if (i < len(str)-2):
                    i += 1
                else: break
            if str[i] == '*' and i != len(str)-1 and str[i+1] == '/': #注释的结尾
                jud1 = 0
                hang -= 1
                i += 2
            else: break
for datas in output:
    data_list = datas.split(' ')
    print(f"{data_list[0]:<15}{data_list[1]:<15}{data_list[3]:<15}{data_list[2]:<15}")


