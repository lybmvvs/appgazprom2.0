import sys
import copy
import pandas as pd
import statistics
import datetime
import locale
from PyQt5 import QtWidgets
from forming_GRP_new import Ui_GRP


app = QtWidgets.QApplication(sys.argv)
GRP = QtWidgets.QWidget()
ui = Ui_GRP()
ui.setupUi(GRP)
GRP.show()


class Inpxlsx():

    def inp_first_file(self):
        global grp_dad
        name1 = ui.lineEdit.text()
        grp_dad = pd.read_excel(name1,header=[1], index_col=[1])
        print(name1,grp_dad.shape)

    ui.pushButton.clicked.connect(inp_first_file)

    def inp_second_file(self):
        global grp_gtm
        name2 = ui.lineEdit_2.text()
        grp_gtm = pd.read_excel(name2,header=[1], index_col=[1])
        print(name2,grp_gtm.shape)

    ui.pushButton_2.clicked.connect(inp_second_file)

    def inp_third_file(self):
        global coordinates
        name3 = ui.lineEdit_3.text()
        coordinates = pd.read_excel(name3)
        print(name3,coordinates.shape)

    ui.pushButton_3.clicked.connect(inp_third_file)

    def process(self):
        global coordinates, grp_dad, grp_gtm,we_here
        grp_dad.reset_index(drop=True)
        grp_dad.reset_index(inplace=True)
        #вставка 22.02.22
        grp_dad['Номер скважины'] = grp_dad.apply(
            lambda x:
            str(x['Номер скважины']), axis=1)
        grp_gtm['Скважина'] = grp_gtm.apply(
            lambda x:
            str(x['Скважина']), axis=1)
        #вставка 22.02.22
        #берем имя пласта из ячейки с текстом
        plasttt = ui.lineEdit_5.text()
        grp_dad['удалю'] = grp_dad.apply(
            lambda x:
            'нет' if plasttt in str(x['Пласт'])
            else 'да', axis=1)
        grp_dad = grp_dad.drop(grp_dad[grp_dad['удалю'] == 'да'].index).reset_index(drop=True)
        grp_dad = grp_dad.drop(['удалю'], axis=1)
        grp_gtm.reset_index(drop=True)
        grp_gtm.reset_index(inplace=True)
        grp_gtm = grp_gtm[grp_gtm['Объект разработки до ГТМ'].notna()]
#берем имя пласта из той же ячейки
        plastt = ui.lineEdit_5.text()
        grp_gtm = grp_gtm.drop(grp_gtm[grp_gtm['Объект разработки до ГТМ'] != plastt].index).reset_index(drop=True)
        coordinates['Length'] = coordinates.apply(
            lambda x: ((x['Координата забоя Х (по траектории)'] - x['Координата X']) ** (2) +
                       (x['Координата забоя Y (по траектории)'] - x['Координата Y']) ** (2)) ** (0.5)
            , axis=1)
        coordinates['№ скважины'] = coordinates.apply(
            lambda x:
            str(x['№ скважины']), axis=1)
        grp = copy.deepcopy(grp_dad)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        grp_now_we_go = copy.deepcopy(grp_gtm)

        grp_now_we_go['Скважина'] = grp_now_we_go.apply(
            lambda x:
            str(x['Скважина']), axis=1)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # grp.reset_index(drop=True)
        # grp.reset_index(inplace=True)
        # grp = grp.drop(['Unnamed: 0', 'Подрядчик', 'Комментарии', 'Страница', 'Unnamed: 6', 'Азимут'], axis=1)
        # grp = grp.drop(
        #    ['V гель', 'V без под', 'V под', 'М бр', 'Гель', 'Конц', 'Расход', 'Эфф', 'Рпл Хорнер', 'Проппант', 'k',
        #     'Ноб', 'Нэф', 'Верх', 'Низ'], axis=1)
        # grp = grp.drop(['Xf', 'Hf', 'Wf', 'PIdsg', 'Скин-фактор', 'JD', 'FCD', 'М пр', 'Покр', 'План'], axis=1)
        grp['Номер скважины'] = grp.apply(
            lambda x:
            str(x['Номер скважины']), axis=1)
        # координаты скважин для нашего объекта
        my_wells = grp['Номер скважины'].tolist()
        my_wells_no_repeat = []
        for x in my_wells:
            if x not in my_wells_no_repeat:
                my_wells_no_repeat.append(x)

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # координаты скважин для нашего объекта, которых нет во фраклисте
        my_wells_gtm = grp_now_we_go['Скважина'].tolist()
        my_wells_no_repeat_gtm = []
        for x in my_wells_gtm:
            if x not in my_wells_no_repeat_gtm:
                my_wells_no_repeat_gtm.append(x)

        my_wells_only_gtm = []
        for i in my_wells_no_repeat_gtm:
            if i not in my_wells_no_repeat:
                my_wells_only_gtm.append(i)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        wells_GTM = pd.DataFrame({"Номер скважины": my_wells_only_gtm
                                  })
        coordinates_f = coordinates[
            coordinates['№ скважины'].isin(my_wells_no_repeat)].reset_index(drop=True)
        coordinates_f = coordinates_f.drop(['Координата X', 'Координата Y', 'Координата забоя Х (по траектории)',
                                            'Координата забоя Y (по траектории)'], axis=1)
        new = coordinates_f['№ скважины'].tolist()
        coordinates_f['Номер скважины'] = new
        coordinates_f = coordinates_f.drop(['№ скважины'], axis=1)
        final = grp.merge(coordinates_f, on='Номер скважины')

        #coordinates_f = coordinates[
        #    coordinates['№ скважины'].isin(my_wells_no_repeat)].reset_index(drop=True)
        #coordinates_f = coordinates_f.drop(['Координата X', 'Координата Y', 'Координата забоя Х (по траектории)',
        #                                'Координата забоя Y (по траектории)'], axis=1)
        #new = coordinates_f['№ скважины'].tolist()
        #coordinates_f['Номер скважины'] = new
        #coordinates_f = coordinates_f.drop(['№ скважины'], axis=1)
        #final = grp.merge(coordinates_f, on='Номер скважины')
        final['Длиина ГС, м'] = final.apply(
            lambda x:
            x['Length'] if x['Наклон'] >= 70
            else 0, axis=1)
        final = final.drop(['Наклон', 'Length'], axis=1)
        final_number = final.groupby('Номер скважины').agg(
            {'Дата': lambda x:
            x.tolist()}
        )
        # !!!!!!!!!!!!!!!!!!!!!!!!!!
        coordinates_gtm = coordinates[
            coordinates['№ скважины'].isin(my_wells_only_gtm)].reset_index(drop=True)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        coordinates_gtm = coordinates_gtm.drop(['Координата X', 'Координата Y', 'Координата забоя Х (по траектории)',
                                                'Координата забоя Y (по траектории)'], axis=1)
        new_g = coordinates_gtm['№ скважины'].tolist()
        coordinates_gtm['Номер скважины'] = new_g
        coordinates_gtm = coordinates_gtm.drop(['№ скважины'], axis=1)

        wells_GTM = wells_GTM.merge(coordinates_gtm, on='Номер скважины')
        wells_GTM['Длина ГС, м'] = wells_GTM.apply(
        lambda x:
        x['Length'] if x['Length'] >= 110
        else 0, axis=1)
        wells_GTM = wells_GTM.drop(['Length'], axis=1)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        grp_ggtm = copy.deepcopy(grp_gtm)
        grp_ggtm.reset_index(drop=True)
        grp_ggtm.reset_index(inplace=True)
        grp_ggtm['Скважина'] = grp_ggtm.apply(
            lambda x:
            str(x['Скважина']), axis=1)
        grp_ggtm = grp_ggtm[grp_ggtm['Скважина'].isin(my_wells_only_gtm)].reset_index(drop=True)
        # grp_1 = grp_1.drop(['С начала мероприятия', 'С начала года', 'За текущий месяц', 'P нас', 'В-ть жидк.', 'Коб'],
        #                   axis=1)
        # grp_1 = grp_1.drop(['Пл-ть нефти', 'Факт', 'План', 'Комментарий', 'Dэк', 'Пласт', 'Страница'], axis=1)
        # grp_1 = grp_1.drop(['Unnamed: 11', 'Hэфф', 'Pпл.2', 'H дин.1', 'Pзаб.2', 'Состояние.1', 'Кпр'], axis=1)
        # grp_1 = grp_1.drop(['Скин-фактор.1', 'Интервалы перф..1', 'Насос.1', 'Напор.1', 'Производительность.1'], axis=1)
        # grp_1 = grp_1.drop(
        #    ['%.2', 'Qж.2', 'Qн.2', 'Hспуск.1', 'Кач.1', 'Част.1', 'Lхода.1', 'Метод.1', 'Скин-фактор', 'Pзаб.1',
        #     'Метод', 'Re'], axis=1)
        # grp_1 = grp_1.drop(['Pпл.1', '%.1', 'Qж.1', 'Qн.1', 'Окончание', 'Начало', 'Производительность', 'Насос'],
        #                   axis=1)
        # grp_1 = grp_1.drop(['Интервалы перф.', 'Hвд', 'Состояние', 'Pзаб', 'Pпл', 'H дин', 'Lхода', 'Напор'], axis=1)
        # grp_1 = grp_1.drop(['Месторождение', 'Unnamed: 0', 'Куст', 'Част', 'Кач', 'Hспуск', 'Qн', 'Qж', '%'], axis=1)
        # grp_1 = grp_1[grp_1['Скважина'].isin(my_wells_no_repeat)].reset_index(drop=True)
        # даты введения ГРП и ВНС на скважинах очень важно!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        grp_gang = copy.deepcopy(grp_ggtm)
        grp_gang['Дата ВНР после ГС \\ ГРП \\ЗБГС'] = grp_gang.apply(
            lambda x:
            x['ВНР.1'] if 'КР7-2' in str(x['Краткое описание мероприятий'])
            else x['ВНР.1'] if 'Ввод добывающих сква' in str(x['Краткое описание мероприятий'])
            else 'нет', axis=1)
        grp_gang['Тип ГТМ'] = grp_gang.apply(
            lambda x:
            'ГРП' if 'КР7-2' in str(x['Краткое описание мероприятий'])
            else 'ВНС' if 'Ввод добывающих сква' in str(x['Краткое описание мероприятий'])
            else 'нет', axis=1)
        grp_gang = grp_gang.drop(grp_gang[grp_gang['Дата ВНР после ГС \\ ГРП \\ЗБГС'] == 'нет'].index)
        grp_gang = grp_gang.groupby(by=['Скважина', 'Дата ВНР после ГС \ ГРП \ЗБГС']).agg(
            {'Тип ГТМ': lambda x:
            x.tolist()[0]}
        )
        grp_gang.reset_index(inplace=True)
        # GOOOOOOOOOOOOO
        grp_gang['index'] = grp_gang.index
        grp_vnski_double = grp_gang.drop(grp_gang[grp_gang['Тип ГТМ'] != 'ВНС'].index)
        grp_vnski_double['index'] = grp_vnski_double.index
        grp_vnski_double = grp_vnski_double.groupby('Скважина').agg(
            {'index': lambda x:
            x.tolist()[1:]}
        )
        sveta = []
        for i in grp_vnski_double['index']:
            sveta += i
        grp_gang = grp_gang[~grp_gang['index'].isin(sveta)].reset_index(drop=True)
        grp_gang = grp_gang.drop(['index'], axis=1)
        # GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
        vvvvv = grp_gang['Скважина'].tolist()

        grp_gang['Номер скважины'] = vvvvv
        grp_gang = grp_gang.drop(['Скважина'], axis=1)
        # !!!!!!!!!!!!!!!!!!!!!!!!
        grp_gang['Полудлина трещины, м'] = grp_gang.apply(
            lambda x:
            100, axis=1)
        grp_gang['Ширина трещины, мм'] = grp_gang.apply(
            lambda x:
            4, axis=1)
        grp_gang['Проницаемость проппанта, Д'] = grp_gang.apply(
            lambda x:
            100, axis=1)
        grp_gang['Полудлина трещины, м'] = grp_gang.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип ГТМ'])
            else x['Полудлина трещины, м']
            , axis=1)
        grp_gang['Ширина трещины, мм'] = grp_gang.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип ГТМ'])
            else x['Ширина трещины, мм']
            , axis=1)
        grp_gang['Проницаемость проппанта, Д'] = grp_gang.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип ГТМ'])
            else x['Проницаемость проппанта, Д']
            , axis=1)
        # ДОБАВИТЬ В ВНС
        grp_gang['Число стадий ГРП'] = grp_gang.apply(
            lambda x:
            1, axis=1)
        grp_gang['Число стадий ГРП'] = grp_gang.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип ГТМ'])
            else x['Число стадий ГРП']
            , axis=1)
        wells_GTM = wells_GTM.merge(grp_gang, on='Номер скважины')
        wells_GTM['ГС/ННС'] = wells_GTM.apply(
            lambda x:
            'ННС' if x['Длина ГС, м'] == 0
            else 'ГС', axis=1)
        # редактируем его в зависимости от наличия грп
        wells_GTM['ГС/ННС'] = wells_GTM.apply(
            lambda x:
            str(x['ГС/ННС']) + '+ГРП' if str(x['Тип ГТМ']) == 'ГРП'
            else x['ГС/ННС'], axis=1)
        new_400 = wells_GTM['Номер скважины'].tolist()
        wells_GTM['Скважина №'] = new_400
        wells_GTM = wells_GTM.drop(['Номер скважины'], axis=1)
        wells_GTM['Пласт'] = wells_GTM.apply(
            lambda x:
            plastt, axis=1)
        wells_GTM = wells_GTM.reindex(
            columns=['Скважина №', 'Длина ГС, м', 'Число стадий ГРП', 'Полудлина трещины, м', 'Ширина трещины, мм',
                     'Проницаемость проппанта, Д', 'Дата ВНР после ГС \ ГРП \ЗБГС', 'ГС/ННС', 'Тип ГТМ', 'Пласт'])
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        grp_1 = copy.deepcopy(grp_gtm)
        grp_1.reset_index(drop=True)
        grp_1.reset_index(inplace=True)
        grp_1['Скважина'] = grp_1.apply(
            lambda x:
            str(x['Скважина']), axis=1)
        grp_1 = grp_1[grp_1['Скважина'].isin(my_wells_no_repeat)].reset_index(drop=True)
        # grp_1 = grp_1.drop(['С начала мероприятия', 'С начала года', 'За текущий месяц', 'P нас', 'В-ть жидк.', 'Коб'],
        #                   axis=1)
        # grp_1 = grp_1.drop(['Пл-ть нефти', 'Факт', 'План', 'Комментарий', 'Dэк', 'Пласт', 'Страница'], axis=1)
        # grp_1 = grp_1.drop(['Unnamed: 11', 'Hэфф', 'Pпл.2', 'H дин.1', 'Pзаб.2', 'Состояние.1', 'Кпр'], axis=1)
        # grp_1 = grp_1.drop(['Скин-фактор.1', 'Интервалы перф..1', 'Насос.1', 'Напор.1', 'Производительность.1'], axis=1)
        # grp_1 = grp_1.drop(
        #    ['%.2', 'Qж.2', 'Qн.2', 'Hспуск.1', 'Кач.1', 'Част.1', 'Lхода.1', 'Метод.1', 'Скин-фактор', 'Pзаб.1',
        #     'Метод', 'Re'], axis=1)
        # grp_1 = grp_1.drop(['Pпл.1', '%.1', 'Qж.1', 'Qн.1', 'Окончание', 'Начало', 'Производительность', 'Насос'],
        #                   axis=1)
        # grp_1 = grp_1.drop(['Интервалы перф.', 'Hвд', 'Состояние', 'Pзаб', 'Pпл', 'H дин', 'Lхода', 'Напор'], axis=1)
        # grp_1 = grp_1.drop(['Месторождение', 'Unnamed: 0', 'Куст', 'Част', 'Кач', 'Hспуск', 'Qн', 'Qж', '%'], axis=1)
        # grp_1 = grp_1[grp_1['Скважина'].isin(my_wells_no_repeat)].reset_index(drop=True)
        # даты введения ГРП и ВНС на скважинах очень важно!!!!!!!
        grp_3 = copy.deepcopy(grp_1)
        grp_3['Дата ВНР после ГС \\ ГРП \\ЗБГС'] = grp_3.apply(
            lambda x:
            x['ВНР.1'] if 'КР7-2' in str(x['Краткое описание мероприятий'])
            else x['ВНР.1'] if 'Ввод добывающих сква' in str(x['Краткое описание мероприятий'])
            else 'нет', axis=1)
        grp_3['Тип ГТМ'] = grp_3.apply(
            lambda x:
            'ГРП' if 'КР7-2' in str(x['Краткое описание мероприятий'])
            else 'ВНС' if 'Ввод добывающих сква' in str(x['Краткое описание мероприятий'])
            else 'нет', axis=1)
        grp_3 = grp_3.drop(grp_3[grp_3['Дата ВНР после ГС \\ ГРП \\ЗБГС'] == 'нет'].index)
        grp_3 = grp_3.groupby(by=['Скважина', 'Дата ВНР после ГС \ ГРП \ЗБГС']).agg(
            {'Тип ГТМ': lambda x:
            x.tolist()[0]}
        )
        grp_3.reset_index(inplace=True)
        vvv = grp_3['Скважина'].tolist()

        grp_3['Номер скважины'] = vvv
        grp_3 = grp_3.drop(['Скважина'], axis=1)

        # GGGOOOOOOOOOOOOOOOOO
        grp_3['index'] = grp_3.index
        grp_vnski_d = grp_3.drop(grp_3[grp_3['Тип ГТМ'] != 'ВНС'].index)
        grp_vnski_d['index'] = grp_vnski_d.index
        grp_vnski_d = grp_vnski_d.groupby('Номер скважины').agg(
            {'index': lambda x:
            x.tolist()[1:]}
        )
        svetka = []
        for i in grp_vnski_d['index']:
            svetka += i
        grp_3 = grp_3[~grp_3['index'].isin(svetka)].reset_index(drop=True)
        grp_3 = grp_3.drop(['index'], axis=1)
        # GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
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
        # for i in grp_2['ГРП']:
        #    if 'вдс' in i:
        #        i.remove('вдс')
        new_1 = grp_2['Скважина'].tolist()
        grp_2['Номер скважины'] = new_1
        grp_2 = grp_2.drop(['Скважина'], axis=1)

        #WARNINGS???????????????????????????
        final = final.merge(grp_3, on='Номер скважины', how='right')
        #final = final.merge(grp_2, on='Номер скважины')
        #final['Число стадий ГРП'] = final.apply(
        #    lambda x:
        #    len(x['ГРП']) if len(x['ГРП']) > 0
        #    else 0, axis=1)
        final['Число стадий ГРП'] = final.apply(
            lambda x:
            3, axis=1)
        #final = final.drop(['ГРП'], axis=1)
        #WARNINGS??????????????????????
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
        final_re1 = copy.deepcopy(final_re)

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
        final_re2 = final_re.merge(final, on='Номер скважины', how='left')
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
        #n = 1
        #z = sotired_final['Пласт'].value_counts()[:n].index.tolist()
        #plast = str(z[0])
        plast = ui.lineEdit_5.text()
        sotired_final = sotired_final.drop(sotired_final[sotired_final['Пласт'] != plast].index).reset_index(drop=True)
        zzz = sotired_final['Длиина ГС, м'].tolist()
        sotired_final['Длина ГС, м'] = zzz

        sotired_final = sotired_final.drop(['Длиина ГС, м'], axis=1)
        sotired_final = sotired_final.reindex(
            columns=['Скважина №', 'Длина ГС, м', 'Число стадий ГРП', 'Полудлина трещины, м', 'Ширина трещины, мм',
                     'Проницаемость проппанта, Д', 'Дата ВНР после ГС \ ГРП \ЗБГС', 'ГС/ННС', 'Тип ГТМ', 'Пласт'])
        # корректное число стадий для грп разных периодов из ФРАКЛИСТА
        sotired_final['Дата ВНР после ГС \ ГРП \ЗБГС'] = sotired_final.apply(
            lambda x:
            str(x['Дата ВНР после ГС \ ГРП \ЗБГС']), axis=1)
        sotired_final['месяц с грп'] = sotired_final.apply(
            lambda x:
            x['Дата ВНР после ГС \ ГРП \ЗБГС'][:4],
            axis=1
        )
        grp_number = copy.deepcopy(grp_dad)
        # grp_number.reset_index(drop=True)
        # grp_number.reset_index(inplace=True)

        # grp=grp.drop(['Unnamed: 0','Подрядчик','Комментарии','Страница','Unnamed: 6','Азимут'],axis=1)
        # grp=grp.drop(['V гель','V без под','V под','М бр','Гель','Конц','Расход','Эфф','Рпл Хорнер','Проппант','k','Ноб','Нэф','Верх','Низ'],axis=1)
        # grp=grp.drop(['Xf','Hf','Wf','PIdsg','Скин-фактор','JD','FCD','М пр','Покр','План'],axis=1)
        grp_number['Номер скважины'] = grp_number.apply(
            lambda x:
            str(x['Номер скважины']), axis=1)
        grp_number['Дата'] = grp_number.apply(
            lambda x:
            str(x['Дата']), axis=1)
        grp_number['месяц с грп'] = grp_number.apply(
            lambda x:
            x['Дата'][:4],
            axis=1
        )
        grp_number_group = grp_number.groupby(by=['Номер скважины', 'месяц с грп']).agg(
            {'Наклон': lambda x:
            x.tolist()}
        )
        grp_number_group.reset_index(inplace=True)
        grp_number_group['число стадий'] = grp_number_group.apply(
            lambda x:
            len(x['Наклон']), axis=1)
        grp_number_group = grp_number_group.drop('Наклон', axis=1)
        blabla = grp_number_group['Номер скважины'].tolist()

        grp_number_group['Скважина №'] = blabla
        grp_number_group = grp_number_group.drop(['Номер скважины'], axis=1)
        sotired_final = sotired_final.merge(grp_number_group, on=['месяц с грп', 'Скважина №'], how='left')
        milan = sotired_final['число стадий'].tolist()
        sotired_final = sotired_final.drop(['Число стадий ГРП'], axis=1)
        sotired_final['Число стадий ГРП'] = milan
        sotired_final = sotired_final.drop(['число стадий'], axis=1)
        sotired_final['Дата ВНР после ГС \ ГРП \ЗБГС'] = pd.to_datetime(sotired_final['Дата ВНР после ГС \ ГРП \ЗБГС'])
        sotired_final = sotired_final.reindex(
            columns=['Скважина №', 'Длина ГС, м', 'Число стадий ГРП', 'Полудлина трещины, м', 'Ширина трещины, мм',
                     'Проницаемость проппанта, Д', 'Дата ВНР после ГС \ ГРП \ЗБГС', 'ГС/ННС', 'Тип ГТМ', 'Пласт',
                     'месяц с грп'])
        sotired_final = pd.concat([sotired_final, wells_GTM])
        # ставим нули для ВНС
        sotired_final['Полудлина трещины, м'] = sotired_final.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип ГТМ'])
            else x['Полудлина трещины, м']
            , axis=1)
        sotired_final['Ширина трещины, мм'] = sotired_final.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип ГТМ'])
            else x['Ширина трещины, мм']
            , axis=1)
        sotired_final['Проницаемость проппанта, Д'] = sotired_final.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип ГТМ'])
            else x['Проницаемость проппанта, Д']
            , axis=1)
        # ДОБАВИТЬ В ВНС
        sotired_final['Число стадий ГРП'] = sotired_final.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип ГТМ'])
            else x['Число стадий ГРП']
            , axis=1)
        sotired_final.reset_index(drop=True)
        sotired_final.reset_index(inplace=True)
        # sotired_final = sotired_final.drop(['level_0'], axis=1)
        sotired_final = sotired_final.drop(['index'], axis=1)
        sotired_final["is_duplicate"] = sotired_final.duplicated()
        sotired_final = sotired_final.drop(sotired_final[sotired_final['is_duplicate'] == True].index)
        sotired_final.reset_index(inplace=True)
        sotired_final = sotired_final.drop(['index'], axis=1)
        sotired_final['level_0'] = sotired_final.index
        # удаляем если в одном месяце
        dele = copy.deepcopy(sotired_final)
        dele['чек'] = dele.apply(
            lambda x:
            x['Скважина №'].partition('_')[0] if '_' in str(x['Скважина №'])
            else x['Скважина №'], axis=1)
        dele['месяц'] = dele.apply(
            lambda x:
            str(x['Дата ВНР после ГС \ ГРП \ЗБГС'])[:7],
            axis=1
        )
        dele = dele.groupby(by=['чек', 'месяц']).agg(
            {'level_0': lambda x:
            x.tolist()}
        )
        dele['скока_их'] = dele.apply(
            lambda x: len(x['level_0'])
            , axis=1)
        dele = dele.drop(dele[dele['скока_их'] < 2].index).reset_index(drop=True)
        to_stay = []
        all_wells = []
        for i in dele['level_0']:
            all_wells += i
        for i in dele['level_0']:
            to_stay.append(i[-1])
        # замена
        alli = copy.deepcopy(sotired_final)
        alli = alli[alli['level_0'].isin(all_wells)].reset_index(drop=True)
        if alli.shape[0] != 0:

            alli = alli.drop(alli[alli['Тип ГТМ'] == 'ВНС'].index).reset_index(drop=True)
            alli = alli.groupby('Скважина №').agg(
            {'level_0': lambda x:
            x.tolist()[0]}
            )
            definetely_stay = alli['level_0'].tolist()
            array_3 = list(all_wells)
            for x in definetely_stay:
                try:
                    array_3.remove(x)
                except ValueError:
                    pass
        # вот досюда
            sotired_final = sotired_final[~sotired_final['level_0'].isin(array_3)].reset_index(drop=True)
        sotired_final = sotired_final.drop(['level_0'], axis=1)
        # проверяем ЗБС
        grp_4 = copy.deepcopy(grp_gtm)

        grp_4['Скважина'] = grp_4.apply(
            lambda x:
            str(x['Скважина']), axis=1)
        grp_4 = grp_4[grp_4['Скважина'].isin(my_wells_no_repeat + my_wells_only_gtm)].reset_index(drop=True)
        # grp_4
        grp_zbs = grp_4.drop(grp_4[grp_4['Тип'] != '3БС'].index).reset_index(drop=True)
        # grp_zbs = grp_4.loc[grp_4['Тип'] == 'ЗБС']
        grp_zbs = grp_zbs.groupby('Скважина').agg(
            {'Начало.1': lambda x:
            x.tolist()[1] if len(x.tolist()) > 1
            else x.tolist()[0]}
        )
        grp_zbs.reset_index(drop=True)
        grp_zbs.reset_index(inplace=True)
        # grp_zbs

        vv = grp_zbs['Скважина'].tolist()

        grp_zbs['Скважина №'] = vv
        grp_zbs = grp_zbs.drop(['Скважина'], axis=1)
        sotired_final_zbs = sotired_final.merge(grp_zbs, on='Скважина №')
        # sotired_final_zbs
        abba = sotired_final_zbs['Скважина №'].tolist()
        # abba
        if sotired_final_zbs.shape[0] != 0:
            sotired_final_zbs['Длина ГС, м'] = sotired_final_zbs.apply(
            lambda x:
            0 if x['Дата ВНР после ГС \ ГРП \ЗБГС'] < x['Начало.1'] else x['Длина ГС, м'],
            axis=1
            )
            sotired_final_zbs['Число стадий ГРП'] = sotired_final_zbs.apply(
            lambda x:
            1 if x['Дата ВНР после ГС \ ГРП \ЗБГС'] < x['Начало.1'] else x['Число стадий ГРП'],
            axis=1
            )
            sotired_final_zbs['Скважина №'] = sotired_final_zbs.apply(
            lambda x:
            str(x['Скважина №'])
            + ('_Л' if x['Длина ГС, м'] == 0 else ''),
            axis=1
            )
            sotired_final_zbs['L'] = sotired_final_zbs.apply(
                lambda x:
                1 if 'Л' in str(x['Скважина №'])
                else 0, axis=1)
            sotired_final_zbs['ГС/ННС'] = sotired_final_zbs.apply(
                lambda x:
                str(x['ГС/ННС']).replace('ГС', 'ННС') if x['L'] == 1 else str(x['ГС/ННС']),
                axis=1
            )
            sotired_final_zbs = sotired_final_zbs.drop(['L'], axis=1)
            sotired_final_zbs = sotired_final_zbs.drop(['Начало.1'], axis=1)
            sotired_final = sotired_final[~sotired_final['Скважина №'].isin(abba)].reset_index(drop=True)
        sotired_final1 = pd.concat([sotired_final, sotired_final_zbs])
        sotired_final1.reset_index(drop=True)
        sotired_final1.reset_index(inplace=True)
        # приставка ФРАК там где надо
        sotired_final.reset_index(drop=True)
        sotired_final.reset_index(inplace=True)
        step = sotired_final.drop(
            sotired_final[(sotired_final['ГС/ННС'] == 'ГС') | (sotired_final['ГС/ННС'] == 'ННС')].index)
        step['для_фрак'] = step.apply(
            lambda x:
            x['Скважина №'].partition('_')[0] if '_' in str(x['Скважина №'])
            else x['Скважина №'], axis=1)
        step = step.groupby(by=['для_фрак']).agg(
            {'index': lambda x:
            x.tolist()}
        )
        step.reset_index(inplace=True)
        step.rename(columns={'для_фрак': 'список'}, inplace=True)

        step['Length'] = step.apply(
            lambda x: len(x['index'])
            , axis=1)
        step = step.drop(step[step['Length'] < 1].index)
        gang1 = []
        gang2 = []
        gang3 = []
        gang4 = []
        gang5 = []
        gang6 = []
        gang7 = []
        gang8 = []
        gang9 = []
        gang10 = []
        for i in step['index']:
            if len(i) >= 1:
                gang1.append(i[0])
            if len(i) >= 2:
                gang2.append(i[1])
            if len(i) >= 3:
                gang3.append(i[2])
            if len(i) >= 4:
                gang4.append(i[3])
            if len(i) >= 5:
                gang5.append(i[4])
            if len(i) >= 6:
                gang6.append(i[5])
            if len(i) >= 7:
                gang7.append(i[6])
            if len(i) >= 8:
                gang8.append(i[7])
            if len(i) >= 9:
                gang9.append(i[8])
            if len(i) >= 10:
                gang10.append(i[9])
            else:
                pass
        sotired_final['Скважина №'] = sotired_final.apply(
            lambda x:
            x['Скважина №'] + '_ГРП' if x['index'] in gang1
            else x['Скважина №'], axis=1)
        sotired_final['Скважина №'] = sotired_final.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_1' if x['index'] in gang2
            else x['Скважина №'], axis=1)
        sotired_final['Скважина №'] = sotired_final.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_2' if x['index'] in gang3
            else x['Скважина №'], axis=1)
        sotired_final['Скважина №'] = sotired_final.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_3' if x['index'] in gang4
            else x['Скважина №'], axis=1)
        sotired_final['Скважина №'] = sotired_final.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_4' if x['index'] in gang5
            else x['Скважина №'], axis=1)
        sotired_final['Скважина №'] = sotired_final.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_5' if x['index'] in gang6
            else x['Скважина №'], axis=1)
        sotired_final['Скважина №'] = sotired_final.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_6' if x['index'] in gang7
            else x['Скважина №'], axis=1)
        sotired_final['Скважина №'] = sotired_final.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_7' if x['index'] in gang8
            else x['Скважина №'], axis=1)
        sotired_final['Скважина №'] = sotired_final.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_8' if x['index'] in gang9
            else x['Скважина №'], axis=1)
        sotired_final['Скважина №'] = sotired_final.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_9' if x['index'] in gang10
            else x['Скважина №'], axis=1)
        sotired_final = sotired_final.drop(['index'], axis=1)
        # sotired_final = sotired_final.drop(['месяц с грп'], axis=1)
        sotired_final = sotired_final.drop(['месяц с грп'], axis=1)
        sotired_final = sotired_final.drop(['is_duplicate'], axis=1)
        sotired_final.reset_index(drop=True)
        sotired_final.reset_index(inplace=True)
        sotired_final = sotired_final.drop(['index'], axis=1)
        sotired_final['Число стадий ГРП'] = sotired_final.apply(
            lambda x:
            1 if x['Длина ГС, м'] == 0 and 'ГРП' in x['ГС/ННС']
            else x['Число стадий ГРП'], axis=1)
        sotired_final_zbs.reset_index(drop=True)
        sotired_final_zbs.reset_index(inplace=True)
        step1 = sotired_final_zbs.drop(
            sotired_final_zbs[(sotired_final_zbs['ГС/ННС'] == 'ГС') | (sotired_final_zbs['ГС/ННС'] == 'ННС')].index)
        step1 = step1.groupby(by=['Скважина №']).agg(
            {'index': lambda x:
            x.tolist()}
        )
        step1.reset_index(inplace=True)
        step1['Length'] = step1.apply(
            lambda x: len(x['index'])
            , axis=1)
        step1 = step1.drop(step1[step1['Length'] < 1].index)
        gang11 = []
        gang21 = []
        gang31 = []
        gang41 = []
        gang51 = []
        gang61 = []
        gang71 = []
        gang81 = []
        gang91 = []
        gang101 = []
        for i in step1['index']:
            if len(i) >= 1:
                gang11.append(i[0])
            if len(i) >= 2:
                gang21.append(i[1])
            if len(i) >= 3:
                gang31.append(i[2])
            if len(i) >= 4:
                gang41.append(i[3])
            if len(i) >= 5:
                gang51.append(i[4])
            if len(i) >= 6:
                gang61.append(i[5])
            if len(i) >= 7:
                gang71.append(i[6])
            if len(i) >= 8:
                gang81.append(i[7])
            if len(i) >= 9:
                gang91.append(i[8])
            if len(i) >= 10:
                gang101.append(i[9])
            else:
                pass
        sotired_final_zbs['Скважина №'] = sotired_final_zbs.apply(
            lambda x:
            x['Скважина №'] + '_ГРП' if x['index'] in gang11
            else x['Скважина №'], axis=1)
        sotired_final_zbs['Скважина №'] = sotired_final_zbs.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_1' if x['index'] in gang21
            else x['Скважина №'], axis=1)
        sotired_final_zbs['Скважина №'] = sotired_final_zbs.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_2' if x['index'] in gang31
            else x['Скважина №'], axis=1)
        sotired_final_zbs['Скважина №'] = sotired_final_zbs.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_3' if x['index'] in gang41
            else x['Скважина №'], axis=1)
        sotired_final_zbs['Скважина №'] = sotired_final_zbs.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_4' if x['index'] in gang51
            else x['Скважина №'], axis=1)
        sotired_final_zbs['Скважина №'] = sotired_final_zbs.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_5' if x['index'] in gang61
            else x['Скважина №'], axis=1)
        sotired_final_zbs['Скважина №'] = sotired_final_zbs.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_6' if x['index'] in gang71
            else x['Скважина №'], axis=1)
        sotired_final_zbs['Скважина №'] = sotired_final_zbs.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_7' if x['index'] in gang81
            else x['Скважина №'], axis=1)
        sotired_final_zbs['Скважина №'] = sotired_final_zbs.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_8' if x['index'] in gang91
            else x['Скважина №'], axis=1)
        sotired_final_zbs['Скважина №'] = sotired_final_zbs.apply(
            lambda x:
            x['Скважина №'] + '_ФРАК_9' if x['index'] in gang101
            else x['Скважина №'], axis=1)
        sotired_final_zbs = sotired_final_zbs.drop(['index'], axis=1)
        sotired_final_zbs = sotired_final_zbs.drop(['месяц с грп'], axis=1)
        sotired_final_zbs = sotired_final_zbs.drop(['is_duplicate'], axis=1)
        sotired_final_zbs.reset_index(drop=True)
        sotired_final_zbs.reset_index(inplace=True)
        sotired_final_zbs = sotired_final_zbs.drop(['index'], axis=1)
        sotired_final_zbs['Число стадий ГРП'] = sotired_final_zbs.apply(
            lambda x:
            1 if x['Длина ГС, м'] == 0 and 'ГРП' in x['ГС/ННС']
            else x['Число стадий ГРП'], axis=1)
        we_here = pd.concat([sotired_final, sotired_final_zbs])
        we_here['Число стадий ГРП'] = we_here.apply(
            lambda x:
            1 if 'ФРАК' in str(x['Скважина №'])
            else x['Число стадий ГРП'], axis=1)
        we_here['Число стадий ГРП'] = we_here.apply(
            lambda x:
            0 if 'ГС' == str(x['ГС/ННС'])
            else x['Число стадий ГРП'], axis=1)
        we_here['Число стадий ГРП'] = we_here.apply(
            lambda x:
            0 if 'ННС' == str(x['ГС/ННС'])
            else x['Число стадий ГРП'], axis=1)
        we_here['Скважина №'] = we_here.apply(
            lambda x:
            str(x['Скважина №']).replace('_Л', 'Л') if '_Л' in str(x['Скважина №']) else str(x['Скважина №']),
            axis=1
        )









        #sotired_final1 = sotired4.reindex(
        #    columns=['Скважина №', 'Длина ГС, м', 'Число стадий ГРП', 'Полудлина трещины, м', 'Ширина трещины, мм',
        #             'Проницаемость проппанта, Д', 'Дата ВНР после ГС \ ГРП \ЗБГС', 'ГС/ННС', 'Тип ГТМ', 'Пласт'])
        #sotired_final.columns = ['Скважина №', 'Длина ГС, м', 'Число стадий ГРП', 'Полудлина трещины, м', 'Ширина трещины, мм',
        #            'Проницаемость проппанта, Д', 'Дата ВНР после ГС \ ГРП \ЗБГС', 'ГС/ННС', 'Тип ГТМ', 'Пласт']
        ui.lineEdit_4.setText('Успешно!')

    ui.pushButton_4.clicked.connect(process)

    def exp_file(self):
        global we_here

        we_here.to_excel('GRP_new.xlsx')

    ui.pushButton_5.clicked.connect(exp_file)


sys.exit(app.exec_())


