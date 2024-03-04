import requests

# API endpoint base URL'si
url = 'http://localhost:5000/assignment/query'

# Örnek filtre ve sıralama verileri
filters = {"main_symbol": "NALCN"}
ordering = [{"main_af_vcf": "DESC"}, {"main_dp": "ASC"}]

# Sayfa numarası ve sayfa boyutu
page = 2
page_size = 5

# İstek gövdesi
payload = {
    "filters": filters,
    "ordering": ordering,
    "page": page,
    "page_size": page_size
}

try:
    # JSON verisiyle birlikte isteği gönder
    response = requests.post(url, json=payload)

    # Yanıtı kontrol et
    if response.status_code == 200:
        # Başarılı bir yanıt alındıysa verileri yazdır
        data = response.json()
        print("Results:")
        for result in data['results']:
            print(result)
    else:
        # Hata durumunda durum kodunu ve hata mesajını yazdır
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    # Diğer hata durumlarında hatayı yazdır
    print(f"An error occurred: {str(e)}")
