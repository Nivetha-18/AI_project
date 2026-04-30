from flask import Flask, request, jsonify, render_template
from model import detect_ai_text, plagiarism_score, get_matches
from utils import extract_text_from_file

app = Flask(__name__)

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/text')
def text_page():
    return render_template('text.html')

@app.route('/plagiarism')
def plagiarism_page():
    return render_template('plagiarism.html')

# ---------------- AI DETECTION ----------------

@app.route('/detect-ai', methods=['POST'])
def detect_ai():
    data = request.get_json()
    text = data.get("text", "")

    result = detect_ai_text(text)
    return jsonify(result)

# ---------------- PLAGIARISM ----------------

@app.route('/plagiarism-check', methods=['POST'])
def plagiarism_check():

    text1 = ""
    text2 = ""

    # FILE INPUT
    if 'file1' in request.files and 'file2' in request.files:
        file1 = request.files['file1']
        file2 = request.files['file2']

        text1 = extract_text_from_file(file1)
        text2 = extract_text_from_file(file2)

    # TEXT INPUT
    else:
        text1 = request.form.get("text1", "")
        text2 = request.form.get("text2", "")

    if not text1.strip() or not text2.strip():
        return jsonify({"percentage": 0, "matches": []})

    score = plagiarism_score(text1, text2)
    matches = get_matches(text1, text2)

    return jsonify({
        "percentage": score,
        "matches": matches
    })

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)