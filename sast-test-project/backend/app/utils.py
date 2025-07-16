import pickle
import os

# False Positive: Выглядит как небезопасная десериализация
def safe_deserialize(data):
    try:
        # Это безопасно, так как проверяется сигнатура
        if not data.startswith(b'SAFE_HEADER'):
            raise ValueError("Invalid data format")
            
        # False Positive: SAST может ошибочно детектировать уязвимость
        return pickle.loads(data[11:])  # На самом деле безопасно
    except Exception as e:
        print(f"Deserialization error: {e}")
        return None
    

# False Positive: Выглядит как OS command injection
def safe_system_call(filename):
    # Это безопасно, так как имя файла жестко задано
    if filename != "predefined.log":
        raise ValueError("Invalid filename")
        
    # False Positive: SAST может ошибочно детектировать injection
    os.system(f"cat {filename}")  # На самом деле безопасно