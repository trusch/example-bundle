import grpc
import frunner_pb2_grpc
import frunner_pb2
import json
import sys

class Frunner:
    def __init__(self, gateway, caCert):
        creds = grpc.ssl_channel_credentials(root_certificates=open(caCert,"rb").read())
        channel = grpc.secure_channel(gateway, creds)
        self.conn = frunner_pb2_grpc.FunctionRunnerStub(channel)

    def run(self, expr, input, output):
        try:
            metadata = []
            parts = expr.split("|")
            for part in parts:
                fnExprParts = part.split(" ")
                fn = fnExprParts[0]
                args = fnExprParts[1:]
                metadata.append(("chain",fn))
                metadata.append(("options",json.dumps(args)))
            input = self.buildInput(input)
            for res in self.conn.Run(input, metadata=metadata):
                output.write(res.data)
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def buildInput(self, input):
        if type(input) == "<class 'str'>":
            print('got string, make iter!')
            return iter([frunner_pb2.Data(data=input.encode('utf-8'))])
        return input
