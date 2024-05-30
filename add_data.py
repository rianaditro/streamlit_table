import random, pandas


def new_data(module):

    calls = random.randint(0,100)
    failed = random.randint(0,100)
    asr = calls/(calls+failed)

    if module == 'module_4':
        data = [{'module':0, '-':0, 'reset':0, 'minutes':0, 'hms':0, 'calls':calls, 'reject':0, 'failed':failed, 'coffs':0, 'smses':0,'asr':asr}]
    elif module == 'module_32':
        data = [{'module':0, 'sim':0, 'net':0, 'minutes':0, 'hms':0, 'calls':calls, 'reject':0, 'failed':failed, 'coffs':0, 'smses':0,'asr':asr}]
    elif module == 'module_ge':
        data = [{'mobile_port':0, 'port_status':0, 'signal_strenght':0, 'call_duration':0, 'dialed_calls':0, 'successfull_calls':calls, 'asr':asr, 'acd':0, 'allocated_ammount':0, 'consumed_amount':0}]
        
    df = pandas.DataFrame(data)
    return df



