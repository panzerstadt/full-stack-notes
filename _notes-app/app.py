import markdown
from flask import Flask
from flask import render_template, Markup
import os

app = Flask(__name__)
print('app initiated. name of app: {0}'.format(__name__))

readme_files = []
for paths in os.walk('../'):
    for path in paths[2]:
        if 'md' in path:
            readme_files.append([paths[0], path])
            print('filename: ', path)
            print('tuple: ', paths)

test = readme_files[0]
testdir = os.path.join(test[0], test[1])
testname = test[1]

print(open(testdir).read())

@app.route('/unformatted/')
def homepage_unformatted():
    md_content = Markup(markdown.markdown(open(testdir).read()))
    return render_template('index.html', name=testname, content=md_content)

@app.route('/')
def homepage():
    pass

if __name__ == '__main__':
    app.run(debug=True)