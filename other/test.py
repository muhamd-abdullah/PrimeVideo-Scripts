a = ['x-amz-id-2', 'x-amz-request-id', 'Vary', 'x-amz-storage-class', 'x-amz-server-side-encryption', 'x-amz-meta-dv-checksum-sha-1', 'x-amz-meta-dv-checksum-md5', 'x-amz-meta-dv-checksum-sha-256', 'Accept-Ranges', 'Content-Type', 'Server', 'X-LLID', 'Age', 'Date', 'Content-Length', 'X-Server-IP', 'Access-Control-Allow-Origin', 'Access-Control-Allow-Headers', 'Access-Control-Allow-Methods', 'Timing-Allow-Origin', 'Access-Control-Max-Age', 'Access-Control-Expose-Headers']
b = ['Content-Type', 'Content-Length', 'Connection', 'Date', 'Last-Modified', 'ETag', 'x-amz-storage-class', 'x-amz-server-side-encryption', 'x-amz-meta-dv-checksum-sha-1', 'x-amz-meta-dv-checksum-md5', 'x-amz-meta-dv-checksum-sha-256', 'Accept-Ranges', 'Server', 'X-Cache', 'Via', 'X-Amz-Cf-Pop', 'X-Amz-Cf-Id', 'Age']
c = set(b)-set(a)
print(list(c))

d = set(a)-set(b)
print(list(d))
