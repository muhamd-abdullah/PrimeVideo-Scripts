import re


def cgen_adultswim(url, num_chunks):
    print("Generating for adultswim:")
    print(url, "\n")
    chunks = []
    parts = url.split('_')
    
    if len(parts) != 2:
        print("Invalid input URL format.")
        return chunks
    
    base_url = parts[0]
    #numeric_part = int(parts[1].split('.')[0])
    extension = parts[1].split('.')[1]
    
    for i in range(num_chunks):
        #next_numeric_part = numeric_part + i + 1
        next_numeric_part = i
        next_url = f"{base_url}_{next_numeric_part:05d}.{extension}"
        chunk = {"url":next_url, "req_headers":""}
        chunks.append(chunk)
        
    for chunk in chunks:
        print(chunk["url"])

    return chunks

# TESTS ADULTSWIM
sample_url = "https://tve-vod-aka.warnermediacdn.com/adultswim/9f01069006faff6854097179a2e7c1db/layer3/seg-0_00000.ts"
cgen_adultswim(sample_url, 12)




def cgen_vimeo(url, num_chunks):
    print("Generating for vimeo")
    chunks = []
    if "&range=" in url:
        start_bytes = 0
        end_bytes = 1000000
        step_bytes = 1000000 # 1 MB
        base_url = url.rsplit("&")[0]
        for i in range(num_chunks):
            range_string = f"&range={start_bytes}-{end_bytes}"
            segment_url = base_url + range_string
            start_bytes = end_bytes + 1
            end_bytes = start_bytes + step_bytes
            chunk = {"url":segment_url, "req_headers":""}
            chunks.append(chunk)
    elif "segment-" in url:
        segment_match = re.search(r'(.*?/segment-)(\d+)(\.m4s)', url)
        if segment_match:
            base_url = segment_match.group(1)
            start_segment = 1
            end_segment = num_chunks 
            for segment_number in range(start_segment, end_segment + 1):
                segment_url = f"{base_url}/segment-{segment_number}.m4s"
                chunk = {"url":segment_url, "req_headers":""}
                chunks.append(chunk)
    
    for chunk in chunks:
        print(chunk["url"])
    
    return chunks

# TESTS VIMEO
#sample_url = "https://119vod-adaptive.akamaized.net/exp=1691705537~acl=%2F3c5db4ab-c884-446e-9f0b-47ef888eb226%2F%2A~hmac=20b894eb84b902fa9a5f831faab7f4069207b7cf39747daf5deb2449f4810884/3c5db4ab-c884-446e-9f0b-47ef888eb226/sep/video/f9d97343/chop/segment-1.m4s?r=dXM%3D"
#sample_url2 = "https://57vod-adaptive.akamaized.net/exp=1691706100~acl=%2Fc6fdb06c-4caa-4abd-aa1d-799b218dab70%2F%2A~hmac=2eb6a7b91e8dba565d05dc4dd2b01fc241250059ca9e0229b620a207300b4ddd/c6fdb06c-4caa-4abd-aa1d-799b218dab70/parcel/video/3c832955.mp4?r=dXMtd2VzdDE%3D&range=2519023-3777328"
#cgen_vimeo(sample_url, 12)
#cgen_vimeo(sample_url2, 12)




def cgen_tubi(url, num_chunks):
    print("Generating for tubi")
    chunks = []
    
    if "/segment" in url and "fastly" in url:
        base_url =  url.rsplit("-",1)[0]
        extension =  ".ts"
        for i in range(num_chunks):
            url = f"{base_url}-{i}{extension}"
            chunk = {"url":url, "req_headers":""}
            chunks.append(chunk)
    
    elif "akamai" in url:
        print("YESSS")
        start_bytes = 0
        end_bytes = 1000000
        step_bytes = 1000000 # 1 MB
        for i in range(num_chunks):
            chunk = {"url": url, "req_headers":f"bytes={start_bytes}-{end_bytes}"}
            chunks.append(chunk)
            start_bytes = end_bytes + 1
            end_bytes = start_bytes + step_bytes
        
    for chunk in chunks:
        print(chunk["url"],"\t",chunk["req_headers"])

# TESTS TUBI
#sample_url = "https://fastly2.tubi.video/c63cfa29-d32b-434a-85c8-37ad66a7b09c/vtgr1tdl/segment-0.ts"
#sample_url2 = "https://akamai2.tubi.video/b376b585-d98c-4f5e-af60-2d59091ca928/gmot5scc.mp4"
#cgen_tubi(sample_url, 12)
#cgen_tubi(sample_url2, 12)




def cgen_prime(url, num_chunks):
    print("Generating for prime")
    chunks = []
    start_bytes = 0
    end_bytes = 1000000
    step_bytes = 1000000 # 1 MB
    for i in range(num_chunks):
        chunk = {"url": url, "req_headers":f"bytes={start_bytes}-{end_bytes}"}
        chunks.append(chunk)
        start_bytes = end_bytes + 1
        end_bytes = start_bytes + step_bytes

    for chunk in chunks:
        print(chunk["url"],"\t",chunk["req_headers"])

# TESTS PRIME
#sample_url = "https://s3-iad-2.cf.dash.row.aiv-cdn.net/dm/2$z99FsFQc9GVQ-BbYi9I5NP0-R4Y~/2638/2bf6/a889/41e8-bd41-75eae2acb49c/b0963d1d-8ddc-4cdb-af4f-d05eded76934_video_7.mp4?amznDtid=AOAGZA014O5RE"
#cgen_prime(sample_url, 12)




def cgen_magellantv(url, num_chunks):
    print("Generating for magellantv")
    chunks = []
    base_url =  url.rsplit("-",1)[0]
    extension =  ".ts"
    for i in range(num_chunks):
        url = f"{base_url}-{i+1}{extension}"
        chunk = {"url":url, "req_headers":""}
        chunks.append(chunk)

    for chunk in chunks:
        print(chunk["url"])

# TEST MAGELLANTV
#sample_url = "https://videos-cloudfront-usp.jwpsrv.com/64d24a0b_e1da24b1f73a6fc423bc5a845d2c8f1d3c2200fd/site/4pSWjNlc/media/3Ha1yKxn/version/1bt18qWQ/manifest.ism/manifest-audio_eng=112000-video_eng=327574-1.ts"
#cgen_magellantv(sample_url, 12)




def cgen_pbs(url, num_chunks):
    print("Generating for pbs")
    chunks = []
    parts = url.split('_')
    
    if len(parts) != 2:
        print("Invalid input URL format.")
        return chunks
    
    base_url = parts[0]
    extension = parts[1].split('.')[1]
    
    for i in range(num_chunks):
        next_numeric_part = i
        next_url = f"{base_url}_{next_numeric_part:05d}.{extension}"
        chunk = {"url":next_url, "req_headers":""}
        chunks.append(chunk)
        
    for chunk in chunks:
        print(chunk["url"])

    return chunks

# TEST PBS
#sample_url = "https://ga.video.cdn.pbs.org/videos/star-gazers/55fdcc0d-33e7-4905-b235-663d7de62cf3/2000369296/hd-16x9-mezzanine-1080p/stgz326web-hls-16x9-1080p-234p-145k_00001.ts"
#cgen_pbs(sample_url, 12)




def cgen_vudu(url, num_chunks):
    print("Generating for vudu:\n",url,"\n")
    chunks = []
    if "/range/" in url:
        start_bytes = 0
        end_bytes = 1000000
        step_bytes = 1000000 # 1 MB
        base_url = url.rsplit("?",1)[0].rsplit("/",1)[0]
        remaining_url = url.rsplit("?")[1]
        for i in range(num_chunks):
            range_string = f"{start_bytes}-{end_bytes}"
            segment_url = base_url + "/" + range_string + "?" + remaining_url
            start_bytes = end_bytes + 1
            end_bytes = start_bytes + step_bytes
            chunk = {"url":segment_url, "req_headers":""}
            chunks.append(chunk)
    
    for chunk in chunks:
        print(chunk["url"])

# TEST VUDU
#sample_url = "https://ic-2d907100-09fae4-4vuduavod.s.loris.llnwd.net/132/5315941/dash/h264-1000.mp4/range/1035-244575?s=1692118494&e=1692205494&u=87791344&p=46&h=112fc11bd596cb99eccc3e2b91079a09"
#cgen_vudu(sample_url, 12)




def cgen_crackle(url, num_chunks):
    print("Generating for crackle\n",url,"\n")
    chunks = []
    base_url =  url.rsplit("_",1)[0]
    extension =  ".mp4"
    for i in range(num_chunks):
        url = f"{base_url}_{i+1}{extension}"
        chunk = {"url":url, "req_headers":""}
        chunks.append(chunk)

    for chunk in chunks:
        print(chunk["url"])

# TEST CRACKLE
#sample_url = "https://prod-vod-cdn1.crackle.com/fef95e6b5ee695e858b64691c95f580f/us-west-2/out/v1/09cc668698c84218bc3359ef6779fb7f/cc1a04f1519a4e01acf1471c93fb6e40/0c95bacd7d024a70a637a132e386d300/7dff831647c843b7b1ab778ef3643566/index_video_4_0_init.mp4"
#cgen_crackle(sample_url, 12)




def cgen_plutotv(url,num_chunks):
    print("Generating for plutotv")
    url = url.split("?")[0]
    print(url,"\n")

    chunks = []
    base_url = url.rsplit('/',1)[0]
    extension = ".m4s"
    
    for i in range(num_chunks):
        next_numeric_part = i + 1
        next_url = f"{base_url}/{next_numeric_part:05d}{extension}"
        chunk = {"url":next_url, "req_headers":""}
        chunks.append(chunk)
        
    for chunk in chunks:
        print(chunk["url"])

    return chunks

# TEST PLUTOTV
#sample_url = "https://siloh-sp.plutotv.net/304_18_ad/creative/646ae977cca99a90ac0b1aa8_ad/720p/20230522_040303/dash/video/240p-300/00001.m4s?CMCD=bl%3D30200%2Cbr%3D348%2Cd%3D5000%2Cdl%3D30200%2Cmtp%3D26200%2Cot%3Dv%2Crtp%3D300%2Csf%3Dd%2Csid%3D%22d1df4799-f872-4518-93b0-6e26039257ff%22%2Cst%3Dv%2Ctb%3D385"
#cgen_plutotv(sample_url, 12)