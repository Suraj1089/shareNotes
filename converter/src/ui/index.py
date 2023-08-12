#!/usr/bin/env python3
from datetime import datetime
from typing import List, Tuple
from uuid import uuid4
import base64
import io
import requests

from nicegui import Client, ui, events

# Add necessary imports for nicegui and other libraries

anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}'
ui.add_head_html(f'<style>{anchor_style}</style>')


class File:
    def __init__(self, e: events.UploadEventArguments):
        self.name = e.name
        self.content = e.content.read()
        self.id = str(uuid4())
        self.uploaded_at = datetime.now()

    def showUploadedFile(self):
        ui.notify(f'Uploaded {self.name}')
        ui.button('Convert', on_click=lambda e: self.analyse()
                  ).classes('w-full mt-6')
        with ui.expansion('show/hide uploded file').classes('w-full text-black'):
            base64_pdf = base64.b64encode(self.content).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="100%"></iframe>'
            ui.html(pdf_display).classes('w-full h-screen')

    def analyse(self):
        ui.notify(f'Analyzing {self.name}')
        res = requests.post('http://localhost:8000/extract/',
                            files={'file': self.content})
        
        

        ui.notify(f'Analysis Complete {res.json()}')

    def process(self,path):
        pass
    def __repr__(self):
        return f'<File {self.name}>'

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


with ui.header().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
    ui.markdown('''
    # PDF Analyzer
    ''').classes('text-3xl font-bold text-center text-black mb-6 w-full')

    file = ui.upload(
        label='Upload The Result Pdf File',
        on_upload=lambda e: File(e).showUploadedFile(),
        on_rejected=lambda e: ui.notify(f'Rejected {e}'),
        auto_upload=True,
        max_file_size=1_000_000
    ).props('accept=.pdf').classes('max-w-full w-full')


ui.run()
