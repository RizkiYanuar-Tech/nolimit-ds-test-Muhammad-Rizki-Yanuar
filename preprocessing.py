"""
Library yang digunakan hanya library regex dan pandas untuk lakukan preprocessing
"""
import re
import pandas as pd

def remove_emoji(text):
    """
    Fungsi ini digunakan untuk menghapus emoji dam simbol kode Unicode yang ada di dalam text

    Args:
        text: Input dari kolom teks yang akan dibersikan

    Returns:
        str: String yang sudah bersih dari emoji dan simbol kode Unicode
    """
    emoji_pattern = re.compile("["
                                "\U0001F600-\U0001F64F" # Emoji
                                "\U0001F300-\U0001F5FF" # Simbol
                                "]+",
                                flags=re.UNICODE
                                )
    return emoji_pattern.sub(r'', str(text))

def load_slang_dict():
    """
    Fungsi ini mengembalikan kamus yang berisikan kata slang dan kata baku.

    Kamus ini mencakup:
    - Singkatan
    - Typo
    - Simbol
     - Karakter emoticon

    Args:
        None

    Returns:
        dict: Kamus slang custom yang berisi kata slang dan kata baku.
    """
    # Kamus slang custom
    kamus_baku = {
        # Kalimat
        "dgn": "dengan", "blum": "belum", "blm": "belum", "ndak": "tidak", "tsk": "tidak",
        "tdk": "tidak", "wrn": "warna", "krg": "kurang", "brg": "barang", "mantab": "mantap",
        "sy": "saya", "dscrbs": "deskripsi", "describe":" deskripsi", "hny": "hanya","sdh": "sudah",
        "dr": "dari", "bgmn":"bagaimana", "dech": " ", "deh": " ", "tp": "tapi","tpi": "tapi",
        "yg": "yang", "&": "dan", "\n": " ", "god.": "bagus", "kl": "kalau", "klo": "kalau",
        "smga": "semoga", "smoga": "semoga", "trus": "terus", "danamp;": "dan", "dos": "kotak",
        "dus": "kotak", "prosen": "proses", "thankss": "terima kasih", "thanks": "terima kasih",
        "thx": "terima kasih","seler": "penjual", "seller": "penjual", "paking": "kemasan", 
        "peking": "kemasan","langanan": "langganan", "buat": "untuk", "pokok e": "pokoknya", 
        "jos": "mantap", "pengriman": "pengiriman", "sih": " ", "gimana": "bagaimana", 
        "gmn": "bagaimana", "apaan": "apa", "jlk": "jelek", "jd": "jadi",
        "gk": "tidak", "bgt": "sangat", "banget": "sangat",

        # Emoji
        ":)": " senang ", ":(": " sedih "
    }

    return kamus_baku

def remove_repeated_char(text):
    """
    Fungsi ini menggunakan regex untuk menemukan urutan karakter yang muncul lebih dari 1x
    secara berurutan. Pola (.) akan menangkap karakter dan \1+ akan mencocokan apakah karakter
    tersebut diulang satu kali atau lebih

    Args:
        text (string): Input teks yang akan dibersihkan

    Return:
        str:
    """
    pattern = re.compile(r'(.)\1+')
    return pattern.sub(r'\1', str(text))

def normalisasi_duplikasi(text):
    """
    Fungsi ini digunakan untuk merubah angka 2 pada kalimat (misal: "hati2") menjadi
    bentuk formal (misal: "hati-hati")

    Args:
        text (string): Input teks yang akan dibersihkan

    Return:
        str: Teks yang sudah dibersihkan
    """
    pattern = re.compile(r'([a-zA-Z]+)2')
    return pattern.sub(r'\1-\1', str(text))

def remove_punctuation(text):
    """
    Menghapus SEMUA tanda baca KECUALI hyphen (-) internal
    dan menggantinya dengan spasi.
    """
    pattern = re.compile(r'[^\w\s-]')
    return pattern.sub(' ', str(text))

def labeling(rating):
    """
    Fungsi ini mengambil nilai integer dari kolom rating dan mengubahnya menjadi tiga
    label string:
        - positif
        - netral
        - negatif

    Args:
        rating (int): Nilai integer dari kolom rating yang akan diubah menjadi label

    Returns:
        str: Label sentiment ('positif', 'netral', 'negatif') berdasarkan nilai rating
    """
    if rating >= 4:
        return "positif"
    elif rating == 3:
        return "netral"
    elif rating <=2:
        return "negatif"


def preprocessing_text(text, kamus_baku):
    """
    Alur preprocessing yang disesuaikan dengan preprocessing sebelumnya
    """
    text = str(text).lower() # Ubah menjadi lowercase
    text = remove_emoji(text) # Hapus emoji dari text
    text = remove_repeated_char(text) # Hapus karakter, tanda baca yg muncul > 1x berurutan
    text = normalisasi_duplikasi(text) # ubah kalimat hati2 -> hati-hati

    # Ubah kata slang menjadi bentuk baku
    temp_series = pd.Series([text])
    temp_series = temp_series.replace(kamus_baku, regex=True)
    text = temp_series.iloc[0]

    text = remove_punctuation(text) # Hapus tanda baca
    text = text.strip() # Hapus spasi diawal dan akhir kalimat
    text = re.sub(r'\s+', ' ', text) # Ubah setiap spasi, tab, baris baru yang berlebihan menjadi 1 spasi

    return text
