import csv
import sys

# reverse row order in a csv file 
# save new file as '<name-of-old-file>-reversed.csv'
def reverseCSV(file):
    newfile = file[:file.find('.')] + "-reversed.csv"
    with open(file) as fr, open(newfile,"w",newline="") as fw:
        cr = csv.reader(fr,delimiter=";")
        cw = csv.writer(fw,delimiter=";")
        cw.writerow(next(cr))
        cw.writerows(reversed(list(cr)))
    print("New file:", newfile)

if __name__ == "__main__":
    reverseCSV(sys.argv[1])
