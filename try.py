import sys
print(f"Python version: {sys.version}")
print(f"Current working directory: {sys.path[0]}")

try:
    import verb_pattern_analyzer
    print("Contents of verb_pattern_analyzer module:")
    print(dir(verb_pattern_analyzer))
    
    from verb_pattern_analyzer import analyze_paragraph
    print("Successfully imported analyze_paragraph")
except ImportError as e:
    print(f"Error importing from verb_pattern_analyzer: {e}")
    print("Contents of verb_pattern_analyzer.py:")
    with open('verb_pattern_analyzer.py', 'r') as f:
        print(f.read())
    sys.exit(1)

from flask import Flask, render_template, request
from verb_pattern_analyzer import analyze_paragraph

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def analyze():
    result = None
    paragraph = ''
    if request.method == 'POST':
        paragraph = request.form['paragraph']
        result = analyze_paragraph(paragraph)
    return render_template('try.html', result=result, paragraph=paragraph)

if __name__ == '__main__':
    app.run(debug=True)
