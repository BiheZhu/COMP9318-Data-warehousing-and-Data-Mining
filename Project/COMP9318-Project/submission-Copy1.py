import os
import helper
def fool_classifier(test_data): ## Please do not change the function defination...
    ##..................................#
    ##..................................#
    ## Read the test data file, i.e., 'test_data.txt' from Present Working Directory...
    with open(test_data,'r') as test:
        samples = [line.strip().split(' ') for line in test]
    ##..................................#    
    ##..................................#
    
    ## You are supposed to use pre-defined class: 'strategy()' in the file `helper.py` for model training (if any),
    #  and modifications limit checking
    strategy_instance=helper.strategy() 
    parameters={} 
    ##..................................#
    ##..................................#
    
    ## Your implementation goes here....#    
    v_class0 = {}
    v_class1 = {}
    # vocabulary of class0 with word frequency
    for row in strategy_instance.class0:
        for word in row:
            if word in v_class0:
                temp = { word: v_class0[word] + 1 }
                v_class0.update(temp)
            else:
                temp = { word: 1 }
                v_class0.update(temp)
    # vocabulary of class1 with word frequency
    for row in strategy_instance.class1:
        for word in row:
            if word in v_class1:
                temp = { word: v_class1[word] + 1 }
                v_class1.update(temp)
            else:
                temp = { word: 1 }
                v_class1.update(temp)
    #v_class0 = sorted(v_class0.items(), key=lambda x: x[1], reverse = True)  
    #v_class0 = sorted(v_class0.items(), key=lambda x: x[1], reverse = True)  
    diff_dict = {}
    for word in v_class0:
        if word not in v_class1:
            diff_dict[word] = v_class0[word]
    diff_list = list( sorted(diff_dict.items(), key=lambda x: x[1], reverse = True))
    
    ##..................................#
    ##..................................#
    
    total_modify = 20 
    for sample in samples:
        sample_set = set(sample)
        tag = []
        nb_of_type = [0, 0, 0, 0]
        for word in range(len(sample)):
            if sample[word] in v_class1 and sample[word] in v_class0:
                if v_class1[sample[word]] > 2 * v_class0[sample[word]] and v_class1[sample[word]] - v_class0[sample[word]] >= 5:
                # replace those words with those which only exists in v_class0
                    tag.append(2)
                    nb_of_type[2] += 1
                else:
                    tag.append(1)
                    nb_of_type[1] += 1
            elif sample[word] in v_class1 and sample[word] not in v_class0:
            # delete all of them if possible(nb < 20) and add words only exists in b 
                tag.append(3)
                nb_of_type[3] += 1
            elif sample[word] not in v_class1 and sample[word] in v_class0:
                tag.append(0)
                nb_of_type[0] += 1
            elif sample[word] not in v_class1 and sample[word] not in v_class0:
                tag.append(1)
                nb_of_type[1] += 1
        
        record_dict = {}
        nb_modify = 0
        j = 0
        for tag_num in range(4, 0, -1):
            for i in range(len(sample)):
                if sample[i] in record_dict:
                    tmp = sample[i]
                    sample[i] = record_dict[tmp]
                else:
                    if nb_modify < total_modify:
                        if tag[i] == tag_num:
                            nb_modify += 2
                            if j == len(diff_list):                         
                                j = 0
                            if diff_list[j][0] in sample_set:
                                for t in range(j+1, len(diff_list), 1):
                                    if diff_list[t][0] not in sample_set:
                                        j = t
                                        break
                            record_dict.update( {sample[i]: diff_list[j][0]} )
                            sample[i] = diff_list[j][0]
                            j += 1
                    else:
                        break
        for i in range(len(sample)):
            if sample[i] in record_dict:
                tmp = sample[i]
                sample[i] = record_dict[tmp]
        #print(record_dict)
    ##..................................#
    ##..................................#
    
    ## Write out the modified file, i.e., 'modified_data.txt' in Present Working Directory...
    #set current working directory
    path = os.getcwd()
    os.chdir(path)
    file = open('modified_data.txt','w')
    for s in range(len(samples)):
        line = ' '.join(samples[s])
        file.write(line)
        file.write(" \n")
    file.close()
    ##..................................#
    ##..................................#
    #print(s)
    ##You can check that the modified text is within the modification limits.
    modified_data='./modified_data.txt'
    assert strategy_instance.check_data(test_data, modified_data)
    return strategy_instance ## NOTE: You are required to return the instance of this class.