import spacy
from spacy.matcher import Matcher
import re

# load pre-trained model
nlp = spacy.load('en_core_web_sm')

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
