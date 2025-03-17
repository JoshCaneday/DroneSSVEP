import numpy as np
import collections

class Threshold:
    def __init__(self):
        self.threshold = 200000
        self.data = collections.deque()
        # self.timestamps = collections.deque()
        self.curr_power = 0
        self.channel = 0
    

    def calibrate(self, normal_samples, blink_samples):
        # Expect normal_samples and blink_samples  to be 5 x 200 samples
        normal_power = np.mean(np.square(normal_samples[self.channel])) * 600
        blink_power = np.mean(np.square(blink_samples[self.channel])) * 600

        self.threshold = (normal_power + blink_power) / 2

    def check_threshold(self, data):
        # expect data to be 1 x 8
        '''
        returns returns true if blink detected

        '''
        self.data.append(data[self.channel] ** 2)
        self.curr_power += data[self.channel] ** 2
        if len(self.data) < 600:
            return False
        #print(self.cur_power)
        res = False
        if self.curr_power > self.threshold:
            res = True
            self.data = collections.deque()
            self.curr_power = 0
        else:
            self.curr_power -= self.data.popleft()

        return res
    def create_threshold(self,data):
        # Expect data to be 2 x n x num_channels
        rest = np.array(data[0])
        squeeze = np.array(data[1])
        num_rest_samples = rest.shape[0]
        num_squeeze_samples = squeeze.shape[0]
        rest = np.sum(rest,axis=0)
        squeeze = np.sum(squeeze,axis=0)
        rest.squeeze()
        squeeze.squeeze()

        rest /= num_rest_samples
        squeeze /= num_squeeze_samples

        


        
