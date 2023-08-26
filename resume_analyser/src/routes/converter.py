from fastapi import APIRouter, UploadFile, File
import io
from fastapi.responses import RedirectResponse
from ..utils import converter
from ..db import schemas
import pypdf
from ..db.config import BASE_DIR
import shutil
from fastapi import status
from fastapi.responses import JSONResponse
import os 
from typing import List
import re 
from ..utils.converter import Links
from collections import defaultdict
from ..utils import parser




router = APIRouter(
    tags=["converter"]
)


# route to upload user uploaded resume files
@router.post("/upload",status_code=status.HTTP_201_CREATED)
def upload(file: UploadFile = File(...)):
    try:
        # if folder not present
        path = BASE_DIR / 'uploads/pdf'
        if not os.path.exists(path=path):
            os.makedirs(path)
        
        # with open(f'{path}/{file.filename}', 'wb') as f:
        #     shutil.copyfileobj(file.file, f)

        with open(f'{path}/{file.filename}', 'wb') as buffer:
            buffer.write(file.file.read())
    
    except Exception as e:
        return JSONResponse(
            content=f'Error in uploading {file.filename}',
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    finally:
        file.file.close()
        
    return {"message": f"Successfully uploaded {file.filename}",
            "path": BASE_DIR / f'uploads/pdf/{file.filename}'
            }


@router.post('/analyse')
def analyse_resume(path: str):
    # check if file exists
    if not os.path.exists(path):
        return JSONResponse(
            content=f'File {path} not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    with open(path,'rb') as file:
        resume,links = converter.convert(file)
    
    with open('sample.txt','w') as txt:
        txt.write(resume)
    
    social_links = defaultdict(list)

    # find social links
    links = Links(links)
    social_links['linkedin'] = links.get_links_by_platform('linkedin')
    social_links['github'] = links.get_links_by_platform('github')
    social_links['twitter'] = links.get_links_by_platform('twitter')
    social_links['facebook'] = links.get_links_by_platform('facebook')
    social_links['instagram'] = links.get_links_by_platform('instagram')
    social_links['portfolio'] = links.get_links_by_platform('portfolio')
    social_links['projects'] = links.get_links_by_platform('github_project')

      
    # find name
    name = parser.extract_name(resume)

    # find email
    email = parser.extract_email(resume)

    # find phone number
    phone = parser.get_phone_number(resume)

    # find skills
    skills = []
    for line in resume.split('\n'):
        if line.strip().isupper():
            skills.append(line)

    # find education
    education = parser.extract_education(resume)

    # find experience
    experience = parser.extract_experience(resume)

    # find projects
    projects = []
    for line in resume.split('\n'):
        if 'projects' in line.lower():
            projects.append(line)

    # find achievements
    achievements = []
    for line in resume.split('\n'):
        if 'achievements' in line.lower():
            achievements.append(line)

    # find certifications
    certifications = []
    for line in resume.split('\n'):
        if 'certifications' in line.lower():
            certifications.append(line)

    # find hobbies
    hobbies = []
    for line in resume.split('\n'):
        if 'hobbies' in line.lower():
            hobbies.append(line)

    # find languages
    languages = []
    for line in resume.split('\n'):
        if 'languages' in line.lower():
            languages.append(line)

    # find interests
    interests = []
    for line in resume.split('\n'):
        if 'interests' in line.lower():
            interests.append(line)

    # find references
    references = []
    for line in resume.split('\n'):
        if 'references' in line.lower():
            references.append(line)

    # find address
    address = None
    for line in resume.split('\n'):
        if 'address' in line.lower():
            address = line
            break

    # find summary
    summary = None
    for line in resume.split('\n'):
        if 'summary' in line.lower():
            summary = line
            break

    # find objective
    objective = None
    for line in resume.split('\n'):
        if 'objective' in line.lower():
            objective = line
            break

    # find courses
    courses = []
    for line in resume.split('\n'):
        if 'courses' in line.lower():
            courses.append(line)

    # find publications 
    publications = []
    for line in resume.split('\n'):
        if 'publications' in line.lower():
            publications.append(line)

    # find awards
    awards = []
    for line in resume.split('\n'):
        if 'awards' in line.lower():
            awards.append(line)

    
    return {
        'name': name,
        'email': email,
        'phone': phone,
        'skills': skills,
        'education': education,
        'experience': experience,
        'projects': projects,
        'achievements': achievements,
        'certifications': certifications,
        'hobbies': hobbies,
        'languages': languages,
        'interests': interests,
        'references': references,
        'address': address,
        'summary': summary,
        'objective': objective,
        'courses': courses,
        'publications': publications,
        'awards': awards,
        'social_links': social_links
    }