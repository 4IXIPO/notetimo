import csv
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# Определение заголовков CSV
FIELDNAMES = [
    "part_number",  # Артикул
    "name",         # Наименование
    "field3",
    "field4",
    "field5",
    "field6",
    "field7",
    "field8",
    "price",
    "brand",
    "field11"
]

# Читаем CSV в память
def read_csv(filename="C:/Users/opilane/Desktop/htmlcss-main/panda2/LE.txt"):
    spare_parts = []
    with open(filename, "r", encoding="latin-1") as file:
        reader = csv.DictReader(file, fieldnames=FIELDNAMES, delimiter="\t", skipinitialspace=True)
        for row in reader:
            row["name"] = row["name"].strip()  # Убираем лишние пробелы
            row["price"] = float(row["price"].replace(",", ".")) if row["price"].replace(",", "").isdigit() else 0.0
            spare_parts.append(row)
    return spare_parts


# Загружаем данные при старте сервера
spare_parts_data = read_csv()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode())

    def _filter_data(self, params):
        filtered_data = spare_parts_data

        # Фильтр по имени
        if "name" in params:
            name = params["name"][0].lower()
            filtered_data = [part for part in filtered_data if name in part["name"].lower()]

        # Фильтр по артикулу
        if "sn" in params:
            serial_number = params["sn"][0]
            filtered_data = [part for part in filtered_data if part["part_number"] == serial_number]

        return filtered_data

    def _paginate_data(self, data, params):
        # Страница по умолчанию — 1, на странице 30 элементов
        page = int(params.get("page", [1])[0])
        per_page = 30
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        return data[start_index:end_index]

    def _sort_data(self, data, params):
        if "sort" in params:
            sort_by = params["sort"][0]
            reverse = False
            if sort_by.startswith("-"):
                reverse = True
                sort_by = sort_by[1:]

            if sort_by in FIELDNAMES:
                data = sorted(data, key=lambda x: x.get(sort_by, ""), reverse=reverse)

        return data

    def do_GET(self):
        url_components = urlparse(self.path)
        params = parse_qs(url_components.query)

        # Фильтрация
        filtered_data = self._filter_data(params)

        # Сортировка
        sorted_data = self._sort_data(filtered_data, params)

        # Пагинация
        paginated_data = self._paginate_data(sorted_data, params)

        self._send_json(paginated_data)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Allow", "GET, OPTIONS")
        self.end_headers()


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
