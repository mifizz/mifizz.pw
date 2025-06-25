from flask import Flask, render_template, request, json, Response, send_from_directory
import kitis_api as kapi

app = Flask(__name__, static_folder="static", template_folder="templates")
kapi.init_api()

@app.route("/")
def p_index():
    return render_template("index.html")

@app.route("/kitis/testdump/<path:filename>")
def serve_kitis_testdump(filename):
    return send_from_directory("kitis/testdump", filename)

@app.errorhandler(404)
def page_not_found(e):
    # Extract the path from the request
    path = request.path.strip("/").lower()
    try:
        if path == "404":
            return render_template("404.html"), 404
        return render_template(f"{path}.html"), 200
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
    json_r = json.dumps(r, ensure_ascii=False)
    return Response(json_r, content_type="application/json; charset=utf-8")

if __name__ == "__main__":
    app.run(debug=True)
