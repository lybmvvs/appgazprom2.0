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
        # вставка 22.02.22
        grp_dad['Номер скважины'] = grp_dad.apply(
            lambda x:
            str(x['Номер скважины']), axis=1)
        grp_gtm['Скважина'] = grp_gtm.apply(
            lambda x:
            str(x['Скважина']), axis=1)

        # вставка 22.02.22
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
        grp_gtm = grp_gtm.drop(grp_gtm[grp_gtm['Объект разработки до ГТМ'] != plasttt].index).reset_index(drop=True)
        coordinates['Length'] = coordinates.apply(
            lambda x: ((x['Координата забоя Х (по траектории)'] - x['Координата X']) ** (2) +
                       (x['Координата забоя Y (по траектории)'] - x['Координата Y']) ** (2)) ** (0.5)
            , axis=1)
        coordinates['№ скважины'] = coordinates.apply(
            lambda x:
            str(x['№ скважины']), axis=1)
        grp = copy.deepcopy(grp_dad)
        grp_now_we_go = copy.deepcopy(grp_gtm)

        # координаты скважин для нашего объекта
        my_wells = grp['Номер скважины'].tolist()
        my_wells_no_repeat = []
        for x in my_wells:
            if x not in my_wells_no_repeat:
                my_wells_no_repeat.append(x)
        my_wells_gtm = grp_now_we_go['Скважина'].tolist()
        my_wells_no_repeat_gtm = []
        for x in my_wells_gtm:
            if x not in my_wells_no_repeat_gtm:
                my_wells_no_repeat_gtm.append(x)
        my_wells_only_frak = []
        for i in my_wells_no_repeat:
            if i not in my_wells_no_repeat_gtm:
                my_wells_only_frak.append(i)
        wells_GTM = pd.DataFrame({"Номер скважины": my_wells_no_repeat_gtm
                                  })
        coordinates_f = coordinates[
            coordinates['№ скважины'].isin(my_wells_no_repeat_gtm)].reset_index(drop=True)
        coordinates_f = coordinates_f.drop(['Координата X', 'Координата Y', 'Координата забоя Х (по траектории)',
                                            'Координата забоя Y (по траектории)'], axis=1)
        new = coordinates_f['№ скважины'].tolist()
        coordinates_f['Скважина'] = new
        coordinates_f = coordinates_f.drop(['№ скважины'], axis=1)
        grp_now_we_go['Скважина'] = grp_now_we_go.apply(
                    lambda x:
                    str(x['Скважина']), axis=1)
        coordinates_f['Скважина'] = coordinates_f.apply(
            lambda x:
            str(x['Скважина']), axis=1)
        final = grp_now_we_go.merge(coordinates_f, on='Скважина')
        final['Длина ГС, м'] = final.apply(
            lambda x:
            x['Length'] if x['Length'] >= 110
            else 0, axis=1)
        final = final.drop(['Length'], axis=1)
        final_number = final.groupby(by=['Скважина', 'ВНР.1', 'Тип', 'Объект разработки до ГТМ']).agg(
            {'Длина ГС, м': lambda x:
            x.tolist()[0]}
        )
        final_number.reset_index(inplace=True)

        final_number['Дата ВНР после'] = final_number.apply(
            lambda x:
            x['ВНР.1'] if 'ГРП' == str(x['Тип'])
            else x['ВНР.1'] if 'ВНС' in str(x['Тип'])

            else 'нет', axis=1)
        final_number = final_number.drop(final_number[final_number['Дата ВНР после'] == 'нет'].index)
        final_number.reset_index(inplace=True)
        final_number['Тип'] = final_number.apply(
            lambda x:
            'ВНС' if 'ВН' in str(x['Тип'])
            else x['Тип'], axis=1)
        final_number['index'] = final_number.index
        grp_vnski_double = final_number.drop(final_number[final_number['Тип'] != 'ВНС'].index)
        grp_vnski_double['index'] = grp_vnski_double.index
        grp_vnski_double = grp_vnski_double.groupby('Скважина').agg(
            {'index': lambda x:
            x.tolist()[1:]}
        )
        sveta = []
        for i in grp_vnski_double['index']:
            sveta += i
        final_number = final_number[~final_number['index'].isin(sveta)].reset_index(drop=True)
        final_number = final_number.drop(['index'], axis=1)
        final_number = final_number.drop(['ВНР.1'], axis=1)
        final_number['Полудлина трещины, м'] = final_number.apply(
            lambda x:
            100, axis=1)
        final_number['Ширина трещины, мм'] = final_number.apply(
            lambda x:
            4, axis=1)
        final_number['Проницаемость проппанта, Д'] = final_number.apply(
            lambda x:
            100, axis=1)
        final_number['Полудлина трещины, м'] = final_number.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип'])
            else x['Полудлина трещины, м']
            , axis=1)
        final_number['Ширина трещины, мм'] = final_number.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип'])
            else x['Ширина трещины, мм']
            , axis=1)
        final_number['Проницаемость проппанта, Д'] = final_number.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип'])
            else x['Проницаемость проппанта, Д']
            , axis=1)
        # ДОБАВИТЬ В ВНС
        final_number['Число стадий ГРП'] = final_number.apply(
            lambda x:
            1, axis=1)
        final_number['Число стадий ГРП'] = final_number.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип'])
            else x['Число стадий ГРП']
            , axis=1)
        final_number['ГС/ННС'] = final_number.apply(
            lambda x:
            'ННС' if x['Длина ГС, м'] == 0
            else 'ГС', axis=1)
        final_number['index'] = final_number.index
        final_number['index'] = final_number.apply(
            lambda x:
            str(x['index'])
            + ('_да' if x['Тип'] == 'ГРП' else ''),
            axis=1
        )
        final_double = final_number.groupby(by=['Скважина', 'Дата ВНР после']).agg(
            {'index': lambda x:
            x.tolist()}
        )
        final_double.reset_index(inplace=True)
        final_double['длина'] = final_double.apply(
            lambda x:
            len(x['index']), axis=1)
        final_double = final_double.drop(final_double[final_double['длина'] == 1].index)
        welles = []
        for i in final_double['index']:
            welles += i
        welles_corr = []
        for i in welles:
            if 'да' in i:
                welles_corr.append(i)
        welles_incorr = []
        for i in welles:
            if 'да' not in i:
                welles_incorr.append(i)
        final_number = final_number[~final_number['index'].isin(welles_corr)].reset_index(drop=True)
        final_number['ГС/ННС'] = final_number.apply(
            lambda x:
            str(x['ГС/ННС'])
            + ('+ГРП' if x['index'] in welles_incorr else ''),
            axis=1
        )
        final_number['Полудлина трещины, м'] = final_number.apply(
            lambda x:
            100 if 'ГРП' in str(x['ГС/ННС'])
            else x['Полудлина трещины, м']
            , axis=1)
        final_number['Ширина трещины, мм'] = final_number.apply(
            lambda x:
            4 if 'ГРП' in str(x['ГС/ННС'])
            else x['Ширина трещины, мм']
            , axis=1)
        final_number['Проницаемость проппанта, Д'] = final_number.apply(
            lambda x:
            100 if 'ГРП' in str(x['ГС/ННС'])
            else x['Проницаемость проппанта, Д']
            , axis=1)
        final_number['Число стадий ГРП'] = final_number.apply(
            lambda x:
            1 if 'ГРП' in str(x['ГС/ННС'])
            else x['Число стадий ГРП']
            , axis=1)
        final_number['Тип'] = final_number.apply(
            lambda x:
            'ГРП' if 'ГРП' in str(x['ГС/ННС'])
            else x['Тип']
            , axis=1)
        new_400 = final_number['Скважина'].tolist()
        final_number['Скважина №'] = new_400
        final_number = final_number.drop(['Скважина'], axis=1)
        final_number = final_number.drop(['index'], axis=1)
        new_300 = final_number['Тип'].tolist()
        final_number['Тип ГТМ'] = new_300
        final_number = final_number.drop(['Тип'], axis=1)
        new_200 = final_number['Объект разработки до ГТМ'].tolist()
        final_number['Пласт'] = new_200
        final_number = final_number.drop(['Объект разработки до ГТМ'], axis=1)
        final_number = final_number.reindex(
            columns=['Скважина №', 'Длина ГС, м', 'Число стадий ГРП', 'Полудлина трещины, м', 'Ширина трещины, мм',
                     'Проницаемость проппанта, Д', 'Дата ВНР после', 'ГС/ННС', 'Тип ГТМ', 'Пласт'])
        final_number['Дата ВНР после'] = final_number.apply(
            lambda x:
            str(x['Дата ВНР после']), axis=1)
        final_number['месяц с грп'] = final_number.apply(
            lambda x:
            x['Дата ВНР после'][:4],
            axis=1
        )
        grp = copy.deepcopy(grp_dad)
        grp['Дата'] = grp.apply(
            lambda x:
            str(x['Дата']), axis=1)
        grp['месяц с грп'] = grp.apply(
            lambda x:
            x['Дата'][:4],
            axis=1
        )
        grp = grp.groupby(by=['Номер скважины', 'месяц с грп']).agg(
            {'Пласт': lambda x:
            x.tolist()}
        )
        grp['Количество'] = grp.apply(
            lambda x:
            len(x['Пласт'])
            , axis=1)
        grp.reset_index(inplace=True)
        new_100 = grp['Номер скважины'].tolist()
        grp['Скважина №'] = new_100
        grp = grp.drop(['Номер скважины'], axis=1)
        grp = grp.drop(['Пласт'], axis=1)
        sotired = final_number.merge(grp, on=['месяц с грп', 'Скважина №'], how='left')
        sotired = sotired.drop(['Число стадий ГРП'], axis=1)
        new_50 = sotired['Количество'].tolist()
        sotired['Число стадий ГРП'] = new_50
        sotired = sotired.drop(['Количество'], axis=1)
        sotired['Число стадий ГРП'] = sotired.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип ГТМ'])
            else x['Число стадий ГРП']
            , axis=1)
        sotired['Дата ВНР после'] = pd.to_datetime(sotired['Дата ВНР после'])
        sotired['ГС/ННС'] = sotired.apply(
            lambda x:
            str(x['ГС/ННС']) + '+ГРП' if str(x['Тип ГТМ']) == 'ГРП' and 'ГРП' not in str(x['ГС/ННС'])
            else x['ГС/ННС'], axis=1)
        sotired = sotired.reindex(
            columns=['Скважина №', 'Длина ГС, м', 'Число стадий ГРП', 'Полудлина трещины, м', 'Ширина трещины, мм',
                     'Проницаемость проппанта, Д', 'Дата ВНР после', 'ГС/ННС', 'Тип ГТМ', 'Пласт'])
        sotired['Число стадий ГРП'] = sotired.apply(
            lambda x:
            0 if str(x['Тип ГТМ']) == 'ВНС'
            else x['Число стадий ГРП'], axis=1)
        sotired['Полудлина трещины, м'] = sotired.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип ГТМ'])
            else x['Полудлина трещины, м']
            , axis=1)
        sotired['Ширина трещины, мм'] = sotired.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип ГТМ'])
            else x['Ширина трещины, мм']
            , axis=1)
        sotired['Проницаемость проппанта, Д'] = sotired.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип ГТМ'])
            else x['Проницаемость проппанта, Д']
            , axis=1)
        # ДОБАВИТЬ В ВНС
        sotired['Число стадий ГРП'] = sotired.apply(
            lambda x:
            0 if 'ВНС' in str(x['Тип ГТМ'])
            else x['Число стадий ГРП']
            , axis=1)
        # удаляем если в одном месяце
        sotired['index'] = sotired.index
        dele = copy.deepcopy(sotired)
        dele['чек'] = dele.apply(
            lambda x:
            x['Скважина №'].partition('_')[0] if '_' in str(x['Скважина №'])
            else x['Скважина №'], axis=1)
        dele['месяц'] = dele.apply(
            lambda x:
            str(x['Дата ВНР после'])[:7],
            axis=1
        )
        dele = dele.groupby(by=['чек', 'месяц']).agg(
            {'index': lambda x:
            x.tolist()}
        )
        dele['скока_их'] = dele.apply(
            lambda x: len(x['index'])
            , axis=1)
        dele = dele.drop(dele[dele['скока_их'] < 2].index).reset_index(drop=True)
        to_stay = []
        all_wells = []
        for i in dele['index']:
            all_wells += i
        for i in dele['index']:
            to_stay.append(i[-1])
        alli = copy.deepcopy(sotired)
        alli = alli[alli['index'].isin(all_wells)].reset_index(drop=True)
        alli = alli.drop(alli[alli['Тип ГТМ'] == 'ВНС'].index).reset_index(drop=True)
        alli = alli.groupby('Скважина №').agg(
            {'index': lambda x:
            x.tolist()[0]}
        )
        definetely_stay = alli['index'].tolist()
        array_3 = list(all_wells)
        for x in definetely_stay:
            try:
                array_3.remove(x)
            except ValueError:
                pass
                # вот досюда
        sotired = sotired[~sotired['index'].isin(array_3)].reset_index(drop=True)
        sotired = sotired.drop(['index'], axis=1)
        # проверяем ЗБС
        grp_4 = copy.deepcopy(grp_gtm)

        grp_4['Скважина'] = grp_4.apply(
            lambda x:
            str(x['Скважина']), axis=1)
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
        sotired_final_zbs = sotired.merge(grp_zbs, on='Скважина №')
        abba = sotired_final_zbs['Скважина №'].tolist()

        arura = []
        #14.04
        #sotired_final = pd.DataFrame()
        #14.04
        for i in abba:
            if i not in arura:
                arura.append(i)
        if sotired_final_zbs.shape[0] != 0:
                # sotired_final_zbs['Число стадий ГРП'] = sotired_final_zbs.apply(
                #    lambda x:
                #    1 if x['Дата ВНР после'] < x['Начало.1'] else x['Число стадий ГРП'],
                #    axis=1
                # )
                # sotired_final_zbs['Скважина №'] = sotired_final_zbs.apply(
                #    lambda x:
                #    str(x['Скважина №'])
                #    + ('_Л' if x['Дата ВНР после'] < x['Начало.1'] else ''),
                #    axis=1
                # )
            # 21.03.22
            sotired_final_zbs['Длина ГС, м'] = sotired_final_zbs.apply(
                    lambda x:
                    0 if x['Дата ВНР после'] < x['Начало.1'] else x['Длина ГС, м'],
                    axis=1
                )
            sotired_final_zbs['Число стадий ГРП'] = sotired_final_zbs.apply(
                    lambda x:
                    1 if x['Дата ВНР после'] < x['Начало.1'] else x['Число стадий ГРП'],
                    axis=1
                )
            sotired_final_zbs['Скважина №'] = sotired_final_zbs.apply(
                    lambda x:
                    str(x['Скважина №'])
                    + ('_Л' if x['Длина ГС, м'] == 0 else ''),
                    axis=1
                )
            # 21.03.22

            sotired_final_zbs = sotired_final_zbs.drop(['Начало.1'], axis=1)
        #14.04 got him
        sotired_final = sotired[~sotired['Скважина №'].isin(arura)].reset_index(drop=True)
        #14.04 got him
        sotired_final1 = pd.concat([sotired_final, sotired_final_zbs])
        sotired_final1.reset_index(drop=True)
        sotired_final1.reset_index(inplace=True)
        # приставка ФРАК там где надо
        sotired_final.reset_index(drop=True)
        sotired_final.reset_index(inplace=True)
        sotired_final['index'] = sotired_final.index
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
        sotired_final.reset_index(drop=True)
        sotired_final.reset_index(inplace=True)
        sotired_final = sotired_final.drop(['index'], axis=1)
        sotired_final['Число стадий ГРП'] = sotired_final.apply(
            lambda x:
            1 if x['Длина ГС, м'] == 0 and 'ГРП' in x['ГС/ННС']
            else x['Число стадий ГРП'], axis=1)
        if sotired_final_zbs.shape[0] != 0:
            sotired_final_zbs['index'] = sotired_final_zbs.index
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
        # 21.03.22
        we_here['ГС/ННС'] = we_here.apply(
            lambda x:
            str(x['ГС/ННС']).replace('ГС', 'ННС')
            if 0 == x['Длина ГС, м']
            else x['ГС/ННС'], axis=1)
        we_here['Число стадий ГРП'] = we_here.apply(
            lambda x:
            2 if 'ГС' in x['ГС/ННС'] and 'ГРП' in x['ГС/ННС'] and x['Число стадий ГРП'] == 1
            else x['Число стадий ГРП'], axis=1)

        # 21.03.22








        #sotired_final1 = sotired4.reindex(
        #    columns=['Скважина №', 'Длина ГС, м', 'Число стадий ГРП', 'Полудлина трещины, м', 'Ширина трещины, мм',
        #             'Проницаемость проппанта, Д', 'Дата ВНР после ГС \ ГРП \ЗБГС', 'ГС/ННС', 'Тип ГТМ', 'Пласт'])
        #sotired_final.columns = ['Скважина №', 'Длина ГС, м', 'Число стадий ГРП', 'Полудлина трещины, м', 'Ширина трещины, мм',
        #            'Проницаемость проппанта, Д', 'Дата ВНР после ГС \ ГРП \ЗБГС', 'ГС/ННС', 'Тип ГТМ', 'Пласт']
        ui.lineEdit_4.setText('Успешно!')

    ui.pushButton_4.clicked.connect(process)

    def exp_file(self):
        global we_here
        we_here.reset_index(drop=True)
        we_here.reset_index(inplace=True)
        #we_here = we_here.drop(['level_0'], axis=1)
        we_here = we_here.drop(['index'], axis=1)
        we_here.to_excel('GRP_new.xlsx')

    ui.pushButton_5.clicked.connect(exp_file)


sys.exit(app.exec_())


