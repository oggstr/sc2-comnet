content = None
with open("model.md", "r") as f:
    content = f.readlines()
    content = [line.replace("  ", " ") for line in content]

with open("model.md", "w") as f:
    f.writelines(content)