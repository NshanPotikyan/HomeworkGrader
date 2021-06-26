import json
from code_similarity import detect, summarize


def join(text):
    """
    Helper function to join the strings in a list
    :param text: list of strings
    :returns: string
    """
    return ''.join(text)


def notebook_to_dict(file_name):
    """
    Function for loading the jupyter notebook as a dict
    :param file_name: str of the .ipynb file name
    :return: dict
    """
    file = open(file_name, mode='r', encoding="utf8")
    return json.load(file)


def dict_to_notebook(some_dict, file_name):
    """
    Function for writing a jupyter notebook (JN) file (.ipynb)
    from a dict
    :param some_dict: dict that has a special format for JN files
    :param file_name: str of the JN file name
    :return:
    """
    with open(file_name, mode='w') as f:
        json.dump(some_dict, f)


def insert_cell(notebook, position, content, content_type):
    """
    Inserts a new text cell inside the given notebook
    :param notebook: dict of the JN file
    :param position: int of the cell positional index
    :param content: str of the content that needs to be added
    :param content_type: str of the content type, currently it can be one of these
                         'grade', 'comment', 'total_grade'
    :return: dict of the modified JN file
    """
    notebook['cells'].insert(position,
                             create_new_cell(content=content,
                                             content_type=content_type))
    return notebook


def create_new_cell(content, content_type):
    """
    Generates a new text cell that will be added to the existing notebook
    :param content: str of the content that needs to be added
    :param content_type: str of the content type, currently it can be one of these
                         'grade', 'comment', 'total_grade', 'empty'
    :return:
    """
    if content_type == 'grade':
        title = "<font color='red'>**Grade:**</font>"
    elif content_type == 'empty':
        title = ""
        content = ""
    elif content_type == 'comment':
        title = "<font color='red'>**Comment:**</font>"
    elif content_type == 'total_grade':
        title = "<font color='red'>**Total Grade:**</font>"
    else:
        raise Exception(f"""The content_type was not specified correctly.
        Should be one of these 'grade', 'comment', 'total_grade', 'empty', but {content_type}
        was provided.
        """)
    return {'cell_type': 'markdown',
            'metadata': {'id': ''},
            'source': [f'{title} {content}']}


def hamming_dist(str1, str2):
    """
    Calculates the hamming distance between two strings
    :param str1:
    :param str2:
    :return: float
    """
    dist = 0
    for i in range(len(str1)):
        dist += (str2[i] != str1[i]) * 1
    return dist


def detect_summarize(pycode_list, names, tolerance_level=0.9):
    """
    Goes over all code strings and looks for potential plagiarism
    :param pycode_list: list of str containing python code
    :param names: list of str containing student names
    :param tolerance_level: float of the plagiarism tolerance level
    :return:
    """
    cheaters = []
    for i in range(len(pycode_list)):
        results = detect(pycode_list[i:], keep_prints=True, module_level=True)
        for index, func_ast_diff_list in results:
            sum_plagiarism_percent, _, _ = summarize(func_ast_diff_list)
            if sum_plagiarism_percent > tolerance_level:
                print('{:.2f} % of {} code structure is similar with {} code structure.'.format(
                    sum_plagiarism_percent * 100, names[i], names[index + i]))
                print(names[i], pycode_list[i], sep='\n****\n')
                print(names[i+index], pycode_list[i+index], sep='\n****\n')
                penalize = input('Do you want to penalize for plagiarism? Yes(1) or No(2)')
                if penalize:
                    cheaters.append([names[i], names[i+index]])
    return cheaters
