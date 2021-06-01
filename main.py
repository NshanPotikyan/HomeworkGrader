import argparse
import configs as cf

from graders import Grader

parser = argparse.ArgumentParser(description="Homework checking.")

parser.add_argument('--path', default=None,
                    help="The path to the jupyter notebook files.")
parser.add_argument('--mode', default=None,
                    help="The grading mode, supports either 'per_problem' or 'per_student' grading")
parser.add_argument('--nr_problems', type=int, default=None,
                    help="The number of problems to be checked, \
                     if None, then the number of problems will be determined automatically from one of the files.")

args = parser.parse_args()

if __name__ == "__main__":
    if args.path:
        path = args.path
    else:
        path = cf.path

    if args.mode:
        mode = args.mode
    else:
        mode = cf.mode

    if args.nr_problems:
        nr_problems = args.nr_problems
    else:
        nr_problems = cf.nr_problems

    grader = Grader(path=path, student_ids=cf.student_ids, mode=mode, nr_problems=nr_problems)
    grader.grade()
