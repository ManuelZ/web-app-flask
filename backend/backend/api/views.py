# Built-in imports
from pathlib import Path

# External imports
from flask import request
from flask import make_response
from flask import Response
from flask import jsonify
from flask import current_app
import sqlalchemy as sa

# Local imports
from backend.extensions import db
from backend.api import bp
from backend.models import File


@bp.route("/files", methods=["GET"])
def list_files():

    try:
        limit = int(request.args.get("limit", 20))
        limit = limit if ((limit > 0) and (limit < 1e6)) else 20

        offset = int(request.args.get("offset", 0))
        offset = offset if (offset >= 0 and offset < 1e6) else 0

        filesize_low = int(request.args.get("lower_filesize_limit", 0))
        filesize_high = int(request.args.get("upper_filesize_limit", 1e6))

        filetypes = request.args.get("filetypes", "")
        if filetypes != "":
            filetypes_filter = [f"{f.lower()}" for f in filetypes.split(",")]
        else:
            filetypes_filter = []

        # The percent sign % wildcard matches any sequence of zero or more characters
        filename_filter = request.args.get("filename", "%")
        filename_filter = f"%{filename_filter}%"

    except Exception as e:
        msg = f"Trouble when parsing the given arguments:\n{e}"
        print(msg)
        return jsonify({"msg": msg})

    data = []
    msg = ""
    try:
        query = (
            sa.select(File)
            .where(File.filetype.in_(filetypes_filter))
            .where(File.filename.like(filename_filter))
            .where(File.filesize.between(filesize_low, filesize_high))
            .limit(limit)
            .offset(offset)
        )

        files = db.session.scalars(query).all()
        data = [f.to_dict() for f in files]
        msg = "Success"

    except Exception as e:
        msg = f"Error in SELECT operation: {e}"
        print(msg)
        data = ""

    finally:
        return jsonify({"msg": msg, "data": data})


@bp.route("/index", methods=["POST"])
def create_index():
    base_directory = Path(current_app.config["TEST_DATA_PATH"])

    files = []
    for child in base_directory.glob("**/*.*"):
        if child.is_file():
            filename = child.name
            filesize = int(child.stat().st_size)
            filetype = child.suffix.lstrip(".").lower()
            absolute_path = str(child.absolute())

            files.append(
                {
                    "path": absolute_path,
                    "filename": filename,
                    "filesize": filesize,
                    "filetype": filetype,
                }
            )

    try:
        db.session.execute(sa.insert(File), files)
        db.session.commit()
        return make_response(jsonify({"total_files": len(files)}), 200)

    except Exception as e:
        print(f"Error serializing the index: {str(e)}")
        return Response(status=500)
