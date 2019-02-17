from flask import Flask, render_template, request, redirect, url_for
from detect_face import detect_face
from stat import S_ISREG, ST_CTIME, ST_MODE
from uuid import uuid1
from pixels import Pixels
from random import randint
import time
from PIL import Image
<<<<<<< HEAD
from os import remove
from coolname import generate_slug, RandomGenerator
=======
import os
>>>>>>> 1434f47ba110c6b7d3c4f3028f0b8ed3a4209119

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MAX_WIDTH = 400
MAX_HEIGHT = 400
MAX_FILES = 256



# kanyeGenerator = RandomGenerator(

# )


@app.route("/", methods=["GET", "POST"])
@app.route("/<id>", methods=["GET", "POST"])
def main(id=None):
    if request.method == "POST":
        file = request.files["file"]
        if file:
            id = str(uuid1())
            id = generate_slug(2)
            upload_path = "static/done/"
            temp_path = "img/"
            temp_file_path = temp_path + id + file.filename
            orig_file_path = upload_path + "orig_" + id + ".png"
            done_file_path = upload_path + id + ".png"

        entries = (os.path.join(upload_path, fn) for fn in os.listdir(upload_path))
        entries = ((os.stat(path), path) for path in entries)
        entries = (
            (stat[ST_CTIME], path) for stat, path in entries if S_ISREG(stat[ST_MODE])
        )
        sorted_entries = sorted(entries)
        print(MAX_FILES)
        print(len(sorted_entries))

        if len(sorted_entries) > MAX_FILES:
            for i in range(0, len(sorted_entries) - MAX_FILES):
                path = sorted_entries[i][1]
                if "example" not in path:
                    os.remove(path)

        file.save(temp_file_path)

        img = Image.open(temp_file_path)

        if img.width > MAX_WIDTH:
            ratio = img.width / MAX_WIDTH
            img = img.resize((int(img.width / ratio), int(img.height / ratio)))
        elif img.height > MAX_HEIGHT:
            ratio = img.height / MAX_HEIGHT
            img = img.resize((int(img.width / ratio), int(img.height / ratio)))

        img.save(orig_file_path)

        os.remove(temp_file_path)

        faces = detect_face(orig_file_path)

        if len(faces) > 0:
            pixels = Pixels(img, faces)
            # pixels.markFacesLandmarks()
            kanye = pixels.faceSwap(), faces
            img.putdata(pixels.data)

        img.save(done_file_path)

        return redirect("/" + id)
    else:
        if not id:
            id = "example" + str(randint(1, 2))
        return render_template("main.html", id=id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
