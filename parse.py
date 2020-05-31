## parser.py

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Myproject.settings")
import django
django.setup()

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from django.utils import timezone

import time

from s_parser.models import AllLanguages
from s_parser.models import BlogData


class ClassLink:
    class_name = ""
    link = ""

    def __init__(self, class_name, link):
        self.class_name = class_name
        self.link = link

class ClassInfo:
    language_name = ""
    class_name = ""
    method_name = ""
    param_name = ""
    link = ""
    score = ""
    pub_date = ""
    etc = ""

    def toString(self):
        print("LAN:", self.language_name, "CLASS:", self.class_name, "METHOD:", self.method_name, "PARAM:", self.param_name, "LINK:", self.link)

    def __init__(self, language_name, class_name, method_name, param_name, link, score, pub_date, etc):
        self.language_name = language_name
        self.class_name = class_name
        self.method_name = method_name
        self.param_name = param_name
        self.link = link
        self.score = score
        self.pub_date = pub_date
        self.etc = etc

# javascript parser
def js_parse():
    driver = wd.Chrome(executable_path='/usr/local/bin/chromedriver')
    driver.implicitly_wait(3)

    driver.get('https://devdocs.io/javascript/')
    driver.implicitly_wait(5)

    data = []

    classlist = driver.find_elements_by_css_selector('._list-sub ._list-item svg')
    linkidx = len(classlist)

    # find class name 
    classes = driver.find_elements_by_css_selector('._list-sub > ._list-item > ._list-text')

    startidx = 1

    for x in range(linkidx):

        # open class list bar
        classlist[x].click()
        classname = classes[x].text

        # find method name
        methodlist = driver.find_elements_by_tag_name('section div div div a')
        methodidx = len(methodlist)

        for y in range(startidx, methodidx):
            param_ok = False

            method = methodlist[y].text
            idx = method.find('.')
            if(idx != -1):
                methodname = method[idx+1:]
            else:
                continue

            # find parameters
            try:
                methodlist[y].click()
                driver.implicitly_wait(5)
                try:
                    param_ok = driver.find_element_by_id('Parameters')

                    if(param_ok):
                        params = driver.find_elements_by_css_selector('main div dl > dt > code')
                        for param in params:
                            param = param.text
                    else:
                        param = ""

                    data.append(ClassInfo(
                        language_name='javascript',
                        class_name=classname,
                        link="",
                        method_name=methodname,
                        param_name=param,
                        score=-1,
                        pub_date=timezone.now(),
                        etc=-1
                    ))

                except exceptions.NoSuchElementException:
                    continue

            except exceptions.ElementClickInterceptedException:
                continue

        startidx = methodidx+1

    driver.close()
    driver.quit()

    return data

# selenium ver.
def parse_info_php():
    base_url = "https://www.php.net/manual/en/reserved.interfaces.php"
    #Must input your chromedriver path below!!
    driver = wd.Chrome(executable_path='/usr/local/bin/chromedriver')

    ### access site [GET]
    driver.get(base_url)
    ### implicit waits
    driver.implicitly_wait(5)

    ### scrap class name and link to detail page
    link_list = driver.find_element_by_id('reserved.interfaces').find_elements_by_css_selector('li')
    link_data = [];
    for link_item in link_list:
        link_data.append(ClassLink(class_name=link_item.text,
                                   link=link_item.find_element_by_css_selector('a').get_attribute('href')))

    class_data = []
    for class_item in link_data:

        ### access detail class page
        driver.get(class_item.link)
        ### implicit waits
        driver.implicitly_wait(5)

        if 'class' in driver.find_element_by_class_name('title').text:
            method_list = driver.find_elements_by_class_name('methodsynopsis')
            for method_item in method_list:
                class_data.append(ClassInfo(
                    language_name='php',
                    class_name=class_item.class_name,
                    link=class_item.link,
                    method_name=method_item.find_element_by_class_name('methodname').text,
                    param_name= '' if method_item.find_element_by_class_name('methodparam').text == 'void' else method_item.find_element_by_class_name('methodparam').text,
                    # TODO: edit score?, pub_date, etc
                    score=-1,
                    pub_date=timezone.now(),
                    etc=""
                ))

        driver.back()
        ### implicit waits
        driver.implicitly_wait(5)

    return class_data

def parse_info_java():
    base_url = 'https://docs.oracle.com/javase/10/docs/api/allclasses-noframe.html'
    #Must input your chromedriver path below!!
    driver = wd.Chrome(executable_path='/usr/local/bin/chromedriver')

    ### access site [GET]
    driver.get(base_url)
    ### waits
    time.sleep(10)

    


    driver.switch_to.frame(driver.find_element_by_class_name("truste_box_overlay_inner").find_element_by_tag_name('iframe'))
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/div[8]/div[1]/div/div[2]/div[2]/a[1]").click()
    driver.switch_to.default_content()
    time.sleep(5)

    ### scrap class name and link to detail page
    link_list = driver.find_elements_by_css_selector('li')
    link_data = [] # ; i = 0;
    for link_item in link_list:
        link_data.append(ClassLink(class_name=link_item.text,
                                   link=link_item.find_element_by_css_selector('a').get_attribute('href')))
        # i += 1
        # TODO: remove flag
        # if i >= 10: break

    class_data = []; i = 0;
    for class_item in link_data:
        ### access detail class page
        driver.get(class_item.link)
        ### implicit waits
        driver.implicitly_wait(5)

        if driver.find_element_by_id('method.summary').find_element_by_xpath("..").find_elements_by_tag_name('table'):
            method_data = driver.find_element_by_id('method.summary').find_element_by_xpath("..").find_element_by_tag_name('table')

            method_list = method_data.find_elements_by_class_name('colSecond')
            for j in range(1, len(method_list)):
                ### insert class data into ClassInfo Object List
                class_data.append(ClassInfo(
                    language_name='java',
                    class_name=class_item.class_name,
                    link=class_item.link,
                    ### pre-process method info
                    method_name=method_list[j].text[0:method_list[j].text.find('(')],
                    param_name=method_list[j].text[method_list[j].text.find('(') + 1:-1],
                    # TODO: edit score?, pub_date, etc
                    score=-1,
                    pub_date=timezone.now(),
                    etc=""
                ))
        i += 1
        driver.back()
        ### implicit waits
        driver.implicitly_wait(5)

    driver.close()
    driver.quit()

    return class_data

def parse_info_sql():
    base_url = 'https://docs.oracle.com/database/121/JAJDB/oracle/sql/package-summary.html'
    # Must input your chromedriver path below!!
    driver = wd.Chrome(executable_path='/usr/local/bin/chromedriver')

    ### access site [GET]
    driver.get(base_url)
    ### waits
    time.sleep(10)

    driver.switch_to.frame(
        driver.find_element_by_class_name("truste_box_overlay_inner").find_element_by_tag_name('iframe'))
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/div[8]/div[1]/div/div[2]/div[2]/a[1]").click()
    driver.switch_to.default_content()
    time.sleep(5)

    tables = driver.find_elements_by_class_name("oac_no_warn")
    link_table = tables[2:4]
    link_list = []
    for tmp_table in link_table:
        tmp_data = tmp_table.find_elements_by_tag_name('tr')
        link_list += tmp_data[1:]

    link_data = []
    for link_item in link_list:
        link_data.append(ClassLink(class_name=link_item.find_element_by_tag_name('b').text,
                                   link=link_item.find_element_by_tag_name('a').get_attribute('href')))

    class_data = []
    for class_item in link_data:
        driver.get(class_item.link)
        driver.implicitly_wait(5)

        tmp_b = driver.find_elements_by_tag_name('b')
        for b in tmp_b:
            if "Method Summary" in b.text:
                method_list = b.find_element_by_xpath("../../../..").find_elements_by_tag_name('tr')[1:]
                break
            else:
                method_list = []

        if method_list.__len__() == 0:
            driver.back()
            continue

        for method_item in method_list:
            sssibal = method_item.find_elements_by_css_selector('td > code')
            for s in sssibal:
                if "(" in s.text:
                    # print(s.text[0:s.text.find('(')], " / ", s.text[s.text.find('(') + 1:-1])
                    class_data.append(ClassInfo(
                        language_name='sql',
                        class_name=class_item.class_name,
                        link=class_item.link,
                        ### pre-process method info
                        method_name=s.text[0:s.text.find('(')],
                        param_name=s.text[s.text.find('(') + 1:-1],
                        # TODO: edit score?, pub_date, etc
                        score=-1,
                        pub_date=timezone.now(),
                        etc=""
                    ))

            # driver.back()
            # ### implicit waits
            # driver.implicitly_wait(5)

    driver.close()
    driver.quit()
    return class_data

def parse_info_servlet():
    base_url = "https://tomcat.apache.org/tomcat-5.5-doc/servletapi/"
    driver = wd.Chrome(executable_path='/usr/local/bin/chromedriver')

    ### access site [GET]
    driver.get(base_url)
    ### implicit waits
    driver.implicitly_wait(5)

    driver.get(driver.find_element_by_name("packageFrame").get_attribute('src'))
    link_list = driver.find_element_by_class_name("FrameItemFont").find_elements_by_tag_name('a')
    link_data = []
    for link_item in link_list:
        link_data.append(ClassLink(class_name=link_item.text,
                                   link=link_item.get_attribute('href')))

    class_data = []
    for class_item in link_data:
        ### access detail class page
        driver.get(class_item.link)
        ### implicit waits
        driver.implicitly_wait(5)

        tmp_b = driver.find_elements_by_tag_name('b')
        for b in tmp_b:
            if "Method Summary" in b.text:
                method_list = b.find_element_by_xpath("../../../..").find_elements_by_tag_name('tr')[1:]
                break
            else:
                method_list = []

        if method_list.__len__() == 0:
            driver.back()
            continue

        for method_item in method_list:
            sssibal = method_item.find_elements_by_css_selector('td > code')
            for s in sssibal:
                if "(" in s.text:
                    # print(s.text[0:s.text.find('(')], " / ", s.text[s.text.find('(') + 1:-1])
                    class_data.append(ClassInfo(
                        language_name='servlet',
                        class_name=class_item.class_name,
                        link=class_item.link,
                        ### pre-process method info
                        method_name=s.text[0:s.text.find('(')],
                        param_name=s.text[s.text.find('(') + 1:-1],
                        # TODO: edit score?, pub_date, etc
                        score=-1,
                        pub_date=timezone.now(),
                        etc=""
                    ))

    driver.close()
    driver.quit()

    return class_data

# 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    
    all_languages_list = parse_info_java()
    #all_languages_list.extend(parse_info_php())
    #all_languages_list=parse_info_php()
    #all_languages_list.extend(parse_info_servlet())
    #all_languages_list.extend(parse_info_sql())
    for item in all_languages_list:
        # item.toString()
        AllLanguages(
            languageName=item.language_name,
            className=item.class_name,
            methodName=item.method_name,
            parameterName=item.param_name,
            link=item.link,
            score=item.score,
            pub_date=item.pub_date,
            etc=item.etc
        ).save()

    all_languages_list = js_parse()
    for item in all_languages_list:
        item.toString()
        AllLanguages(
            languageName=item.language_name,
            className=item.class_name,
            methodName=item.method_name,
            parameterName=item.param_name,
            link=item.link,
            score=item.score,
            pub_date=item.pub_date,
            etc=item.etc
        ).save()