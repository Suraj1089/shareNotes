import spacy
import re
import spacy


def get_phone_number(string):
    r = re.compile(r'(\+\d{1,3}[-\.\s]??)?(\d{1,4}[-\.\s]??)?(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    
    cleaned_numbers = []
    for groups in phone_numbers:
        full_number = ''.join(groups)
        cleaned_number = re.sub(r'\D', '', full_number)
        cleaned_numbers.append(cleaned_number)
    
    return cleaned_numbers

def get_email(text):
    '''
    function to extract email from resume text
    Args:
        resume_text: Plain resume text
    Returns:
        Email of the candidate if email is found else None
    '''
    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    return email

def get_user_name(text):
    '''
    function to extract name from resume text
    Args:
        resume_text: Plain resume text
    Returns:
        Name of the candidate if name is found else None
    '''
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    for ent in doc.ents:
        if(ent.label_ == 'PERSON'):
            return ent.text
    return None

def get_skills(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    skills = []
    for ent in doc.ents:
        if(ent.label_ == 'PERSON'):
            skills.append(ent.text)
    return skills

def get_education(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    education = []
    for ent in doc.ents:
        if(ent.label_ == 'PERSON'):
            education.append(ent.text)
    return education

def get_experience(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    experience = []
    for ent in doc.ents:
        if(ent.label_ == 'PERSON'):
            experience.append(ent.text)
    return experience

def get_projects(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    projects = []
    for ent in doc.ents:
        if(ent.label_ == 'PERSON'):
            projects.append(ent.text)
    return projects

import spacy
from spacy.matcher import Matcher

def extract_education(resume_text):
    # Load the English language model
    nlp = spacy.load("en_core_web_sm")

    # Preprocess the resume text
    doc = nlp(resume_text)

    # Define a pattern to match education information
    matcher = Matcher(nlp.vocab)
    education_pattern = [
        {"LOWER": {"in": ["bachelor's", "bachelors", "bsc", "b.sc","BE","Btech"]}},
        {"IS_ALPHA": True, "OP": "*"},
        {"LOWER": {"in": ["in"]}},
        {"IS_ALPHA": True, "OP": "*"},
        {"LOWER": {"in": ["computer", "science", "engineering", "biology","pharmacy","electronics","mechanical","civil","electrical"]}},
    ]
    matcher.add("EducationPattern", [education_pattern])

    # Apply the matcher to extract education information
    matches = matcher(doc)

    education_info = []
    for match_id, start, end in matches:
        span = doc[start:end]
        education_info.append(span.text)

    print(education_info)
    return education_info

