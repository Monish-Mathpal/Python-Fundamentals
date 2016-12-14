#sort list by second lowest grade
#Given the names and grades for each student in a Physics class of #'n' students, store them in a nested list and print the name(s) of any #student(s) having the second lowest grade.
#Note: If there are multiple students with the same grade, order #their names alphabetically and print each name on a new line.


n1 = int(input())
l_name_grade = [[input(),float(input())] for l_name_grade in range(n1)]
slowest = sorted(list(set([grade for name,grade in l_name_grade])))[1]

