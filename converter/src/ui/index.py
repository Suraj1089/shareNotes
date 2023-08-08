#!/usr/bin/env python3
from datetime import datetime
from typing import List, Tuple
from uuid import uuid4

from nicegui import Client, ui


anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}'
ui.add_head_html(f'<style>{anchor_style}</style>')
with ui.header().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
    file = ui.upload(label='Upload Result Pdf File',on_upload=lambda e: ui.notify(f'Uploaded {e.name}'),on_rejected=lambda e: ui.notify('Rejected {e.name}'),auto_upload=True).props('accept=.pdf').classes('max-w-full w-full')


ui.run()