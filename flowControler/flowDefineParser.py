#-*- coding="utf-8" -*-
import json
import os

class FlowDefineParser:
    def parse(filename):
        r = os.getcwd()
        path = os.path.join(r+"/data/flow_youxiangzhuce.json")
        with open(path) as flow_info:
            flow = json.load(flow_info, encoding="utf-8")
            # for i in flow:
            print(flow)


x = FlowDefineParser()
x.parse()

