from azure.storage.blob import *
import base64
from azure.storage.filedatalake import DataLakeFileClient , FileSystemClient
import sys

if __name__ == "__main__":
    connection_string = sys.argv[1]
    file = DataLakeFileClient.from_connection_string(eval(connection_string),file_system_name="gen-ai/raw", file_path="/flight_policy_rules.pdf")
    file_system = FileSystemClient.from_connection_string(eval(connection_string),file_system_name="gen-ai")

    paths = file_system.get_paths()
    print(f"paths:{paths}")
    for path in paths:
        if ".pdf" in path.name:
            file_client = file_system.get_file_client(path.name)
            print(f"file_client:{file_client}")
            mem_file = file_client.download_file()
            print(f"mem_file:{mem_file}")
            file_bytes = base64.b64encode(mem_file.readall())
            #print(f"file_bytes:{file_bytes}")
            encoded_utf_string = file_bytes.decode('utf-8')
            
            ##### Writing Byte content into Txt File ####  
            file_name = "/topics/"+path.name.split("/")[len(path.name.split("/"))-1].replace(".pdf",".txt")
            print(f"file_name:{file_name}")
            file_client = file_system.get_file_client(file_name)
            print(f"file_client:{file_client}")
            file_client.create_file()
            file_client.append_data(data=encoded_utf_string,offset=0)
            file_client.flush_data(len(encoded_utf_string))
