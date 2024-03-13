```markdown
# google_it Library

The `google_it` library provides a simple interface to perform various Google searches and extract information from the search results.

## Installation

You can install the `google_it` library using pip:

```bash
pip install google_it
```

Once installed, you can import the library into your Python code using:

```python
import google_it
```

## Code Examples

### Performing a Google Search

You can perform a Google search using the `search` function. Here's an example:

```python
import google_it

query = "OpenAI"
results = google_it.search(query)

for result in results:
    print(result.title)
    print(result.url)
    print(result.description)
    print()
```

### Getting Top Stories

You can retrieve top stories from Google using the `top_stories` function. Here's how:

```python
import google_it

top_stories = google_it.top_stories()

for story in top_stories:
    print(story.title)
    print(story.url)
    print()
```

### Translating Text

You can use the `translate` function to translate text from one language to another:

```python
import google_it

source_text = "Hello, world!"
target_language = "es"

translation = google_it.translate(source_text, target_language)
print("Translated Text:", translation)
```

### Getting Weather Information

You can retrieve weather information using the `weather` function:

```python
import google_it

weather_info = google_it.weather(location="New York")
print("Location:", weather_info.location)
print("Forecast:", weather_info.forecast)
print("Temperature:", weather_info.temperature)
```

These are just a few examples of how you can use the `google_it` library to interact with Google search results and extract useful information. Check out the documentation for more functions and features!

