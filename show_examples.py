#!/usr/bin/env python3
"""
Примеры рецептов из базы знаний MIXTRIX
"""

import sqlite3
import json

def show_examples():
    """Показать примеры рецептов"""
    print("🍹 MIXTRIX Bot - Примеры рецептов из базы знаний")
    print("=" * 60)
    
    conn = sqlite3.connect('cocktails.db')
    cursor = conn.cursor()
    
    # IBA Official рецепты
    print("🏆 IBA Official рецепты:")
    print("-" * 40)
    cursor.execute('SELECT name, base_spirit, description FROM recipes WHERE source = "IBA Official" LIMIT 5')
    iba_recipes = cursor.fetchall()
    
    for name, spirit, desc in iba_recipes:
        print(f"• {name} ({spirit})")
        if desc:
            print(f"  {desc[:80]}...")
        print()
    
    # El Copitas рецепты
    print("🎨 El Copitas Bar рецепты:")
    print("-" * 40)
    cursor.execute('SELECT name, base_spirit, description FROM recipes WHERE source = "El Copitas Bar" LIMIT 3')
    copitas_recipes = cursor.fetchall()
    
    for name, spirit, desc in copitas_recipes:
        print(f"• {name} ({spirit})")
        if desc:
            print(f"  {desc[:80]}...")
        print()
    
    # Liquid Intelligence рецепты
    print("🧪 Liquid Intelligence рецепты:")
    print("-" * 40)
    cursor.execute('SELECT name, base_spirit, description FROM recipes WHERE source = "Liquid Intelligence" LIMIT 3')
    li_recipes = cursor.fetchall()
    
    for name, spirit, desc in li_recipes:
        print(f"• {name} ({spirit})")
        if desc:
            print(f"  {desc[:80]}...")
        print()
    
    # The Flavor Bible рецепты
    print("📖 The Flavor Bible рецепты:")
    print("-" * 40)
    cursor.execute('SELECT name, base_spirit, description FROM recipes WHERE source = "The Flavor Bible" LIMIT 3')
    fb_recipes = cursor.fetchall()
    
    for name, spirit, desc in fb_recipes:
        print(f"• {name} ({spirit})")
        if desc:
            print(f"  {desc[:80]}...")
        print()
    
    conn.close()
    
    print("=" * 60)
    print("✅ Примеры показаны!")

if __name__ == "__main__":
    show_examples()











