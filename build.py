# -*- coding: utf-8 -*- #

import os
import shutil
import sys
from pathlib import Path

from config import *

def delete_folder_contents(dst):
    """Delete all contents of dst.
    """
    print('\tDeleting {}...'.format(dst))
    for item in os.listdir(dst):
        s = os.path.join(dst, item)
        # print('\t{}                  '.format(s))#, end='\r')
        if os.path.isdir(s):
            shutil.rmtree(s)
        else:
            os.remove(s)


def copytree(src, dst, symlinks=False, ignore=None):
    """Copy directory and all contents from src to dst.
    """
    print('\tCopying {}'.format(dst))
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        # print('\t{}                  '.format(d))#, end='\r')
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def copy_file(src, dst):
    """Copy file from src to dst.
    """
    shutil.copy(src, dst)
 

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
            if content.startswith('category: '):
                metadata['category'] = content.replace('category: ','').replace('\n','')

    return metadata


def insert_text_in_file(original, add, insertionPoint):
    """Inserts text from add into original at insertionPoint    
    """
    # read original 
    f = open(original, "r")
    contents = f.readlines()
    f.close()

    # read addition
    f = open(add, "r")
    contentsAdd = f.readlines()
    f.close()

    # get index of insertionPoint
    i=0
    for line in contents:
        if insertionPoint in line:
            index = i
        i+=1

    # add text
    contents[index:index] = contentsAdd

    # write original with addition
    f = open(original, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()


def replace_text_in_file(original, add, replaceText):
    """Replaces replaceText with add in original file.
    """
    with open(original, 'r') as f:
      content = f.read()

    content = content.replace(replaceText, add)

    with open(original, 'w') as f:
      f.write(content)


def convert_md_to_html(article, pathOutput):
    """Converts markdown (.md) files to .html files.

    :param article: pathlib path to article .md file
    :param metadata: dictionary of file metadata
    """
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
        templateArticle[line] = templateArticle[line].replace('#IMAGE#', metadata['image'])
            
    with open(article) as f:
        md = [x.strip('') for x in f]
    

    md = md[md.index('\n'):] # drop metadata from article text
    mdString = ''.join(md)
    body = markdown2.markdown(mdString, extras=['footnotes','smarty-pants','cuddled-lists','target-blank-links','tables','templateArticleer-ids','break-on-newline'])
    body = [body]

    templateArticle[templateArticle.index('#BODY#')] = body

    pathOutput = pathOutput/Path('articles/'+metadata['slug']+'.html')

    with open(pathOutput, mode='wt', encoding='utf-8') as myfile:
        for lines in templateArticle:
            myfile.write(''.join(lines))
            myfile.write('\n')
    print('\tSaved {}'.format(pathOutput))



def construct_index(articles, categories, pathOutput):
    """Copies index.html to pathOutput, and constructs page using categories and articles.
    """

    # copy index from template
    copy_file('theme/index.html', pathOutput)

    # get categories and titles
    metadataAll = {}
    i = 0
    for article in articles:
        metadata = get_metadata(article)
        metadataAll[i] = metadata
        i+=1
 
    # update index with categories
    for category in categories:
        # print(category)
        original = pathOutput/'index.html'
        
        # insert text
        insert_text_in_file(original, add='theme/indexNav.html', insertionPoint='#CATEGORY_NAV#')
        insert_text_in_file(original, add='theme/indexCategory.html', insertionPoint='#CATEGORIES#')
        
        # replace text
        replace_text_in_file(original, add=category, replaceText='#CATEGORY#')
        replace_text_in_file(original, add=category.replace(' ',''), replaceText='#CATEGORY_ID#')
        
        # update articles
        for key in metadataAll:
            if metadataAll[key]['category']==category:
                # print('\t{}'.format(metadataAll[key]['title']))
                insert_text_in_file(original, add='theme/indexArticle.html', insertionPoint='#ARTICLES#')
                replace_text_in_file(original, add=metadataAll[key]['title'], replaceText='#TITLE#')
                replace_text_in_file(original, add=metadataAll[key]['image'], replaceText='#IMAGE#')
                replace_text_in_file(original, add=metadataAll[key]['slug'], replaceText='#SLUG#')

    # clean insertionPoints
    replace_text_in_file(original, add='', replaceText='#CATEGORIES#')
    replace_text_in_file(original, add='', replaceText='#CATEGORY_NAV#')
    replace_text_in_file(original, add='', replaceText='#ARTICLES#')

	

# --------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # paths
    pathOutput = Path(OUTPUT_PATH)
    pathArticles = Path(PATH+'/articles')
    
    # get variables
    categories = CATEGORIES
    articles = list(pathArticles.glob('*.md'))

    # output articles
    print('Converting articles...')
    for article in articles:
        convert_md_to_html(article, pathOutput)

    # output index
    print('Building index.html...')
    construct_index(articles, categories, pathOutput)


    # output assets
    print('Copying assets...')
    src = Path('theme/assets')
    dst = pathOutput/'assets'
    delete_folder_contents(dst)
    copytree(src, dst, symlinks=False, ignore=None)

    # output images
    print('Copying images...')
    src = Path('content/images')
    dst = pathOutput/'images'
    delete_folder_contents(dst)
    copytree(src, dst, symlinks=False, ignore=None)


    print('Done.\n')