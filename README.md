# DecentraVote - PROTOTYPE
## - Blockchain Based E-Voting System

> [!CAUTION]
> **Development/Protoype/Concept Model. Not intended for Practical/Real World Applications**

> [!WARNING]
> **Requires Ganache and Mongodb**

> [!IMPORTANT]
> **Must install all dependencies**

---
## How to run?

### 1. Install dependencies
```cmd
cd backend
pip install -r requirements.txt
```

### 2. Start Ganache

### 3. Install solc once (in a python shell)

```py
from solcx import install_solc
install_solc("0.8.17")
```

### 4. Deploy Contract
```cmd
cd backend
python deploy.py
```

### 5. Run the Backend
```cmd
cd backend
python app.py
```

### 6. Open Index.html in a Browser
---

## Tested on

> Machine: **Windows**
> 
> Python Version: **3.10.x**