import spacy
from spacy.matcher import Matcher
import re
from nltk.corpus import stopwords


import en_core_web_sm

nlp = en_core_web_sm.load()
# load pre-trained model
# nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

def extract_name(resume_text):
    '''
    function to extract name from resume text
    Args:
        resume_text: Plain resume text
    Returns:
        Name of the candidate if name is found else None
    '''
    nlp_text = nlp(resume_text)
    
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
    matcher.add('NAME', [pattern], on_match = None)
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text
    

def get_phone_number(string):
    r = re.compile(r'(\+\d{1,3}[-\.\s]??)?(\d{1,4}[-\.\s]??)?(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    
    cleaned_numbers = []
    for groups in phone_numbers:
        full_number = ''.join(groups)
        cleaned_number = re.sub(r'\D', '', full_number)
        cleaned_numbers.append(cleaned_number)
    
    return cleaned_numbers



# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))

# Education Degrees
EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]

def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education

def extract_experience(text):
    '''
    function to extract experience from resume text
    Args:
        resume_text: Plain resume text
    Returns:
        Experience of the candidate if experience is found else None
    '''
    # nlp_text = nlp(text)
    # Sentence
    sub_patterns = ['[A-Z][a-z]* [A-Z][a-z]* Private Limited','[A-Z][a-z]* [A-Z][a-z]* Pvt. Ltd.','[A-Z][a-z]* [A-Z][a-z]* Inc.', '[A-Z][a-z]* LLC',
                    ]
    pattern = '({})'.format('|'.join(sub_patterns))
    experience = re.findall(pattern, text)
    return experience

def extract_email(text):
    '''
    function to extract email from resume text
    Args:
        resume_text: Plain resume text
    Returns:
        Email of the candidate if email is found else None
    '''
    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    return email