import requests
import datetime
import pandas as pd
from matplotlib import pyplot
import csv
import pymysql

def get_weather(coordinates):
    url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=bd20ed06cd4805d0e5572bf3411cc927&units=metric'.format(coordinates[0], coordinates[1])
    try:
       res = requests.get(url)
       data = res.json()
    except Exception as e:
       print(e)  
       return None
    return data

def convert_date_format(date_str):
  date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
  return date_obj.strftime('%Y-%m-%d')

def main():
  # Nhập tọa độ từ máy
  latitude = input("Nhập vĩ độ: ")
  longitude = input("Nhập kinh độ: ")
  sovutainan = input("Nhập số vụ tai nạn: ")
  # Tạo mảng chứa tọa độ
  coordinates = [latitude, longitude]
  # Lấy dữ liệu thời tiết
  weather_data = get_weather(coordinates)
  if weather_data is None:
    return
  # Lấy thời gian hiện tại
  now = datetime.datetime.now()
  # In dữ liệu thời tiết
  print(f"Ngày: {now.strftime('%d/%m/%Y')}, {now.strftime('%H:%M:%S')}")
  print(f"số vụ tai nạn: {sovutainan}")
  print(f"Nhiệt độ: {weather_data['main']['temp']}°C")
  print(f"Gió: {weather_data['wind']['speed']} m/s")
  print(f"Áp suất: {weather_data['main']['pressure']} hPa")
  print(f"Độ ẩm: {weather_data['main']['humidity']}%")
  print(f"Mô tả: {weather_data['weather'][0]['description']}")

 # Tạo Pandas DataFrame từ dữ liệu thời tiết  
  df = pd.DataFrame({
  "ngày": now.strftime("%d/%m/%Y"),
  "giờ": now.strftime('%H:%M:%S'),
  "tainan":sovutainan,
  "nhiệt độ": weather_data['main']['temp'],
  "ngió": weather_data['wind']['speed'],
  "áp suất": weather_data['main']['pressure'],
  "độ ẩm": weather_data['main']['humidity'],
  "mô tả": weather_data['weather'][0]['description']
  }, index=[0])
  # Đổi định dạng ngày tháng trước khi insert vào bảng
  df = df.assign(ngày=df['ngày'].apply(convert_date_format))
  # Lưu DataFrame vào tệp CSV
  df.to_csv("weather_data.csv", mode="a", header=False, index=False)
  # Kết nối với MySQL
def connect():

  mydb = pymysql.connect(
      host="127.0.0.1",
      user="root",
      password="01215654221p",
      database="weather_data"
  )

  # Tạo bảng thời tiết
  mycursor = mydb.cursor()
  mycursor.execute("""CREATE TABLE IF NOT EXISTS weather_data (
      ngay DATE,
      gio TIME,
      tainan FLOAT,
      nhiet_do FLOAT,
      ngio FLOAT,
      ap_suat FLOAT,
      do_am FLOAT,
      mo_ta VARCHAR(255)
  )""")

  # Đọc dữ liệu thời tiết từ file CSV
  with open("weather_data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
      # Insert dữ liệu thời tiết vào bảng
    for row in reader:
          mycursor.execute("""INSERT INTO weather_data (ngay, gio, tainan, nhiet_do, ngio, ap_suat, do_am, mo_ta)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", row)    
  # Đóng kết nối với MySQL
  mydb.commit()
  mydb.close()
def dothi():
  # Đọc dữ liệu từ file CSV vào một DataFrame
  df = pd.read_csv("weather_data.csv")
  pyplot.plot(df['ngày'], df['nhiệt độ'], color = 'red', linestyle='-', marker='.')
  pyplot.plot(df['ngày'], df['ngió'], color = 'blue', linestyle='-', marker='.')
  pyplot.bar(df['ngày'], df['tainan'], color = 'green', linestyle='-')
  pyplot.plot(df['ngày'], df['độ ẩm'], color = 'yellow', linestyle='-', marker='.')  
  pyplot.xlabel("Day")
  pyplot.ylabel("Chỉ số thời tiết")
  pyplot.legend(["nhiệt độ","ngió","độ ẩm", "tainan"])
  pyplot.style.use('Solarize_Light2')
  pyplot.show()

if __name__ == "__main__":
   #main()
   #connect()
   dothi()