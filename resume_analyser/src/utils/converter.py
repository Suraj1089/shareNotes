
import io
import pypdf
from typing import List
import re
import pandas as pd
from typing import Tuple


def convert(path: str) -> Tuple:
    """Converts pdf to text"""
    print('path in convert ', path)
    text = ""
    links = []
    reader = pypdf.PdfReader(path)
    noOfPages = len(reader.pages)
    for line in range(noOfPages):
        page = reader.pages[line]
        
        # find embeded links
        if "/Annots" in page:
            for annot in page["/Annots"]:
                subtype = annot.get_object()["/Subtype"]
                if subtype == "/Link":
                    links.append(annot.get_object()['/A']['/URI'])
        text += page.extract_text()
    return (text,links)

def convert2(path):
    """Converts pdf to text"""
    text = ""
    reader = pypdf.PdfReader(path)
    noOfPages = len(reader.pages)
    for line in range(0,noOfPages):
        page = reader.pages[line]
        text += page.extract_text()
    return (text,[])


class Links:
    """
    Class to find links from a list of links
    Attributes:
        links: List of links

    """
    def __init__(self, links: List[str]):
        '''
        Args:
            links: List of links

        '''
        self.links = links

    def get_links_by_platform(self, platform: str) -> List[str]:
        '''
           function to get links by platform
            Args:
                platform: platform name
            Returns:
                List of links
        '''
        if platform == 'github':
            pattern = r'https:\/\/github\.com\/[A-Za-z0-9_.-]+'
        elif platform == 'linkedin':
            pattern = r'https:\/\/www\.linkedin\.com\/in\/[A-Za-z0-9_.-]+'
        elif platform == 'twitter':
            pattern = r'https:\/\/twitter\.com\/[A-Za-z0-9_.-]+'
        elif platform == 'facebook':
            pattern = r'https:\/\/www\.facebook\.com\/[A-Za-z0-9_.-]+'
        elif platform == 'instagram':
            pattern = r'https:\/\/www\.instagram\.com\/[A-Za-z0-9_.-]+'
        elif platform == 'portfolio':
            pattern = r'https:\/\/[A-Za-z0-9_.-]+\.com'
        elif platform == 'github_project':
            pattern = r'https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+'
        else:
            raise ValueError(f"Unsupported platform: {platform}")

        for link in self.links:
            matches = re.findall(pattern, link)
            if matches and platform == 'github_project':
                # return list of projects
                return matches
            elif matches:
                # return first match for other platforms
                return matches[0]
        return None
 
