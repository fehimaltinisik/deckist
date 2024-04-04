import importlib.resources
import os.path
import re
from datetime import datetime
from datetime import timedelta
from io import BytesIO

import pandas as pd
from pandas import DataFrame

from src.config.csvfiles import GTFS_DATA_CSV_FILE_READ_OPTIONS
from src.config.csvfiles import GTFS_DATA_ENCODING
from src.config.csvfiles import GTFS_RESOURCE_PATH
from src.config.logging import configure_logger

TIME_FORMATS_REGEX_MATCHER = r'(\d{2}):(\d{2}):(\d{2})'
BROKEN_TIME_FORMATS_REGEX_MATCHER = r'((?<!2[0-3])\d{2}):(\d{2}):(\d{2})'

DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
WEBSERVICE_PROJECT_ROOT_PATH: str = os.path.join(DIR_PATH, '..')

ROUTES_CSV_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, 'routes.csv').__str__()
TRIPS_CSV_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, 'trips.csv').__str__()
STOPS_CSV_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, 'stops.csv').__str__()
STOP_TIMES_CSV_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, 'stop_times.csv').__str__()


def is_timestamp_broken(time_str):
    return re.match(BROKEN_TIME_FORMATS_REGEX_MATCHER, time_str)


def fix_broken_timestamp(time_str):
    if pd.isna(time_str):
        return time_str

    match = re.match(TIME_FORMATS_REGEX_MATCHER, time_str)

    if not match:
        return time_str

    today: datetime = datetime.today()
    hours, minutes, seconds = map(int, match.groups())
    is_next_day: bool = True if hours >= 24 else False
    correct_hour: int = hours % 24 if is_next_day else hours
    correct_day: int = (today + timedelta(days=1)).day if is_next_day else today.day

    time = datetime(
        year=today.year,
        month=today.month,
        day=correct_day,
        hour=correct_hour,
        minute=minutes,
        second=seconds
    )

    return time


def preprocess_routes():
    with open(ROUTES_CSV_PATH, 'r', encoding=GTFS_DATA_ENCODING) as csv_file:
        stops_data = csv_file.readlines()
        stops_data[66 - 1] = '68,1,11D,KURAN KURSU - GÜNEY CAMİİ,3,HATTIMIZ ÜMRANİYE METRODAN RİNG OLARAK HİZMET VERMEKTEDİR.,11D_G_D0\n'
        stops_data[93 - 1] = '95,1,11H,TAŞOCAKLARI CAMİİ - TEPEÜSTÜ,3,SEFERLER TAŞOCAKLARIDAN KALKAR Y.MAHALLE GÜZERGAHI İLE GİDER.,11H_G_D2189\n'
        stops_data[102 - 1] = '104,1,11K,KAZIM KARABEKİR - ÜMRANİYE METRO,3,HATTIMIZ ÜMRANİYE METRODAN RİNG OLARAK HİZMET VERMEKTEDİR.,11K_G_D0\n'
        stops_data[110 - 1] = '113,1,11M,EVTAŞ BLOKLARI - SEREN SOKAK,3,HATTIMIZ BULGURLU METRODAN RİNG OLARAK HİZMET VERMEKTEDİR.,11M_G_D0\n'
        stops_data[132 - 1] = '141,1,11ST,DUMLUPINAR - ÜMRANİYE METRO,3,HATTIMIZ ÜMRANİYE METRODAN RİNG OLARAK HİZMET VERMEKTEDİR.,11ST_G_D0\n'
        stops_data[175 - 1] = '185,1,12,KADIKÖY - ÜSKÜDAR MARMARAY,3,ARAÇLARIMIZ İŞ CUMARTESİ VE PAZAR GÜNLERİNDE ÜSKÜDAR MARMARAYDAN RİNG,12_G_D2992\n'
        stops_data[201 - 1] = '216,1,121BS,SULTANİYE - SULTANİYE,3,SAAT UYGULAMASI BULUNMAYAN ZAMAN DİLİMİNDE MECİDİYEKÖY MEZARLIKA GİRMEZ MECİDİYEKÖY VİYADÜKTEN YOLCU ALARAK DEVAM EDER.,121BS_G_D2617\n'
        stops_data[373 - 1] = '422,1,132K,KARTAL - SULTANBEYLİ PERONLAR,3,HAFTASONU DÖNÜŞ İSTİKAMETİNDE VİAPORT İŞ MERKEZİNE GİRMEZ REYHAN CAD. GÜZERGAHINI KULLANIR.,132K_D_D1760\n'
        stops_data[397 - 1] = '448,1,132T,KARTAL METRO - AKFIRAT,3,SEFERLER AKFIRATTAN ORHANLI TOKİ KONUTLARINA DA GİRER.,132T_D_D1416\n'
        stops_data[404 - 1] = '455,1,132T,AKFIRAT - KARTAL METRO,3,SEFERLER AKFIRATTAN ORHANLI TOKİ KONUTLARINA DA GİRER.,132T_G_D1415\n'
        stops_data[436 - 1] = '501,1,133G,KARTAL - GÜLENSU MAHALLESİ,3,KIŞLALI CADDESINE PAZARTESI GÜNLERI KURULAN SEMT PAZARI NEDENIYLE ARAÇLARIMIZ GÜLENSU MAHALLESİ YÖNÜNDE MALTEPE KIZ ANADOLU İMAM HATIP LISESI DURAĞINDAN SONRA ORHANGAZI CADDESI  D100 KARAYOLU GÜZERGÂHI ILE HIZMET VERECEKTIR,133G_D_D0\n'
        stops_data[873 - 1] = '1018,1,15F,KADIKÖY - TÜRK ALMAN ÜNİVERSİTESİ,3,SEFERLER ÜSKÜDAR GÜZERGAHINDAN GİDER GECE SAAT 00:30-05:30 ARASI BİNİŞLER ÇİFT BİLETLİDİR.,15F_D_D1117\n'
        stops_data[877 - 1] = '1022,1,15F,ŞAHİNKAYA GARAJI - KADIKÖY,3,SEFERLER ÜSKÜDAR GÜZERGAHINDAN GİDER GECE SAAT 00:30-05:30 ARASI BİNİŞLER ÇİFT BİLETLİDİR.,15F_G_D1118\n'
        stops_data[2696 - 1] = '3715,1,9A,HALİLURRAHMAN CAMİİ - ÜMRANİYE METRO,3,HATTIMIZ ÜMRANİYE METRODAN RİNG OLARAK HİZMET VERMEKTEDİR.,9A_G_D0\n'
        stops_data[2967 - 1] = '4046,1,KM43,MESLEK YÜKSEKOKULU - MARMARA EĞİTİM KÖYÜ,3,SABAH SEFERLERİ ANA GÜZERGAHI İLE MALTEPEYE GİDER MALTEPE DEN EKSPRES OLARAK EĞİTİM KÖYÜNE DÖNER.,KM43_G_D2081\n'
        stops_data[2968 - 1] = ''
        stops_data[4298 - 1] = '24448,1,19T,ATATÜRK BULVARI - ATATÜRK BULVARI,3,ARAÇLARIMIZ İŞ CUMARTESİ PAZAR GÜNLERİ 10:00 SAATİNE KADAR KADIKÖYDEN RİNG.,19T_G_D6394\n'
        stops_data[4804 - 1] = '25186,1,HT11,GİYİMKENT - KUYUMCUKENT,3,42 EVLER ATATÜRK CD. VE FATİH CD. DURAKLARINDAN GEÇMEZ.,HT11_G_D6942\n'
        stops_data[4805 - 1] = '25187,1,33Y,GİYİMKENT - EMİNÖNÜ,3,42 EVLER ATATÜRK CD. VE FATİH CD. DURAKLARINDAN GEÇMEZ.,33Y_G_D6943\n'
        stops_data[5245 - 1] = '52554,1,139T,TEPE ÜSTÜ - TEDAŞ ÖNÜ,3,YEŞİLVADİ SATMAZLI AHMETLİ GÜZERGAHINDAN.,139T_G_D1860\n'
        stops_data[5246 - 1] = '52555,1,139T,TEDAŞ ÖNÜ - TEPE ÜSTÜ,3,YEŞİLVADİ SATMAZLI AHMETLİ GÜZERGAHINDAN.,139T_D_D1861\n'
        stops_data[5551 - 1] = '53424,1,15ÇK,SAĞLIK OCAĞI - KADIKÖY,3,PAZAR GÜNÜ KURULAN SEMT PAZARINDAN DOLAYI ARAÇLARIMIZ SAĞLIK OCAĞI DURAĞINDAN BAŞLAR.,15ÇK_G_D2797\n'
        stops_data[5993 - 1] = '53959,1,KM43,MESLEK YÜKSEKOKULU - MARMARA EĞİTİM KÖYÜ,3,AKŞAM SEFERLERİ EĞİTİM KÖYÜNDEN EKSPRES OLARAK MALTEPEYE GİDER DÖNÜŞTE ANA GÜZERGAHI İLE DÖNER.,KM43_G_D3457\n'
        stops_data[6297 - 1] = '54378,1,11CÜ,HATTAT HASAN ÇELEBİ CADDESİ - MİLLET BAHÇESİ,3,SEFERLER DÖNÜŞ YÖNÜNDE KISIKLI DURAĞINDAN SONRA NURBABA SOKAK GÜZERGAHINDA DEVAM ETMEKTEDİR.,11CÜ_G_D2211\n'
        stops_data[6652 - 1] = '54815,1,KM28,MUSTAFA KARUŞAĞI İLKOKULU - OKAN ÜNİVERSİTESİ,3,SEFERLER KURTKÖY METRO İSTASYONU İLE OKAN ÜNİVERSİTESİ ARASINDA ANKARA CADDESİ GÜZERGAHINI KULLANIR.,KM28_D_D4115\n'
        stops_data[6830 - 1] = '55032,1,AVR1,YENİBOSNA METRO - 15 TEMMUZ ŞEHİTLERİ ANADOLU İMAM HATİP LİSESİ,3,YENİBOSNA METRO 15 TEMMUZ A.İ.H.L - FATİH CAD. GÜZERGAHINDA HİZMET VERİR.,AVR1_D_D4302\n'
        stops_data[7364 - 1] = '55609,1,11H,ŞEHİT MURAT AKDEMİR - TEPEÜSTÜ,3,SEFER ŞEHİT MURAT AKDEMİR DURAĞINDAN BAŞLAR YENİ MAHALLE GÜZERGAHINDAN GİDER.,11H_G_D4376\n'
        stops_data[7365 - 1] = '55610,1,11H,ŞEHİT MURAT AKDEMİR - TEPEÜSTÜ,3,SEFER ŞEHİT MURAT AKDEMİR DURAĞINDAN BAŞLAR HEKİMBAŞI GÜZERGAHINDAN GİDER."",11H_G_D4377\n'
        stops_data[7367 - 1] = '55612,1,121B,YENİ CAMİİ - MECİDİYEKÖY VİYADÜK,3,06:50 SEFERİ GİDİŞ YÖNÜNDE YENİ CAMİİ DURAĞINDAN BAŞLAR 17:00 SEFERİ İSE DÖNÜŞTE YENİ CAMİİ DURAĞINA KADAR HİZMET VERİR.,121B_G_D4380\n'
        stops_data[7368 - 1] = '55613,1,121B,KAVACIK AKTARMA - MECİDİYEKÖY VİYADÜK,3,06:50 SEFERİ GİDİŞ YÖNÜNDE YENİ CAMİİ DURAĞINDAN BAŞLAR 17:00 SEFERİ İSE DÖNÜŞTE YENİ CAMİİ DURAĞINA KADAR HİZMET VERİR.,121B_G_D4381\n'

    data = ''.join(stops_data).encode(GTFS_DATA_ENCODING)
    buffer = BytesIO()
    buffer.write(bytearray(data))
    buffer.seek(0)

    stops: DataFrame = pd.read_csv(buffer, **GTFS_DATA_CSV_FILE_READ_OPTIONS)
    stops.to_csv(os.path.join(WEBSERVICE_PROJECT_ROOT_PATH, *GTFS_RESOURCE_PATH.split('.'), 'routes.clean.csv'), index=False, encoding=GTFS_DATA_ENCODING)


def preprocess_trips():
    trips: DataFrame = pd.read_csv(TRIPS_CSV_PATH, **GTFS_DATA_CSV_FILE_READ_OPTIONS)
    trips.to_csv(os.path.join(WEBSERVICE_PROJECT_ROOT_PATH, *GTFS_RESOURCE_PATH.split('.'), 'trips.clean.csv'), index=False, encoding=GTFS_DATA_ENCODING)


def preprocess_stops():
    with open(STOPS_CSV_PATH, 'r', encoding=GTFS_DATA_ENCODING) as csv_file:
        stops_data = csv_file.readlines()
        stops_data[7239 - 1] = '5252106,188081,HAMAM ÇEŞME CADDESİ,direction: GİDİŞ,41.1967699991065,28.3342789998908,0\n'
        stops_data[2726 - 1] = '293931,115782,YEŞİLTEPE,direction: Y TEPESON DURAK,41.1210750085358,29.0004309863058,0\n'
        stops_data[3723 - 1] = '292084,121453,EYÜPSULTAN,direction: GOP DEMİRKAPI,41.0459989732968,28.9335930493867,0\n'
        stops_data[4456 - 1] = '799932,125692,MAHMUTBEY,direction: B.KÖY-H BOSTAN,41.0553130011521,28.8283619974608,0\n'
        stops_data[4638 - 1] = '579151,126752,MAHMUTBEY İLKOKULU,direction: B KÖY-H BOSTAN,41.0558690287277,28.8256099897759,0\n'
        stops_data[7564 - 1] = '292708,201632,ŞİRİNDERE KÖPRÜSÜ,direction: M ŞEVKET PAŞA,41.1469499835828,29.1691470436733,0\n'

    data = ''.join(stops_data).encode(GTFS_DATA_ENCODING)
    buffer = BytesIO()
    buffer.write(bytearray(data))
    buffer.seek(0)

    stops: DataFrame = pd.read_csv(buffer, **GTFS_DATA_CSV_FILE_READ_OPTIONS)
    stops.to_csv(os.path.join(WEBSERVICE_PROJECT_ROOT_PATH, *GTFS_RESOURCE_PATH.split('.'), 'stops.clean.csv'), index=False, encoding=GTFS_DATA_ENCODING)


def preprocess_stop_times():
    # 192763
    stop_times: DataFrame = pd.read_csv(
        STOP_TIMES_CSV_PATH,
        dtype={
            'trip_id': 'Int32',
            'stop_id': 'Int32',
            'stop_sequence': 'Int16'
        },
        **GTFS_DATA_CSV_FILE_READ_OPTIONS
    )
    # stop_times.drop(columns=['timepoint'], inplace=True)
    stop_times['arrival_time'] = stop_times['arrival_time'].apply(fix_broken_timestamp)
    stop_times['departure_time'] = stop_times['departure_time'].apply(fix_broken_timestamp)
    stop_times.to_csv(os.path.join(WEBSERVICE_PROJECT_ROOT_PATH, *GTFS_RESOURCE_PATH.split('.'), 'stop_times.clean.csv'), index=False, encoding=GTFS_DATA_ENCODING)


def main():
    configure_logger()
    preprocess_routes()
    preprocess_trips()
    preprocess_stops()
    preprocess_stop_times()


if __name__ == '__main__':
    main()
