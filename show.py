from msvcrt import getch

import requests
from bs4 import BeautifulSoup as soup


def load(roll):
    data = data_main
    data['txtRegNo'] = (male_roll if male else female_roll) + roll

    res = soup(requests.post(site, data=data).content, features='html.parser')
    for key in asp_dat:
        data[key] = res.find(id=key).get('value')
    data['ddlExam'] = exam_code

    res = soup(requests.post(site, data=data).content, features='html.parser')

    details = (res.find(id='LbStudentName').contents[0], str(roll), res.find(id='lbloddSgpa').contents[0])
    print(f'{details[1].rjust(2)} │ {details[0].center(25)} │ {details[2]}')
    score_dat.append(details)


if __name__ == '__main__':
    first_roll_no = 430419020001
    last_roll_no = 430419010065
    exam_code = 'C19A01'
    site = 'http://jisexams.in/JISEXAMS/studentServices/frmViewStudentGradeCardResult.aspx'

    if male := str(first_roll_no)[7] == '1':
        male_roll = first_roll_no - 1
        female_roll = male_roll + 10000
    else:
        female_roll = first_roll_no - 1
        male_roll = female_roll - 10000

    score_dat = list()

    login_page = soup(requests.get(site).content, features='html.parser')
    data_main = {'btnView.x': '0', 'btnView.y': '0'}
    asp_dat = ('__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION')
    for key in asp_dat:
        data_main[key] = login_page.find(id=key).get('value')

    for i in range(1, int(str(last_roll_no)[-3:])):
        try:
            load(i)
        except:
            try:
                male = not male
                load(i)
            except:
                pass

    score_dat = sorted(score_dat, key=lambda x: float(x[2]), reverse=True)

    for rank, details in enumerate(score_dat):
        print(f'{str(rank + 1).rjust(3)} │ {details[0].center(25)} │ {details[1].rjust(2)} │ {details[2]}')
    getch()
