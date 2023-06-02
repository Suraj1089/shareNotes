from os import environ
from Bard import Chatbot
from fastapi import APIRouter,Request,HTTPException
import random


router = APIRouter(
    tags=['Recommendation']
)

BARD_TOKEN = environ.get("BARD_TOKEN")

chatbot = Chatbot(BARD_TOKEN)

# print(chatbot.ask("top 10 leader names in india"))

def recommend_projects(data: dict):
    expertise = data['expertise']
    skills = (data['skills'])
    print(expertise,skills)

    queries = [
    f"I have {expertise} in programming with basic knowledge of {skills}. Can you suggest 6 to 7 projects to help me improve my skills?",
    f"I have {expertise} skills in {skills}. Could you recommend some projects that would challenge me and allow me to further enhance my skills?",
    f"As an {expertise} in {skills}, what projects would you recommend for someone at my level?",
    f"I have {expertise} in {skills}. Can you suggest 5 to 6 full-stack projects that would allow me to apply my skills in both areas?",
    f"Recommend me some projects to improve my {skills} skills.",
    f"My skills are {skills}, and I am {expertise} in programming. Can you suggest 4 to 8 projects to help me improve my skills?",
    f"I am {expertise} in {skills}. Can you suggest some 6 to 9 projects that would challenge me and allow me to further enhance my skills?",
    f"What projects would you recommend for someone at my level? I have {expertise} in {skills}.",
    f"Suggest some projects that I can do in my final year of engineering. I have {expertise} in {skills}.",
    f"I want to expand my knowledge in {skills} and become an expert. Can you recommend 7 to 9 projects that will help me achieve this goal?",
    f"I'm skilled in {skills} and looking for advanced projects. Can you suggest 8 to 9 projects that will push my abilities to the next level?",
    f"As someone with {expertise} in {skills}, I want to work on complex projects. Can you provide recommendations for 7 to 8 challenging projects?",
    f"I have experience in {skills} and I'm eager to take on more projects. Can you suggest 9 to 10 interesting projects to further enhance my skills?",
    f"I'm passionate about {skills} and I have {expertise} years of experieance and I am always looking to learn more. Could you suggest 10 projects that cover a wide range of concepts and technologies?",
]


    query = random.choice(queries)
    data = chatbot.ask(query)
    print(data['content'])
    return data['content']

@router.post('/recommend')
async def recommend(request: Request):
    data = await request.form()
    data = dict(data)
    projects = recommend_projects(dict(data))
    
    if projects:
        return {
            'projects':projects
        }
    raise HTTPException(status_code=404,detail="Error in loading projects")

