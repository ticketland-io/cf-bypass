1. Install deps 

`pip3 install .`

2. Build proto buf definition

[Reference](https://grpc.io/docs/languages/python/basics/)

first install toos `pip3 install grpcio-tools`

```bash
 python3 -m grpc_tools.protoc -I ./proto --python_out=./src/grpc --pyi_out=./src/grpc --grpc_python_out=./src/grpc ./proto/file_server.proto
 ```

3. Run with `python3 .`
