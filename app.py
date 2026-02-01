import streamlit as st
import hashlib
import time
import json
from datetime import datetime

# ==========================================
# 1. CORE BLOCKCHAIN CLASSES
# ==========================================

class Transaction:
    def __init__(self, sender, receiver, amount, timestamp=None, tx_id=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp if timestamp else time.time()
        self.id = tx_id if tx_id else self.calculate_hash()

    def calculate_hash(self):
        """Generates a unique hash for the transaction data."""
        tx_string = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}"
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp
        }

class Block:
    def __init__(self, index, previous_hash, transactions, difficulty):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.mining_time = 0

    def calculate_hash(self):
        """Calculates the hash of the block contents."""
        # We sort transactions to ensure consistent hashing
        tx_string = json.dumps([tx.to_dict() for tx in self.transactions], sort_keys=True)
        block_string = f"{self.index}{self.timestamp}{tx_string}{self.previous_hash}{self.difficulty}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self):
        """Performs Proof of Work."""
        target = "0" * self.difficulty
        start_time = time.time()
        
        # UI placeholder for mining progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        while self.hash[:self.difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            
            # Update UI every 500 attempts to prevent slowing down too much
            if self.nonce % 500 == 0:
                status_text.text(f"Mining... Nonce: {self.nonce} | Hash: {self.hash}")
        
        end_time = time.time()
        self.mining_time = end_time - start_time
        
        status_text.empty()
        progress_bar.empty()
        return True

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = 2  # Starting difficulty
        self.processed_tx_ids = set() 
        self.mining_times = []

    def create_genesis_block(self):
        """Creates the first block in the chain."""
        return Block(0, "0", [], 1)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction, secure_mode=True):
        """Adds a transaction to the pending pool with replay protection logic."""
        if secure_mode:
            if transaction.id in self.processed_tx_ids:
                return False, "❌ REPLAY ATTACK BLOCKED: Transaction ID already exists!"
            
            for tx in self.pending_transactions:
                if tx.id == transaction.id:
                    return False, "❌ REPLAY ATTACK BLOCKED: Transaction already pending!"

        self.pending_transactions.append(transaction)
        if secure_mode:
             self.processed_tx_ids.add(transaction.id)
             
        return True, "✅ Transaction added successfully!"

    def adjust_difficulty(self):
        """Simple dynamic difficulty adjustment."""
        if len(self.chain) < 2:
            return
        
        latest_block = self.get_latest_block()
        prev_block = self.chain[-2]
        time_taken = latest_block.mining_time
        target_time = 2.0 
        
        if time_taken < target_time:
            self.difficulty += 1
        elif time_taken > target_time and self.difficulty > 1:
            self.difficulty -= 1

    def mine_pending_transactions(self, miner_address, auto_adjust=False):
        if not self.pending_transactions:
            return False, "No transactions to mine."

        new_block = Block(
            index=len(self.chain),
            previous_hash=self.get_latest_block().hash,
            transactions=self.pending_transactions,
            difficulty=self.difficulty
        )

        new_block.mine_block()
        self.chain.append(new_block)
        
        for tx in self.pending_transactions:
            self.processed_tx_ids.add(tx.id)

        self.pending_transactions = []
        self.mining_times.append(new_block.mining_time)

        if auto_adjust:
            self.adjust_difficulty()

        return True, f"Block #{new_block.index} mined successfully in {new_block.mining_time:.4f}s!"

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False, f"Block {i} hash mismatch! Data tampered?"
            
            if current.previous_hash != previous.hash:
                return False, f"Block {i} invalid previous hash link!"

        return True, "Blockchain is valid."

    def corrupt_block(self, block_index, new_data):
        if block_index < len(self.chain):
            if self.chain[block_index].transactions:
                self.chain[block_index].transactions[0].amount = new_data
            else:
                return False, "Block has no transactions to tamper."
            return True, "Block tampered."
        return False, "Invalid block index."

# ==========================================
# 2. STREAMLIT UI SETUP
# ==========================================

st.set_page_config(page_title="EduChain: Advanced Blockchain Simulator", layout="wide", page_icon="🔗")

if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()
if 'wallet_alice' not in st.session_state:
    st.session_state.wallet_alice = 100
if 'wallet_bob' not in st.session_state:
    st.session_state.wallet_bob = 0

bc = st.session_state.blockchain

st.title("🔗 EduChain: Advanced Blockchain Simulator")
st.markdown("### A College-Level Practical Demonstration of Blockchain Mechanics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Blocks Mined", len(bc.chain))
col2.metric("Pending Tx", len(bc.pending_transactions))
col3.metric("Current Difficulty", bc.difficulty)
col4.metric("Chain Status", "Valid" if bc.is_chain_valid()[0] else "INVALID", delta_color="normal" if bc.is_chain_valid()[0] else "inverse")

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================

with st.sidebar:
    st.header("⚙️ Network Settings")
    
    secure_mode = st.toggle("🔒 Secure Mode (Prevent Replay)", value=True)
    if secure_mode:
        st.success("Replay Protection: ACTIVE")
    else:
        st.error("Replay Protection: DISABLED (Vulnerable)")

    st.divider()

    auto_difficulty = st.checkbox("🤖 Auto-Adjust Difficulty", value=False)
    if not auto_difficulty:
        new_difficulty = st.slider("Manual Difficulty (Zeros)", 1, 5, bc.difficulty)
        bc.difficulty = new_difficulty
    
    st.divider()
    
    st.header("🛠️ Admin Tools")
    if st.button("🧪 Corrupt Block 1 (Tamper Data)"):
        success, msg = bc.corrupt_block(1, 999999)
        if success:
            st.toast(msg, icon="😈")
        else:
            st.toast(msg, icon="⚠️")

    if st.button("🧹 Reset Blockchain"):
        st.session_state.blockchain = Blockchain()
        st.session_state.wallet_alice = 100
        st.session_state.wallet_bob = 0
        if 'last_tx' in st.session_state:
            del st.session_state.last_tx
        st.rerun()

# ==========================================
# 4. TABS UI
# ==========================================

tab1, tab2, tab3, tab4 = st.tabs(["💸 Transactions & Mining", "⛓️ Blockchain Inspector", "🛡️ Replay Attack Demo", #"📚 Theory & Viva"])

# --- TAB 1: TRANSACTIONS & MINING ---
with tab1:
    st.subheader("1️⃣ Create Transaction")
    
    col_tx1, col_tx2 = st.columns(2)
    
    with col_tx1:
        st.info(f"Alice's Balance: {st.session_state.wallet_alice} Coins")
        receiver = st.text_input("Receiver", value="Bob")
        
        # --- SAFE INPUT LOGIC ---
        if st.session_state.wallet_alice > 0:
            # Smart default: If balance is < 10, default to the balance amount
            default_amount = 10 if st.session_state.wallet_alice >= 10 else st.session_state.wallet_alice
            
            amount = st.number_input(
                "Amount", 
                min_value=1, 
                max_value=st.session_state.wallet_alice, 
                value=default_amount
            )
            
            if st.button("Send Transaction"):
                tx = Transaction("Alice", receiver, amount)
                success, msg = bc.add_transaction(tx, secure_mode=secure_mode)
                
                if success:
                    st.session_state.wallet_alice -= amount
                    st.session_state.wallet_bob += amount
                    st.success(msg)
                    st.session_state.last_tx = tx
                else:
                    st.error(msg)
        else:
            st.error("⚠️ Alice is out of money! Use 'Reset Blockchain' in the sidebar.")
    
    with col_tx2:
        st.write("### ⏳ Pending Transactions")
        if bc.pending_transactions:
            for i, tx in enumerate(bc.pending_transactions):
                st.code(f"TxID: {tx.id[:15]}...\nFrom: {tx.sender} -> To: {tx.receiver}: {tx.amount} Coins")
        else:
            st.info("No pending transactions.")

    st.divider()
    
    st.subheader("2️⃣ Mining Zone")
    st.write(f"Current Target: Hash must start with **{bc.difficulty} zeros**")
    
    if st.button("⛏️ Mine Block"):
        if not bc.pending_transactions:
            st.warning("No transactions to mine!")
        else:
            with st.spinner("Mining in progress... Calculating hashes..."):
                success, msg = bc.mine_pending_transactions("Miner1", auto_adjust=auto_difficulty)
                if success:
                    st.balloons()
                    st.success(msg)
                else:
                    st.error(msg)

# --- TAB 2: BLOCKCHAIN INSPECTOR ---
with tab2:
    st.subheader("🔍 Chain Explorer")
    
    is_valid, valid_msg = bc.is_chain_valid()
    if is_valid:
        st.success(f"✅ {valid_msg}")
    else:
        st.error(f"❌ {valid_msg}")
        st.warning("The chain is broken! A block has been modified, invalidating subsequent hashes.")

    for block in bc.chain:
        with st.expander(f"Block #{block.index} [{'Genesis' if block.index == 0 else 'Mined'}] - {block.hash[:15]}..."):
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Timestamp:** {datetime.fromtimestamp(block.timestamp)}")
                st.write(f"**Nonce:** {block.nonce}")
                st.write(f"**Difficulty:** {block.difficulty}")
                st.write(f"**Mining Time:** {block.mining_time:.4f}s")
            with c2:
                st.write(f"**Previous Hash:**")
                st.code(block.previous_hash)
                st.write(f"**Current Hash:**")
                st.code(block.hash)
            
            st.write("---")
            st.write("**Transactions:**")
            if block.transactions:
                st.json([tx.to_dict() for tx in block.transactions])
            else:
                st.write("System Block (No user transactions)")

# --- TAB 3: REPLAY ATTACK DEMO ---
with tab3:
    st.subheader("⚔️ Replay Attack Simulation")
    
    st.markdown("""
    **Scenario:** An attacker captures a valid transaction sent by Alice and tries to re-broadcast it.
    """)
    
    if 'last_tx' in st.session_state:
        last_tx = st.session_state.last_tx
        st.write("##### Captured Transaction:")
        st.code(f"ID: {last_tx.id}\n{last_tx.sender} -> {last_tx.receiver} : {last_tx.amount}")
        
        col_hack1, col_hack2 = st.columns(2)
        
        with col_hack1:
            st.warning("Current Mode: " + ("SECURE" if secure_mode else "VULNERABLE"))
            
            if st.button("😈 Execute Replay Attack"):
                success, msg = bc.add_transaction(last_tx, secure_mode=secure_mode)
                
                if success:
                    st.error("⚠️ ATTACK SUCCESSFUL! Duplicate transaction accepted.")
                    st.session_state.wallet_alice -= last_tx.amount
                    st.session_state.wallet_bob += last_tx.amount
                else:
                    st.success(msg)
                    
        with col_hack2:
            st.write("##### Result Analysis")
            if secure_mode:
                st.info("System checked TxID history and rejected duplicate.")
            else:
                st.warning("System ignored Uniqueness. Duplicate Tx accepted into pool.")
                
    else:
        st.info("Send a transaction in Tab 1 first to capture it.")

# --- TAB 4: THEORY & VIVA ---
#with tab4:
#    st.header("📚 Theory & Viva Explanations")
    
#    with st.expander("What is a Blockchain?"):
#        st.write("A distributed, immutable ledger. Blocks are chained via hashes.")
#    with st.expander("What is Proof of Work (PoW)?"):
#        st.write("A consensus mechanism requiring computational effort (finding a Nonce) to secure the network.")
#    with st.expander("What is a Replay Attack?"):
#        st.write("Maliciously repeating a valid data transmission. Prevented by Unique IDs/Nonces.")
#    with st.expander("How does Difficulty Adjustment work?"):
#        st.write("Adjusts required zeros in hash to keep mining time constant despite computer power changes.")
