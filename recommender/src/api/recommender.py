from os import environ
from Bard import Chatbot
from fastapi import APIRouter,Request,HTTPException
import random
from .schemas import Recoomendation


router = APIRouter(
    tags=['Recommendation']
)


BARD_TOKEN = environ.get("BARD_TOKEN")

chatbot = Chatbot(BARD_TOKEN)

# print(chatbot.ask("top 10 leader names in india"))

def recommend_projects(data: dict):
    expertise = data['expertise']
    skills = ' '.join(data['skills[]'])
    print(expertise,skills)

    queries = [

            f"I am a {expertise} in programming with basic knowledge of {skills}. Can you suggest some projects 6 5o 7 to help me improve my skills?",

            f"I have {expertise} skills in {skills}. Could you recommend some projects that would challenge me and allow me to further enhance my skills?",

            f"As an {expertise} in {skills} What projects would you recommend for someone at my level?",

            f"I have {expertise} in {skills} Can you suggest some 5 to 6 full-stack projects that would allow me to apply my skills in both areas?",

            f"recommend me some projects to improve my {skills} skills",

            f"my skills are {skills} and i am {expertise} in programming. Can you suggest some 4 to 8 projects to help me improve my skills?",

            f"i am {expertise} in {skills}. Can you suggest some 6 ro 9 projects that would challenge me and allow me to further enhance my skills?",

            f"would you recommend for someone at my level? I have {expertise} in {skills}",

            f"Suggest some projects that I can do in my final year of engineering. I have {expertise} in {skills}"

        ]

    query = random.choice(queries)
    data = chatbot.ask(query)
    print(data['content'])
    return data['content']

@router.post('/recommend')
async def recommend(request: Request):
    data = await request.form()
    data = dict(data)
    print(dict(data))
    print(data.keys())
    # print(data["skills"])
    projects = recommend_projects(dict(data))
    
    if projects:
        return {
            'projects':projects
        }
    raise HTTPException(status_code=404,detail="Error in loading projects")

    # data = {
    #     'expertise':form_data['expertise'],
    #     'skills':form_data['skills'].split(',')
    # }

    # projects = recommend_projects(data)
    # if projects:
    #     return {
    #         'projects':projects
    #     }
    # raise HTTPException(status_code=404,detail="No projects found")
