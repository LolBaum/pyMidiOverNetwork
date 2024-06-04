import os
from pathlib import Path

path = "logs"
file = "pythonInfo.log"
file_path = Path(path, file)

os.makedirs(path, exist_ok=True)

if not file_path.exists():
    with open(file_path, 'w') as file:
        pass
else:
    #print(f"The file '{file_path}' already exists.")
    pass
