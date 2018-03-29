# -*- coding: utf-8 -*- #

import os
import shutil
import sys
from pathlib import Path

from config import *

# --------------------------------------------------------------------------------------------------------
def delete_folder_contents(dst):
    print('Deleting {}...'.format(dst))
    for item in os.listdir(dst):
        s = os.path.join(dst, item)
        # print('\t{}                  '.format(s))#, end='\r')
        if os.path.isdir(s):
            shutil.rmtree(s)
        else:
            os.remove(s)


# --------------------------------------------------------------------------------------------------------
def copytree(src, dst, symlinks=False, ignore=None):
    print('Copying {}'.format(dst))
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        # print('\t{}                  '.format(d))#, end='\r')
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
 

def convert_md_to_html(article, pathOutput):
    """Converts markdown (.md) files to .html files.

    :param article: pathlib path to article .md file
    :param metadata: dictionary of file metadata
    """

    def get_metadata(article):
        """Gets metadata from article.md templateArticleer.

        :param article: pathlib paths to each article
        """
        metadata = {'title':'a', 'date':'a', 'updated':'a', 'comments':True,
        'slug':'a', 'tags':['a'], 'prepTime':'a', 'cookTime':'a', 'image':'a'}

        with open(article) as f:  
            for line, content in enumerate(f):
                if content.startswith('Title: '):
                    metadata['title'] = content.replace('Title: ','').replace('\n','')
                if content.startswith('date: '):
                    metadata['date'] = content.replace('date: ','').replace('\n','')
                if content.startswith('updated: '):
                    metadata['updated'] = content.replace('updated: ','').replace('\n','')
                if content.startswith('comments: '):
                    metadata['comments'] = content.replace('comments: ','').replace('\n','')
                if content.startswith('slug: '):
                    metadata['slug'] = content.replace('slug: ','').replace('\n','')
                if content.startswith('tags: '):
                    tags = content.replace('tags: ','').replace('\n','').split(',')
                    tags = [x.lstrip(' ') for x in tags]
                    metadata['tags'] = tags
                if content.startswith('prepTime: '):
                    metadata['prepTime'] = content.replace('prepTime: ','').replace('\n','')
                if content.startswith('cookTime: '):
                    metadata['cookTime'] = content.replace('cookTime: ','').replace('\n','')
                if content.startswith('image: '):
                    metadata['image'] = content.replace('image: ','').replace('\n','')

        return metadata


    metadata = get_metadata(article)

    import markdown2
    from markdown2 import markdown_path
    with open('theme/article.html') as f:
        templateArticle = [x.strip('\n,') for x in f]
           
    templateArticle = [x.strip() for x in templateArticle]    

    for line in range(len(templateArticle)):
        templateArticle[line] = templateArticle[line].replace('#TITLE#', metadata['title'])
        templateArticle[line] = templateArticle[line].replace('#COOKTIME#', metadata['cookTime'])
        templateArticle[line] = templateArticle[line].replace('#PREPTIME', metadata['prepTime'])
            
    with open(article) as f:
        md = [x.strip('') for x in f]
    
    mdString = ''.join(md)
    content = markdown2.markdown(mdString, extras=['footnotes','smarty-pants','cuddled-lists','target-blank-links','tables','templateArticleer-ids','break-on-newline'])
    content = [content]

    templateArticle[templateArticle.index('#BODY#')] = content

    pathOutput = pathOutput/Path('articles/'+metadata['slug']+'.html')
    # pathOutput = pathOutput/Path(metadata['slug']+'.html')

    with open(pathOutput, mode='wt', encoding='utf-8') as myfile:
        for lines in templateArticle:
            myfile.write(''.join(lines))
            myfile.write('\n')
    print('\tSaved {}'.format(pathOutput))



    

	


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


    # paths
    pathOutput = Path(OUTPUT_PATH)

    # get article paths
    pathArticles = Path(PATH+'/articles')
    articles = list(pathArticles.glob('*.md'))

    # output articles
    for article in articles:
        convert_md_to_html(article, pathOutput)


    # output index

    # output assets
    src = Path('theme/assets')
    dst = pathOutput/'assets'
    delete_folder_contents(dst)
    copytree(src, dst, symlinks=False, ignore=None)



    print('Done.\n')