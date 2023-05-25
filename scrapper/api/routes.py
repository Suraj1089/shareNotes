from fastapi import APIRouter,Request,HTTPException,status
from .scrapper import get_page_data,generate_query_url,scrap_projects,scrap_readme
import requests
import os
from fastapi.responses import JSONResponse,HTMLResponse
import pandas as pd

router = APIRouter()


@router.post('/message')
async def contact(request: Request):
    form_data = await request.form()
    url = os.getenv('PORTFOLIO_URL')+ 'message'
    try:
        r = requests.post(url=url,data=form_data)
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Unable to send message try again!'
        )
    print(r.status_code)
    if r.status_code == 201:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content='Message sent Succefully!'
        )

    raise HTTPException(
        status_code=status.WS_1013_TRY_AGAIN_LATER,
        detail='Unable to send message try again!'
    )

@router.post('/scrap')
async def scrap_search_query(request: Request,page: int = 1):
    data = await request.form()
    keyword = data['keyword']
    page = data['pageNumber']
    url = generate_query_url(keyword,page)
    soup = get_page_data(url)
    if soup is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Error in fetching data! Try Again!'
        )
    # if not none scrap projectsdata
    projects = scrap_projects(soup)
    df = pd.DataFrame(projects)
    # df.to_csv('projects.csv')

    
    return df.to_html()


@router.post('/readme',response_class=HTMLResponse)
async def get_readme(request: Request):
    data = await request.form()
    url = data['url']
    readme = scrap_readme(url)
    if readme is not None:
        print('not null')
        return HTMLResponse(readme,status_code=status.HTTP_200_OK)
        
    return {"data":"readme not present"}