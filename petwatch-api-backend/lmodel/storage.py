import boto3

class Storage(object):
    def __init__(self, 
                 uri='http://localhost:9000', 
                 access_key='minio_access_key', 
                 secret_key='minio_secret_key'):
        self.uri = uri
        self.access_key = access_key
        self.secret_key = secret_key
        self.s3 = boto3.client(
            's3',
            endpoint_url=self.uri,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

    def create_bucket(self, bucket):
        # Verificar se o bucket existe e, se não existir, criar
        existing_buckets = [b['Name'] for b in self.s3.list_buckets()['Buckets']]
        if bucket not in existing_buckets:
            self.s3.create_bucket(Bucket=bucket)

    def upload(self, bucket, file_local, file_target):
        # Verificar se o bucket existe e, se não existir, criar
        self.create_bucket(bucket)

        # Fazer o upload do arquivo
        self.s3.upload_file(file_local, bucket, file_target)

    def list_objects(self, bucket):
        # Listar objetos no bucket
        response = self.s3.list_objects(Bucket=bucket)
        for obj in response.get('Contents', []):
            print(obj['Key'])

# Exemplo de uso:
if __name__ == "__main__":
    s3_storage = Storage(uri='http://localhost:9000', access_key='minio_access_key', secret_key='minio_secret_key')
    s3_storage.upload('mybucket', 'local_file.txt', 'remote_file.txt')
    s3_storage.list_objects('mybucket')
