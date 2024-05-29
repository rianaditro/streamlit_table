# import pandas as pd


# get index for slicing list
def get_index(txt_file:str)->list:
    indexes = []
    i = 0
    for i in range(len(txt_file)):
        if '[Statistics of calls on module #' in txt_file[i] or '------------------------------------------------------------------------------' in txt_file[i]:
            indexes.append(i)
    del indexes[:4]
    return indexes

def format_dict(text:list, keys:list)->dict:
    result = dict()
    text = text.split(' ')
    text = [i for i in text if i != '']
    # i = 0
    for i in range(len(text)):
        result[keys[i]] = text[i].replace('\n','').replace('\r','')
        # i += 1
    # add ASR column calls/calls+failed
    print(result)
    calls = int(result['calls'])
    failed = int(result['failed'])
    calls_failed = calls + failed
    try:
        asr = (calls/calls_failed) * 100
        result['asr'] = round(asr, 1)
    except ZeroDivisionError:
        result['asr'] = 0
    return result

def format_list(raw_list:list,keys:list,module_no:int)->list:
    result = []
    for item in raw_list:
        data_dict = format_dict(item,keys)
        data_dict['module'] = '#m' + str(module_no)
        result.append(data_dict)
    return result

def extract_module_32(txt_file):
    indexes = get_index(txt_file)
    keys = ['sim', 'net', 'grp', 'minutes', 'hms', 'calls', 'reject', 'failed', 'coffs', 'smses']
    result = []
    for i, start in enumerate(range(2,len(indexes),5)):
        data_per_module = txt_file[indexes[start]+1:indexes[start]+5]
        data_per_module = format_list(data_per_module, keys,i)
        result.extend(data_per_module)
    return result

def extract_module_4(txt_file):
    indexes = get_index(txt_file)
    print(indexes)
    result = []
    keys = ['module', '-', 'reset', 'minutes', 'hms', 'calls', 'reject', 'failed', 'coffs', 'smses']
    for i, start in enumerate(range(1,len(indexes),5)):
        data_per_module = [txt_file[indexes[start]+1]]
        data_per_module = format_list(data_per_module, keys,i)
        result.extend(data_per_module)
    return result
    


# if __name__ == '__main__':
#     with open('statistics 32 module.txt','r') as f:
#         module32 = f.readlines()

#     with open('statistics(7).txt','r') as f:
#         module4 = f.readlines()

#     # m32 = extract_module_32(module32)
    

#     m4 = extract_module_4(module4)
        
#     df = pd.DataFrame(m4)
#     df.to_excel('output.xlsx')