from convert import convtoconf, parse

with open('../../example.md') as f:
    markdown = convtoconf(f.read())
    print(markdown)
