# -*- coding: utf-8 -*-

import markdown
from flask import Flask
from flask import render_template, Markup, request
import os
from collections import OrderedDict
print('markdown version: ', markdown.version)

"""
NOTES
-----

backslashes available in markdown:
\ backslash
` backtick
* asterisk
_ underscore
{} curly braces
[] square brackets
() parentheses
# hashmark
+ plus sign
- minus sign (hyphen) 
. dot
! exclamation mark

++ RESERVED CHARACTERS:
||| complete

"""


def iterate_till_blank(file_obj, strip_ends=True):
    result = []
    while True:
        try:
            new_line = file_obj.__next__()
        except StopIteration:
            break
        if len(new_line) <= 1:
            break
        else:
            if strip_ends: result.append(new_line.strip())
            else: result.append(new_line)
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


def first(s):
    '''Return the first element from an ordered collection
       or an arbitrary element from an unordered collection.
       Raise StopIteration if the collection is empty.
    '''
    return next(iter(s))


def md_progressbar(percent, title=None):
    """
    returns markdown formatted progressbar coutesy of progressed.io
    website : https://github.com/fehmicansaglam/progressed.io
    :param percent:
    :return: ![Progress](http://progressed.io/bar/<percent>)
    """
    if title:
        progressbar = '![Progress](http://progressed.io/bar/{0}?title={1})'.format(percent, title)
    else:
        progressbar = '![Progress](http://progressed.io/bar/{0})'.format(percent)
    return progressbar


def is_unsorted(name):
    if 'unsorted' in str(name).lower():
        return True


def ensure_url(line_of_text, split_key=' '):
    words = line_of_text.split(split_key)  # split lines by spacing
    for i, character in enumerate(words):
        if character[:4] == 'http':
            # add formatting to both urls in the middle and end of lines
            # (urls at the end of the line have a '\n' escape
            if character.endswith('\n'):
                words[i] = '<' + character.strip() + '>' + '\n'
            else:
                words[i] = '<' + character + '>'
    return split_key.join(words)


def build_all_files(full_filepaths, urlify=True):
    """
    HEAVY. opens all files and stores them as a huge variable.
    :param full_filepaths: filepaths as an input list
    :param urlify: apply markdown formatting to ensure urls turn into links in markdown viewers
    :returns: a tuple with the format (filepath, file_as_string) for every filepath
    """
    result = []  # stores files as objects
    for i, full_filepath in enumerate(full_filepaths):
        with open(full_filepath, encoding='utf-8', errors='ignore') as readme:
            readme = readme.readlines()
            for j, line in enumerate(readme):
                if urlify:
                    line = ensure_url(line)
                    readme[j] = line

            result.append(''.join(readme))
    return zip(full_filepaths, result)


def build_content_dict_from_tuple(file_tuples, keyword='todo', flag_complete=True):
    """
    DISCLAIMER : ONLY DESIGNED TO WORK WITH PERSONAL MARKDOWN RULES

    actually not very safe, as the todo keyword can be very easily typed into notes

    searches a list of files (in string format) for the first instance of a given keyword
    and builds an ordered dictionary consisting of:
    {filename : [absolute_path, line_containing_keyword, content_related_to_line]}

    :return: OrderedDict() in the format {filename : [absolute_path, line_containing_keyword, content_related_to_line]}
    """
    from os.path import basename, splitext

    result = OrderedDict()
    for full_filepath, file_str in file_tuples:
        todo_boolean = False
        filename = splitext(basename(full_filepath))[0]  # get clean filename
        filename = filename[:-7]  # remove -readme

        if flag_complete:
            if '|||' in file_str:
                result[filename] = [full_filepath, None, None, True]
                print('completion flag found!')
                break

        readme = iter(file_str.splitlines())  #makes the same iterable as open() function

        for line in readme:
            if keyword in line.lower():
                # strips markdown formatting on left and \n + spaces on both sides
                subtitle = line.lstrip('#').strip()
                content = iterate_till_blank(readme)
                result[filename] = [full_filepath, subtitle, content, False]
                todo_boolean = True
                break
            else:
                continue

        if not todo_boolean:
            result[filename] = [full_filepath, None, None, False]

    return result


def build_content_dict_from_filepaths(full_filepaths, keyword='todo'):
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



app = Flask(__name__)
print('app initiated. name of app: {0}'.format(__name__))

# global variables
full_filepaths, filenames = get_full_and_simple_filepaths(folder='./', keyword='.md', debug=False)
file_tuples = build_all_files(full_filepaths)

# temp = build_content_dict_from_tuple(file_tuples)
# for k, v in temp.items():
#     print(k, v)


def dashboard():
    # TODO: this is where to put all the dashboard stuff, it stays on every page since it
    # TODO: lives within the layout page
    return ''



@app.route('/full/')
def all_readmes():
    global file_tuples

    md = ''
    for file in full_filepaths:
        with open(file) as single_readme:
            md += single_readme.read()
            md += '\n----\n'

    full_readme_md = md
    md_content = Markup(markdown.markdown(full_readme_md))
    return render_template('card_single.html', name='all the readmes', content=md_content)

@app.route('/todo/')
def todo():
    global file_tuples

    # find keyword from filepaths
    todo_dict = build_content_dict_from_tuple(file_tuples, keyword='todo')

    # rebuild markdown formatting for todo list
    md_list = []
    for k, v in todo_dict.items():
        # title with links
        md_block_0 = '#### [{0}]({1})\n'.format(k, v[0])
        # todo : (currently relative links, only works in github markdown)
        # TODO: CONVERT LINKS INTO GITHUB URLS HERE

        # subtitle and contents
        md_block_1 = ''
        if v[1]:
            percentage = 0
            md_block_1 += '###### {0}\n'.format(v[1])  # subtitle
            # if there is a todolist, then check for contents
            if v[2]:
                # make a percentage
                percentage = max(0, (5 - len(v[2]))) * 20
                # write contents
                for lines in v[2]:
                    md_block_1 += '{0}\n'.format(lines)  # contents
        elif v[3]:
            md_block_1 += '###### complete!\n'
            percentage = 100
        else:
            md_block_1 += '\nno todo list found.\n'
            percentage = 0

        # progress bar
        md_block_2 = md_progressbar(percentage)

        md = '\n'.join([md_block_0, md_block_2, md_block_1])
        #md += '\n----'
        md_list.append([md, percentage])

    # then join all individual mds with \n to make a combined md
    # todo_list_md = '\n'.join(md_list[0])
    # print(todo_list_md)
    md_contents = [Markup(markdown.markdown(md_pair[0])) for md_pair in md_list]
    percentages = [md_pair[1] for md_pair in md_list]
    return render_template('card_multiple_with_dashboard.html',
                           name='to-do list',
                           dashboard_contents=dashboard(),
                           contents=zip(percentages, md_contents))


@app.route('/single-page/')
def readme_card():
    test_content = """
    <h1>hey</h1>
    <p style="font-size: 80vmin">3days</p>
    """
    return render_template('card_single.html', name='test', content=test_content)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    print(request.method)
    return todo()

if __name__ == '__main__':
    app.run()