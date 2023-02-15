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

args = parser.parse_args()

if args.operation == "download":
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