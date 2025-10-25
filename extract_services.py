import json

def extract_links(data):
    """
    Recursively extract all non-null 'link' values from the JSON data structure.
    """
    links = []
    
    if isinstance(data, dict):
        # If current item has a 'link' field and it's not null, add it to the list
        if 'link' in data and data['link'] is not None:
            links.append(data['link'])
        
        # Recursively process all values in the dictionary
        for value in data.values():
            links.extend(extract_links(value))
    
    elif isinstance(data, list):
        # Recursively process all items in the list
        for item in data:
            links.extend(extract_links(item))
    
    return links

# Load the JSON data
with open("services.json", "r", encoding="utf-8") as f:
    services = json.load(f)

# Extract all links
all_links = extract_links(services)

# Base URL to prepend to relative links
base_url = "https://www.elitebodyhome.com"

# Write all links to links.txt file with base URL prepended
with open("links.txt", "w", encoding="utf-8") as f:
    for link in all_links:
        # If link already starts with http/https, use it as is
        if link.startswith(('http://', 'https://')):
            full_url = link
        else:
            # For relative links, prepend the base URL
            full_url = base_url + link
        f.write(full_url + "\n")

# Print summary
print("All links found in the JSON:")
print("=" * 50)
for i, link in enumerate(all_links, 1):
    print(f"{i:3d}. {link}")

print(f"\nTotal links found: {len(all_links)}")
print(f"All links have been written to 'links.txt'")
