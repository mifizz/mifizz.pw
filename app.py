from flask import Flask, render_template, request, jsonify
import kitis_api as kapi

app = Flask(__name__, static_folder="static", template_folder="templates")
kapi.init_api()

@app.route("/")
def p_index():
    return render_template("index.html")

@app.route("/<page>/")
@app.route("/<page>")
def serve_page(page):
    page = page.lower()
    if page == "404":
        return render_template("404.html"), 404
    try:
        return render_template(f"{page}.html"), 200
    except:
        return render_template("404.html"), 404

@app.route("/kitis/api/", methods=["POST"])
@app.route("/kitis/api", methods=["POST"])
def json_kitis_api():
    post_data = request.get_json()
    if not post_data or not "source_type" in post_data or not "source" in post_data:
        return "Bad request: must provide correct json!", 400

    source_type = post_data["source_type"]
    source      = post_data["source"]

    try:
        r = kapi.get_schedule(source_type, source)
    except Exception as e:
        if isinstance(e, KeyError):
            if "_" in f"{e}":
                return f"KeyError: {e} - Invalid source_type!", 400
            else:
                return f"KeyError: {e} - Invalid source!", 400
        else:
            return f"Error: {e}", 400
    
    return jsonify(r)

if __name__ == "__main__":
    app.run()