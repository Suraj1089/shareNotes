from fastapi import APIRouter,Request,HTTPException,status
from .scrapper import get_page_data,generate_query_url,scrap_projects
import requests
import os
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post('/message')
async def contact(request: Request):
    form_data = await request.form()
    print(form_data)
    url = os.getenv('PORTFOLIO_URL')+ 'message'
    r = requests.post(url=url,data=form_data)
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
    url = generate_query_url(keyword,page)
    print('generated url ' , url)
    soup = get_page_data(url)
    print(soup)
    if soup is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Error in fetching data! Try Again!'
        )
    # if not none scrap projectsdata
    projects = scrap_projects(soup)
    # print(projects)
    
    return {"data":"genraeted"}
