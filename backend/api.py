from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

DB_FILE = 'momo_transactions.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions with optional filtering"""
    conn = get_db_connection()
    
    # Get query parameters
    transaction_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    min_amount = request.args.get('min_amount')
    max_amount = request.args.get('max_amount')
    limit = request.args.get('limit', 100)
    
    # Build query
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []
    
    if transaction_type:
        query += " AND transaction_type = ?"
        params.append(transaction_type)
    
    if start_date:
        query += " AND date_time >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND date_time <= ?"
        params.append(end_date)
    
    if min_amount:
        query += " AND amount >= ?"
        params.append(float(min_amount))
    
    if max_amount:
        query += " AND amount <= ?"
        params.append(float(max_amount))
    
    query += " ORDER BY date_time DESC LIMIT ?"
    params.append(int(limit))
    
    cursor = conn.execute(query, params)
    transactions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(transactions)

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get transaction statistics"""
    conn = get_db_connection()
    
    # Total transactions by type
    cursor = conn.execute('''
        SELECT transaction_type, COUNT(*) as count, SUM(amount) as total_amount
        FROM transactions 
        GROUP BY transaction_type
    ''')
    type_stats = [dict(row) for row in cursor.fetchall()]
    
    # Monthly statistics
    cursor = conn.execute('''
        SELECT 
            strftime('%Y-%m', date_time) as month,
            COUNT(*) as count,
            SUM(amount) as total_amount
        FROM transactions 
        WHERE date_time IS NOT NULL
        GROUP BY strftime('%Y-%m', date_time)
        ORDER BY month
    ''')
    monthly_stats = [dict(row) for row in cursor.fetchall()]
    
    # Overall statistics
    cursor = conn.execute('''
        SELECT 
            COUNT(*) as total_transactions,
            SUM(amount) as total_amount,
            AVG(amount) as avg_amount,
            MAX(amount) as max_amount,
            MIN(amount) as min_amount
        FROM transactions
    ''')
    overall_stats = dict(cursor.fetchone())
    
    conn.close()
    
    return jsonify({
        'by_type': type_stats,
        'by_month': monthly_stats,
        'overall': overall_stats
    })

@app.route('/api/transaction/<int:transaction_id>', methods=['GET'])
def get_transaction_detail(transaction_id):
    """Get detailed information for a specific transaction"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
    transaction = cursor.fetchone()
    conn.close()
    
    if transaction:
        return jsonify(dict(transaction))
    else:
        return jsonify({'error': 'Transaction not found'}), 404

@app.route('/api/search', methods=['GET'])
def search_transactions():
    """Search transactions by text"""
    search_term = request.args.get('q', '')
    
    if not search_term:
        return jsonify([])
    
    conn = get_db_connection()
    cursor = conn.execute('''
        SELECT * FROM transactions 
        WHERE raw_message LIKE ? OR sender LIKE ? OR recipient LIKE ?
        ORDER BY date_time DESC
        LIMIT 50
    ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)