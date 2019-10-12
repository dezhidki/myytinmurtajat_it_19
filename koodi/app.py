from flask import Flask, render_template, jsonify
import time
import binascii

app = Flask(__name__)

current_password = "TEST1"

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def group_bits(text):
    return " ".join(text[i:i + 4] for i in range(0, len(text), 4))


def solution():
    return "Solution"

@app.route("/api/verify/<string:code>")
def check_solution(code):
    if code != current_password:
        return jsonify({
            "success": false,
            "redirect": None
        })    


@app.route("/")
def index():
    first_letter = group_bits(text_to_bits(current_password[0]))
    second_letter = group_bits(text_to_bits(current_password[1]))
    return render_template("koodi_main.html", first_letter=first_letter, second_letter=second_letter)