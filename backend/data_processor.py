import xml.etree.ElementTree as ET
import sqlite3
import re
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_processing.log'),
        logging.StreamHandler()
    ]
)

class MoMoDataProcessor:
    def __init__(self, xml_file: str, db_file: str):
        self.xml_file = xml_file
        self.db_file = db_file
        self.unprocessed_messages = []
        
    def create_database(self):
        """Create database schema for MoMo transactions"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT,
                transaction_type TEXT NOT NULL,
                amount REAL,
                fee REAL DEFAULT 0,
                sender TEXT,
                recipient TEXT,
                phone_number TEXT,
                agent_name TEXT,
                agent_phone TEXT,
                bank_name TEXT,
                reference TEXT,
                meter_number TEXT,
                bundle_type TEXT,
                bundle_size TEXT,
                validity_period TEXT,
                date_time TEXT,
                raw_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logging.info("Database schema created successfully")
    
    def parse_xml(self) -> List[str]:
        """Parse XML file and extract SMS messages"""
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            messages = [sms.find('body').text for sms in root.findall('sms')]
            logging.info(f"Parsed {len(messages)} SMS messages from XML")
            return messages
        except Exception as e:
            logging.error(f"Error parsing XML: {e}")
            return []
    
    def categorize_message(self, message: str) -> Dict:
        """Categorize SMS message and extract relevant data"""
        message = message.strip()
        
        # Extract common patterns
        amount_pattern = r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*RWF'
        date_pattern = r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})'
        txid_pattern = r'(?:Transaction ID|TxId):\s*(\w+)'
        phone_pattern = r'(250\d{9})'
        
        # Extract basic info
        amount_match = re.search(amount_pattern, message)
        date_match = re.search(date_pattern, message)
        txid_match = re.search(txid_pattern, message)
        
        amount = float(amount_match.group(1).replace(',', '')) if amount_match else 0
        date_time = date_match.group(1) if date_match else None
        transaction_id = txid_match.group(1) if txid_match else None
        
        # Categorize by message content
        if 'received' in message.lower() and 'from' in message.lower():
            return self._parse_incoming_money(message, amount, date_time, transaction_id)
        elif 'payment' in message.lower() and ('completed' in message.lower() or 'paid' in message.lower()):
            if 'airtime' in message.lower():
                return self._parse_airtime_payment(message, amount, date_time, transaction_id)
            elif 'cash power' in message.lower() or 'electricity' in message.lower() or 'eucl' in message.lower():
                return self._parse_cashpower_payment(message, amount, date_time, transaction_id)
            else:
                return self._parse_payment_to_code(message, amount, date_time, transaction_id)
        elif 'sent' in message.lower() and re.search(phone_pattern, message):
            return self._parse_transfer_mobile(message, amount, date_time, transaction_id)
        elif 'deposit' in message.lower() and 'bank' in message.lower():
            return self._parse_bank_deposit(message, amount, date_time, transaction_id)
        elif 'withdrawn' in message.lower() and 'agent' in message.lower():
            return self._parse_agent_withdrawal(message, amount, date_time, transaction_id)
        elif 'bank transfer' in message.lower() or 'transferred to' in message.lower():
            return self._parse_bank_transfer(message, amount, date_time, transaction_id)
        elif 'bundle' in message.lower() or 'internet' in message.lower() or 'voice' in message.lower():
            return self._parse_bundle_purchase(message, amount, date_time, transaction_id)
        elif 'third party' in message.lower():
            return self._parse_third_party(message, amount, date_time, transaction_id)
        else:
            self.unprocessed_messages.append(message)
            return None
    
    def _parse_incoming_money(self, message: str, amount: float, date_time: str, transaction_id: str) -> Dict:
        sender_match = re.search(r'from\s+([^.]+?)\.', message)
        sender = sender_match.group(1).strip() if sender_match else None
        
        return {
            'transaction_type': 'Incoming Money',
            'amount': amount,
            'sender': sender,
            'transaction_id': transaction_id,
            'date_time': date_time,
            'raw_message': message
        }
    
    def _parse_payment_to_code(self, message: str, amount: float, date_time: str, transaction_id: str) -> Dict:
        recipient_match = re.search(r'to\s+([^.]+?)(?:\s+has been|\.)', message)
        recipient = recipient_match.group(1).strip() if recipient_match else None
        
        return {
            'transaction_type': 'Payment to Code Holder',
            'amount': amount,
            'recipient': recipient,
            'transaction_id': transaction_id,
            'date_time': date_time,
            'raw_message': message
        }
    
    def _parse_transfer_mobile(self, message: str, amount: float, date_time: str, transaction_id: str) -> Dict:
        phone_match = re.search(r'(250\d{9})', message)
        fee_match = re.search(r'Fee:\s*(\d+(?:\.\d{2})?)\s*RWF', message)
        
        return {
            'transaction_type': 'Transfer to Mobile Number',
            'amount': amount,
            'phone_number': phone_match.group(1) if phone_match else None,
            'fee': float(fee_match.group(1)) if fee_match else 0,
            'transaction_id': transaction_id,
            'date_time': date_time,
            'raw_message': message
        }
    
    def _parse_bank_deposit(self, message: str, amount: float, date_time: str, transaction_id: str) -> Dict:
        bank_match = re.search(r'(?:to|deposit to)\s+([^.]+?)(?:\s+has been|\.|Ref)', message)
        ref_match = re.search(r'(?:Ref|Reference):\s*(\w+)', message)
        
        return {
            'transaction_type': 'Bank Deposit',
            'amount': amount,
            'bank_name': bank_match.group(1).strip() if bank_match else None,
            'reference': ref_match.group(1) if ref_match else None,
            'transaction_id': transaction_id,
            'date_time': date_time,
            'raw_message': message
        }
    
    def _parse_airtime_payment(self, message: str, amount: float, date_time: str, transaction_id: str) -> Dict:
        fee_match = re.search(r'Fee:\s*(\d+(?:\.\d{2})?)\s*RWF', message)
        
        return {
            'transaction_type': 'Airtime Bill Payment',
            'amount': amount,
            'fee': float(fee_match.group(1)) if fee_match else 0,
            'transaction_id': transaction_id,
            'date_time': date_time,
            'raw_message': message
        }
    
    def _parse_cashpower_payment(self, message: str, amount: float, date_time: str, transaction_id: str) -> Dict:
        meter_match = re.search(r'Meter:\s*(\w+)', message)
        
        return {
            'transaction_type': 'Cash Power Bill Payment',
            'amount': amount,
            'meter_number': meter_match.group(1) if meter_match else None,
            'transaction_id': transaction_id,
            'date_time': date_time,
            'raw_message': message
        }
    
    def _parse_third_party(self, message: str, amount: float, date_time: str, transaction_id: str) -> Dict:
        initiator_match = re.search(r'initiated by\s+([^.]+?)\.', message)
        
        return {
            'transaction_type': 'Third Party Transaction',
            'amount': amount,
            'sender': initiator_match.group(1).strip() if initiator_match else None,
            'transaction_id': transaction_id,
            'date_time': date_time,
            'raw_message': message
        }
    
    def _parse_agent_withdrawal(self, message: str, amount: float, date_time: str, transaction_id: str) -> Dict:
        agent_match = re.search(r'agent:\s*([^(]+?)\s*\(([^)]+)\)', message)
        
        return {
            'transaction_type': 'Agent Withdrawal',
            'amount': amount,
            'agent_name': agent_match.group(1).strip() if agent_match else None,
            'agent_phone': agent_match.group(2) if agent_match else None,
            'transaction_id': transaction_id,
            'date_time': date_time,
            'raw_message': message
        }
    
    def _parse_bank_transfer(self, message: str, amount: float, date_time: str, transaction_id: str) -> Dict:
        bank_match = re.search(r'(?:transferred to|to)\s+([^.]+?)\.', message)
        ref_match = re.search(r'(?:Ref|Reference):\s*(\w+)', message)
        
        return {
            'transaction_type': 'Bank Transfer',
            'amount': amount,
            'bank_name': bank_match.group(1).strip() if bank_match else None,
            'reference': ref_match.group(1) if ref_match else None,
            'transaction_id': transaction_id,
            'date_time': date_time,
            'raw_message': message
        }
    
    def _parse_bundle_purchase(self, message: str, amount: float, date_time: str, transaction_id: str) -> Dict:
        bundle_size_match = re.search(r'(\d+(?:\.\d+)?(?:GB|MB|minutes?))', message)
        validity_match = re.search(r'(?:valid|Valid).*?(\d+\s+days?)', message)
        
        bundle_type = 'Internet' if 'GB' in message or 'MB' in message else 'Voice'
        
        return {
            'transaction_type': 'Internet/Voice Bundle Purchase',
            'amount': amount,
            'bundle_type': bundle_type,
            'bundle_size': bundle_size_match.group(1) if bundle_size_match else None,
            'validity_period': validity_match.group(1) if validity_match else None,
            'transaction_id': transaction_id,
            'date_time': date_time,
            'raw_message': message
        }
    
    def insert_transaction(self, transaction: Dict):
        """Insert transaction into database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions (
                transaction_id, transaction_type, amount, fee, sender, recipient,
                phone_number, agent_name, agent_phone, bank_name, reference,
                meter_number, bundle_type, bundle_size, validity_period,
                date_time, raw_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            transaction.get('transaction_id'),
            transaction.get('transaction_type'),
            transaction.get('amount'),
            transaction.get('fee', 0),
            transaction.get('sender'),
            transaction.get('recipient'),
            transaction.get('phone_number'),
            transaction.get('agent_name'),
            transaction.get('agent_phone'),
            transaction.get('bank_name'),
            transaction.get('reference'),
            transaction.get('meter_number'),
            transaction.get('bundle_type'),
            transaction.get('bundle_size'),
            transaction.get('validity_period'),
            transaction.get('date_time'),
            transaction.get('raw_message')
        ))
        
        conn.commit()
        conn.close()
    
    def process_data(self):
        """Main processing function"""
        logging.info("Starting data processing...")
        
        # Create database
        self.create_database()
        
        # Parse XML
        messages = self.parse_xml()
        
        processed_count = 0
        for message in messages:
            transaction = self.categorize_message(message)
            if transaction:
                self.insert_transaction(transaction)
                processed_count += 1
        
        # Log unprocessed messages
        if self.unprocessed_messages:
            with open('unprocessed_messages.log', 'w') as f:
                for msg in self.unprocessed_messages:
                    f.write(f"{msg}\n\n")
        
        logging.info(f"Processing complete: {processed_count} transactions processed, {len(self.unprocessed_messages)} unprocessed")

if __name__ == "__main__":
    processor = MoMoDataProcessor('../data/sms_data_clean.xml', 'momo_transactions.db')
    processor.process_data()