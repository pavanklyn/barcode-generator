"""
Random Joke Generator using JokeAPI
Fetches random jokes from an external API and displays them.
"""

import requests
import json
from typing import Dict, Optional


class JokeGenerator:
    """A class to fetch and display random jokes from JokeAPI."""
    
    BASE_URL = "https://v2.jokeapi.dev/joke"
    
    def __init__(self):
        """Initialize the JokeGenerator."""
        self.session = requests.Session()
    
    def get_random_joke(self, joke_type: str = "Any") -> Optional[Dict]:
        """
        Fetch a random joke from the API.
        
        Args:
            joke_type (str): Type of joke - "Any", "General", "Programming", "Knock-knock"
            
        Returns:
            Dict: Joke data or None if request fails
        """
        try:
            url = f"{self.BASE_URL}/{joke_type}"
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching joke: {e}")
            return None
    
    def display_joke(self, joke_data: Dict) -> None:
        """
        Display the joke in a formatted way.
        
        Args:
            joke_data (Dict): The joke data from API
        """
        if not joke_data or joke_data.get("error"):
            print("Could not retrieve a joke. Please try again.")
            return
        
        if joke_data.get("type") == "single":
            # Single-part joke
            print(f"\n😄 {joke_data.get('joke')}\n")
        elif joke_data.get("type") == "twopart":
            # Two-part joke (setup and delivery)
            print(f"\n😄 Setup: {joke_data.get('setup')}")
            print(f"   Delivery: {joke_data.get('delivery')}\n")
    
    def get_multiple_jokes(self, count: int = 5, joke_type: str = "Any") -> list:
        """
        Fetch multiple random jokes.
        
        Args:
            count (int): Number of jokes to fetch
            joke_type (str): Type of joke
            
        Returns:
            list: List of joke data
        """
        jokes = []
        for _ in range(count):
            joke = self.get_random_joke(joke_type)
            if joke:
                jokes.append(joke)
        return jokes
    
    def save_jokes_to_file(self, jokes: list, filename: str = "jokes.json") -> None:
        """
        Save jokes to a JSON file.
        
        Args:
            jokes (list): List of jokes to save
            filename (str): Output filename
        """
        try:
            with open(filename, 'w') as f:
                json.dump(jokes, f, indent=2)
            print(f"✅ Jokes saved to {filename}")
        except IOError as e:
            print(f"Error saving jokes: {e}")


def main():
    """Main function to demonstrate the JokeGenerator."""
    print("🎭 Welcome to Random Joke Generator! 🎭")
    print("=" * 50)
    
    generator = JokeGenerator()
    
    # Get and display a single joke
    print("\n📝 Fetching a random joke...\n")
    joke = generator.get_random_joke()
    generator.display_joke(joke)
    
    # Get multiple jokes
    print("📚 Fetching 3 programming jokes...\n")
    jokes = generator.get_multiple_jokes(count=3, joke_type="Programming")
    for i, joke_data in enumerate(jokes, 1):
        print(f"Joke {i}:")
        generator.display_joke(joke_data)
    
    # Save jokes to file
    if jokes:
        generator.save_jokes_to_file(jokes)
    
    print("=" * 50)
    print("✨ Thank you for using Random Joke Generator! ✨")


if __name__ == "__main__":
    main()