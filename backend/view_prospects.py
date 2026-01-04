#!/usr/bin/env python3
"""
Simple script to view all prospects in the database
"""
import sqlite3
import sys
from datetime import datetime

DB_PATH = "prospects.db"

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, company_name, email, created_at FROM prospects ORDER BY created_at DESC")
    prospects = cursor.fetchall()
    
    if not prospects:
        print("No prospects found in the database.")
    else:
        print(f"\n{'='*80}")
        print(f"Total Prospects: {len(prospects)}")
        print(f"{'='*80}\n")
        
        for prospect in prospects:
            prospect_id, name, company_name, email, created_at = prospect
            print(f"ID: {prospect_id}")
            print(f"Name: {name}")
            print(f"Company: {company_name}")
            print(f"Email: {email}")
            print(f"Registered: {created_at}")
            print(f"{'-'*80}\n")
    
    conn.close()
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

