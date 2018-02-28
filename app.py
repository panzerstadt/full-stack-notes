# -*- coding: utf-8 -*-

import markdown
from flask import Flask
from flask import render_template, Markup
import os
from collections import OrderedDict
print('markdown version: ', markdown.version)


def iterate_till_blank(file_obj, strip_ends=True):
    result = []
    while True:
        try:
            new_line = file_obj.__next__()
        except StopIteration:
            break
        if len(new_line) != 1:
            if strip_ends: result.append(new_line.strip())
            else: result.append(new_line)
        else:
            break
    return result


def get_full_and_simple_filepaths(folder='./', keyword='.md', ignore=[None], debug=False):
    file_list = []
    full_filepaths = []
    simple_filepaths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if keyword in file:
                if os.path.basename(root).startswith('.'):
                    print('NOT THIS ONE', root)
                    pass
                else:
                    file_list.append([root, file])
                    if debug:
                        print('filename: ', file)
                        print('tuple: ', (root, dirs, files))
    for filepath in file_list:
        full_filepaths.append(os.path.join(filepath[0], filepath[1]))
        simple_filepaths.append(os.path.splitext(filepath[1])[0])
    return full_filepaths, simple_filepaths


def build_content_dict(full_filepaths, keyword='todo'):
    """
    DISCLAIMER : ONLY DESIGNED TO WORK WITH PERSONAL MARKDOWN RULES

    searches a list of filepaths for the first instance of a given keyword
    and builds an ordered dictionary consisting of:
    {filename : [absolute_path, line_containing_keyword, content_related_to_line]}

    :return: OrderedDict() in the format {filename : [absolute_path, line_containing_keyword, content_related_to_line]}
    """
    from os.path import basename, splitext
    filenames = [splitext(basename(f))[0] for f in full_filepaths]  # get clean filename
    filenames = [f[:-7] for f in filenames]  # remove -readme

    result = OrderedDict()
    for i, full_filepath in enumerate(full_filepaths):
        with open(full_filepath, encoding='utf-8', errors='ignore') as readme:
            for line in readme:
                if keyword in line.lower():
                    # strips markdown formatting on left and \n + spaces on right
                    subtitle = line.lstrip('#').strip()
                    content = iterate_till_blank(readme)
                    result[filenames[i]] = [full_filepath, subtitle, content]
                    break
                else:
                    result[filenames[i]] = [full_filepath, None, None]
    return result


def first(s):
    '''Return the first element from an ordered collection
       or an arbitrary element from an unordered collection.
       Raise StopIteration if the collection is empty.
    '''
    return next(iter(s))

app = Flask(__name__)
print('app initiated. name of app: {0}'.format(__name__))

# global variables
full_filepaths, filenames = get_full_and_simple_filepaths(folder='./', keyword='.md', debug=True)


@app.route('/full/')
def all_readmes():
    global full_filepaths

    md = ''
    for file in full_filepaths:
        with open(file) as single_readme:
            md += single_readme.read()
            md += '\n----\n'

    full_readme_md = md
    md_content = Markup(markdown.markdown(full_readme_md))
    return render_template('card_single.html', name='all the readmes', content=md_content)

@app.route('/todo/')
@app.route('/')
def todo():
    global full_filepaths

    # find keyword from filepaths
    todo_dict = build_content_dict(full_filepaths, keyword='todo')

    # rebuild markdown formatting for todo list
    md_list = []
    for k, v in todo_dict.items():
        md = '#### [{0}]({1})\n'.format(k, v[0])  # title
        if v[1]:
            md += '###### {0}\n'.format(v[1])  # subtitle
        else:
            md += '###### complete!'
        if v[2]:
            # make a percentage

            # write contents
            for lines in v[2]:
                md += '{0}\n'.format(lines)  # contents
        md += '\n----'
        md_list.append(md)

    # then join all individual mds with \n to make a combined md
    todo_list_md = '\n'.join(md_list)
    print(todo_list_md)
    md_content = Markup(markdown.markdown(todo_list_md))
    return render_template('card_multiple.html', name='to-do list', content=md_content)


#@app.route('/')
def homepage():
    pass

# if __name__ == '__main__':
#     app.run()