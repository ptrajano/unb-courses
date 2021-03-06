# -*- coding: utf-8 -*-
"""
Created on Thu May 12 19:02:54 2022

@author: Pedro T. Ferreira
"""

import requests
from bs4 import BeautifulSoup
import os



URL_ORIGINAL = "https://sigraweb.unb.br/matriculaweb/graduacao/curso_rel.aspx?cod=1"
URL_MAJOR = "https://sigraweb.unb.br/matriculaweb/graduacao/"
URL_CURRICULUM = "https://sigraweb.unb.br/matriculaweb/graduacao/curriculo.aspx?cod="
URL_COURSE = "https://sigraweb.unb.br"

def recursive_all_sibling(class_type, saving_vector):
    saving_vector.append(class_type.get_text() + '\n')
    try:
        recursive_all_sibling(class_type.next_sibling, saving_vector)
    except AttributeError:
        return



def scraping_site_majors():
    
    page = requests.get(URL_ORIGINAL)
    link_majors = []
    sub_major = []
    if page.status_code == 404:
            print("PAGE NOT FOUND")
            return
    src = page.content
    soup = BeautifulSoup(src, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.find('curso_dados') != -1:
            link_majors.append(href)
    for x in link_majors:
        url = URL_MAJOR + x
        page = requests.get(url)
        
        if page.status_code == 404:
                print("PAGE NOT FOUND")
                return
        
        src = page.content
        soup = BeautifulSoup(src, 'html.parser')
        try: 
            for x in soup.findAll("td"):
                try:
                    if int(x["colspan"]) == 3:
                        sub_major.append(x.get_text())
                except(ValueError, KeyError):
                    pass
                for i in range(len(sub_major)):
                    sub_major[i] = sub_major[i] 
                    sub_major[i] = sub_major[i].replace('\t', '').replace('\n', '').replace('\r', '')
                    sub_major[i] = sub_major[i] + '\n'
                    print(sub_major[i])
        except AttributeError: 
            print("TABLE NOT FOUND, ERROR IN WEBSITE")
    with open('major_list.txt', 'w') as file_major_list:
        file_major_list.writelines(sub_major)



def scraping_site_curriculum(x):
    
    link_courses = []
    course_content = []
    
    code, major_name = x.split(' - ', 1)
    
    father_directory = os.getcwd()
    directory_name = (code + '_' + major_name).replace(' ', '') 
    
    try:
        os.mkdir(directory_name)
    except FileExistsError:
        pass
    
    try:
        os.chdir(directory_name)
        
        url = URL_CURRICULUM + code
        page = requests.get(url)
        
        if page.status_code == 404:
                print("PAGE NOT FOUND")
                return
            
        src = page.content
        soup = BeautifulSoup(src, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.find('/matriculaweb/graduacao/disciplina.aspx?cod=') != -1:
                link_courses.append(href)
        for link in link_courses:    
            url = URL_COURSE + link
            page = requests.get(url)
            
            if page.status_code == 404:
                print("PAGE NOT FOUND")
                return
            
            src = page.content
            soup = BeautifulSoup(src, 'html.parser')
            body = soup.find('body')
            div = body.find('div')
            try:
                tr = div.find('tr')
                recursive_all_sibling(tr, course_content)
                file_name = (course_content[1].split(': ', 1)[1] + '_' + course_content[2].split(': ', 1)[1].replace(' ', '') + '.txt').replace('\n', '').replace('/', '')
                print(file_name)
                with open(file_name, 'w') as file_course:
                    file_course.writelines(course_content)
            except AttributeError:
                print("COURSE NOT FOUND, ERROR IN WEBSITE")
            course_content = []
        os.chdir(father_directory)
        return 0
    except KeyboardInterrupt:
        os.chdir(father_directory)
        return 1



def scraping_site_majors_curriculum():
    with open('major_list.txt', 'r') as file:
        major_names = file.readlines()
        
    for i in range(len(major_names)):
        major_names[i] = major_names[i].replace('\n', '')
        
    father_directory = os.getcwd()
    directory_name = 'majors_curriculum'
    
    try:
        os.mkdir(directory_name)
    except FileExistsError:
        pass
    
    try:
        os.chdir(directory_name)
        for major in major_names:
            print(major)
            if scraping_site_curriculum(major):
                os.chdir(father_directory)
                return
        os.chdir(father_directory)
        print()
        print()
    except KeyboardInterrupt:
        os.chdir(father_directory)
        

"""
def scraping_site():
    x = 'curso_dados.aspx?cod=175'
    url = "https://sigraweb.unb.br/matriculaweb/graduacao/" + x
    page = requests.get(url)
    sub_major = []
    if page.status_code == 404:
            print("PAGE NOT FOUND")
            return
    
    src = page.content
    soup = BeautifulSoup(src, 'html.parser')
    body = soup.find('body')
    h4 = body.find('h4')
    h4 = h4.get_text()
    trash ,h4 = h4.split('Curso:')
    for x in soup.findAll("td"):
        try:
            if int(x["colspan"]) == 3:
                sub_major.append(x.get_text())
        except(ValueError, KeyError) as e:
            c = 0
    trash, h4 = h4.split(' - ')    
    for i in range(len(sub_major)):
        sub_major[i] = sub_major[i] + (' ' + h4)*(len(sub_major) != 1)
        sub_major[i] = sub_major[i].replace('\t', '').replace('\n', '').replace('\r', '')
    print(sub_major)
    
"""
#scraping_site_majors()
scraping_site_majors_curriculum()
#scraping_site_curriculum("8150 - ADMINISTRA????O")