from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import datetime
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QHeaderView
from collections import defaultdict
import numpy as np

# text = "E -> E + T \nE -> T\nT -> T * F\nT -> F\nF ->(E)\nF -> i"
# text = "S -> BB\nB -> aB\nB -> b"
my_dict = defaultdict(list)  # 记录各个终结符的产生式
my_dicts = defaultdict(list)  # 代表每组项目，暂时存储
VNT = []  # 终结符
VT = set([])  # 非终结符
MAX = 50  # 生成最多的项目集个数
Inum = 0  # 记录项目集的个数
end = []  # 记录，上一个状态数，通过的字符，下一个状态数[最终结果]
numset = []  # 列表，修订状态数
endstate = []  # 最终存储项目集镞 [最终结果]
guiyue = []  # 记录每条文法


def isTerminal(c):  # 若c介于A-Z之间则认为是非终结符(注意添加 self参数)
    if c < 'A' or c > 'Z':
        return True
    else:
        return False


def SplitText(text):  # 把文法中E->A|B 切分为E->A和E->B
    mytext = ""
    for i in text:
        if (i != ' '):  # 删除字符串的空格
            mytext += i;

    # 将文法化为集合
    i = mytext.split('\n')
    # 创造增广文法
    guiyue.append(text[0] + "'->" + text[0])
    # 遍历拆分后的每一行
    for j in i:
        if (VNT.count(j[0]) == 0):  # 没出现过的终结符
            VNT.append(j[0])
        for k in range(1, len(j)): # 遍历当前行(退出循环时指向右部)
            if (j[k] == '-' and j[k + 1] == '>'):
                k = k + 2
                break
        guiyue.append(j)
        my_dict[j[0]].append(j[k:])


# mylist是推导式的右部
def getFirst(mylist):  # 计算目标字符串的Frist集
    Zlist = []
    for i in mylist:
        if (i not in VNT): # 当前是终结符(终结符的first集是自己)
            Zlist.append(i)
            return Zlist
        else:
            for j in my_dict[i]:  # 遍历非终结符的产生式

                if (j[0] == i):
                    continue
                time = 0
                # 遍历产生式j的每个字符
                for ch in j:
                    if (ch not in VNT): # 如果是终结符
                        Zlist.append(ch)
                        break
                    else: # 非终结符
                        Firstlist = getFirst(ch)  # 递归得到Frist集
                        if 'ε' in Firstlist:  # Firstlist其实是指一个list
                            time += 1
                        else:
                            # 将这些字符添加到Zlist中
                            for vi in Firstlist:
                                Zlist.append(vi)
                if (time == len(j)):
                    Zlist.append('ε')
            return Zlist


def getSymbol(mystr):  # 根据Frist集得到下一个状态的展望符
    # 遍历 mystr 找点
    for i in range(0, len(mystr)):
        if (mystr[i] == '.'):
            mylist = list(mystr[i + 2:])
            break

    Zlist = ['#']
    if (mylist[0] == ','):
        mylist = mylist[1:]
    if (mylist[0] == '#'):
        VT.add('#')
        return Zlist
    a = getFirst(mylist)
    VT.update(set(a))
    return a  # 存储展望符





def CLOSURE(mystr, num):  # 用于项目集内容的补充(找等价项目)
    my_dicts[num].append(mystr)  # 先加上它本身
    zhanwang = getSymbol(mystr)  # 再计算展望符
    # 遍历mystr 记录点后面那个字符
    for i in range(0, len(mystr)):
        if (mystr[i] == '.'):
            ch = mystr[i + 1]
    # 后面那个字符是非终结符
    if (ch in VNT):
        # 遍历非终结符ch的每个产生式
        for j in range(0, len(my_dict[ch])):
            #  取得非终结符ch的一个产生式的右部ch2
            ch2 = my_dict[ch][j]
            # 遍历展望符的每个元素
            for k in range(0, len(zhanwang)):
                mystr = ch + "->." + ch2 + "," + zhanwang[k]
                # 如果新的项目不在项目集中
                if (my_dicts[num].count(mystr) == 0):
                    my_dicts[num].append(mystr) # 添加
                # 如果ch2是一个非终结符 继续向下
                if (ch2[0] in VNT):
                    for ss in my_dict[ch2[0]]:
                        zhanwangs = getSymbol(mystr)
                        for kk in range(0, len(zhanwangs)):
                            mystr2 = ch2[0] + "->." + ss + "," + zhanwangs[kk]
                            if (my_dicts[num].count(mystr2) == 0):
                                CLOSURE(mystr2, num)

    else:
        return


def deleteI(delnum):  # 删除重复状态
    for i in delnum:
        del my_dicts[i]


# 往出指的过程
def DFA(mynum):
    # 用于存储新的状态集。
    newstr = []
    # 用于存储字符到状态集序号的映射。
    command = dict()
    global Inum
    # 遍历第mynum个项目集
    for fs in my_dicts[mynum]:  # 用字典存储 目标字符和状态集序号
        # 遍历一个项目(fs) 这个循环的目的是将左部填入
        for i in range(0, len(fs)):
            if (fs[i] == '.'): #规约项目
                if (fs[i + 1] == ','):
                    break
                else: # 产生式右部
                    # 如果新的项目集还没有存储这个点后面的元素
                    if (newstr.count(fs[i + 1]) == 0):
                        newstr.append(fs[i + 1])
                        # 增加项目集序号
                        Inum += 1
                        # 将字符映射到新的状态集序号
                        command[fs[i + 1]] = Inum

    # 再遍历一次
    for fs in my_dicts[mynum]:
        for i in range(0, len(fs)):
            if (fs[i] == '.'):
                if (fs[i + 1] == ','):
                    break
                else: #遇到点后面的元素
                    # 获取这个项目在新的项目集的编号
                    mynums = command[fs[i + 1]]
                    # s1是当前项目
                    s1 = list(fs)
                    # 交换位置(点和点后元素)
                    s1[i] = s1[i + 1]
                    # 在右部的开头加点
                    s1[i + 1] = '.'
                    # 转化为字符串
                    sq = ''.join(s1)  # 巧妙实现字符串的替换
                    CLOSURE(sq, mynums)  # 找等价项目

    delnum = []

    for key, value in command.items():
        for j in range(0, value):
            if (set(my_dicts[j]) == set(my_dicts[value])): # 如果两个状态集合相同
                command[key] = j  # 修改状态序号
                delnum.append(value)
    # 删除多余的集合
    deleteI(delnum)
    for key, value in command.items():
        end.append([mynum, key, value])
        numset.append(mynum)
        numset.append(value)  # 利用集合特性，修订状态数


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(994, 824)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(520, 770, 461, 51))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(Form)
        self.textBrowser_2.setGeometry(QtCore.QRect(25, 771, 421, 41))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(460, 770, 51, 41))
        self.label.setObjectName("label")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(20, 240, 941, 521))
        self.tabWidget.setObjectName("tabWidget")
        self.First = QtWidgets.QWidget()
        self.First.setAccessibleName("")
        self.First.setObjectName("First")
        self.tableView = QtWidgets.QTableView(self.First)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 911, 471))
        self.tableView.setObjectName("tableView")
        self.tabWidget.addTab(self.First, "")
        self.Analyse = QtWidgets.QWidget()
        self.Analyse.setObjectName("Analyse")
        self.tableView_2 = QtWidgets.QTableView(self.Analyse)
        self.tableView_2.setGeometry(QtCore.QRect(10, 10, 911, 471))
        self.tableView_2.setObjectName("tableView_2")
        self.tabWidget.addTab(self.Analyse, "")
        self.Process = QtWidgets.QWidget()
        self.Process.setObjectName("Process")
        self.tableView_3 = QtWidgets.QTableView(self.Process)
        self.tableView_3.setGeometry(QtCore.QRect(10, 10, 911, 471))
        self.tableView_3.setObjectName("tableView_3")
        self.tabWidget.addTab(self.Process, "")
        self.States = QtWidgets.QWidget()
        self.States.setObjectName("States")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.States)
        self.textBrowser_3.setGeometry(QtCore.QRect(10, 10, 911, 471))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.tabWidget.addTab(self.States, "")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 10, 51, 41))
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(33, 46, 441, 181))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setText("E -> E + T \nE -> T\nT -> T * F\nT -> F\nF ->(E)\nF -> i")
        # 初始化，编译原理测试数据
        # self.textEdit.setText("S -> BB\nB -> aB\nB -> b")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(640, 200, 271, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText("i*i+i#")
        # 初始化，编译原理测试数据
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(550, 200, 81, 41))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(650, 110, 251, 71))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.Runs)  # 将按钮与函数Runs()绑定,启动主程序
        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "LR(1)文法"))
        self.label.setText(_translate("Form", "分 析："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.First), _translate("Form", "FIRST集"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Analyse), _translate("Form", "分 析 表"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Process), _translate("Form", "分 析 过 程"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.States), _translate("Form", "项 目 集 族"))
        self.label_2.setText(_translate("Form", "文 法："))
        self.label_3.setText(_translate("Form", "输 入 框"))
        self.pushButton.setText(_translate("Form", "运 行 程 序"))

    def Runs(self):
        global VNT, VT, numset, Inum, endstate, guiyue, my_dict, my_dicts, end  # 初始化
        Inum = 0  # 记录项目集的个数
        my_dict = defaultdict(list)  # 记录各个终结符的产生式
        my_dicts = defaultdict(list)  # 代表每组项目，暂时存储
        VNT = []  # 非终结符
        VT = set([])  # 终结符
        end = []  # 记录，上一个状态数，通过的字符，下一个状态数
        numset = []  # 列表，修订状态数 [最终结果]
        endstate = []  # 最终存储项目集镞 [最终结果]
        guiyue = []  # 记录每条文法
        times = datetime.datetime.now()
        times_str = times.strftime('      %Y-%m-%d   %H:%M:%S')
        self.textBrowser_2.setText('运 行 时 间：' + times_str)
        text = self.textEdit.toPlainText()

        SplitText(text)  # 1 处理文法
        input0 = text[0] + "'->." + text[0] + ',#'  # 输入第一个项目

        CLOSURE(input0, 0)  # 2 生成I0项目集
        # 为第i个项目集往外拓展
        for i in range(0, MAX):
            DFA(i)

        numset = list(set(numset))  # 3 消除重复元素

        for i in end:  # 4 修订状态过程
            i[0] = numset.index(i[0])
            i[2] = numset.index(i[2])
        for i in range(0, len(my_dicts)):
            if my_dicts[i] != []:
                endstate.append(my_dicts[i])  # 5 将修订后的项目集族写入新的列表


        # 将项目集族写入图形界面
        self.textBrowser_3.setText("\t\t\tLR(1)项 目 集 族\n")
        j = 0
        for i in endstate:
            self.textBrowser_3.append('I' + str(j) + ': ' + str(i) + '\n')
            j += 1

        # 将Frist集写入图形界面
        self.model = QStandardItemModel(len(VNT), 5)
        label_y = []
        for s in VNT:
            label_y.append(s)
        self.model.setVerticalHeaderLabels(label_y)
        for row in range(len(VNT)):
            flist = [VNT[row]]  # First集要输入一个列表
            Flist = list(set(getFirst(flist)))
            for column in range(len(Flist)):
                item = QStandardItem(Flist[column])
                self.model.setItem(row, column, item)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setModel(self.model)

        # 构造分析表，写入图形界面
        VT.discard('#')
        VT = list(VT)  # 先删除#
        VT.append('#')  # 想让#在ACTION表最后一列
        label_x = ['状 态'] + VT + VNT
        self.model2 = QStandardItemModel(len(endstate), len(VNT) + len(VT))
        self.model2.setHorizontalHeaderLabels(label_x)
        label_y = []
        for i in range(0, len(endstate)):
            label_y.append(str(i))
        self.model2.setVerticalHeaderLabels(label_y)
        ACTION = [['0'] * len(VT) for i in range(len(endstate))]  # 存储分析表内容，为分析过程做准备
        GOTO = [['0'] * len(VNT) for i in range(len(endstate))]
        for q in end:  # 移进动作
            if (q[1] not in VNT):
                ss = 's' + str(q[2])
                # 放入ACtion表中
                ACTION[int(q[0])][VT.index(q[1])] = ss
            else:
                ss = str(q[2])
                # GOTO表
                GOTO[int(q[0])][VNT.index(q[1])] = ss
            item = QStandardItem(ss)
            self.model2.setItem(int(q[0]), label_x.index(q[1]), item)
        endstr = text[0] + "'->" + text[0] + '.,#'  # 终结标志
        for i in range(len(endstate)):  # 规约动作
            for j in range(len(endstate[i])):
                for k in range(len(endstate[i][j])):
                    if (endstate[i][j][k] == '.'):
                        if (endstate[i][j][k + 1] == ','):
                            # print(guiyue)
                            ii = guiyue.index(endstate[i][j][:k])
                            item = QStandardItem("r" + str(ii))
                            ACTION[i][VT.index(endstate[i][j][k + 2])] = "r" + str(ii)
                            self.model2.setItem(i, label_x.index(endstate[i][j][k + 2]), item)
            if (endstate[i][0] == endstr):
                item = QStandardItem("acc")  # 结束
                self.model2.setItem(i, label_x.index('#'), item)
        self.tableView_2.horizontalHeader().setStretchLastSection(True)
        self.tableView_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_2.setModel(self.model2)
        self.model3 = QStandardItemModel(32, 4)
        # print(ACTION)
        # print(GOTO)
        mystate = [0]  # 状 态
        stack = '#'  # 符 号
        inputstr = self.lineEdit.text()  # 输 入 串
        label_x = ['状 态', '符 号', '输 入 串', '动 作']
        self.model3.setHorizontalHeaderLabels(label_x)
        tabnum = 0
        while (1):
            self.model3.setItem(tabnum, 0, QStandardItem(str(mystate)))
            self.model3.setItem(tabnum, 1, QStandardItem(stack))
            self.model3.setItem(tabnum, 2, QStandardItem(inputstr))
            tabnum += 1
            if (inputstr[0] not in VT):
                self.textBrowser.setText('报 错！')
            else:
                ch = ACTION[mystate[-1]][VT.index(inputstr[0])]  # 读取action值
            if (ch == 'r0'):  # 本质就是acc
                self.textBrowser.setText('分 析 成 功！')
                break
            if (ch == '0'):
                self.textBrowser.setText('报 错！')
                break
            if (ch[0] == 's'):
                mystate.append(int(ch[1:]))  # 状态加一个
                stack += inputstr[0]  # 移进
                inputstr = inputstr[1:]  # 相当于删除第一个元素
            if (ch[0] == 'r'):
                gylist = guiyue[int(ch[1:])].split('->')
                g1 = str(gylist[1])[::-1]
                g0 = str(gylist[0])[::-1]
                gstack = stack[::-1]  # 逆序解决规约问题
                gstack = gstack.replace(g1, g0, 1)
                stack = gstack[::-1]  # 完成规约任务
                strlen = len(gylist[1])  # 计算长度
                for i in range(strlen):
                    mystate.pop()  # 连续出栈
                mystate.append(int(GOTO[mystate[-1]][VNT.index(gylist[0])]))
        self.tableView_3.horizontalHeader().setStretchLastSection(True)
        self.tableView_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_3.setModel(self.model3)


if __name__ == "__main__":
    print(my_dict)
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
