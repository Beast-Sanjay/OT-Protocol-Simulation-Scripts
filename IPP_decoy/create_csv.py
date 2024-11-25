import csv

frame_list = []
s7_list = [["No.","Time","Source","Destination","Protocol","Length","TCP payload","Info"]]
with open("frame_numbers_filter.txt",'r') as f:
    content = f.read()
    frame_list = eval(content)


print(frame_list,' =========== frame list')

with open("s7comm.csv",'r',errors='ignore') as file:
    csv_reader  = csv.reader(file)
    next(csv_reader)

    for row in csv_reader:
        #print(row[0],' ------------ 00000000')
        if int(row[0]) in frame_list:
            print(row,' ----- xxxxxxxxxxxxxxxx')
            s7_list.append(row)


with open("s7comm_filter.csv", mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write the data to the CSV file row by row
    for row in s7_list:
        csv_writer.writerow(row)
