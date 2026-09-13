# Drill D (ceiling): generalize into a reusable function
# define a reusable function taking a filename and a keyword
# Return a list of lines in `filename` containing `keyword`
def file_name_fun(filename,keyword):
    with open(filename) as f:
            list = []

            for line in f:
                if keyword in line:
                    list.append(line)

    return list
           
         

print(file_name_fun("data/demo_service.log","INFO") )
