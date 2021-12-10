import sys
import copy
import pandas as pd
import statistics
from PyQt5 import QtWidgets
from forming_GRP import Ui_GRP



app = QtWidgets.QApplication(sys.argv)
GRP = QtWidgets.QWidget()
ui = Ui_GRP()
ui.setupUi(GRP)
GRP.show()


class Inpxlsx():

    def inp_first_file(self):
        global grp
        name1 = ui.lineEdit.text()
        grp = pd.read_excel(name1,header=[1], index_col=[1])
        print(name1,grp.shape)

    ui.pushButton.clicked.connect(inp_first_file)

    def inp_second_file(self):
        global grp_1
        name2 = ui.lineEdit_2.text()
        grp_1 = pd.read_excel(name2,header=[1], index_col=[1])
        print(name2,grp_1.shape)

    ui.pushButton_2.clicked.connect(inp_second_file)

    def inp_third_file(self):
        global coordinates
        name3 = ui.lineEdit_3.text()
        coordinates = pd.read_excel(name3)
        print(name3,coordinates.shape)

    ui.pushButton_3.clicked.connect(inp_third_file)

    def process(self):
        global coordinates, grp, grp_1,sotired_final
        # вычисление длины ствола гс скважины
        coordinates['Length'] = coordinates.apply(
            lambda x: ((x['Координата забоя Х (по траектории)'] - x['Координата X']) ** (2) +
                       (x['Координата забоя Y (по траектории)'] - x['Координата Y']) ** (2)) ** (0.5)
            , axis=1)
        coordinates['№ скважины'] = coordinates.apply(
            lambda x:
            str(x['№ скважины']), axis=1)
        grp.reset_index(drop=True)
        grp.reset_index(inplace=True)
        #grp = grp.drop(['Unnamed: 0', 'Подрядчик', 'Комментарии', 'Страница', 'Unnamed: 6', 'Азимут'], axis=1)
        #grp = grp.drop(
        #    ['V гель', 'V без под', 'V под', 'М бр', 'Гель', 'Конц', 'Расход', 'Эфф', 'Рпл Хорнер', 'Проппант', 'k',
        #     'Ноб', 'Нэф', 'Верх', 'Низ'], axis=1)
        #grp = grp.drop(['Xf', 'Hf', 'Wf', 'PIdsg', 'Скин-фактор', 'JD', 'FCD', 'М пр', 'Покр', 'План'], axis=1)
        grp['Номер скважины'] = grp.apply(
            lambda x:
            str(x['Номер скважины']), axis=1)
        # координаты скважин для нашего объекта
        my_wells = grp['Номер скважины'].tolist()
        my_wells_no_repeat = []
        for x in my_wells:
            if x not in my_wells_no_repeat:
                my_wells_no_repeat.append(x)
        coordinates = coordinates[
            coordinates['№ скважины'].isin(my_wells_no_repeat)].reset_index(drop=True)
        coordinates = coordinates.drop(['Координата X', 'Координата Y', 'Координата забоя Х (по траектории)',
                                        'Координата забоя Y (по траектории)'], axis=1)
        new = coordinates['№ скважины'].tolist()
        coordinates['Номер скважины'] = new
        coordinates = coordinates.drop(['№ скважины'], axis=1)
        final = grp.merge(coordinates, on='Номер скважины')
        final['Длиина ГС, м'] = final.apply(
            lambda x:
            x['Length'] if x['Наклон'] >= 70
            else 0, axis=1)
        final = final.drop(['Наклон', 'Length'], axis=1)
        final_number = final.groupby('Номер скважины').agg(
            {'Дата': lambda x:
            x.tolist()}
        )
        grp_1.reset_index(drop=True)
        grp_1.reset_index(inplace=True)
        grp_1['Скважина'] = grp_1.apply(
            lambda x:
            str(x['Скважина']), axis=1)
        grp_1 = grp_1[grp_1['Скважина'].isin(my_wells_no_repeat)].reset_index(drop=True)
        #grp_1 = grp_1.drop(['С начала мероприятия', 'С начала года', 'За текущий месяц', 'P нас', 'В-ть жидк.', 'Коб'],
        #                   axis=1)
        #grp_1 = grp_1.drop(['Пл-ть нефти', 'Факт', 'План', 'Комментарий', 'Dэк', 'Пласт', 'Страница'], axis=1)
        #grp_1 = grp_1.drop(['Unnamed: 11', 'Hэфф', 'Pпл.2', 'H дин.1', 'Pзаб.2', 'Состояние.1', 'Кпр'], axis=1)
        #grp_1 = grp_1.drop(['Скин-фактор.1', 'Интервалы перф..1', 'Насос.1', 'Напор.1', 'Производительность.1'], axis=1)
        #grp_1 = grp_1.drop(
        #    ['%.2', 'Qж.2', 'Qн.2', 'Hспуск.1', 'Кач.1', 'Част.1', 'Lхода.1', 'Метод.1', 'Скин-фактор', 'Pзаб.1',
        #     'Метод', 'Re'], axis=1)
        #grp_1 = grp_1.drop(['Pпл.1', '%.1', 'Qж.1', 'Qн.1', 'Окончание', 'Начало', 'Производительность', 'Насос'],
        #                   axis=1)
        #grp_1 = grp_1.drop(['Интервалы перф.', 'Hвд', 'Состояние', 'Pзаб', 'Pпл', 'H дин', 'Lхода', 'Напор'], axis=1)
        #grp_1 = grp_1.drop(['Месторождение', 'Unnamed: 0', 'Куст', 'Част', 'Кач', 'Hспуск', 'Qн', 'Qж', '%'], axis=1)
        #grp_1 = grp_1[grp_1['Скважина'].isin(my_wells_no_repeat)].reset_index(drop=True)
        # даты введения ГРП и ВНС на скважинах очень важно!!!!!!!
        grp_3 = copy.deepcopy(grp_1)
        grp_3 = grp_1
        grp_3['Дата ВНР после ГС \\ ГРП \\ЗБГС'] = grp_3.apply(
            lambda x:
            x['Начало.1'] if 'КР7-2' in str(x['Краткое описание мероприятий'])
            else x['Начало.1'] if 'Ввод добывающих сква' in str(x['Краткое описание мероприятий'])
            else 'нет', axis=1)
        grp_3['Тип ГТМ'] = grp_3.apply(
            lambda x:
            'ГРП' if 'КР7-2' in str(x['Краткое описание мероприятий'])
            else 'ВНС' if 'Ввод добывающих сква' in str(x['Краткое описание мероприятий'])
            else 'нет', axis=1)
        grp_3 = grp_3.drop(grp_1[grp_1['Дата ВНР после ГС \\ ГРП \\ЗБГС'] == 'нет'].index)
        grp_3 = grp_3.groupby(by=['Скважина', 'Дата ВНР после ГС \ ГРП \ЗБГС']).agg(
            {'Тип ГТМ': lambda x:
            x.tolist()[0]}
        )
        grp_3.reset_index(inplace=True)
        vvv = grp_3['Скважина'].tolist()

        grp_3['Номер скважины'] = vvv
        grp_3 = grp_3.drop(['Скважина'], axis=1)
        grp_2 = copy.deepcopy(grp_1)
        grp_2['ГРП'] = grp_2.apply(
            lambda x:
            'грп' if 'КР7-2' in str(x['Краткое описание мероприятий'])
            else 'вдс' if 'Ввод добывающих сква' in str(x['Краткое описание мероприятий'])
            else 'нет', axis=1)
        grp_2 = grp_2.drop(grp_2[grp_2['ГРП'] == 'нет'].index)
        grp_2 = grp_2.groupby('Скважина').agg(
            {'ГРП': lambda x:
            x.tolist()}
        )
        grp_2.reset_index(inplace=True)
        for i in grp_2['ГРП']:
            if 'вдс' in i:
                i.remove('вдс')
        new_1 = grp_2['Скважина'].tolist()
        grp_2['Номер скважины'] = new_1
        grp_2 = grp_2.drop(['Скважина'], axis=1)
        final = final.merge(grp_2, on='Номер скважины')
        final['Число стадий ГРП'] = final.apply(
            lambda x:
            len(x['ГРП']) if len(x['ГРП']) > 0
            else 0, axis=1)
        final = final.drop(['ГРП'], axis=1)
        # число стадий грп по фраклисту
        final = final.drop(['Дата'], axis=1)
        final_re = final.groupby(by=['Номер скважины']).agg(
            {'Число стадий ГРП': lambda x:
            statistics.mean(x)}
        )
        final_re.reset_index(inplace=True)
        final_go = final.groupby(by=['Номер скважины']).agg(
            {'Длиина ГС, м': lambda x:
            max(x)}
        )
        final_go.reset_index(inplace=True)
        final_re = final_re.merge(final_go, on='Номер скважины')
        final_re['Число стадий ГРП'] = final_re.apply(
            lambda x:
            1 if x['Длиина ГС, м'] == 0 and x['Число стадий ГРП'] >= 1
            else x['Число стадий ГРП'], axis=1)
        final_re1 = final_re
        final_re1 = final_re1.drop(final_re1[final_re1['Длиина ГС, м'] == 0].index).reset_index(drop=True)
        spisok = final_re1['Номер скважины'].tolist()
        # берем число строк из фраклиста для скважины
        final = final.groupby('Номер скважины').agg(
            {'Число стадий ГРП': lambda x:
            x.tolist()}
        )

        final['Количество'] = final.apply(
            lambda x:
            len(x['Число стадий ГРП'])
            , axis=1)
        final.reset_index(inplace=True)
        final = final[final['Номер скважины'].isin(spisok)].reset_index(drop=True)
        final = final.drop(['Число стадий ГРП'], axis=1)
        final_re2 = final_re.merge(final, on='Номер скважины')
        final_re2 = final_re2.drop(['Число стадий ГРП'], axis=1)
        cv = final_re2['Количество'].tolist()
        final_re2['Число стадий ГРП'] = cv
        final_re2 = final_re2.drop(['Количество'], axis=1)
        final_re = final_re[~final_re['Номер скважины'].isin(spisok)].reset_index(drop=True)
        new_file = pd.concat([final_re, final_re2])
        grp = grp.groupby('Номер скважины').agg(
            {'Пласт': lambda x:
            x.tolist()[0]}
        )
        grp.reset_index(inplace=True)
        new_file = new_file.merge(grp, on='Номер скважины')
        new_file['Полудлина трещины, м'] = new_file.apply(
            lambda x:
            100, axis=1)
        new_file['Ширина трещины, мм'] = new_file.apply(
            lambda x:
            4, axis=1)
        new_file['Проницаемость проппанта, Д'] = new_file.apply(
            lambda x:
            100, axis=1)
        # объединение грп и нью файла по скважинам
        sotired = grp_3.merge(new_file, on='Номер скважины')
        # добавляем последнй столбец
        sotired['ГС/ННС'] = sotired.apply(
            lambda x:
            'ННС' if x['Длиина ГС, м'] == 0
            else 'ГС', axis=1)
        # редактируем его в зависимости от наличия грп
        sotired['ГС/ННС'] = sotired.apply(
            lambda x:
            str(x['ГС/ННС']) + '+ГРП' if str(x['Тип ГТМ']) == 'ГРП'
            else x['ГС/ННС'], axis=1)
        # перемещаем столбцы в нужном порядке
        r = sotired.pop('Дата ВНР после ГС \ ГРП \ЗБГС')
        sotired1 = pd.concat([sotired, r], 1)
        # перемещаем столбцы в нужном порядке
        q = sotired1.pop('ГС/ННС')
        sotired2 = pd.concat([sotired1, q], 1)
        # перемещаем столбцы в нужном порядке
        z = sotired2.pop('Тип ГТМ')
        sotired3 = pd.concat([sotired2, z], 1)
        # перемещаем столбцы в нужном порядке
        d = sotired3.pop('Пласт')
        sotired4 = pd.concat([sotired3, d], 1)
        i = sotired4['Номер скважины'].tolist()
        sotired4['Скважина №'] = i
        sotired4 = sotired4.drop(['Номер скважины'], axis=1)
        sotired_final = sotired4.reindex(
            columns=['Скважина №', 'Длиина ГС, м', 'Число стадий ГРП', 'Полудлина трещины, м', 'Ширина трещины, мм',
                     'Проницаемость проппанта, Д', 'Дата ВНР после ГС \ ГРП \ЗБГС', 'ГС/ННС', 'Тип ГТМ', 'Пласт'])
        sotired_final['Число стадий ГРП'] = sotired.apply(
            lambda x:
            0 if str(x['Тип ГТМ']) == 'ВНС'
            else x['Число стадий ГРП'], axis=1)
        n = 1
        z = sotired_final['Пласт'].value_counts()[:n].index.tolist()
        plast = str(z[0])
        sotired_final = sotired_final.drop(sotired_final[sotired_final['Пласт'] != plast].index).reset_index(drop=True)
        zzz = sotired_final['Длиина ГС, м'].tolist()
        sotired_final['Длина ГС, м'] = zzz

        sotired_final = sotired_final.drop(['Длиина ГС, м'], axis=1)
        sotired_final = sotired_final.reindex(
            columns=['Скважина №', 'Длина ГС, м', 'Число стадий ГРП', 'Полудлина трещины, м', 'Ширина трещины, мм',
                     'Проницаемость проппанта, Д', 'Дата ВНР после ГС \ ГРП \ЗБГС', 'ГС/ННС', 'Тип ГТМ', 'Пласт'])
        # ставим нули для ВНС
        sotired_final_VNS = sotired_final.groupby('Скважина №').agg(
            {'Тип ГТМ': lambda x:
            x.tolist()}
        )
        sotired_final_VNS['тип'] = sotired_final_VNS.apply(
            lambda x: ''.join(x['Тип ГТМ'])
            , axis=1)
        sotired_final_VNS = sotired_final_VNS.drop(sotired_final_VNS[sotired_final_VNS['тип'] != 'ВНС'].index)
        sotired_final_VNS['Скважина №'] = sotired_final_VNS.index
        vns_only = sotired_final_VNS['Скважина №'].tolist()
        sotired_final_to_red = sotired_final[
            sotired_final['Скважина №'].isin(vns_only)].reset_index(drop=True)
        sotired_final_to_red['Полудлина трещины, м'] = 0
        sotired_final_to_red['Ширина трещины, мм'] = 0
        sotired_final_to_red['Проницаемость проппанта, Д'] = 0
        sotired_final = sotired_final[~sotired_final['Скважина №'].isin(vns_only)].reset_index(drop=True)
        sotired_final = pd.concat([sotired_final, sotired_final_to_red])
        sotired_final = sotired_final.reset_index(drop=True)


        #sotired_final1 = sotired4.reindex(
        #    columns=['Скважина №', 'Длина ГС, м', 'Число стадий ГРП', 'Полудлина трещины, м', 'Ширина трещины, мм',
        #             'Проницаемость проппанта, Д', 'Дата ВНР после ГС \ ГРП \ЗБГС', 'ГС/ННС', 'Тип ГТМ', 'Пласт'])
        #sotired_final.columns = ['Скважина №', 'Длина ГС, м', 'Число стадий ГРП', 'Полудлина трещины, м', 'Ширина трещины, мм',
        #            'Проницаемость проппанта, Д', 'Дата ВНР после ГС \ ГРП \ЗБГС', 'ГС/ННС', 'Тип ГТМ', 'Пласт']
        ui.lineEdit_4.setText('Успешно!')

    ui.pushButton_4.clicked.connect(process)

    def exp_file(self):
        global sotired_final

        sotired_final.to_excel('GRP_new.xlsx',index=False)

    ui.pushButton_5.clicked.connect(exp_file)


sys.exit(app.exec_())


