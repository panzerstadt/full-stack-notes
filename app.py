# -*- coding: utf-8 -*-

import markdown
from flask import Flask
from flask import render_template, Markup, request, url_for
import os, datetime
from collections import OrderedDict
print('markdown version: ', markdown.version)

"""
NOTES
-----
Markdown workflow:
1. parse markdown into css through python's markdown library
2. match css style to github-markdown form css stylesheet embedded in layout.html

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


def countdown(due_date='2017/04/15'):
    """
    :param due_date: year/month/day/hour   hour is optional
    :return: string denoting time left
    """
    # create countdown timer
    future = due_date.split('/')
    current = datetime.datetime.now()

    time_left = []
    time_left.append(int(future[0]) - current.year)
    time_left.append(int(future[1]) - current.month)
    time_left.append(int(future[2]) - current.day)

    t = time_left
    return '{0}yr {1}mth {2}dy(s) left.'.format(t[0], t[1], t[2])


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


def markdown_to_html(markdown_str):
    return Markup(markdown.markdown(markdown_str))


def image_center_autosize(img_html, fullscreen=True):
    if fullscreen: styles = 'height:70vmin;width:70vmin;margin-left:auto;margin-right:auto;display:block'
    else: styles = 'width:400px;margin-left:auto;margin-right:auto;display:block'

    temp = img_html.split('src')
    img_html = temp[0] + Markup('style="{0}"'.format(styles)) + ' src' + temp[1]
    return img_html


# todo: TURN THIS INTO A PYPI PACKAGE!
def generate_chart(chart_type='pie',
                   doughnut_center_str=None,
                   chart_size='200x100',
                   chart_data='t:20,80',
                   chart_label=None,
                   label_color=None,
                   chart_colors=None,
                   chart_animate=None,
                   api_source=1,
                   markdown=True,
                   markdown_label=None):
    """
    ### todo: turn this into a package on pypi!
    source: https://image-charts.com/documentation
    settings:
    cht = chart type                                *REQUIRED
    chs = chart size, (int(width) x int(height))    *REQUIRED
    chd = chart data                                *REQUIRED
    chl = chart label
    chan = either empty, or <duration>,<easing>  animates the chart (gif)
    chf = SOMETHING

    sample:
    https://chart.googleapis.com/chart?cht=p&chs=250x100&chd=t:20,5,75&chl=Done|In%20Progress|To%20Do

    javascript code automation from dev:
    https://image-charts.com/documentation#javascript-encoding-script

    :param api_source: 0 = google api, 1 = image-charts
    :return:
    """
    source = ['chart.googleapis.com', 'image-charts.com']
    colors = ['FFC00C', 'EA469E', '03A9F4']  # orange, red, blue

    # all the settings
    settings = []
    if chart_type == 'pie': settings.append('cht=p')
    if chart_type == 'doughnut':
        settings.append('cht=pd')
        if doughnut_center_str:
            settings.append('chli={0}'.format(doughnut_center_str))
    if chart_size: settings.append('chs={0}'.format(chart_size))
    if chart_data: settings.append('chd={0}'.format(chart_data))
    if chart_label: settings.append('chl={0}'.format(chart_label))
    if label_color: settings.append('chdls={0}'.format(label_color))
    if chart_colors: settings.append('chco={0}'.format(chart_colors))

    settings.append('chf=bg,s,00000000')

    if chart_animate == False:
        pass
    elif chart_animate == True:
        settings.append('chan')
    elif chart_animate is not None and len(chart_animate) >= 0:
        settings.append('chan=' + chart_animate)

    settings = iter(settings)
    chart_settings = '&'.join(settings)

    # build the url request
    chart_url  = 'https://'
    chart_url += source[api_source] + '/'
    chart_url += 'chart?'
    chart_url += chart_settings

    if markdown:
        if not markdown_label:
            markdown_label = 'alt text'
        chart_url = '![{0}]({1})'.format(markdown_label, chart_url)

    return chart_url


def progress_doughnut_chart(progress=60, centered=True):
    chart = generate_chart(markdown=True,
                           chart_type='doughnut',
                           doughnut_center_str='{0}'.format(str(progress)+'%'),
                           chart_size='600x600',
                           chart_label='not%20done|done',
                           label_color='FFC00C',
                           chart_animate=False,
                           chart_colors='DB2B39|7FD8D5',
                           chart_data='t:{0},{1}'.format(100 - progress, progress))

    chart = markdown_to_html(chart)
    if centered: chart = image_center_autosize(chart)

    return chart


def is_unsorted(name):
    if 'unsorted' in str(name).lower():
        return True


def ensure_relative_links(line_of_text, query_keyword='query'):
    return '/?{0}={1}'.format(query_keyword, line_of_text)

# not automated on markdown pyhton lib, but automatic on github
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


# todo: https://stackoverflow.com/questions/28207761/where-does-flask-look-for-image-files
def ensure_images(line_of_text):
    if './' in line_of_text:
        line_of_text = line_of_text.replace('./', './static/', 1)
        print(line_of_text)
    return line_of_text


def build_all_files(full_filepaths, urlify=True, fix_images=True):
    """
    HEAVY. opens all files and stores them as a huge variable.
    :param full_filepaths: filepaths as an input list
    :param urlify: apply markdown formatting to ensure urls turn into links in markdown viewers
    :param fix_images:
    :returns: a list with the format (filepath, file_as_string) for every filepath
    """
    result = []  # stores files as objects
    for i, full_filepath in enumerate(full_filepaths):
        with open(full_filepath, encoding='utf-8', errors='ignore') as readme:
            readme = readme.readlines()
            for j, line in enumerate(readme):
                if urlify:
                    line = ensure_url(line)
                if fix_images:
                    line = ensure_images(line)
                readme[j] = line

            result.append(''.join(readme))

    # if i return an iterator it will be gone the next time
    #[print(markdown_to_html(readme_page)) for readme_page in result]
    return list(zip(full_filepaths, result))


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
                todo_boolean = True
                #print('completion flag found in {0}!'.format(filename))
                pass

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


# OLD
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


def dashboard(list_of_stuff):
    # TODO: this is where to put all the dashboard stuff, it stays on every page since it
    # TODO: lives within the layout page
    if isinstance(list_of_stuff, str): return list_of_stuff
    else: return '\n'.join(list_of_stuff)


# OLD
@app.route('/full/')
def all_readmes():
    global file_tuples

    _, edited_readme_file = zip(*file_tuples)

    md = ''
    for file in edited_readme_file:
        md += file
        md += '\n----\n'

    full_readme_md = md
    md_content = Markup(markdown.markdown(full_readme_md))
    return render_template('card_single.html', name='all the readmes', content=md_content)


@app.route('/todo/')
def todo():
    global file_tuples

    # find keyword from filepaths
    todo_dict = build_content_dict_from_tuple(file_tuples, keyword='todo')

    # rebuild markdown formatting for todolist
    md_list = []
    for k, v in todo_dict.items():
        # title with links
        # ?filepath= turns the absolute filepath into a get request argument
        md_block_0 = '#### [{0}](?filepath={1})\n'.format(k, v[0])

        # subtitle and contents
        md_block_1 = ''
        if v[3]:
            md_block_1 += '###### complete!\n'
            percentage = 100
        elif v[1]:
            percentage = 0
            md_block_1 += '###### {0}\n'.format(v[1])  # subtitle
            # if there is a todolist, then check for contents
            if v[2]:
                # make a percentage
                percentage = max(0, (5 - len(v[2]))) * 20
                # write contents
                for lines in v[2]:
                    md_block_1 += '{0}\n'.format(lines)  # contents
        else:
            md_block_1 += '\nno todo list found.\n'
            percentage = 0

        # progress bar
        md_block_2 = md_progressbar(percentage)

        md = '\n'.join([md_block_0, md_block_2, md_block_1])
        md_list.append([md, percentage])

    # calculate total percentage of stuff done
    total_percentage = sum([int(x[1]) for x in md_list])/ (len(md_list)*100)
    total_percentage = round(total_percentage*100)  #turn it into an integer
    total_chart = progress_doughnut_chart(total_percentage)

    # format markdown into html
    html_contents = [markdown_to_html(md_pair[0]) for md_pair in md_list]
    percentages = [md_pair[1] for md_pair in md_list]
    #[print(html_page) for html_page in html_contents]
    return render_template('card_multiple_with_dashboard.html',
                           name='to-do list',
                           dashboard=dashboard(total_chart),
                           countdown_timer=countdown('2018/04/15'),
                           contents=zip(percentages, html_contents))


@app.route('/single-page/<query>')
def readme_card(query=None):
    #query = open(query).read()  #this opens the original readme.md file instead of the edited (parsed) version
    global file_tuples

    filepaths, edited_readme_file = zip(*file_tuples)
    #[print(snippet) for snippet in edited_readme_file]
    if query in filepaths:
        file_index = filepaths.index(query)
        print('found{0}!'.format(query))
        print('in index number: {0}'.format)
        html_content = markdown_to_html(edited_readme_file[file_index])
        return render_template('card_single.html', name=query, content=html_content)
        pass
    test_content = markdown_to_html(query)
    #test_content = ensure_images(test_content)
    #print(test_content)
    return render_template('card_single.html', name='test', content=test_content)

# @app.route('/images/<image_name>')
# def return_image_content(image_name):
#     return open('./images/{0}'.format(image_name))
#     #return open('./images/{0}'.format(image_name)).read()


@app.route('/', methods=['GET', 'POST'])
def homepage():
    filepath_query = request.args.get('filepath')
    print('filepath queried: ', filepath_query)
    if filepath_query:
        return readme_card(filepath_query)
    image_query = request.args.get('image')
    print('image queried: ', image_query)

    return todo()

if __name__ == '__main__':
    app.run()
