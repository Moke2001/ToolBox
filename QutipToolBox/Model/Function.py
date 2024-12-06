class  Function:
    def __init__(self,function,uuid):
        self.function=function
        self.uuid=uuid

    def MyFunction(self,t,args):
        function_params=args.get(self.uuid,None)
        return self.function(t,function_params)
