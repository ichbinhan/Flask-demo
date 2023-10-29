from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)
# 資料是寫死固定的，可寫在全域端
books = {1: "Python book", 2: "Java book", 3: "Flask book"}


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

    return render_template(
        "books.html",
        books=books,
    )
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


##邏輯引用不重複出現
if __name__ == "__main__":
    app.run(debug=True)
