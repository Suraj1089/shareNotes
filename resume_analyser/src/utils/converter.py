
import io
import pypdf
from typing import List
import re
import pandas as pd


def convert(path):
    """Converts pdf to text"""
    text = ""
    reader = pypdf.PdfReader(path)
    noOfPages = len(reader.pages)
    for line in range(0,noOfPages):
        page = reader.pages[line]
        text += page.extract_text()
    return text



def remove_subject_names(text: str, subject_names: List[str]) -> str:
    """Removes subject names from text"""
    for name in subject_names:
        name = name.strip()
        text = text.replace(name,'')
    return text



def extractPrnNo(text: str) -> pd.DataFrame:
    # function to extract prn no from text
    pattern = re.findall(
        r'7\d{7}[a-zA-Z]*', text
    )
    prn_no = {'PRN-NO': []}
    for i in pattern:
        prn_no['PRN-NO'].append(i.split()[0])

    return pd.DataFrame(prn_no)



def extract_student_details(text: str) -> pd.DataFrame:
    """Extracts student details from text"""
    pattern = re.findall(
        r'[STB]\d{9}\s*\w*\s*\w*\s*\w*\s*\w*\w*\s*\w*\s*\w*\s*\w*\s*', text)
    students = {'seat_no': [], 'name': []}
    for i in pattern:
        # split the string
        data = i.split()
        students['seat_no'].append(data[0])
        students['name'].append(data[1]+' '+data[2]+' '+data[3])
        dataframe = pd.DataFrame(students)
    return dataframe



def extract_student_sgpa(text: str) -> pd.DataFrame:
    """Extracts student sgpa from text"""
    pattern = re.findall(r'SGPA1\W*\d*\W*\d*', text)
    # SGPA1: 8.3
    d = {'sgpa':[],'score':[]}
    for i in pattern:
        temp = i.split()
        d['sgpa'].append(temp[0])
        d['score'].append(temp[1])
    return pd.DataFrame(d)


def get_txt_file(path) -> str:
    """Returns text from txt file"""
    with open(path,'r') as f:
        text = f.read()
    return text

def cleanText(text: str) -> str:
    subjects = ['OBJECT ORIENTED PROG. LAB','DATA STRUCTURES & ALGO. LAB','LOGIC DESIGN COMP. ORG. LAB','LOGIC DESIGN & COMP. ORG.','DATA STRUCTURES & ALGO.','INFORMATION AND CYBER SECURITY', 'MACHINE LEARNING & APPS.','DESIGN AND ANALYSIS OF ALG.' 
                'SOFTWARE DESIGN AND MODELING', 'BUS. ANALYTICS & INTEL.', 'SW. TESTING & QA.',
                'COMPUTER LABORATORY-VII', 'COMPUTER LABORATORY-VII', 'COMPUTER LABORATORY-VIII', 
                'COMPUTER LABORATORY-VIII', 'PROJECT PHASE-I', 'CRITICAL THINKING',
                'DISTRIBUTED COMPUTING SYSTEM', 'UBIQUITOUS COMPUTING', 'INTERNET OF THINGS (IOT)', 
                'INTERNET OF THINGS (IOT)', 'SOCIAL MEDIA ANALYTICS', 'COMPUTER LABORATORY-IX', 'COMPUTER LABORATORY-IX', 
                'COMPUTER LABORATORY-X', 'PROJECT WORK', 'PROJECT WORK', 'IOT- APPLI. IN ENGG. FIELD','INFO. & STORAGE RETRIEVAL']
    
    for i in subjects:
        text = text.replace(i, '')

    # SE subject names and TE subject names
    # BE subjects
    text = text.replace('INFO. & STORAGE RETRIEVAL','')
    text = text.replace('SOFTWARE PROJECT MANAGEMENT','')
    text = text.replace('DEEP LEARNING','')
    text = text.replace('MOBILE COMPUTING','')
    text = text.replace('INTRODUCTION TO DEVOPS','')
    text = text.replace('LAB PRACTICE III','')
    text = text.replace('LAB PRACTICE IV','')
    text = text.replace('PROJECT STAGE-I','')
    text = text.replace('COPYRIGHTS AND PATENTS','')
    text = text.replace('PROJECT STAGE II','')
    text = text.replace('DISTRIBUTED SYSTEMS','')
    text = text.replace('GAME ENGINEERING','')
    text = text.replace('BLOCKCHAIN TECHNOLOGY','')
    text = text.replace('STARTUP & ENTREPRENEURSHIP','')
    text = text.replace('LAB PRACTICE VI','')
    text = text.replace('LAB PRACTICE V','')
    text = text.replace('CYBER LAWS & USE OF S.M','')
    text = text.replace('TOTAL GRADE POINTS / TOTAL CREDITS','')
    text = text.replace('FOURTH YEAR','')
    text = text.replace('SE SGPA','')
    text = text.replace('FE SGPA','')
    text = text.replace('TE SGPA','')
    text = text.replace('FIRST CLASS WITH DISTINCTION','')
    text = text.replace('CGPA','')

    
    
    text = text.replace('DESIGN AND ANALYSIS OF ALG.','')
    text = text.replace('COMPUTER ORGANIZATION & ARCH.','')
    text = text.replace('THEORY OF COMPUTATION', '')
    text = text.replace('OPERATING SYSTEMS', '')
    text = text.replace('MACHINE LEARNING', '')
    text = text.replace('HUMAN COMPUTER INTERACTION', '')
    text = text.replace('A DESIGN AND ANALYSIS OF ALG.', '')
    text = text.replace('SEMINAR', '')
    text = text.replace('HUMAN COMP. INTERACTION-LAB.', '')
    text = text.replace('LABORATORY PRACTICE-I', '')
    text = text.replace('OPERATING SYSTEMS LAB(TW+PR)', '')
    text = text.replace('(TW+PR)', '')
    text = text.replace('STARTUP ECOSYSTEMS', '')
    text = text.replace('SEMINAR', '')
    text = text.replace('SEMINAR', '')
    text = text.replace('DISCRETE MATHEMATICS', '')
    text = text.replace('LOGIC DESIGN & COMP. ORG.', '')
    text = text.replace('DATA STRUCTURES & ALGO.', '')
    text = text.replace('OBJECT ORIENTED PROGRAMMING', '')
    text = text.replace('BASIC OF COMPUTER NETWORK', '')
    text = text.replace('LOGIC DESIGN COMP. ORG. LAB', '')
    text = text.replace('DATA STRUCTURES & ALGO. LAB', '')
    text = text.replace('DATA STRUCTURES & ALGO. LAB', '')
    text = text.replace('OBJECT ORIENTED PROG. LAB', '')
    text = text.replace('SOFT SKILL LAB', '')
    text = text.replace('ETHICS AND VALUES IN IT', '')
    text = text.replace('LAB', '')
    text = text.replace(
        'SAVITRIBAI PHULE PUNE UNIVERSITY ,S.E.(2019 CREDIT PAT.) EXAMINATION, OCT/NOV 2021', '')
    text = text.replace(
        'COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE', '')
    text = text.replace(
        'BRANCH CODE:  29-S.E.(2019 PAT.)(INFORMATIOM TECHNOLOGY)', '')
    text = text.replace('DATE : 21 APR 2022 ', '')
    text = text.replace(
        'COURSE NAME                      ISE      ESE     TOTAL      TW       PR       OR    Tot% Crd  Grd   GP  CP  P&R ORD', '')
    text = text.replace(
        'SAVITRIBAI PHULE PUNE UNIVERSITY, S.E.(2015 COURSE) EXAMINATION,MAY 2018', '')
    text = text.replace(
        'SAVITRIBAI PHULE PUNE UNIVERSITY ,T.E.(2019 COURSE) EXAMINATION, OCT/NOV 2021', '')
    text = text.replace(
        'COLLEGE    : D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE', '')
    text = text.replace(
        'COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE', '')
    text = text.replace(
        'BRANCH CODE: 29-S.E.(2015 PAT.)(INFORMATIOM TECHNOLOGY)', '')
    text = text.replace(
        'BRANCH CODE: 60-T.E.(2019 PAT.)(INFORMATION TECHNOLOGY)', '')
    text = text.replace('DATE       : 23 JUL 2018', '')
    text = text.replace('DATE : 06 MAY 2022', '')
    text = text.replace(
        '............CONFIDENTIAL- FOR VERIFICATION AND RECORD ONLY AT COLLEGE, NOT FOR DISTRIBUTION.......................................', '')
    text = text.replace(
        '....................................................................................................', '')
    text = text.replace(
        '............                  .......  .......  .......  .......  .......  .......  ...  ...  ...   ... ...  ... ...', '')

    text = text.replace('PAGE :-', '')
    text = text.replace('SEAT NO.', '')
    text = text.replace('SEAT NO.:', '')
    text = text.replace('NAME :', '')
    text = text.replace('MOTHER :', '')
    text = text.replace('PRN :', '')
    text = text.replace('CLG.: DYPP[8]', '')

    text = text.replace('..............................', '')
    text = text.replace('SEM.:1', '')
    text = text.replace('SEM.:2', '')
    text = text.replace(
        'OE       TH     [OE+TH]     TW       PR       OR    Tot% Crd  Grd  Pts   Pts', '')
    text = text.replace(
        'OE       TH     [OE+TH]     TW       PR       OR    Tot% Crd  Grd  Pts   Pts', '')
    text = text.replace('DYPP', '')
    text = text.replace('Grd   Crd', '')
    text = text.replace('SEM. 2', '')
    text = text.replace('SEM. 1', '')
    text = text.replace('~', '')
    text = text.replace(' .', '')
    text.replace('~', 'nan')
    text = text.replace('*', ' ')
    text = text.replace(':', ' ')
    text = text.replace('-', 'n')
    text = text.replace('SECOND YEAR SGPA', '')
    text = text.replace('TOTAL CREDITS EARNED ', '')

    text = text.strip()
    return text
# function to display pdf
