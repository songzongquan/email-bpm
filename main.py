from flowControler.flowControler import FlowControler
from common.config  import *

info = getMainEmailInfo()
print(info)



f = FlowControler()
f.main()

