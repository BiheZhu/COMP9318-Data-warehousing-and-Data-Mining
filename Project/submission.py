# Written by Bin Zhu and Bihe Zhu
import os
import helper



def fool_classifier(test_data): ## Please do not change the function defination...
    strategy_instance=helper.strategy() 
    parameters={} 
    ##..................................#
    ##..................................#
    
    ##..................................#
    ##..................................#
    with open(test_data,'r') as test:
        samples = [line.strip().split(' ') for line in test]            
    ##..................................#
    ##..................................#
    ## Your implementation goes here....# 
    v_class0 = {}
    v_class1 = {}
    W_dict=dict() # the w dictionary
    Seta = 0.001  # learning speed
    
    # vocabulary of class0 with word occurence
    row_c0 = 0
    for row in strategy_instance.class0:
        row_c0 += 1
        row_set = set(row)
        for word in row_set:
        #for word in row:
            if word in v_class0:
                temp = { word: v_class0[word] + 1 }
                v_class0.update(temp)
            else:
                temp = { word: 1 }
                v_class0.update(temp)
            if word in W_dict:
                continue
            else:
                temp_1 = { word: 0.0 }
                W_dict.update(temp_1)

    total_class0 = sum(v_class0.values())
    #print(total_class0)
    #print(list( sorted(v_class0.items(), key=lambda x: x[1], reverse = True))[0:30], '\n')

    # vocabulary of class1 with word occurence
    row_c1 = 0
    for row in strategy_instance.class1:
        row_c1 += 1
        row_set = set(row)
        for word in row_set:
        #for word in row:
            if word in v_class1:
                temp = { word: v_class1[word] + 1 }
                v_class1.update(temp)
            else:
                temp = { word: 1 }
                v_class1.update(temp)
            if word in W_dict:
                continue
            else:
                temp_1 = { word: 0.0 }
                W_dict.update(temp_1)
    total_class1 = sum(v_class1.values())
    #print(total_class1)
    #print(list( sorted(v_class1.items(), key=lambda x: x[1], reverse = True))[0:30], '\n')

    # print(row_c0/row_c1)
    iteration = 1
    while(iteration<=2000):
        for eachrow in strategy_instance.class0:
            word_set = set(eachrow)
            sum0 = 0
            for eachword in word_set:
                sum0 += W_dict[eachword]
            while(sum0 >= -5):
                for eachword in word_set:
                    W_dict[eachword] = W_dict[eachword]-Seta
                sum0 =0
                for eachword in word_set:
                    sum0 += W_dict[eachword]

        for eachrow in strategy_instance.class1:
            word_set = set(eachrow)
            sum0 = 0
            for eachword in word_set:
                sum0 += W_dict[eachword]
            while(sum0 <= 5):
                for eachword in word_set:
                    W_dict[eachword] = W_dict[eachword]+(row_c0/row_c1)*Seta
                sum0 =0
                for eachword in word_set:
                    sum0 += W_dict[eachword]
                    
        iteration += 1
    # print(len(W_dict))
    # print(W_dict)
##    for each in W_dict:
##        print(type(each))
##        print(each)

    W_list = []
    for each in W_dict:
        W_list.append([each,W_dict[each]])
    # print(len(W_list))
    W_list.sort(key =lambda x:x[1]) # w from small to big
    # W_list = W_list_temp
    # 这一行妄图根据w的值将W_list进行从小到大排序总是出错，拜托朱队长帮忙看看是啥问题
    
    # print(W_list_temp)
    modified_samples = []
    for sample in samples:
        length = len(sample)
        new_sample = []
        sample_word_set = set(sample)
        sample_w_list = []
        change_record=dict()
        for eachword in sample_word_set:
            if eachword in W_dict:
                sample_w_list.append([eachword, W_dict[eachword]])
            else:
                sample_w_list.append([eachword, 0.0])
            
        sample_w_list.sort(key =lambda x:x[1], reverse = True) # w from big to small
        # print(sample_w_list)
        # print(test_w_list)
        nb_modify = 0
        i = 0
        j = 0
        while(nb_modify<20):  # 替换
            if sample_w_list[i][1] <= 0: # 所有该被替换的词都被替换过了。但是没够20次修改
                break
            else:
                if W_list[j][0] in sample_word_set:
                    j += 1
                    continue
                else:
                    temp_dict = { sample_w_list[i][0]:W_list[j][0] }
                    change_record.update(temp_dict)
                    i += 1
                    j += 1
                    nb_modify += 2
        if (sample_w_list[i][1] <= 0): # 如果替换结束之后未达到20， 进行下一步的增加
            while(nb_modify<20):
                new_sample.append(W_list[j][0])
                j += 1
                nb_modify += 1
        # print(len(change_record))
        # print(change_record)
        # print(new_sample)
        k = 0   # 开始根据change_record进行统一替换操作
        while(k<length):
            if sample[k] in change_record:
                new_sample.append(change_record[sample[k]])

            else:
                new_sample.append(sample[k])
            k += 1
        # print(len((set(new_sample)-set(sample)) | (set(sample)-set(new_sample))))
        modified_samples.append(new_sample)
        
    
    ##..................................#
    ##..................................#
    ## Write out the modified file, i.e., 'modified_data.txt' in Present Working Directory...
    #set current working directory
    path = os.getcwd()
    os.chdir(path)
    file = open('modified_data.txt','w')
    for s in range(len(modified_samples)):
        line = ' '.join(modified_samples[s])
        file.write(line)
        file.write(" \n")
    file.close()
    ##..................................#
    ##..................................#
    ##You can check that the modified text is within the modification limits.
    modified_data='./modified_data.txt'
    assert strategy_instance.check_data(test_data, modified_data)
    return strategy_instance ## NOTE: You are required to return the instance of this class.



# fool_classifier("test_data.txt")
# just for testing on our own mechine


