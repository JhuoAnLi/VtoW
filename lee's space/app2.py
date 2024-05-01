from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.json
        input_text = data.get("input", "")
        return egfunctions(input_text)
    return render_template("index2.html")


def egfunctions(input_text):
    outputarr = ["option 1", "option 2", "option 3"]
    return outputarr


if __name__ == "__main__":
    app.run(debug=True)
