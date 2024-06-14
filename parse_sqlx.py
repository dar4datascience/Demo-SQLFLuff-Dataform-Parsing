import re

def extract_section(content, section_name):
    # Use regex to find the section
    pattern = re.compile(f'({section_name} {{(?:[^{{}}]+|{{(?:[^{{}}]+|{{[^{{}}]*}})*}})*}})', re.DOTALL)
    match = pattern.search(content)

    if match:
        section_content = match.group(1).strip()
        start_pos = match.start()
        end_pos = match.end()

        # Find the line numbers for the start and end positions
        start_line = content[:start_pos].count('\n') + 1
        end_line = content[:end_pos].count('\n') + 1

        return section_content, start_line, end_line

    return None, None, None



def map_sqlx_to_dict(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    line_dict = {i+1: line.strip() for i, line in enumerate(lines)}

    return line_dict

# Example usage
file_path = "demo.sqlx"
line_dict = map_sqlx_to_dict(file_path)
#print(line_dict)

# First, map the .sqlx file to a dictionary
file_path = "demo.sqlx"
line_dict = map_sqlx_to_dict(file_path)

# Then, read the .sqlx file content
with open(file_path, 'r') as file:
    content = file.read()

# Now, extract the 'config' section
config_content, config_start_line, config_end_line = extract_section(content, 'config')
print(f"Config section content:\n{config_content}")
print(f"Config section starts at line: {config_start_line}")
print(f"Config section ends at line: {config_end_line}")

# Extract the 'declare' section
declare_content, declare_start_line, declare_end_line = extract_section(content, 'declare')
print(f"Declare section content:\n{declare_content}")
print(f"Declare section starts at line: {declare_start_line}")
print(f"Declare section ends at line: {declare_end_line}")


def extract_sql(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Remove block comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # Extract config and declare sections
    config_section, config_start, config_end = extract_config(content)
    print(config_section)
    declare_section, declare_start, declare_end = extract_declare(content)
    print(declare_section)

    # Remove config and declare sections from content
    content = content[:config_start] + content[config_end:]
    content = content[:declare_start] + content[declare_end:]

    # Extract SQL transformation logic
    pattern = re.compile(r'SQL transformation logic\s*{(.*?)\}', re.DOTALL)
    match = pattern.search(content)
    if match:
        sql_logic = match.group(1).strip()
    else:
        return None

    # Replace ${ref("table_name")} with table_name
    sql_logic = re.sub(r'\$\{ref\("([^"]+)"\)\}', r'\1', sql_logic)

    return sql_logic.strip()

# # Example usage
# file_path = "demo.sqlx"
# pure_sql = extract_sql(file_path)
# print("Pure SQL:\n", pure_sql)
