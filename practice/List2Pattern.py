import re

# Function to extract pattern from a list of strings
def extract_pattern(strings, pattern):
    extracted = []
    for string in strings:
        matches = re.findall(pattern, string)
        extracted.extend(matches)
    return extracted


def main():
    # Example usage
    list_of_strings = ['abc123', 'def456', 'ghi789', 'abc456']
    pattern = r'abc(\d+)'

    # Extract the pattern
    extracted_patterns = extract_pattern(list_of_strings, pattern)

    # Print the results
    print(extracted_patterns)


if __name__ == '__main__':
    main()