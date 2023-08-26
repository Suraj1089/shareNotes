import spacy
import re



def get_phone_number(string):
    r = re.compile(r'(\+\d{1,3}[-\.\s]??)?(\d{1,4}[-\.\s]??)?(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    
    cleaned_numbers = []
    for groups in phone_numbers:
        full_number = ''.join(groups)
        cleaned_number = re.sub(r'\D', '', full_number)
        cleaned_numbers.append(cleaned_number)
    
    return cleaned_numbers

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