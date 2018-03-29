# -*- coding: utf-8 -*- #

import os
import shutil
import sys
from pathlib import Path

from config import *

# --------------------------------------------------------------------------------------------------------
def delete_folder_contents(src):
    print('Deleting files...\n')
    for item in os.listdir(src):
        s = os.path.join(src, item)
        #print('\t{}                  '.format(s))#, end='\r')
        if os.path.isdir(s):
            shutil.rmtree(s)
        else:
            os.remove(s)


# --------------------------------------------------------------------------------------------------------
def copytree(src, dst, symlinks=False, ignore=None):
    print('Copying files...\n')
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        #print('\t{}                  '.format(d))#, end='\r')
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
 





def convert_md_to_html(pathArticles):
    # import pandas as pd
    import markdown2
    from markdown2 import markdown_path

    def build(shortName, title, author, ISBN, yearPublished, yearRead):
        with open('_head.html') as f:
            head = [x.strip('\n,') for x in f]
       
        with open('_foot.html') as f:
            foot = [x.strip('\n,') for x in f]
        
        head = [x.strip() for x in head]    
        foot = [x.strip() for x in foot]

        for line in range(len(head)):
            head[line] = head[line].replace('#SHORTNAME#',shortName)
            head[line] = head[line].replace('#TITLE#',title)
            head[line] = head[line].replace('#AUTHOR#',author)
            head[line] = head[line].replace('#ISBN#',ISBN)
            head[line] = head[line].replace('#YEARPUBLISHED#',yearPublished)
            head[line] = head[line].replace('#YEARREAD#',yearRead)
                
        with open(shortName+'.md') as f:
            md = [x.strip('') for x in f]
        
        mdString = ''.join(md)
        content = markdown2.markdown(mdString, extras=['footnotes','smarty-pants','cuddled-lists','target-blank-links','tables','header-ids','break-on-newline'])
        content = [content]
        doc = head+content+foot

        with open('../'+shortName+'.html', mode='wt', encoding='utf-8') as myfile:
            for lines in doc:
                myfile.write(''.join(lines))
                myfile.write('\n')
        print('\tSaved {}.html'.format(shortName))

    def get_metadata(article):
        """Gets metadata from article.md header.

        :param article: pathlib paths to each article
        """
        metadata = {'title':'a', 'date':'a', 'updated':'a', 'comments':True,
        'slug':'a', 'tags':['a'], 'prepTime':'a', 'cookTime':'a', 'image':'a'}

        with open(article) as f:  
            for line, content in enumerate(f):
                if content.startswith('Title: '):
                    metadata['title'] = content.replace('Title: ','')
                if content.startswith('date: '):
                    metadata['date'] = content.replace('date: ','')
                if content.startswith('updated: '):
                    metadata['updated'] = content.replace('updated: ','')
                if content.startswith('comments: '):
                    metadata['comments'] = content.replace('comments: ','')
                if content.startswith('slug: '):
                    metadata['slug'] = content.replace('slug: ','')
                if content.startswith('tags: '):
                    tags = content.replace('tags: ','').replace('\n','').split(',')
                    tags = [x.lstrip(' ') for x in tags]
                    metadata['tags'] = tags
                if content.startswith('prepTime: '):
                    metadata['prepTime'] = content.replace('prepTime: ','')
                if content.startswith('cookTime: '):
                    metadata['cookTime'] = content.replace('cookTime: ','')
                if content.startswith('image: '):
                    metadata['image'] = content.replace('image: ','')

        print(metadata)
        return metadata


    articles = list(pathArticles.glob('*.md'))

    for article in articles:
        get_metadata(article)

	


# --------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # get paths
    # homePath = Path.cwd().home()
    # for parent in Path.cwd().parents:
    #     if str(parent)[-6:]=='GitHub':
    #         GitHubPath = parent


    # src = GitHubPath/'blog-source/output'
    # dst = GitHubPath/'blog'

    # delete_folder_contents(dst)
    # copytree(src, dst, symlinks=False, ignore=None)

    pathArticles = Path(PATH+'/articles')


    convert_md_to_html(pathArticles)



    print('Done.\n')