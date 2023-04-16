import pymongo

MONGO_HOST="localhost"
MONGO_PORT="27017"
MONGO_TIMEOUT=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PORT+"/"

MONGO_DB="escuela"
MONGO_COLECTION="alumnos"

try:
    client=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIMEOUT)
    client.server_info()
    print("Connected to DB")

    dataBase=client[MONGO_DB]
    colection=dataBase[MONGO_COLECTION]
    for document in colection.find():
        print(document["nombre"])

    client.close()
except pymongo.errors.ServerSelectionTimeoutError as timeoutError:
    print("Timeout error "+timeoutError)
except  pymongo.errors.ConnectionFailure as connectionFailure:
    print("Connection failure "+connectionFailure)