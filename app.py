from flask import Flask, render_template, request, redirect, url_for, flash
import os
import rasterio
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
app.secret_key = "secret_key"
app.config["UPLOAD_FOLDER"] = "./uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files["file"]
        
        if file.filename == "" or not file.filename.lower().endswith(".tif"):
            flash("Please upload a valid TIF file")
            return redirect(request.url)
        
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        

        return redirect(url_for("process_file", filename=file.filename))
    
    return render_template("index.html")

@app.route("/process/<filename>")
def process_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    with rasterio.open(file_path) as dataset:
        band1 = dataset.read(1)
        
        metadata = {
            "Width": dataset.width,
            "Height": dataset.height,
            "Number of bands": dataset.count,
            "Data type": band1.dtype,
            "Coordinate Reference System": dataset.crs
        }
        
        plt.figure(figsize=(10, 6))
        plt.hist(band1.ravel(), bins=50, color="blue", alpha=0.7)
        plt.title("Histogram of Band 1 Pixel Values")
        plt.xlabel("Pixel Values")
        plt.ylabel("Frequency")
        
        histogram_path = os.path.join("static", "histogram.png")
        plt.savefig(histogram_path)
        plt.close()
        non_zero_mask = band1 > 0
        filtered_band1 = band1[non_zero_mask]

        non_zero_info = {
            "Total non-zero pixels": filtered_band1.size,
            "Sample non-zero values": filtered_band1[:10].tolist()
        }
        
    return render_template("result.html", metadata=metadata, histogram_path=histogram_path, non_zero_info=non_zero_info)

if __name__ == "__main__":
    app.run(debug=True)
