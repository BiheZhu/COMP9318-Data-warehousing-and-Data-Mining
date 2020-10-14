## import modules here 
import pandas as pd
import numpy as np


################# Question 1 #################

# helper functions
def project_data(df, d):
    # Return only the d-th column of INPUT
    return df.iloc[:, d]

def select_data(df, d, val):
    # SELECT * FROM INPUT WHERE input.d = val
    col_name = df.columns[d]
    return df[df[col_name] == val]

def remove_first_dim(df):
    # Remove the first dim of the input
    return df.iloc[:, 1:]

def slice_data_dim0(df, v):
    # syntactic sugar to get R_{ALL} in a less verbose way
    df_temp = select_data(df, 0, v)
    return remove_first_dim(df_temp)

def deepcopy(L):
    # copy the elements of L to a
    a = []
    for x in L:
        a.append(x)
    return a

def single_tuple(input_data):
    # binary code: 0000, 0001, 0010, .... , 1111 (dim = 4)
    # or 000, 001, 010, ... , 111 (dim = 3)
    # in which the '1' represents 'ALL' 

    num_of_dims = input_data.shape[1] - 1
    rows = 2 ** num_of_dims
    vals = list(input_data.loc[0])
    L = []
    for i in range(rows):
        temp = bin(i)
        result = temp[2:]
        L.append(result)
    final = []
    for i in L:
        if len(i) < num_of_dims:
            temp = '0' * (num_of_dims-len(i)) + i
            i = temp
        final.append(i)
    result = []
    for code in final:
        temp = deepcopy(vals)
        for j in range(len(code)):
            if code[j] == '1':
                temp[j] = 'ALL'
        result.append(temp)
    result = pd.DataFrame(result, columns=list(input_data))
    return result

def buc_rec(df, result, output):
    # Note that input is a DataFrame
    dims = df.shape[1]
    if dims == 1:
        # only the measure dim
        input_sum = sum(project_data(df, 0))   
        result.append(input_sum)
        output.loc[len(output)] = result
    else:
        # the general case
        dim0_vals = set(project_data(df, 0).values)        
        temp_result = deepcopy(result)        
        for dim0_v in dim0_vals:            
            result = deepcopy(temp_result)           
            sub_data = slice_data_dim0(df, dim0_v)            
            result.append(dim0_v)
            buc_rec(sub_data, result, output)
        ## for R_{ALL}
        sub_data = remove_first_dim(df)        
        result = deepcopy(temp_result)
        result.append("ALL")        
        buc_rec(sub_data, result, output)

def buc_rec_optimized(df):# do not change the heading of the function
    if df.shape[0] == 1:
        output = single_tuple(df)
    else:
        dims = list(df)
        output = pd.DataFrame(columns=dims)
        buc_rec(df, [], output)
    return output



################# Question 2 #################
def sse(arr):
    if len(arr) == 0: # deal with arr == []
        return 0.0

    avg = np.average(arr)
    val = sum( [(x-avg)*(x-avg) for x in arr] )
    return val

def v_opt_dp(x, num_bins):# do not change the heading of the function
    mark_matrix = [ [0 for j in range(len(x))] for i in range(num_bins) ]
    matrix = [ [-1 for j in range(len(x))] for i in range(num_bins) ]
    bins = []
    mark_bin = []
    for i in range(num_bins):
        for j in range(len(x)-1, -1, -1):           
            if i+j == len(x) - 1:    # 5 
                matrix[i][j] = 0
                mark_matrix[i][j] = j+1
            elif i+j >= len(x) or i+j < num_bins - 1:   # >=6 or < 3
                matrix[i][j] = -1
            elif i == 0:
                matrix[i][j] = sse(x[j:])
            else:
                mincost = 1000000000
                mark = -1
                for y in range(j+1, len(x)):
                    if matrix[i-1][y] >= 0:
                        cost = sse(x[j:y]) + matrix[i-1][y]
                        temp_cost = min(mincost, cost)
                        if temp_cost < mincost:
                            mark = y
                            mincost = temp_cost                    
                mark_matrix[i][j] = mark
                matrix[i][j] = mincost
    total_min_cost = matrix[num_bins-1][0]
    temp_cost = total_min_cost
    mark_bin.append(0)
    j = 0
    for i in range(num_bins-1, 0, -1):
        mark_bin.append(mark_matrix[i][j])
        j = mark_matrix[i][j]
    for i in range(num_bins):
        if i < num_bins - 1:
            bins.append( x[ mark_bin[i] : mark_bin[i+1] ] )
        else:
            bins.append( x[ mark_bin[i] : len(x) ] )
    print('mark_bin: ', mark_bin)
    return matrix, bins 