import json
import requests
import sqlite3

class GameCollection:
    """Class representing a collection of video games."""

    def __init__(self):
        """Initialize the database connection."""
        self.conn = sqlite3.connect('games.db')
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        """Set up the database and create the table if it doesn't exist."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS games 
                              (title TEXT, platform TEXT, genre TEXT, year TEXT, rating TEXT)''')
        self.conn.commit()

    def add_game(self, title, platform, genre, year):
        """Add a game to the collection."""
        # Mock an API request to get a game rating based on title
        rating = self.get_game_rating(title)
        self.cursor.execute("INSERT INTO games (title, platform, genre, year, rating) VALUES (?, ?, ?, ?, ?)",
                            (title, platform, genre, year, rating))
        self.conn.commit()

    def get_game_rating(self, title):
        """Mock an API request to get a game rating based on the title."""
        # In a real-world scenario, you'd use the 'requests' library to fetch data from an actual API
        # For this example, we'll just return a mock rating for simplicity
        response = requests.get(f"https://api.example.com/game-rating/{title}")
        return response.json().get('rating')
        return "4.5/5"  # Mock rating

    def list_games(self):
        """List all games in the collection."""
        self.cursor.execute("SELECT title, platform, genre, year, rating FROM games")
        for game in self.cursor.fetchall():
            print(f"{game[0]} ({game[3]}) - {game[2]} on {game[1]} - Rating: {game[4]}")

    def search_game(self, title):
        """Search for a game by title."""
        self.cursor.execute("SELECT title, platform, genre, year, rating FROM games WHERE title LIKE ?", (f"%{title}%",))
        for game in self.cursor.fetchall():
            print(f"{game[0]} ({game[3]}) - {game[2]} on {game[1]} - Rating: {game[4]}")

    def edit_game(self, old_title, new_title, new_platform, new_genre, new_year):
        """Edit game details."""
        self.cursor.execute("UPDATE games SET title=?, platform=?, genre=?, year=? WHERE title=?", 
                            (new_title, new_platform, new_genre, new_year, old_title))
        self.conn.commit()

    def delete_game(self, title):
        """Delete a game by title."""
        self.cursor.execute("DELETE FROM games WHERE title=?", (title,))
        self.conn.commit()

    def __del__(self):
        """Close the database connection when the object is destroyed."""
        self.conn.close()


def main():
    """Main function to run the Video Game Collection CLI application."""
    collection = GameCollection()

    while True:
        print("\nVideo Game Collection Manager")
        print("1. Add a new game")
        print("2. List all games")
        print("3. Search for a game by title")
        print("4. Edit game details")
        print("5. Delete a game")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter game title: ")
            platform = input("Enter game platform (e.g., PC, PS5, Xbox): ")
            genre = input("Enter game genre (e.g., Action, RPG): ")
            year = input("Enter release year: ")
            collection.add_game(title, platform, genre, year)
        elif choice == "2":
            collection.list_games()
        elif choice == "3":
            title = input("Enter game title to search: ")
            collection.search_game(title)
        elif choice == "4":
            old_title = input("Enter the title of the game you want to edit: ")
            new_title = input("Enter new game title: ")
            new_platform = input("Enter new game platform: ")
            new_genre = input("Enter new game genre: ")
            new_year = input("Enter new release year: ")
            collection.edit_game(old_title, new_title, new_platform, new_genre, new_year)
        elif choice == "5":
            title = input("Enter the title of the game you want to delete: ")
            collection.delete_game(title)
        elif choice == "6":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
