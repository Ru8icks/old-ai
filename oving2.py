import numpy as nump

#observation model
observation = nump.array([[0.9, 0.0],[0.0, 0.2]])
#dynamic model
dynamic = nump.array([[0.7, 0.3],[0.3 , 0.7]])
#initial probability of rain
initial_prob = nump.array([0.5, 0.5])
#evidence of rain
evidence = [True, True, False, True, True]



def forward(fw_vector, evidence, observation, dynamic):
    if not evidence:
        #getting correct observation odds based on presence off umbrella (true false)
        observation = nump.eye(len(observation))-observation
    #equation 15.12    
    result = nump.dot(observation, nump.transpose(dynamic))
    result = nump.dot(result, fw_vector)
    
    return normalise(result)
    
    #help function for normalise
def normalise(v):
    return v/v.sum()
    
    
def backward(bw_vector, evidence, observation, dynamic):
    #setting correct observation
    if not evidence:
        observation = nump.eye(len(observation))-observation
    #equation 15.13
    result = nump.dot(dynamic, observation)
    result = nump.dot(result, bw_vector)
    #normalising result on return
    return normalise(result)
    
def forward_backward(evidence, initial_prob, observation, dynamic):
    #length of evidence array
    ev_length = len(evidence) + 1
    #initialise empty forward message array
    fw = nump.array([None]*ev_length)
    #add initial probability to the array
    fw[0] = initial_prob
    print "forward: "
    #forward result
    for i in range(1, ev_length):
        fw[i] = forward(fw[i-1], evidence[i-1], observation, dynamic)
        print " %i : %s" %(i, fw[i])
    #smoothin and backward initialisation 
    sm = nump.array([None]*ev_length)
    sm[0] = initial_prob
    bw = nump.array([1,1])
    print "backward: "
    #for all backward
    for j in range(ev_length-1, -1, -1):
        # normalize and calculate new probability on account of the previous value
        sm[j] = normalise(fw[j]*bw)
        print " %i : %s" %(j, bw)
        bw = backward(bw, evidence[j-1], observation, dynamic)
    print "smoothed: "
    for k in range(len(sm)):
        print "%i: %s" %(k, sm[k])
    return
    
    
result = forward_backward(evidence, initial_prob, observation, dynamic)

