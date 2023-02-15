from google.cloud import firestore
import json
import os
import argparse

db = firestore.Client()

parser = argparse.ArgumentParser(description='Web dumper')
parser.add_argument('-o', '--operation',
                        type=str,
                        choices=['upload', 'download', 'none'],
                        default='none', required=True,
                        help='Choose a operation.')
parser.add_argument('-t', '--target',
                        type=str,
                        choices=['content', 'assets', 'none'],
                        default='none', required=True,
                        help='Choose a target.')

args = parser.parse_args()

if args.operation == "none" or args.target == "none":
  print("You must indicate an operation and a target")
  exit()

if args.operation == "download":
  if args.target == "content":
    print("Downloading content")
    print("-------------------")
    if not os.path.exists("content"): os.mkdir("content")
    collection = db.collections()
    for collection in collection:
      print(collection.id)
      if not os.path.exists("content/" + collection.id): os.mkdir("content/" + collection.id)
      for doc in collection.stream():
          print("--", doc.id)
          doc_file = open("content/" + collection.id + "/" + doc.id + ".json", 'w')
          doc_file.write(json.dumps(doc.to_dict()))
          doc_file.close()

elif args.operation == "upload":
  if args.target == "content":
    print("Uploading content")
    print("-----------------")
    for collection in os.listdir("content"):
      print(collection)
      # Upload resorce elements
      onlyfiles = [f for f in os.listdir("content/" + collection) if os.path.isfile(os.path.join("content/" + collection, f))]
      for element in onlyfiles:
          # Upload element
          filename = element.split(".")[0]
          print("--", filename)
          doc = db.collection(collection).document(filename)
          with open("content/" + collection + "/" + element, 'r') as f:
              doc.set(json.load(f))