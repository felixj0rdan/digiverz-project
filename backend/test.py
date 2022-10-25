# from flask import Flask, render_template
# from flask_wtf import FlaskForm
# from wtforms import FileField, SubmitField
# from werkzeug.utils import secure_filename
# import os
# from wtforms.validators import InputRequired

# app = Flask(__name__)
# app.config["SECRET_KEY"] = "supersecretkey"
# app.config["UPLOAD_FOLDER"] = "assets"


# class UploadFileForm(FlaskForm):
#     file = FileField("File", validators=[InputRequired()])
#     submit = SubmitField("Upload File")


# @app.route("/", methods=["GET", "POST"])
# @app.route("/home", methods=["GET", "POST"])
# def home():
#     form = UploadFileForm()
#     if form.validate_on_submit():
#         file = form.file.data  # First grab the file
#         file.save(
#             os.path.join(
#                 os.path.abspath(os.path.dirname(_file_)),
#                 app.config["UPLOAD_FOLDER"],
#                 secure_filename(file.filename),
#             )
#         )  # Then save the file
#         return "File has been uploaded."
#     return render_template("index.html", form=form)


# if __name__ == "__main__":
#     app.run(debug=True)
import pandas as pd
from datetime import date, timedelta, datetime

months = 3


start_date = date.today()
print(start_date)

count = 10


pred_df = pd.DataFrame(
    {
        "Date": [
            single_date
            for single_date in (start_date + timedelta(n) for n in range(count))
        ]
    }
)
print(pred_df)
pred_df["Date"] = pd.to_datetime(pred_df["Date"])
pred_df.sort_values(by="Date", inplace=True)
pred_df = pred_df.groupby(pd.Grouper(key="Date", freq="1D")).sum()

print(pred_df.head())
