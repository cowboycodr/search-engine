import json

def search(query, index_data):
    query = query.lower().split()
    results = []

    for index in index_data:
        keywords = index["keywords"]
        title = index["title"]
        url = index["url"]

        for word in query:
            if word in keywords:
                results.append(f"{title} - {url}")

                break

    return results

with open("data.json", "r") as file:
    index_data = json.loads(file.read())

while True:
    results = search(input("Search >>> "), index_data)

    for idx, result in enumerate(results):
        print(f"{idx + 1}. {result}")