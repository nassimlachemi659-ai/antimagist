import requests, json

messages = [
    {"role": "system", "content": "You are AI."},
    {"role": "user", "content": "test"},
    {"role": "assistant", "content": ""},
    {"role": "user", "content": "hey"}
]

try:
    response = requests.post("http://localhost:11434/api/chat", json={
        "model": "llama3.2",
        "messages": messages,
        "stream": True,
        "options": {"temperature": 0.7}
    }, timeout=45)

    print("Status:", response.status_code)
    print("Content:", response.text)
except Exception as e:
    print("ERROR:", e)
