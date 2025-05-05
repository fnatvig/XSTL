import pandas as pd

def get_wnd_avg(arr, wnd_goose_pkt_num):
    new_arr = []
    for i in range(len(arr)):

        if i > wnd_goose_pkt_num[i]:
            new_element = 0
            k=0
            for j in range(i, i-wnd_goose_pkt_num[i],-1):
                new_element += arr[j]
                k+=1
            new_arr.append(new_element/k)
        elif i == 0:
            new_arr.append(arr[0]/1)
        else:
            new_element = 0
            k=0
            for j in range(i, -1,-1):
                new_element += arr[j]
                k+=1
            new_arr.append(new_element/k)

    return new_arr

def get_wnd_goose_pkt_num(arr, t_seconds):
    wnd_goose_pkt_num = []
    t, k = 0, 0 
    for i in range(len(arr)):
        
        while t<t_seconds:
            if (i-k) >= 0:
                t += arr[i]-arr[i-k]
                k +=1
            else:
                break
        wnd_goose_pkt_num.append(k)
        t, k = 0, 0 
    return wnd_goose_pkt_num

def get_wnd_avg_goose_data_length(arr, wnd_goose_pkt_num):
    return get_wnd_avg(arr, wnd_goose_pkt_num)

def get_wnd_avg_goose_pkt_interval(arr, wnd_goose_pkt_num):
    return get_wnd_avg(arr, wnd_goose_pkt_num)

def get_wnd_goose_pkt_num_of_same(arr, wnd_goose_pkt_num):
    wnd_goose_pkt_num_of_same_event = []
    for i in range(len(arr)):

        if i > wnd_goose_pkt_num[i]:
            new_element = 0
            for j in range(i, i-wnd_goose_pkt_num[i],-1):
                if arr[j] == arr[i]:
                    new_element += 1
            wnd_goose_pkt_num_of_same_event.append(new_element)
        elif i == 0:
            wnd_goose_pkt_num_of_same_event.append(1)
        else:
            new_element = 0
            for j in range(i, -1,-1):
                if arr[j] == arr[i]:
                    new_element += 1
            wnd_goose_pkt_num_of_same_event.append(new_element)

    return wnd_goose_pkt_num_of_same_event

def get_wnd_goose_num_of_all_events(arr, wnd_goose_pkt_num):
    wnd_goose_pkt_num_of_all_events = []
    for i in range(len(arr)):
        sublist = []
        if i > wnd_goose_pkt_num[i]:
            for j in range(i, i-wnd_goose_pkt_num[i],-1):
                sublist.append(arr[j])
        else:
            for j in range(i, -1,-1):
                sublist.append(arr[j])

        wnd_goose_pkt_num_of_all_events.append(len(set(sublist)))

    return wnd_goose_pkt_num_of_all_events

def get_wnd_goose_pkt_num_of_greater_than_current_sqNum(arr, wnd_goose_pkt_num):
    wnd_goose_pkt_num_of_greater_than_current_sqNum = []
    for i in range(len(arr)):

        if i > wnd_goose_pkt_num[i]:
            new_element = 0
            for j in range(i, i-wnd_goose_pkt_num[i],-1):
                if arr[j] > arr[i]:
                    new_element += 1
            wnd_goose_pkt_num_of_greater_than_current_sqNum.append(new_element)
        elif i == 0:
            wnd_goose_pkt_num_of_greater_than_current_sqNum.append(1)
        else:
            new_element = 0
            for j in range(i, -1,-1):
                if arr[j] > arr[i]:
                    new_element += 1
            wnd_goose_pkt_num_of_greater_than_current_sqNum.append(new_element)

    return wnd_goose_pkt_num_of_greater_than_current_sqNum

def get_wnd_goose_num_of_all_datSet(arr, wnd_goose_pkt_num):
    wnd_goose_num_of_all_datSet = get_wnd_goose_num_of_all_events(arr, wnd_goose_pkt_num)
    return wnd_goose_num_of_all_datSet

def get_wnd_goose_num_of_same_source(arr, wnd_goose_pkt_num):
    wnd_goose_num_of_same_source  = get_wnd_goose_pkt_num_of_same(arr, wnd_goose_pkt_num)
    return wnd_goose_num_of_same_source

def get_wnd_goose_num_of_all_source(arr, wnd_goose_pkt_num):
    wnd_goose_num_of_all_source  = get_wnd_goose_num_of_all_events(arr, wnd_goose_pkt_num)
    return wnd_goose_num_of_all_source

def get_wnd_goose_num_of_same_dest(arr, wnd_goose_pkt_num):
    wnd_goose_num_of_same_dest  = get_wnd_goose_pkt_num_of_same(arr, wnd_goose_pkt_num)
    return wnd_goose_num_of_same_dest

def get_wnd_goose_num_of_all_dest(arr, wnd_goose_pkt_num):
    wnd_goose_num_of_all_dest  = get_wnd_goose_num_of_all_events(arr, wnd_goose_pkt_num)
    return wnd_goose_num_of_all_dest

def get_advanced_features(df, t_seconds):
    wnd_goose_pkt_num = get_wnd_goose_pkt_num(df.loc[:, 'EpochArrivalTime'], t_seconds)
    wnd_avg_goose_data_length = get_wnd_avg_goose_data_length(df.loc[:, "Length"], wnd_goose_pkt_num)
    wnd_avg_goose_pkt_interval = get_wnd_avg_goose_pkt_interval(df.loc[:, "timeInterval"], wnd_goose_pkt_num)
    wnd_goose_pkt_num_of_same_event = get_wnd_goose_pkt_num_of_same(df.loc[:, "stNum"], wnd_goose_pkt_num)
    wnd_goose_pkt_num_of_same_numDat = get_wnd_goose_pkt_num_of_same(df.loc[:, "numDatSetEntries"], wnd_goose_pkt_num)
    wnd_goose_pkt_num_of_same_goID = get_wnd_goose_pkt_num_of_same(df.loc[:, "goID"], wnd_goose_pkt_num)
    wnd_goose_pkt_num_of_all_events = get_wnd_goose_num_of_all_events(df.loc[:, "stNum"], wnd_goose_pkt_num)
    wnd_goose_pkt_num_of_same_sqNum = get_wnd_goose_pkt_num_of_same(df.loc[:, "sqNum"], wnd_goose_pkt_num)
    wnd_goose_pkt_num_of_greater_than_current_sqNum = get_wnd_goose_pkt_num_of_greater_than_current_sqNum(df.loc[:, "sqNum"], wnd_goose_pkt_num)
    wnd_goose_pkt_num_of_same_datSet = get_wnd_goose_pkt_num_of_same(df.loc[:, "datSet"], wnd_goose_pkt_num) 
    wnd_goose_num_of_all_datSet = get_wnd_goose_num_of_all_datSet(df.loc[:, "datSet"], wnd_goose_pkt_num) 
    wnd_goose_num_of_same_source = get_wnd_goose_num_of_same_source(df.loc[:, "Source"], wnd_goose_pkt_num) 
    wnd_goose_num_of_all_source = get_wnd_goose_num_of_all_source(df.loc[:, "Source"], wnd_goose_pkt_num) 
    wnd_goose_num_of_same_dest = get_wnd_goose_num_of_same_dest(df.loc[:, "Destination"], wnd_goose_pkt_num) 
    wnd_goose_num_of_all_dest = get_wnd_goose_num_of_all_dest(df.loc[:, "Destination"], wnd_goose_pkt_num) 
    return pd.DataFrame(list(zip(wnd_goose_pkt_num,
                         wnd_avg_goose_data_length,
                         wnd_avg_goose_pkt_interval,
                         wnd_goose_pkt_num_of_same_event,
                         wnd_goose_pkt_num_of_all_events,
                         wnd_goose_pkt_num_of_same_sqNum,
                         wnd_goose_pkt_num_of_greater_than_current_sqNum,
                         wnd_goose_pkt_num_of_same_datSet,
                         wnd_goose_pkt_num_of_same_numDat,
                         wnd_goose_pkt_num_of_same_goID,
                         wnd_goose_num_of_all_datSet,
                         wnd_goose_num_of_same_source,
                         wnd_goose_num_of_all_source,
                         wnd_goose_num_of_same_dest,
                         wnd_goose_num_of_all_dest
                         )), 
                         columns = ['wnd_goose_pkt_num',
                         'wnd_avg_goose_data_length',
                         'wnd_avg_goose_pkt_interval',
                         'wnd_goose_pkt_num_of_same_event',
                         'wnd_goose_pkt_num_of_all_events',
                         'wnd_goose_pkt_num_of_same_sqNum',
                         'wnd_goose_pkt_num_of_greater_than_current_sqNum',
                         'wnd_goose_pkt_num_of_same_datSet',
                         'wnd_goose_pkt_num_of_same_numDat',
                         'wnd_goose_pkt_num_of_same_goID',
                         'wnd_goose_num_of_all_datSet',
                         'wnd_goose_num_of_same_source',
                         'wnd_goose_num_of_all_source',
                         'wnd_goose_num_of_same_dest',
                         'wnd_goose_num_of_all_dest'
                         ])

def preprocess_df(df, wnd_size):
    new_df = pd.DataFrame()
    new_df = pd.concat([new_df, get_advanced_features(df, wnd_size)], axis=1)
    return new_df


