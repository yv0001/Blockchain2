# Blockchain2
# 🔗 EduChain: Advanced Blockchain Simulator

**A comprehensive, interactive Blockchain demonstration tool built with Python and Streamlit.**

This project is an educational simulator designed to demonstrate the core mechanics of blockchain technology, including **Proof of Work (PoW)**, **Dynamic Difficulty Adjustment**, and **Security vulnerabilities** like Replay Attacks. It serves as a practical visualization for college-level Blockchain & Cryptography courses.

---

## 🚀 Features

### 1. 🧱 Core Blockchain Architecture

* **Genesis Block & Chaining:** visualizes how blocks are linked via cryptographic hashes (SHA-256).
* **Immutability:** Demonstrates how tampering with old data invalidates the entire chain.

### 2. ⛏️ Mining & Consensus

* **Proof of Work (PoW):** Simulates the computational effort required to mine blocks.
* **Dynamic Difficulty:** Implements an algorithm that auto-adjusts mining difficulty based on network speed (similar to Bitcoin).

### 3. 🛡️ Security Simulations

* **Replay Attack Demo:**
* **Vulnerable Mode:** Shows how attackers can double-spend by re-broadcasting old transactions.
* **Secure Mode:** Demonstrates prevention using Unique Transaction IDs and History Tracking.


* **Tampering Simulation:** Allows "corrupting" a block to visualize chain breakage.

### 4. 📊 Interactive UI

* Built with **Streamlit** for real-time interaction.
* Live dashboard showing **Blocks Mined**, **Difficulty**, and **Chain Validity**.
* Interactive forms for creating transactions and mining blocks.

---

## 🛠️ Installation & Setup

### Prerequisites

* Python 3.8 or higher installed.

### Step 1: Install Dependencies

Open your terminal or command prompt and install Streamlit:

```bash
pip install streamlit

```

### Step 2: Run the Application

Navigate to your project folder and run:

```bash
streamlit run app.py

```

The application will automatically open in your default web browser at `http://localhost:8501`.

---

## 📖 Usage Guide (Demo Flow)

Follow this sequence to demonstrate the project functionality:

### 1️⃣ Transaction Creation

1. Go to the **"Transactions & Mining"** tab.
2. Enter a Receiver (e.g., "Bob") and an Amount.
3. Click **"Send Transaction"**.
4. Observe the transaction appear in the "Pending Transactions" pool.

### 2️⃣ Mining a Block

1. Click the **"Mine Block"** button.
2. Watch the mining progress spinner.
3. Once mined, the block is added to the chain, and the difficulty might adjust based on how fast it was mined.

### 3️⃣ Inspecting the Blockchain

1. Switch to the **"Blockchain Inspector"** tab.
2. Expand the blocks to see details: `Nonce`, `Previous Hash`, `Current Hash`, and `Transactions`.
3. **Check Validity:** The top status bar will show "Chain Status: Valid".

### 4️⃣ Simulating Attacks (The Viva Highlight)

1. **Replay Attack:**
* Go to the **"Replay Attack Demo"** tab.
* **Scenario:** You captured Alice's previous transaction.
* **Vulnerable Mode:** Toggle "Secure Mode" **OFF** in the sidebar. Click "Execute Attack". *Result: Success (Double Spend).*
* **Secure Mode:** Toggle "Secure Mode" **ON**. Click "Execute Attack". *Result: Blocked.*


2. **Tampering:**
* Click **"Corrupt Block 1"** in the Sidebar.
* Check the Inspector tab. The chain status will change to **INVALID** because the hashes no longer match.



---

## 🧠 Technical Concepts Explained

### 🔹 Proof of Work (PoW)

PoW is the mechanism used to secure the network. Miners must solve a mathematical puzzle:

> Find a `Nonce` such that `SHA256(Block Data + Nonce)` starts with `N` zeros.

* **N** is the **Difficulty**.
* This prevents spam and makes rewriting history computationally expensive.

### 🔹 Replay Attack

A replay attack occurs when a valid data transmission is maliciously or fraudulently repeated.

* **Vulnerability:** If the network doesn't check if a specific transaction ID was already processed, it will execute the payment again.
* **Prevention:** We assign a unique ID to every transaction and store a history of processed IDs. If a duplicate ID arrives, it is rejected.

### 🔹 Dynamic Difficulty

To keep the block generation time stable (e.g., 10 minutes in Bitcoin, 2 seconds in this sim):

* **Too Fast?** Increase difficulty (require more zeros).
* **Too Slow?** Decrease difficulty (require fewer zeros).

---

## 📂 Project Structure

```
📁 Blockchain-Project
│
├── app.py           # The main application code (Logic + UI)
├── README.md        # Project documentation
└── requirements.txt # (Optional) List dependencies: streamlit

```

---

## 👨‍💻 Author

**Name:** Yash Vekariya
**Course:** Blockchain and Cryptography
**Date:** 25/01/2026
