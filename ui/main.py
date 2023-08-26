from nicegui import ui, Tailwind\
    #!/usr/bin/env python3
from datetime import datetime
from typing import List, Tuple
from uuid import uuid4
import base64
import io
import requests
from processor import Theme

from nicegui import Client, ui, events

# Add necessary imports for nicegui and other libraries


class File:
    def __init__(self, e: events.UploadEventArguments):
        self.name = e.name
        self.content = e.content.read()
        self.id = str(uuid4())
        self.uploaded_at = datetime.now()

    def showUploadedFile(self):
        with ui.expansion('show/hide uploded file').classes('w-full text-black'):
            base64_pdf = base64.b64encode(self.content).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="100%"></iframe>'
            ui.html(pdf_display).classes('w-full h-screen')

        path = requests.post('http://localhost:8000/upload', files={'file': (self.name, self.content)})
        print(path.json()['path'])

        # create a button to analyse the file
        ui.button('Analyse', on_click=lambda: self.analyse(path.json()['path'])).classes('w-full')

    def analyse(self,path):
        print(path)

with ui.column().classes("bg-gray-10 mx-auto my-auto"):
    with ui.row().classes("mx-auto my-auto"):
        ui.label('Resume Analyser').classes("font-bold text-2xl text-center")

        def set_background(e):
            if dark_mode.value:
                ui.query('body').style('background', 'black')
            else:
                ui.query('body').style('background', 'white')

        dark_mode = ui.dark_mode(value=True, on_change=lambda e: set_background(e))

        with ui.element().classes('max-[360px]:hidden'):
            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)) \
                .props('flat fab-mini color=blue').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)) \
                .props('flat fab-mini color=blue').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)) \
                .props('flat fab-mini color=blue').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)


with ui.row().classes('mx-auto my-auto'):
    ui.markdown('''

        <a href="https://github.com/Suraj1089/shareNotes/network/members"><img src="https://img.shields.io/github/forks/Suraj1089/shareNotes" alt="Forks Badge"/></a>
       '''
                )
    ui.markdown('''
                 <a href="https://github.com/Suraj1089/shareNotes/pulls"><img src="https://img.shields.io/github/issues-pr/Suraj1089/shareNotes" alt="Pull Requests Badge"/></a>
       '''
                )
    ui.markdown('''
                 <a href="https://github.com/Suraj1089/shareNotes/issues"><img src="https://img.shields.io/github/issues/Suraj1089/shareNotes" alt="Issues Badge"/></a>
       ''')
    ui.markdown('''
                 <a href="https://github.com/Suraj1089/shareNotes/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/Suraj1089/shareNotes?color=2b9348"></a>
    ''')

with ui.row().classes("mx-auto my-auto"):
    # align links in a row
    file = ui.upload(
        label='Upload The Result Pdf File',
        on_upload=lambda e: File(e).showUploadedFile(),
        on_rejected=lambda e: ui.notify(f'Rejected {e}'),
        auto_upload=True,
        max_file_size=1_000_000
    ).props('accept=.pdf')
    
    ui.spinner().bind_visibility_from(file, 'uploading', value=True)
with ui.row().classes("mx-auto w-100").style('width: 50vw;'):
    # align links in a row   
    with ui.stepper().props('vertical').classes('w-full') as stepper:
        with ui.step('Preheat'):
            ui.label('Preheat the oven to 350 degrees')
            with ui.stepper_navigation():
                ui.button('Next', on_click=stepper.next)
        with ui.step('Ingredients'):
            ui.label('Mix the ingredients')
            with ui.stepper_navigation():
                ui.button('Next', on_click=stepper.next)
                ui.button('Back', on_click=stepper.previous).props('flat')
        with ui.step('Bake'):
            ui.label('Bake for 20 minutes')
            with ui.stepper_navigation():
                ui.button('Done', on_click=lambda: ui.notify('Yay!', type='positive'))
                ui.button('Back', on_click=stepper.previous).props('flat')

ui.run()
    

ui.run()
