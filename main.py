from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd

app = Flask(__name__)
# 資料是寫死固定的，可寫在全域端
books = {1: "Python book", 2: "Java book", 3: "Flask book"}
ascending = True


# 首頁
@app.route("/")
@app.route("/index")
def index():
    today = datetime.now()
    print(today)
    # 傳遞資料至靜態網頁(template的index)
    return render_template("index.html", today=today)
    # return f"<h1>Hello world!{today}</h1>"


# 書的首頁
@app.route("/books")
def get_all_books():
    today = datetime.now()
    books = {
        1: {
            "name": "Python book",
            "price": 299,
            "image_url": "https://im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/CN1/136/11/CN11361197.jpg&v=58096f9ck&w=348&h=348",
        },
        2: {
            "name": "Java book",
            "price": 399,
            "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/087/31/0010873110.jpg&v=5f7c475bk&w=348&h=348",
        },
        3: {
            "name": "C# book",
            "price": 499,
            "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/036/04/0010360466.jpg&v=62d695bak&w=348&h=348",
        },
    }
    for id in books:
        print(id, books[id]["name"], books[id]["price"], books[id]["image_url"])

    # return render_template("books.html", **locals())
    return render_template("books.html", books=books, today=today)
    # return books


# 書的分頁
@app.route("/books/id=<int:id>", methods=["GET"])
def get_books(id):
    try:
        return f"<h2>{books[id]}</h2>"
    except Exception as e:
        print(e)
    return "<h1>書籍編號錯誤!</h1>"


@app.route("/bmi/name=<n>&weight=<w>&height=<h>")
def get_bmi(n, w, h):
    bmi = round(eval(w) / (eval(h) / 100) ** 2, 2)
    return {"name": n, "weight": w, "height": h, "bmi": bmi}


@app.route("/pm25", methods=["GET", "POST"])
def get_pm25():
    global ascending
    url = "https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sort = False
    if request.method == "POST":
        print(request.form)
        if request.form.get("sort"):
            sort = True
    try:
        df = pd.read_csv(url).dropna()
        # 製作升降序功能
        if sort:
            df = df.sort_values("pm25", ascending=ascending)
            ascending = not ascending
        else:
            # 回復原本狀態
            ascending = True

        columns = df.columns.tolist()
        values = df.values.tolist()
        # 取出 values的最高與最低值
        lowest = df.sort_values("pm25").iloc[0][["site", "pm25"]].values
        highest = df.sort_values("pm25").iloc[-1][["site", "pm25"]].values

        message = "取得資料成功"

    except Exception as e:
        print(e)
        message = "取得資料失敗，請稍後再試"

    return render_template("pm25.html", **locals())


##邏輯引用不重複出現
if __name__ == "__main__":
    app.run(debug=True)
