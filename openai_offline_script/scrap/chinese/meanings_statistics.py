import os
# read all meanings file txt in a loop
files = os.listdir('dream_meaning')

print("total file count",len(files))
total = 0
example_analysis_count=0
phyco_count=0
old_book_source = 0
stock =0
for file in files:
    total+=1
    with open(f'dream_meaning\\{file}', 'r', encoding='utf-8') as f:
        meanings = f.read()
        if '案例分析' in meanings:
            example_analysis_count+=1
            continue
        if '心理学解梦' in meanings:
            phyco_count+=1
            continue
        if '原版周公解梦' in meanings:
            old_book_source+=1
            continue
        if '周公股市' in meanings:
            stock+=1
            continue
        else:
            print(file)

        

print("total",total)

print("example_analysis_count",example_analysis_count)
print("phyco_count",phyco_count)
print("old_book_source",old_book_source)
print("stock",stock)

