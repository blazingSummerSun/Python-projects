from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import json
import csv

# url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
headers = {
    "Accept": "*/*",
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
# req = requests.get(url, headers=headers)
# src = req.text

# with open("index.html", encoding="utf-8") as file:
#     src = file.read()
# soup = BeautifulSoup(src, "lxml")
# allProductsHref = soup.find_all(class_="mzr-tc-group-item-href")
# allCategoriesDict = {}
# for item in allProductsHref:
#     itemText = item.text
#     itemHref = "https://health-diet.ru" + item.get("href")
#     allCategoriesDict[itemText] = itemHref
# with open("all_categories_dict.json", "w", encoding="utf-8") as file:
#     json.dump(allCategoriesDict, file, indent=4, ensure_ascii=False)

with open("all_categories_dict.json", encoding="utf-8") as file:
    allCategories = json.load(file)

iterationCount = int(len(allCategories)) - 1
count = 0
for categoryName, categoryHref in allCategories.items():
    signs = [',', ' ', '-', "'"]
    for item in signs:
        if item in categoryName:
            categoryName = categoryName.replace(item, "_")
    req = requests.get(url=categoryHref, headers=headers)
    src = req.text
    with open(f"data/{count}_{categoryName}.html", 'w', encoding="utf-8") as file:
        file.write(src)
    with open(f"data/{count}_{categoryName}.html", encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    # checking if page existing
    alertBlock = soup.find(class_="uk-alert-danger")
    if (alertBlock is not None):
        continue

    # collect table heads
    tableHead = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    product = tableHead[0].text
    calories = tableHead[1].text
    proteins = tableHead[2].text
    fats = tableHead[3].text
    carbohydrates = tableHead[4].text
    with open(f"data/{count}_{categoryName}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    # collecting products data
    productsData = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

    productInfo = []
    for item in productsData:
        productsTDS = item.find_all("td")

        title = productsTDS[0].find("a").text
        calories = productsTDS[1].text
        proteins = productsTDS[2].text
        fats = productsTDS[3].text
        carbohydrates = productsTDS[4].text
        productInfo.append(
            {
                "Titile": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates
            }
        )
        with open(f"data/{count}_{categoryName}.json", "a", encoding="utf-8") as file:
            json.dump(productInfo, file, indent=4, ensure_ascii=False)

        with open(f"data/{count}_{categoryName}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )
    count += 1
