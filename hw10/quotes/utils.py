from pymongo import MongoClient

def get_mongodb():
    client = MongoClient("mongodb+srv://PSM:GoIThw8@cluster0.y0zbkd4.mongodb.net")
    db =client.Quotes
    return db


if __name__ == "__main__":
    db = get_mongodb()
    quotes = db.quotes.find()
    for quote in quotes:
        print(quote['quote'])
