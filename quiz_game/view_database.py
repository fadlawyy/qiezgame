#!/usr/bin/env python3
"""
Database Viewer for Quiz Game
Simple script to view and explore the SQLite database contents
"""

import sqlite3
import os
import sys
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        os.system('chcp 65001 >nul 2>&1')  # Set UTF-8 code page
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def connect_to_database():
    """Connect to the quiz game database"""
    db_path = os.path.join(os.path.dirname(__file__), 'quiz_game.db')
    if not os.path.exists(db_path):
        print("❌ Database file not found! Run the quiz game first to create it.")
        return None
    return sqlite3.connect(db_path)

def show_tables(conn):
    """Show all tables in the database"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("📋 Database Tables:")
    for table in tables:
        print(f"  • {table[0]}")
    return [table[0] for table in tables]

def show_table_structure(conn, table_name):
    """Show the structure of a specific table"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"\n🏗️  Structure of '{table_name}' table:")
    print("   Column Name    | Type    | Not Null | Default")
    print("   " + "-" * 50)
    for col in columns:
        print(f"   {col[1]:<15} | {col[2]:<7} | {col[3]:<8} | {col[4] or 'None'}")

def show_table_data(conn, table_name, limit=10):
    """Show data from a specific table"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_rows = cursor.fetchone()[0]
    
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
    rows = cursor.fetchall()
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [col[1] for col in cursor.fetchall()]
    
    print(f"\n📊 Data from '{table_name}' table (showing {len(rows)} of {total_rows} rows):")
    if rows:
        # Print header
        header = " | ".join(f"{col[:15]:<15}" for col in columns)
        print("   " + header)
        print("   " + "-" * len(header))
        
        # Print data rows
        for row in rows:
            row_str = " | ".join(f"{str(val)[:15]:<15}" for val in row)
            print("   " + row_str)
    else:
        print("   No data found in this table.")

def show_quiz_statistics(conn):
    """Show quiz game statistics"""
    cursor = conn.cursor()
    
    print("\n📈 Quiz Game Statistics:")
    
    # Total questions
    cursor.execute("SELECT COUNT(*) FROM questions")
    total_questions = cursor.fetchone()[0]
    print(f"   • Total Questions: {total_questions}")
    
    # Questions by category
    cursor.execute("SELECT category, COUNT(*) FROM questions GROUP BY category")
    categories = cursor.fetchall()
    print("   • Questions by Category:")
    for cat, count in categories:
        print(f"     - {cat}: {count}")
    
    # Total players
    cursor.execute("SELECT COUNT(*) FROM players")
    total_players = cursor.fetchone()[0]
    print(f"   • Total Players: {total_players}")
    
    # Total quiz attempts
    cursor.execute("SELECT COUNT(*) FROM scores")
    total_attempts = cursor.fetchone()[0]
    print(f"   • Total Quiz Attempts: {total_attempts}")
    
    # Top 3 players
    cursor.execute('''
        SELECT p.name, MAX(ROUND((s.score * 100.0 / s.total_questions), 2)) as best_percentage
        FROM scores s
        JOIN players p ON s.player_id = p.id
        GROUP BY p.name
        ORDER BY best_percentage DESC
        LIMIT 3
    ''')
    top_players = cursor.fetchall()
    if top_players:
        print("   • Top 3 Players:")
        for i, (name, percentage) in enumerate(top_players, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            print(f"     {medal} {name}: {percentage}%")

def interactive_menu():
    """Interactive menu for database exploration"""
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        while True:
            print("\n" + "="*50)
            print("🎯 QUIZ GAME DATABASE VIEWER")
            print("="*50)
            print("1. Show all tables")
            print("2. View questions")
            print("3. View players")
            print("4. View scores/history")
            print("5. Show quiz statistics")
            print("6. Show table structures")
            print("7. Exit")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                tables = show_tables(conn)
                
            elif choice == '2':
                show_table_data(conn, 'questions', 20)
                
            elif choice == '3':
                show_table_data(conn, 'players')
                
            elif choice == '4':
                show_table_data(conn, 'scores', 15)
                
            elif choice == '5':
                show_quiz_statistics(conn)
                
            elif choice == '6':
                tables = show_tables(conn)
                for table in tables:
                    show_table_structure(conn, table)
                    
            elif choice == '7':
                print("\n👋 Thanks for exploring the database!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-7.")
                
            input("\nPress Enter to continue...")
            
    except KeyboardInterrupt:
        print("\n\n👋 Database viewer closed.")
    finally:
        conn.close()

if __name__ == "__main__":
    interactive_menu()
