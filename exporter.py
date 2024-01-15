import ast
import importlib
import inspect
import autopep8
import os
import copy
from datetime import datetime


global code_to_compact
global custom_name
global name_of_modules


def get_source(module_name, class_name, path):
    class_code = ""
    try:
        if module_name != "":
            module = importlib.import_module(module_name)
            if os.path.dirname(inspect.getfile(module)).__contains__(path):
                class_code = inspect.getsource(getattr(module, class_name))
        else:
            module = importlib.import_module(class_name)
            if os.path.dirname(inspect.getfile(inspect)).__contains__(path):
                class_code = inspect.getsource(module)
        return class_code
    except Exception as e:
        print(f"Error importing or getting source: {e}")
        return ""


def merge_ranges(ranges):
    merged_ranges = []

    if not ranges:
        return merged_ranges

    current_range = ranges[0]

    for start, end in ranges[1:]:

        if current_range[1] == start:
            current_range = (current_range[0], end)
        else:
            merged_ranges.append(current_range)
            current_range = (start, end)

    merged_ranges.append(current_range)

    return merged_ranges


def separate_import_lines_from_the_code(file):
    file_tree = ast.parse(file)
    import_lines = []
    non_import_lines = []
    set_non_import_lines = set()
    for node in ast.walk(file_tree):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            import_lines.append((node.lineno - 1, node.end_lineno))
        elif (hasattr(node, 'lineno') and
              not (isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom) or isinstance(node, ast.Assign)
                   or isinstance(node, ast.alias))):
            for line in range(node.lineno - 1, node.end_lineno):
                set_non_import_lines.add((line, line + 1))
    non_import_lines = sorted(set_non_import_lines)
    # non_import_lines = merge_ranges(non_import_lines)
    # import_lines = merge_ranges(import_lines)
    return import_lines, non_import_lines


def get_module_attr(lines):
    import_lines_tree = ast.parse(lines)
    module_name = []
    class_name = []
    for node in ast.walk(import_lines_tree):
        if isinstance(node, ast.Import):
            temp_name_of_class = node.alias.name if isinstance(node, ast.alias) \
                else "".join([alias.name for alias in node.names])
            module_name.append("")
            class_name.append(temp_name_of_class)
        if isinstance(node, ast.ImportFrom):
            module_name.append(node.module)
            class_name.append(node.alias.name if isinstance(node, ast.alias)
                              else "".join([alias.name for alias in node.names]))
    return module_name, class_name


def replace_import_by_code(file, path):
    import_lines, non_import_lines = separate_import_lines_from_the_code(file)
    temp_import_lines = copy.copy(import_lines)
    modules_source_code = []
    module_attributes = None
    line_and_code = dict()
    new_code = ""
    for start, end in temp_import_lines:
        import_line = "\n".join(file.split("\n")[start: end])
        module_attributes = get_module_attr(import_line)
        if "".join(module_attributes[0]) != '':
            temp_import_lines.remove((start, end))
        else:
            new_code += import_line + "\n"
        for iterator in range(len(module_attributes[0])):
            module_code = get_source(module_attributes[0][iterator],
                                     module_attributes[1][iterator], path)
            if module_code != "":
                new_code += module_code + "\n"
                modules_source_code.append(module_code)
    for start, end in non_import_lines:
        non_import_line = "\n".join(file.split("\n")[start: end])
        new_code += non_import_line + "\n"
    return [new_code, import_lines, module_attributes[1], modules_source_code, non_import_lines]


def create_unique_file(original_filename):
    base, extension = os.path.splitext(original_filename)

    current_datetime = datetime.now()
    current_date = current_datetime.date()
    formatted_date = current_date.strftime("%Y_%m_%d")
    counter = 1
    new_filename = original_filename

    while os.path.exists(new_filename):
        counter += 1
        new_filename = f"{base}_duplicated_{formatted_date}({counter}){extension}"

    return new_filename


def export_compacted_code(code, specific_name, path):
    directory = os.path.join(path, 'exported_code')
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = directory + "/" + "compacted_code" + specific_name + ".py"
    file_name = create_unique_file(file_name)
    f = open(file_name, "x")
    f.write(autopep8.fix_code(code))
    f.close()


def get_manipulate_code_names(names):
    global name_of_modules
    for name in names:
        name_of_modules += "_" + name
    return name_of_modules


def define_custom_name():
    global custom_name
    custom_name = input("Write a custom name:")
    return custom_name


def menu(case_value, names):
    if case_value == 2:
        define_custom_name()
        return "_" + custom_name if custom_name != "" else menu(1, names)
    elif case_value == 1:
        return "_of_" + get_manipulate_code_names(names)
    else:
        # Handle other cases or return a default value
        return "_of_" + get_manipulate_code_names(names)


path_of_code_to_compact = None
root_path = os.path.abspath(os.curdir)
menu_input = 1

if __name__ == '__main__':
    path_of_code_to_compact = input("specify the path of the python code.\n")
    custom_name = ""
    menu_input = int(input(
        'Press 1 for a custom file name based on class names that have been manipulated\n'
        'Press 2 to write a custom file name\n'))
    code_to_compact = open(path_of_code_to_compact, "r").read()
    all_information = replace_import_by_code(code_to_compact, root_path)
    absolute_path = os.path.abspath(path_of_code_to_compact)
    name_of_modules = os.path.basename(absolute_path).replace('.py', '')

    export_compacted_code(all_information[0], menu(menu_input, all_information[2]), root_path)
    for element in all_information:
        print(element)
