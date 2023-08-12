import asyncio
from pyppeteer import launch
import csv
import time
import os

'''
Input: URL of the page containing list of all movies/tvs
Output: This returns individual URLs of the title page, videopage, and chunk of each movie/tv
'''

profile_path = '/Users/abdullah/Library/Application Support/Google/Chrome/Default'
exec_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# URLs of main pages that list all movies/tv of a particular category
urls_main = {
'url_action_movies' : "https://www.primevideo.com/browse/ref=atv_ge_aga_c_vqhlwi_1_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmZpZWxkLWdlbnJlLWJpbj1hdl9nZW5yZV9hY3Rpb24maW5kZXg9ZXUtYW1hem9uLXZpZGVvLWV1cm8mYWR1bHQtcHJvZHVjdD0wJmJxPShub3QgYXZfc2Vjb25kYXJ5X2dlbnJlOidhdl9zdWJnZW5yZV9pbnRlcm5hdGlvbmFsX2luZGlhJykmc2VhcmNoLWFsaWFzPWluc3RhbnQtdmlkZW8mcHZfb2ZmZXJzPUNIOkNIOnN2b2Q6cHJpbWU6dm9kOi0xNjg2Njk2MDAwOjE2ODY2OTYwMDAtJnFzLWF2X3JlcXVlc3RfdHlwZT00JnFzLWlzLXByaW1lLWN1c3RvbWVyPTIiLCJydCI6InZRSEx3aXNtciIsInR4dCI6IlByaW1lIG1vdmllcyIsIm9mZnNldCI6MCwibnBzaSI6MCwib3JlcSI6IjBhZjJmYTQ4LTM1MWUtNDlkMC1hODdiLTBmNmU1MTU0MmNkNjoxNjg2Njk2NTQ2MDAwIiwic3RyaWQiOiIxOjFQTUdSNDIxSDNOSzEjI01aUVdHWkxVTVZTRUdZTFNONTJYR1pMTSIsIm9yZXFrIjoiMTJ5OHhUelFqalBwZExhYzVvdU5PVU9jKzFzcElKSVV6Tm1GaHVwUERIVT0iLCJvcmVxa3YiOjF9&jic=8%7CEgRzdm9k",
'url_action_tv' : "https://www.primevideo.com/browse/ref=atv_ge_aga_c_7kl2bw_2_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmZmllbGQtZ2VucmUtYmluPWF2X2dlbnJlX2FjdGlvbiZpbmRleD1ldS1hbWF6b24tdmlkZW8tZXVybyZhZHVsdC1wcm9kdWN0PTAmYnE9KG5vdCBhdl9zZWNvbmRhcnlfZ2VucmU6J2F2X3N1YmdlbnJlX2ludGVybmF0aW9uYWxfaW5kaWEnKSZzZWFyY2gtYWxpYXM9aW5zdGFudC12aWRlbyZwdl9vZmZlcnM9Q0g6Q0g6c3ZvZDpwcmltZTp2b2Q6LTE2ODY3Mzk4MDA6MTY4NjczOTgwMC0mcXMtYXZfcmVxdWVzdF90eXBlPTQmcXMtaXMtcHJpbWUtY3VzdG9tZXI9MiIsInJ0IjoiN2tsMmJXc21yIiwidHh0IjoiUHJpbWUgVFYgc2hvd3MiLCJvZmZzZXQiOjAsIm5wc2kiOjAsIm9yZXEiOiIyNzM5OWE1OS1mNmNiLTQ2N2UtYmVhYS1lZWUzMmFjZmFkNWI6MTY4NjczOTk4NTAwMCIsInN0cmlkIjoiMToxMTZPUktFM0pWNEVIViMjTVpRV0daTFVNVlNFR1lMU041MlhHWkxNIiwib3JlcWsiOiIxMnk4eFR6UWpqUHBkTGFjNW91Tk9VT2MrMXNwSUpJVXpObUZodXBQREhVPSIsIm9yZXFrdiI6MX0%3D&jic=8%7CEgRzdm9k",
'url_anime_movies' : "https://www.primevideo.com/browse/ref=atv_ge_aga_c_vqhlwi_1_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmZpZWxkLWdlbnJlLWJpbj1hdl9nZW5yZV9hbmltZSZpbmRleD1ldS1hbWF6b24tdmlkZW8tZXVybyZhZHVsdC1wcm9kdWN0PTAmYnE9KG5vdCBhdl9zZWNvbmRhcnlfZ2VucmU6J2F2X3N1YmdlbnJlX2ludGVybmF0aW9uYWxfaW5kaWEnKSZzZWFyY2gtYWxpYXM9aW5zdGFudC12aWRlbyZwdl9vZmZlcnM9Q0g6Q0g6c3ZvZDpwcmltZTp2b2Q6LTE2ODY3Mzk4MDA6MTY4NjczOTgwMC0mcXMtYXZfcmVxdWVzdF90eXBlPTQmcXMtaXMtcHJpbWUtY3VzdG9tZXI9MiIsInJ0IjoidlFITHdpc21yIiwidHh0IjoiUHJpbWUgbW92aWVzIiwib2Zmc2V0IjowLCJucHNpIjowLCJvcmVxIjoiNjk5ZDliYjktMTZlMi00OGJlLTlkNDgtZDJmZjQ2MGVlMDFkOjE2ODY3NDAyOTYwMDAiLCJzdHJpZCI6IjE6MVBNR1I0MjFIM05LMSMjTVpRV0daTFVNVlNFR1lMU041MlhHWkxNIiwib3JlcWsiOiIxMnk4eFR6UWpqUHBkTGFjNW91Tk9VT2MrMXNwSUpJVXpObUZodXBQREhVPSIsIm9yZXFrdiI6MX0%3D&jic=8%7CEgRzdm9k",
'url_anime_tv' : "https://www.primevideo.com/browse/ref=atv_ge_aga_c_7kl2bw_2_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmZmllbGQtZ2VucmUtYmluPWF2X2dlbnJlX2FuaW1lJmluZGV4PWV1LWFtYXpvbi12aWRlby1ldXJvJmFkdWx0LXByb2R1Y3Q9MCZicT0obm90IGF2X3NlY29uZGFyeV9nZW5yZTonYXZfc3ViZ2VucmVfaW50ZXJuYXRpb25hbF9pbmRpYScpJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnB2X29mZmVycz1DSDpDSDpzdm9kOnByaW1lOnZvZDotMTY4NjczOTgwMDoxNjg2NzM5ODAwLSZxcy1hdl9yZXF1ZXN0X3R5cGU9NCZxcy1pcy1wcmltZS1jdXN0b21lcj0yIiwicnQiOiI3a2wyYldzbXIiLCJ0eHQiOiJQcmltZSBUViBzaG93cyIsIm9mZnNldCI6MCwibnBzaSI6MCwib3JlcSI6IjY5OWQ5YmI5LTE2ZTItNDhiZS05ZDQ4LWQyZmY0NjBlZTAxZDoxNjg2NzQwMjk2MDAwIiwic3RyaWQiOiIxOjExNk9SS0UzSlY0RUhWIyNNWlFXR1pMVU1WU0VHWUxTTjUyWEdaTE0iLCJvcmVxayI6IjEyeTh4VHpRampQcGRMYWM1b3VOT1VPYysxc3BJSklVek5tRmh1cFBESFU9Iiwib3JlcWt2IjoxfQ%3D%3D&jic=8%7CEgRzdm9k",
'url_comedy_movies' : "https://www.primevideo.com/browse/ref=atv_ge_agc_c_vqhlwi_1_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmZpZWxkLWdlbnJlLWJpbj1hdl9nZW5yZV9jb21lZHkmaW5kZXg9ZXUtYW1hem9uLXZpZGVvLWV1cm8mYWR1bHQtcHJvZHVjdD0wJmJxPShub3QgYXZfc2Vjb25kYXJ5X2dlbnJlOidhdl9zdWJnZW5yZV9pbnRlcm5hdGlvbmFsX2luZGlhJykmc2VhcmNoLWFsaWFzPWluc3RhbnQtdmlkZW8mcHZfb2ZmZXJzPUNIOkNIOnN2b2Q6cHJpbWU6dm9kOi0xNjg2NzM5ODAwOjE2ODY3Mzk4MDAtJnFzLWF2X3JlcXVlc3RfdHlwZT00JnFzLWlzLXByaW1lLWN1c3RvbWVyPTIiLCJydCI6InZRSEx3aXNtciIsInR4dCI6IlByaW1lIG1vdmllcyIsIm9mZnNldCI6MCwibnBzaSI6MCwib3JlcSI6ImZhYjZhMjQ3LTE2YTItNGYzNS1iYWUxLTY5ZGE1N2I2YmZiZjoxNjg2NzQwMDc4MDAwIiwic3RyaWQiOiIxOjFQTUdSNDIxSDNOSzEjI01aUVdHWkxVTVZTRUdZTFNONTJYR1pMTSIsIm9yZXFrIjoiMTJ5OHhUelFqalBwZExhYzVvdU5PVU9jKzFzcElKSVV6Tm1GaHVwUERIVT0iLCJvcmVxa3YiOjF9&jic=8%7CEgRzdm9k",
'url_comedy_tv' : "https://www.primevideo.com/browse/ref=atv_ge_agc_c_7kl2bw_2_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmZmllbGQtZ2VucmUtYmluPWF2X2dlbnJlX2NvbWVkeSZpbmRleD1ldS1hbWF6b24tdmlkZW8tZXVybyZhZHVsdC1wcm9kdWN0PTAmYnE9KG5vdCBhdl9zZWNvbmRhcnlfZ2VucmU6J2F2X3N1YmdlbnJlX2ludGVybmF0aW9uYWxfaW5kaWEnKSZzZWFyY2gtYWxpYXM9aW5zdGFudC12aWRlbyZwdl9vZmZlcnM9Q0g6Q0g6c3ZvZDpwcmltZTp2b2Q6LTE2ODY3Mzk4MDA6MTY4NjczOTgwMC0mcXMtYXZfcmVxdWVzdF90eXBlPTQmcXMtaXMtcHJpbWUtY3VzdG9tZXI9MiIsInJ0IjoiN2tsMmJXc21yIiwidHh0IjoiUHJpbWUgVFYgc2hvd3MiLCJvZmZzZXQiOjAsIm5wc2kiOjAsIm9yZXEiOiJmYWI2YTI0Ny0xNmEyLTRmMzUtYmFlMS02OWRhNTdiNmJmYmY6MTY4Njc0MDA3ODAwMCIsInN0cmlkIjoiMToxMTZPUktFM0pWNEVIViMjTVpRV0daTFVNVlNFR1lMU041MlhHWkxNIiwib3JlcWsiOiIxMnk4eFR6UWpqUHBkTGFjNW91Tk9VT2MrMXNwSUpJVXpObUZodXBQREhVPSIsIm9yZXFrdiI6MX0%3D&jic=8%7CEgRzdm9k",
'url_documentary_movies' : "https://www.primevideo.com/browse/ref=atv_ge_agd_c_vqhlwi_1_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmZpZWxkLWdlbnJlLWJpbj1hdl9nZW5yZV9kb2N1bWVudGFyeSZpbmRleD1ldS1hbWF6b24tdmlkZW8tZXVybyZhZHVsdC1wcm9kdWN0PTAmYnE9KG5vdCBhdl9zZWNvbmRhcnlfZ2VucmU6J2F2X3N1YmdlbnJlX2ludGVybmF0aW9uYWxfaW5kaWEnKSZzZWFyY2gtYWxpYXM9aW5zdGFudC12aWRlbyZwdl9vZmZlcnM9Q0g6Q0g6c3ZvZDpwcmltZTp2b2Q6LTE2ODY3Mzk4MDA6MTY4NjczOTgwMC0mcXMtYXZfcmVxdWVzdF90eXBlPTQmcXMtaXMtcHJpbWUtY3VzdG9tZXI9MiIsInJ0IjoidlFITHdpc21yIiwidHh0IjoiUHJpbWUgbW92aWVzIiwib2Zmc2V0IjowLCJucHNpIjowLCJvcmVxIjoiNjI4ZThlYzQtN2RmMi00YWQ1LWI0NTQtODA2NWFjYTllOTRkOjE2ODY3NDAzNDYwMDAiLCJzdHJpZCI6IjE6MVBNR1I0MjFIM05LMSMjTVpRV0daTFVNVlNFR1lMU041MlhHWkxNIiwib3JlcWsiOiIxMnk4eFR6UWpqUHBkTGFjNW91Tk9VT2MrMXNwSUpJVXpObUZodXBQREhVPSIsIm9yZXFrdiI6MX0%3D&jic=8%7CEgRzdm9k",
'url_documentary_tv' : "https://www.primevideo.com/browse/ref=atv_ge_agd_c_7kl2bw_2_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmZmllbGQtZ2VucmUtYmluPWF2X2dlbnJlX2RvY3VtZW50YXJ5JmluZGV4PWV1LWFtYXpvbi12aWRlby1ldXJvJmFkdWx0LXByb2R1Y3Q9MCZicT0obm90IGF2X3NlY29uZGFyeV9nZW5yZTonYXZfc3ViZ2VucmVfaW50ZXJuYXRpb25hbF9pbmRpYScpJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnB2X29mZmVycz1DSDpDSDpzdm9kOnByaW1lOnZvZDotMTY4NjczOTgwMDoxNjg2NzM5ODAwLSZxcy1hdl9yZXF1ZXN0X3R5cGU9NCZxcy1pcy1wcmltZS1jdXN0b21lcj0yIiwicnQiOiI3a2wyYldzbXIiLCJ0eHQiOiJQcmltZSBUViBzaG93cyIsIm9mZnNldCI6MCwibnBzaSI6MCwib3JlcSI6IjYyOGU4ZWM0LTdkZjItNGFkNS1iNDU0LTgwNjVhY2E5ZTk0ZDoxNjg2NzQwMzQ2MDAwIiwic3RyaWQiOiIxOjExNk9SS0UzSlY0RUhWIyNNWlFXR1pMVU1WU0VHWUxTTjUyWEdaTE0iLCJvcmVxayI6IjEyeTh4VHpRampQcGRMYWM1b3VOT1VPYysxc3BJSklVek5tRmh1cFBESFU9Iiwib3JlcWt2IjoxfQ%3D%3D&jic=8%7CEgRzdm9k",
'url_drama_movies' : "https://www.primevideo.com/browse/ref=atv_ge_agd_c_vqhlwi_1_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmZpZWxkLWdlbnJlLWJpbj1hdl9nZW5yZV9kcmFtYSZpbmRleD1ldS1hbWF6b24tdmlkZW8tZXVybyZhZHVsdC1wcm9kdWN0PTAmYnE9KG5vdCBhdl9zZWNvbmRhcnlfZ2VucmU6J2F2X3N1YmdlbnJlX2ludGVybmF0aW9uYWxfaW5kaWEnKSZzZWFyY2gtYWxpYXM9aW5zdGFudC12aWRlbyZwdl9vZmZlcnM9Q0g6Q0g6c3ZvZDpwcmltZTp2b2Q6LTE2ODY3Mzk4MDA6MTY4NjczOTgwMC0mcXMtYXZfcmVxdWVzdF90eXBlPTQmcXMtaXMtcHJpbWUtY3VzdG9tZXI9MiIsInJ0IjoidlFITHdpc21yIiwidHh0IjoiUHJpbWUgbW92aWVzIiwib2Zmc2V0IjowLCJucHNpIjowLCJvcmVxIjoiN2JkMDQ2MzItYTM1ZS00ZWU0LWJlMzAtZjA4N2M4ZGE5MGUzOjE2ODY3NDAxMzQwMDAiLCJzdHJpZCI6IjE6MVBNR1I0MjFIM05LMSMjTVpRV0daTFVNVlNFR1lMU041MlhHWkxNIiwib3JlcWsiOiIxMnk4eFR6UWpqUHBkTGFjNW91Tk9VT2MrMXNwSUpJVXpObUZodXBQREhVPSIsIm9yZXFrdiI6MX0%3D&jic=8%7CEgRzdm9k",
'url_drama_tv' : "https://www.primevideo.com/browse/ref=atv_ge_agd_c_7kl2bw_2_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmZmllbGQtZ2VucmUtYmluPWF2X2dlbnJlX2RyYW1hJmluZGV4PWV1LWFtYXpvbi12aWRlby1ldXJvJmFkdWx0LXByb2R1Y3Q9MCZicT0obm90IGF2X3NlY29uZGFyeV9nZW5yZTonYXZfc3ViZ2VucmVfaW50ZXJuYXRpb25hbF9pbmRpYScpJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnB2X29mZmVycz1DSDpDSDpzdm9kOnByaW1lOnZvZDotMTY4NjczOTgwMDoxNjg2NzM5ODAwLSZxcy1hdl9yZXF1ZXN0X3R5cGU9NCZxcy1pcy1wcmltZS1jdXN0b21lcj0yIiwicnQiOiI3a2wyYldzbXIiLCJ0eHQiOiJQcmltZSBUViBzaG93cyIsIm9mZnNldCI6MCwibnBzaSI6MCwib3JlcSI6IjdiZDA0NjMyLWEzNWUtNGVlNC1iZTMwLWYwODdjOGRhOTBlMzoxNjg2NzQwMTM0MDAwIiwic3RyaWQiOiIxOjExNk9SS0UzSlY0RUhWIyNNWlFXR1pMVU1WU0VHWUxTTjUyWEdaTE0iLCJvcmVxayI6IjEyeTh4VHpRampQcGRMYWM1b3VOT1VPYysxc3BJSklVek5tRmh1cFBESFU9Iiwib3JlcWt2IjoxfQ%3D%3D&jic=8%7CEgRzdm9k",
'url_fantasy_movies' : "https://www.primevideo.com/browse/ref=atv_ge_agf_c_vqhlwi_1_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmZpZWxkLWdlbnJlLWJpbj1hdl9nZW5yZV9mYW50YXN5JmluZGV4PWV1LWFtYXpvbi12aWRlby1ldXJvJmFkdWx0LXByb2R1Y3Q9MCZicT0obm90IGF2X3NlY29uZGFyeV9nZW5yZTonYXZfc3ViZ2VucmVfaW50ZXJuYXRpb25hbF9pbmRpYScpJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnB2X29mZmVycz1DSDpDSDpzdm9kOnByaW1lOnZvZDotMTY4Njc0MDQwMDoxNjg2NzQwNDAwLSZxcy1hdl9yZXF1ZXN0X3R5cGU9NCZxcy1pcy1wcmltZS1jdXN0b21lcj0yIiwicnQiOiJ2UUhMd2lzbXIiLCJ0eHQiOiJQcmltZSBtb3ZpZXMiLCJvZmZzZXQiOjAsIm5wc2kiOjAsIm9yZXEiOiJmMDgwZjg5MC1iMTliLTQwNjEtYjg1MS1jNWJkMTg1OWVjOTU6MTY4Njc0MDQwNDAwMCIsInN0cmlkIjoiMToxUE1HUjQyMUgzTksxIyNNWlFXR1pMVU1WU0VHWUxTTjUyWEdaTE0iLCJvcmVxayI6IjEyeTh4VHpRampQcGRMYWM1b3VOT1VPYysxc3BJSklVek5tRmh1cFBESFU9Iiwib3JlcWt2IjoxfQ%3D%3D&jic=8%7CEgRzdm9k",
'url_fantast_tv' : "https://www.primevideo.com/browse/ref=atv_ge_agf_c_7kl2bw_2_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmZmllbGQtZ2VucmUtYmluPWF2X2dlbnJlX2ZhbnRhc3kmaW5kZXg9ZXUtYW1hem9uLXZpZGVvLWV1cm8mYWR1bHQtcHJvZHVjdD0wJmJxPShub3QgYXZfc2Vjb25kYXJ5X2dlbnJlOidhdl9zdWJnZW5yZV9pbnRlcm5hdGlvbmFsX2luZGlhJykmc2VhcmNoLWFsaWFzPWluc3RhbnQtdmlkZW8mcHZfb2ZmZXJzPUNIOkNIOnN2b2Q6cHJpbWU6dm9kOi0xNjg2NzQwNDAwOjE2ODY3NDA0MDAtJnFzLWF2X3JlcXVlc3RfdHlwZT00JnFzLWlzLXByaW1lLWN1c3RvbWVyPTIiLCJydCI6IjdrbDJiV3NtciIsInR4dCI6IlByaW1lIFRWIHNob3dzIiwib2Zmc2V0IjowLCJucHNpIjowLCJvcmVxIjoiZjA4MGY4OTAtYjE5Yi00MDYxLWI4NTEtYzViZDE4NTllYzk1OjE2ODY3NDA0MDQwMDAiLCJzdHJpZCI6IjE6MTE2T1JLRTNKVjRFSFYjI01aUVdHWkxVTVZTRUdZTFNONTJYR1pMTSIsIm9yZXFrIjoiMTJ5OHhUelFqalBwZExhYzVvdU5PVU9jKzFzcElKSVV6Tm1GaHVwUERIVT0iLCJvcmVxa3YiOjF9&jic=8%7CEgRzdm9k",
'url_international_movies' : "https://www.primevideo.com/browse/ref=atv_ge_agi_c_vqhlwi_1_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmZpZWxkLWdlbnJlLWJpbj1hdl9nZW5yZV9pbnRlcm5hdGlvbmFsJmluZGV4PWV1LWFtYXpvbi12aWRlby1ldXJvJmFkdWx0LXByb2R1Y3Q9MCZicT0obm90IGF2X3NlY29uZGFyeV9nZW5yZTonYXZfc3ViZ2VucmVfaW50ZXJuYXRpb25hbF9pbmRpYScpJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnB2X29mZmVycz1DSDpDSDpzdm9kOnByaW1lOnZvZDotMTY4Njc0MDQwMDoxNjg2NzQwNDAwLSZxcy1hdl9yZXF1ZXN0X3R5cGU9NCZxcy1pcy1wcmltZS1jdXN0b21lcj0yIiwicnQiOiJ2UUhMd2lzbXIiLCJ0eHQiOiJQcmltZSBtb3ZpZXMiLCJvZmZzZXQiOjAsIm5wc2kiOjAsIm9yZXEiOiI4ZGE0YjEzNi1kNWI3LTRkMzEtYjgwMi1mMWNlNjg1ODFmYjI6MTY4Njc0MDQ0OTAwMCIsInN0cmlkIjoiMToxUE1HUjQyMUgzTksxIyNNWlFXR1pMVU1WU0VHWUxTTjUyWEdaTE0iLCJvcmVxayI6IjEyeTh4VHpRampQcGRMYWM1b3VOT1VPYysxc3BJSklVek5tRmh1cFBESFU9Iiwib3JlcWt2IjoxfQ%3D%3D&jic=8%7CEgRzdm9k",
'url_international_tv' : "https://www.primevideo.com/browse/ref=atv_ge_agi_c_7kl2bw_2_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmZmllbGQtZ2VucmUtYmluPWF2X2dlbnJlX2ludGVybmF0aW9uYWwmaW5kZXg9ZXUtYW1hem9uLXZpZGVvLWV1cm8mYWR1bHQtcHJvZHVjdD0wJmJxPShub3QgYXZfc2Vjb25kYXJ5X2dlbnJlOidhdl9zdWJnZW5yZV9pbnRlcm5hdGlvbmFsX2luZGlhJykmc2VhcmNoLWFsaWFzPWluc3RhbnQtdmlkZW8mcHZfb2ZmZXJzPUNIOkNIOnN2b2Q6cHJpbWU6dm9kOi0xNjg2NzQwNDAwOjE2ODY3NDA0MDAtJnFzLWF2X3JlcXVlc3RfdHlwZT00JnFzLWlzLXByaW1lLWN1c3RvbWVyPTIiLCJydCI6IjdrbDJiV3NtciIsInR4dCI6IlByaW1lIFRWIHNob3dzIiwib2Zmc2V0IjowLCJucHNpIjowLCJvcmVxIjoiOGRhNGIxMzYtZDViNy00ZDMxLWI4MDItZjFjZTY4NTgxZmIyOjE2ODY3NDA0NDkwMDAiLCJzdHJpZCI6IjE6MTE2T1JLRTNKVjRFSFYjI01aUVdHWkxVTVZTRUdZTFNONTJYR1pMTSIsIm9yZXFrIjoiMTJ5OHhUelFqalBwZExhYzVvdU5PVU9jKzFzcElKSVV6Tm1GaHVwUERIVT0iLCJvcmVxa3YiOjF9&jic=8%7CEgRzdm9k",
'url_music_movies' : "https://www.primevideo.com/browse/ref=atv_ge_agm_c_vqhlwi_1_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmZpZWxkLWdlbnJlLWJpbj1hdl9nZW5yZV9tdXNpY192aWRlb3NfYW5kX2NvbmNlcnRzJmluZGV4PWV1LWFtYXpvbi12aWRlby1ldXJvJmFkdWx0LXByb2R1Y3Q9MCZicT0obm90IGF2X3NlY29uZGFyeV9nZW5yZTonYXZfc3ViZ2VucmVfaW50ZXJuYXRpb25hbF9pbmRpYScpJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnB2X29mZmVycz1DSDpDSDpzdm9kOnByaW1lOnZvZDotMTY4Njc0MDQwMDoxNjg2NzQwNDAwLSZxcy1hdl9yZXF1ZXN0X3R5cGU9NCZxcy1pcy1wcmltZS1jdXN0b21lcj0yIiwicnQiOiJ2UUhMd2lzbXIiLCJ0eHQiOiJQcmltZSBtb3ZpZXMiLCJvZmZzZXQiOjAsIm5wc2kiOjAsIm9yZXEiOiI5NjFmMTRmYS02OWQ3LTQ0NWEtYjZkZi1hZDc4ZmZlMWY0YjI6MTY4Njc0MDU0MDAwMCIsInN0cmlkIjoiMToxUE1HUjQyMUgzTksxIyNNWlFXR1pMVU1WU0VHWUxTTjUyWEdaTE0iLCJvcmVxayI6IjEyeTh4VHpRampQcGRMYWM1b3VOT1VPYysxc3BJSklVek5tRmh1cFBESFU9Iiwib3JlcWt2IjoxfQ%3D%3D&jic=8%7CEgRzdm9k",
'url_music_tv' : "https://www.primevideo.com/browse/ref=atv_ge_agm_c_7kl2bw_2_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmZmllbGQtZ2VucmUtYmluPWF2X2dlbnJlX211c2ljX3ZpZGVvc19hbmRfY29uY2VydHMmaW5kZXg9ZXUtYW1hem9uLXZpZGVvLWV1cm8mYWR1bHQtcHJvZHVjdD0wJmJxPShub3QgYXZfc2Vjb25kYXJ5X2dlbnJlOidhdl9zdWJnZW5yZV9pbnRlcm5hdGlvbmFsX2luZGlhJykmc2VhcmNoLWFsaWFzPWluc3RhbnQtdmlkZW8mcHZfb2ZmZXJzPUNIOkNIOnN2b2Q6cHJpbWU6dm9kOi0xNjg2NzQwNDAwOjE2ODY3NDA0MDAtJnFzLWF2X3JlcXVlc3RfdHlwZT00JnFzLWlzLXByaW1lLWN1c3RvbWVyPTIiLCJydCI6IjdrbDJiV3NtciIsInR4dCI6IlByaW1lIFRWIHNob3dzIiwib2Zmc2V0IjowLCJucHNpIjowLCJvcmVxIjoiOTYxZjE0ZmEtNjlkNy00NDVhLWI2ZGYtYWQ3OGZmZTFmNGIyOjE2ODY3NDA1NDAwMDAiLCJzdHJpZCI6IjE6MTE2T1JLRTNKVjRFSFYjI01aUVdHWkxVTVZTRUdZTFNONTJYR1pMTSIsIm9yZXFrIjoiMTJ5OHhUelFqalBwZExhYzVvdU5PVU9jKzFzcElKSVV6Tm1GaHVwUERIVT0iLCJvcmVxa3YiOjF9&jic=8%7CEgRzdm9k",
'url_mystery_movies' : "https://www.primevideo.com/browse/ref=atv_ge_ags_c_vqhlwi_1_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmZpZWxkLWdlbnJlLWJpbj1hdl9nZW5yZV9zdXNwZW5zZSZpbmRleD1ldS1hbWF6b24tdmlkZW8tZXVybyZhZHVsdC1wcm9kdWN0PTAmYnE9KG5vdCBhdl9zZWNvbmRhcnlfZ2VucmU6J2F2X3N1YmdlbnJlX2ludGVybmF0aW9uYWxfaW5kaWEnKSZzZWFyY2gtYWxpYXM9aW5zdGFudC12aWRlbyZwdl9vZmZlcnM9Q0g6Q0g6c3ZvZDpwcmltZTp2b2Q6LTE2ODY3NDA0MDA6MTY4Njc0MDQwMC0mcXMtYXZfcmVxdWVzdF90eXBlPTQmcXMtaXMtcHJpbWUtY3VzdG9tZXI9MiIsInJ0IjoidlFITHdpc21yIiwidHh0IjoiUHJpbWUgbW92aWVzIiwib2Zmc2V0IjowLCJucHNpIjowLCJvcmVxIjoiZWIwNjc4ODAtMTgyZS00YmJkLWI2YmQtOGZhZTA0MmNkYjNjOjE2ODY3NDA1NzYwMDAiLCJzdHJpZCI6IjE6MVBNR1I0MjFIM05LMSMjTVpRV0daTFVNVlNFR1lMU041MlhHWkxNIiwib3JlcWsiOiIxMnk4eFR6UWpqUHBkTGFjNW91Tk9VT2MrMXNwSUpJVXpObUZodXBQREhVPSIsIm9yZXFrdiI6MX0%3D&jic=8%7CEgRzdm9k",
'url_mystery_tv' : "https://www.primevideo.com/browse/ref=atv_ge_ags_c_7kl2bw_2_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmZmllbGQtZ2VucmUtYmluPWF2X2dlbnJlX3N1c3BlbnNlJmluZGV4PWV1LWFtYXpvbi12aWRlby1ldXJvJmFkdWx0LXByb2R1Y3Q9MCZicT0obm90IGF2X3NlY29uZGFyeV9nZW5yZTonYXZfc3ViZ2VucmVfaW50ZXJuYXRpb25hbF9pbmRpYScpJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnB2X29mZmVycz1DSDpDSDpzdm9kOnByaW1lOnZvZDotMTY4Njc0MDQwMDoxNjg2NzQwNDAwLSZxcy1hdl9yZXF1ZXN0X3R5cGU9NCZxcy1pcy1wcmltZS1jdXN0b21lcj0yIiwicnQiOiI3a2wyYldzbXIiLCJ0eHQiOiJQcmltZSBUViBzaG93cyIsIm9mZnNldCI6MCwibnBzaSI6MCwib3JlcSI6ImViMDY3ODgwLTE4MmUtNGJiZC1iNmJkLThmYWUwNDJjZGIzYzoxNjg2NzQwNTc2MDAwIiwic3RyaWQiOiIxOjExNk9SS0UzSlY0RUhWIyNNWlFXR1pMVU1WU0VHWUxTTjUyWEdaTE0iLCJvcmVxayI6IjEyeTh4VHpRampQcGRMYWM1b3VOT1VPYysxc3BJSklVek5tRmh1cFBESFU9Iiwib3JlcWt2IjoxfQ%3D%3D&jic=8%7CEgRzdm9k",
'url_horror_movies' : "https://www.primevideo.com/browse/ref=atv_ge_agh_c_vqhlwi_1_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmZpZWxkLWdlbnJlLWJpbj1hdl9nZW5yZV9ob3Jyb3ImaW5kZXg9ZXUtYW1hem9uLXZpZGVvLWV1cm8mYWR1bHQtcHJvZHVjdD0wJmJxPShub3QgYXZfc2Vjb25kYXJ5X2dlbnJlOidhdl9zdWJnZW5yZV9pbnRlcm5hdGlvbmFsX2luZGlhJykmc2VhcmNoLWFsaWFzPWluc3RhbnQtdmlkZW8mcHZfb2ZmZXJzPUNIOkNIOnN2b2Q6cHJpbWU6dm9kOi0xNjg2NzM5ODAwOjE2ODY3Mzk4MDAtJnFzLWF2X3JlcXVlc3RfdHlwZT00JnFzLWlzLXByaW1lLWN1c3RvbWVyPTIiLCJydCI6InZRSEx3aXNtciIsInR4dCI6IlByaW1lIG1vdmllcyIsIm9mZnNldCI6MCwibnBzaSI6MCwib3JlcSI6IjBkYWM0ODRhLWRhNmEtNGUzZC1iNzkwLTg4NTBkZjBkNGQ2ODoxNjg2NzQwMTg3MDAwIiwic3RyaWQiOiIxOjFQTUdSNDIxSDNOSzEjI01aUVdHWkxVTVZTRUdZTFNONTJYR1pMTSIsIm9yZXFrIjoiMTJ5OHhUelFqalBwZExhYzVvdU5PVU9jKzFzcElKSVV6Tm1GaHVwUERIVT0iLCJvcmVxa3YiOjF9&jic=8%7CEgRzdm9k",
'url_horror_tv' : "https://www.primevideo.com/browse/ref=atv_ge_agh_c_7kl2bw_2_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmZmllbGQtZ2VucmUtYmluPWF2X2dlbnJlX2hvcnJvciZpbmRleD1ldS1hbWF6b24tdmlkZW8tZXVybyZhZHVsdC1wcm9kdWN0PTAmYnE9KG5vdCBhdl9zZWNvbmRhcnlfZ2VucmU6J2F2X3N1YmdlbnJlX2ludGVybmF0aW9uYWxfaW5kaWEnKSZzZWFyY2gtYWxpYXM9aW5zdGFudC12aWRlbyZwdl9vZmZlcnM9Q0g6Q0g6c3ZvZDpwcmltZTp2b2Q6LTE2ODY3Mzk4MDA6MTY4NjczOTgwMC0mcXMtYXZfcmVxdWVzdF90eXBlPTQmcXMtaXMtcHJpbWUtY3VzdG9tZXI9MiIsInJ0IjoiN2tsMmJXc21yIiwidHh0IjoiUHJpbWUgVFYgc2hvd3MiLCJvZmZzZXQiOjAsIm5wc2kiOjAsIm9yZXEiOiIwZGFjNDg0YS1kYTZhLTRlM2QtYjc5MC04ODUwZGYwZDRkNjg6MTY4Njc0MDE4NzAwMCIsInN0cmlkIjoiMToxMTZPUktFM0pWNEVIViMjTVpRV0daTFVNVlNFR1lMU041MlhHWkxNIiwib3JlcWsiOiIxMnk4eFR6UWpqUHBkTGFjNW91Tk9VT2MrMXNwSUpJVXpObUZodXBQREhVPSIsIm9yZXFrdiI6MX0%3D&jic=8%7CEgRzdm9k",
'url_romance_movies' : "https://www.primevideo.com/browse/ref=atv_ge_agr_c_vqhlwi_1_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmZpZWxkLWdlbnJlLWJpbj1hdl9nZW5yZV9yb21hbmNlJmluZGV4PWV1LWFtYXpvbi12aWRlby1ldXJvJmFkdWx0LXByb2R1Y3Q9MCZicT0obm90IGF2X3NlY29uZGFyeV9nZW5yZTonYXZfc3ViZ2VucmVfaW50ZXJuYXRpb25hbF9pbmRpYScpJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnB2X29mZmVycz1DSDpDSDpzdm9kOnByaW1lOnZvZDotMTY4NjczOTgwMDoxNjg2NzM5ODAwLSZxcy1hdl9yZXF1ZXN0X3R5cGU9NCZxcy1pcy1wcmltZS1jdXN0b21lcj0yIiwicnQiOiJ2UUhMd2lzbXIiLCJ0eHQiOiJQcmltZSBtb3ZpZXMiLCJvZmZzZXQiOjAsIm5wc2kiOjAsIm9yZXEiOiJhMzZkNDU0Ny0zYjI1LTQ0MGUtODUxNy1mMDJlNmM2MjViYjk6MTY4Njc0MDIzNTAwMCIsInN0cmlkIjoiMToxUE1HUjQyMUgzTksxIyNNWlFXR1pMVU1WU0VHWUxTTjUyWEdaTE0iLCJvcmVxayI6IjEyeTh4VHpRampQcGRMYWM1b3VOT1VPYysxc3BJSklVek5tRmh1cFBESFU9Iiwib3JlcWt2IjoxfQ%3D%3D&jic=8%7CEgRzdm9k",
'url_romance_tv' : "https://www.primevideo.com/browse/ref=atv_ge_agr_c_7kl2bw_2_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmZmllbGQtZ2VucmUtYmluPWF2X2dlbnJlX3JvbWFuY2UmaW5kZXg9ZXUtYW1hem9uLXZpZGVvLWV1cm8mYWR1bHQtcHJvZHVjdD0wJmJxPShub3QgYXZfc2Vjb25kYXJ5X2dlbnJlOidhdl9zdWJnZW5yZV9pbnRlcm5hdGlvbmFsX2luZGlhJykmc2VhcmNoLWFsaWFzPWluc3RhbnQtdmlkZW8mcHZfb2ZmZXJzPUNIOkNIOnN2b2Q6cHJpbWU6dm9kOi0xNjg2NzM5ODAwOjE2ODY3Mzk4MDAtJnFzLWF2X3JlcXVlc3RfdHlwZT00JnFzLWlzLXByaW1lLWN1c3RvbWVyPTIiLCJydCI6IjdrbDJiV3NtciIsInR4dCI6IlByaW1lIFRWIHNob3dzIiwib2Zmc2V0IjowLCJucHNpIjowLCJvcmVxIjoiYTM2ZDQ1NDctM2IyNS00NDBlLTg1MTctZjAyZTZjNjI1YmI5OjE2ODY3NDAyMzUwMDAiLCJzdHJpZCI6IjE6MTE2T1JLRTNKVjRFSFYjI01aUVdHWkxVTVZTRUdZTFNONTJYR1pMTSIsIm9yZXFrIjoiMTJ5OHhUelFqalBwZExhYzVvdU5PVU9jKzFzcElKSVV6Tm1GaHVwUERIVT0iLCJvcmVxa3YiOjF9&jic=8%7CEgRzdm9k",
'url_crime_movies' : "https://www.primevideo.com/browse/ref=atv_mv_hom_c_lvccqq_11_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmluZGV4PWV1LWFtYXpvbi12aWRlby1ldXJvJmFkdWx0LXByb2R1Y3Q9MCZicT0oYW5kIChhbmQgc29ydDonZmVhdHVyZWQtcmFuaycgKGFuZCBhdl9zZWNvbmRhcnlfZ2VucmU6J2F2X3N1YmdlbnJlX3N1c3BlbnNlX2NyaW1lJyAobm90IChvciAob3IgYXZfc2Vjb25kYXJ5X2dlbnJlOidhdl9zdWJnZW5yZV9pbnRlcm5hdGlvbmFsX2luZGlhJyBhdl9wcmltYXJ5X2dlbnJlOidhdl9nZW5yZV9raWRzJykgYXZfcHJpbWFyeV9nZW5yZTonYXZfZ2VucmVfYW5pbWUnKSkpKSAobm90IGF2X2tpZF9pbl90ZXJyaXRvcnk6J0NIJykpJnB2X29mZmVycz1DSDpDSDpzdm9kOnByaW1lOnZvZDotMTY4Njc0MDQwMDoxNjg2NzQwNDAwLSZzZWFyY2gtYWxpYXM9aW5zdGFudC12aWRlbyZxcy1hdl9yZXF1ZXN0X3R5cGU9NCZxcy1pcy1wcmltZS1jdXN0b21lcj0yIiwicnQiOiJMdmNjUXFzbXIiLCJ0eHQiOiJDcmltZSBtb3ZpZXMiLCJvZmZzZXQiOjAsIm5wc2kiOjAsIm9yZXEiOiJiYjI0YzA5OC04ODM4LTRiMGEtYTdmMS1iNTcwZWU4YWFjNmU6MTY4Njc0MDY0MzAwMCIsInN0cmlkIjoiMToxM0VVRzRRQlBMODRUViMjTVpRV0daTFVNVlNFR1lMU041MlhHWkxNIiwib3JlcWsiOiIxMnk4eFR6UWpqUHBkTGFjNW91Tk9VT2MrMXNwSUpJVXpObUZodXBQREhVPSIsIm9yZXFrdiI6MX0%3D&jic=8%7CEgRzdm9k",
'url_crime_tv' : "https://www.primevideo.com/browse/ref=atv_tv_hom_c_yzgs7u_8_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmaW5kZXg9ZXUtYW1hem9uLXZpZGVvLWV1cm8mYWR1bHQtcHJvZHVjdD0wJmJxPShhbmQgKGFuZCBzb3J0OidmZWF0dXJlZC1yYW5rJyAoYW5kIGF2X3NlY29uZGFyeV9nZW5yZTonYXZfc3ViZ2VucmVfc3VzcGVuc2VfY3JpbWUnIChub3QgKG9yIChvciBhdl9zZWNvbmRhcnlfZ2VucmU6J2F2X3N1YmdlbnJlX2ludGVybmF0aW9uYWxfaW5kaWEnIGF2X3ByaW1hcnlfZ2VucmU6J2F2X2dlbnJlX2tpZHMnKSBhdl9wcmltYXJ5X2dlbnJlOidhdl9nZW5yZV9hbmltZScpKSkpIChub3QgYXZfa2lkX2luX3RlcnJpdG9yeTonQ0gnKSkmcHZfb2ZmZXJzPUNIOkNIOnN2b2Q6cHJpbWU6dm9kOi0xNjg2NzQwNDAwOjE2ODY3NDA0MDAtJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnFzLWF2X3JlcXVlc3RfdHlwZT00JnFzLWlzLXByaW1lLWN1c3RvbWVyPTIiLCJydCI6IllaR1M3dXNtciIsInR4dCI6IkNyaW1lIFRWIiwib2Zmc2V0IjowLCJucHNpIjowLCJvcmVxIjoiN2YwMzE1OGQtZWYyOC00NmVmLTkxMDQtMGVhNDY5MGI5NDA3OjE2ODY3NDA2ODYwMDAiLCJzdHJpZCI6IjE6MTJKSllXM0dQQkEyVlojI01aUVdHWkxVTVZTRUdZTFNONTJYR1pMTSIsIm9yZXFrIjoiMTJ5OHhUelFqalBwZExhYzVvdU5PVU9jKzFzcElKSVV6Tm1GaHVwUERIVT0iLCJvcmVxa3YiOjF9&jic=8%7CEgRzdm9k",
'url_kids_movies' : "https://www.primevideo.com/browse/ref=atv_mv_hom_c_iyd3uw_12_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmluZGV4PWV1LWFtYXpvbi12aWRlby1ldXJvJmFkdWx0LXByb2R1Y3Q9MCZicT0oYW5kIHNvcnQ6J2ZlYXR1cmVkLXJhbmsnIChhbmQgKGFuZCAob3IgYXZfcHJpbWFyeV9nZW5yZTonYXZfZ2VucmVfa2lkcycpIChub3QgYXZfc2Vjb25kYXJ5X2dlbnJlOidhdl9zdWJnZW5yZV9pbnRlcm5hdGlvbmFsX2luZGlhJykpIChub3QgKG9yIHJlZ3VsYXRvcnlfcmF0aW5nOicxOCAnIHJlZ3VsYXRvcnlfcmF0aW5nOiducicpKSkpJnB2X29mZmVycz1DSDpDSDpzdm9kOnByaW1lOnZvZDotMTY4Njc0MDQwMDoxNjg2NzQwNDAwLSZzZWFyY2gtYWxpYXM9aW5zdGFudC12aWRlbyZxcy1hdl9yZXF1ZXN0X3R5cGU9NCZxcy1pcy1wcmltZS1jdXN0b21lcj0yIiwicnQiOiJJeWQzdXdzbXIiLCJ0eHQiOiJLaWRzIGFuZCBmYW1pbHkgbW92aWVzIiwib2Zmc2V0IjowLCJucHNpIjowLCJvcmVxIjoiODRhMmUyODItZWFlMi00ZTVjLWI3YjEtNjcyYjVjYmEwMTVkOjE2ODY3NDA3MjgwMDAiLCJzdHJpZCI6IjE6MTJMNzZNT0VDR1ZENEcjI01aUVdHWkxVTVZTRUdZTFNONTJYR1pMTSIsIm9yZXFrIjoiMTJ5OHhUelFqalBwZExhYzVvdU5PVU9jKzFzcElKSVV6Tm1GaHVwUERIVT0iLCJvcmVxa3YiOjF9&jic=8%7CEgRzdm9k",
'url_kids_tv' : "https://www.primevideo.com/browse/ref=atv_tv_hom_c_kwy9kj_13_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmaW5kZXg9ZXUtYW1hem9uLXZpZGVvLWV1cm8mYWR1bHQtcHJvZHVjdD0wJmJxPShhbmQgc29ydDonZmVhdHVyZWQtcmFuaycgKGFuZCAoYW5kIChvciBhdl9wcmltYXJ5X2dlbnJlOidhdl9nZW5yZV9raWRzJykgKG5vdCBhdl9zZWNvbmRhcnlfZ2VucmU6J2F2X3N1YmdlbnJlX2ludGVybmF0aW9uYWxfaW5kaWEnKSkgKG5vdCAob3IgcmVndWxhdG9yeV9yYXRpbmc6JzE4ICcgcmVndWxhdG9yeV9yYXRpbmc6J25yJykpKSkmcHZfb2ZmZXJzPUNIOkNIOnN2b2Q6cHJpbWU6dm9kOi0xNjg2NzQwNDAwOjE2ODY3NDA0MDAtJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnFzLWF2X3JlcXVlc3RfdHlwZT00JnFzLWlzLXByaW1lLWN1c3RvbWVyPTIiLCJydCI6Ikt3eTlrSnNtciIsInR4dCI6IktpZHMgYW5kIGZhbWlseSBUViIsIm9mZnNldCI6MCwibnBzaSI6MCwib3JlcSI6IjdmMDMxNThkLWVmMjgtNDZlZi05MTA0LTBlYTQ2OTBiOTQwNzoxNjg2NzQwNjg2MDAwIiwic3RyaWQiOiIxOjEyRjdJUlFDMVNCU1hNIyNNWlFXR1pMVU1WU0VHWUxTTjUyWEdaTE0iLCJvcmVxayI6IjEyeTh4VHpRampQcGRMYWM1b3VOT1VPYysxc3BJSklVek5tRmh1cFBESFU9Iiwib3JlcWt2IjoxfQ%3D%3D&jic=8%7CEgRzdm9k" 
}

urls_main_top = {
#'top_movies': 'https://www.primevideo.com/browse/ref=atv_mv_hom_c_zbfcqv_8_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmluZGV4PWV1LWFtYXpvbi12aWRlby1ldXJvJmFkdWx0LXByb2R1Y3Q9MCZicT0oYW5kIHNvcnQ6J2ZlYXR1cmVkLXJhbmsnIChub3QgKG9yIChvciBhdl9zZWNvbmRhcnlfZ2VucmU6J2F2X3N1YmdlbnJlX2ludGVybmF0aW9uYWxfaW5kaWEnIGF2X3ByaW1hcnlfZ2VucmU6J2F2X2dlbnJlX2tpZHMnKSBhdl9wcmltYXJ5X2dlbnJlOidhdl9nZW5yZV9hbmltZScpKSkmcHZfb2ZmZXJzPUNIOkNIOnN2b2Q6cHJpbWU6dm9kOi0xNjg2NzkzODAwOjE2ODY3OTM4MDAtJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnFzLWF2X3JlcXVlc3RfdHlwZT00JnFzLWlzLXByaW1lLWN1c3RvbWVyPTIiLCJydCI6InpiZmNxdnNtciIsInR4dCI6IlRvcCBtb3ZpZXMiLCJvZmZzZXQiOjAsIm5wc2kiOjAsIm9yZXEiOiIwYzBjOTJhNi04NjdlLTQzNmYtOGM4MC1mMTBlMWM0YzE4OGM6MTY4Njc5NDM3NTAwMCIsInN0cmlkIjoiMToxMzVVTUQ4UzdFME82MyMjTVpRV0daTFVNVlNFR1lMU041MlhHWkxNIiwib3JlcWsiOiIxMnk4eFR6UWpqUHBkTGFjNW91Tk9VT2MrMXNwSUpJVXpObUZodXBQREhVPSIsIm9yZXFrdiI6MX0%3D&jic=8%7CEgRzdm9k',
'top_tv': 'https://www.primevideo.com/browse/ref=atv_tv_hom_c_laptvn_4_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmaW5kZXg9ZXUtYW1hem9uLXZpZGVvLWV1cm8mYWR1bHQtcHJvZHVjdD0wJmJxPShhbmQgc29ydDonZmVhdHVyZWQtcmFuaycgKG5vdCAob3IgKG9yIGF2X3NlY29uZGFyeV9nZW5yZTonYXZfc3ViZ2VucmVfaW50ZXJuYXRpb25hbF9pbmRpYScgYXZfcHJpbWFyeV9nZW5yZTonYXZfZ2VucmVfa2lkcycpIGF2X3ByaW1hcnlfZ2VucmU6J2F2X2dlbnJlX2FuaW1lJykpKSZwdl9vZmZlcnM9Q0g6Q0g6c3ZvZDpwcmltZTp2b2Q6LTE2ODY3OTM4MDA6MTY4Njc5MzgwMC0mc2VhcmNoLWFsaWFzPWluc3RhbnQtdmlkZW8mcXMtYXZfcmVxdWVzdF90eXBlPTQmcXMtaXMtcHJpbWUtY3VzdG9tZXI9MiIsInJ0IjoibEFQdFZuc21yIiwidHh0IjoiVG9wIFRWIiwib2Zmc2V0IjowLCJucHNpIjowLCJvcmVxIjoiMmU4Y2VjNjItZjE4Zi00M2ZmLWI0N2MtOWE1ODYzMjliMzg1OjE2ODY3OTQzOTIwMDAiLCJzdHJpZCI6IjE6MUlBWUcwQlVUMUVWTyMjTVpRV0daTFVNVlNFR1lMU041MlhHWkxNIiwib3JlcWsiOiIxMnk4eFR6UWpqUHBkTGFjNW91Tk9VT2MrMXNwSUpJVXpObUZodXBQREhVPSIsIm9yZXFrdiI6MX0%3D&jic=8%7CEgRzdm9k',
#'recentlyadded_movies': 'https://www.primevideo.com/browse/ref=atv_mv_hom_c_y3hzaq_13_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmluZGV4PWV1LWFtYXpvbi12aWRlby1ldXJvJmFkdWx0LXByb2R1Y3Q9MCZicT0oYW5kIChub3QgYXZfc2Vjb25kYXJ5X2dlbnJlOidhdl9zdWJnZW5yZV9pbnRlcm5hdGlvbmFsX2luZGlhJykgKG5vdCBhdl9wcmltYXJ5X2dlbnJlOidhdl9nZW5yZV9hbmltZScpICkmcHZfb2ZmZXJzPUNIOkNIOnN2b2Q6cHJpbWU6dm9kOjE2ODQyMDI0MDAtOjE2ODY3OTQ0MDAtJnNlYXJjaC1hbGlhcz1pbnN0YW50LXZpZGVvJnFzLWF2X3JlcXVlc3RfdHlwZT00JnFzLWlzLXByaW1lLWN1c3RvbWVyPTIiLCJydCI6InkzaFpBUXNtciIsInR4dCI6IlJlY2VudGx5IGFkZGVkIG1vdmllcyIsIm9mZnNldCI6MCwibnBzaSI6MCwib3JlcSI6ImNjMGIxMjBiLWRjMmYtNGI1MS05MjgwLTA4OTZkODU3MjQwMjoxNjg2Nzk0NDQ3MDAwIiwic3RyaWQiOiIxOjEyM0w5MExFSkZITTVJIyNNWlFXR1pMVU1WU0VHWUxTTjUyWEdaTE0iLCJvcmVxayI6IjEyeTh4VHpRampQcGRMYWM1b3VOT1VPYysxc3BJSklVek5tRmh1cFBESFU9Iiwib3JlcWt2IjoxfQ%3D%3D&jic=8%7CEgRzdm9k',
#'recentlyadded_tv': 'https://www.primevideo.com/browse/ref=atv_tv_hom_c_awsvbq_13_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPVRWIFNob3cmaW5kZXg9ZXUtYW1hem9uLXZpZGVvLWV1cm8mYWR1bHQtcHJvZHVjdD0wJmJxPShhbmQgKG5vdCBhdl9zZWNvbmRhcnlfZ2VucmU6J2F2X3N1YmdlbnJlX2ludGVybmF0aW9uYWxfaW5kaWEnKSAobm90IGF2X3ByaW1hcnlfZ2VucmU6J2F2X2dlbnJlX2FuaW1lJykgKSZwdl9vZmZlcnM9Q0g6Q0g6c3ZvZDpwcmltZTp2b2Q6MTY4NDIwMjQwMC06MTY4Njc5NDQwMC0mc2VhcmNoLWFsaWFzPWluc3RhbnQtdmlkZW8mcXMtYXZfcmVxdWVzdF90eXBlPTQmcXMtaXMtcHJpbWUtY3VzdG9tZXI9MiIsInJ0IjoiQXdTVmJRc21yIiwidHh0IjoiUmVjZW50bHkgYWRkZWQgVFYiLCJvZmZzZXQiOjAsIm5wc2kiOjAsIm9yZXEiOiI3YzI3NWQ3Zi1kYzRmLTQwMDUtOTQ2OS00YjU4MGI0NDQyZmU6MTY4Njc5NDUxMzAwMCIsInN0cmlkIjoiMToxMktUTTdSVkVROEk2VCMjTVpRV0daTFVNVlNFR1lMU041MlhHWkxNIiwib3JlcWsiOiIxMnk4eFR6UWpqUHBkTGFjNW91Tk9VT2MrMXNwSUpJVXpObUZodXBQREhVPSIsIm9yZXFrdiI6MX0%3D&jic=8%7CEgRzdm9k',
}

content_names = [] # store to avoid duplicate movie/tv titles


async def get_url_of_vidchunk(url):
    browser = await launch(userDataDir=profile_path, headless=False, executablePath= exec_path)
    chunk_url = [""]

    def interception_fun(response):
        if "_video_" in response.url and ".mp4" in response.url and "trailer" not in response.url and "s3-dub-" in response.url :
            # Response logic goes here
            #print("URL:", response.url, "\n\n")
            chunk_url[0] = response.url
            #print("Method:", response.request.method)
            #print("Response headers:", response.headers)
            #print("Request Headers:", response.request.headers)
            #print("Response status:", response.status)
        return
    
    try:
        page = await browser.newPage()
        await page.goto(url)
        page.on('response', interception_fun)
        
        # Trigger video playback using JavaScript
        await page.evaluate('''() => {
            const video = document.querySelector('video');
            if (video) {
                video.play();
            }
        }''')
        
        start_time = time.time()
        elapsed_time = 0 
        while True:
            if chunk_url[0] != "":
                break
            else:
                await page.waitFor(1000) # load page for 1 more sec
            
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > 10: # max timeout
                break
    except Exception as e:
        print(url,"\n",e)
    
    await browser.close()
    return chunk_url[0]


async def scroll_to_bottom(page):
    all_link_data = []
    shows_count = 0
    MAX_SHOWS = 130 ### CHANGE IT !!!!
    shows_url = []

    while True:
        link_data = await page.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('[href]'));
            const data = links.map(link => {
                return {
                    href: link.href,
                    text: link.textContent.trim()
                };
            });
            return data;
        }''')
        
        previous_height = await page.evaluate('document.body.scrollHeight')
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await asyncio.sleep(2)  # Adjust the sleep time as needed
        current_height = await page.evaluate('document.body.scrollHeight')

        for data in link_data:
            if "https://www.primevideo.com/detail/" in data['href']:
                if data['href'] not in shows_url: # to avoid duplicates
                    print(data['href'])
                    shows_count += 1
                    all_link_data.append(data)
                    shows_url.append(data['href'])


        #all_link_data.extend(link_data)
  
        if current_height == previous_height or shows_count >= MAX_SHOWS:
            return all_link_data[:MAX_SHOWS+1]
    

async def get_link_addresses(url):
    browser = await launch(userDataDir=profile_path, headless=False, executablePath= exec_path)
    page = await browser.newPage()
    await page.goto(url)
    
    all_link_data = await scroll_to_bottom(page)

    await browser.close()
    return all_link_data


async def get_all_links(url):
    all_link_data = await get_link_addresses(url)
    all_link_data_new = [] # removes duplicates, add videopage url
    global content_names
    
    for data in all_link_data:
        name = data['text']
        url_title = data['href']
        if "https://www.primevideo.com/detail/" in data['href']:
            if name in content_names:
                continue

            vid_id = url_title.split("/detail/")[1].split("/")[0]
            url_videopage = f"https://www.primevideo.com/detail/{vid_id}/ref=atv_hm_fcv_prime_sd_mv_resume_t1ACAAAAAA0wh0?autoplay=1&t=0"
            
            content_names.append(name)
            data_new = {'name':name, 'url_titlepage':url_title, 'url_videopage': url_videopage}
            all_link_data_new.append(data_new)
            
    return all_link_data_new


if __name__ == '__main__':
    count_dict = {}
    keys = ['name', 'url_titlepage', 'url_videopage', 'url_chunk','content']
    
    # Check if the file exists
    if not os.path.exists("already_collected.txt"):
        # Create the file if it doesn't exist
        with open("already_collected.txt", 'w') as already_file:
            already_file.write("already_collected.txt\n")
    
    already_collected = open("already_collected.txt").readlines()

    start_time = time.time()
    elapsed_time = 0
    #y = 0 ####

    for content, main_url in urls_main_top.items():
        print("*"*25,content,"*"*25,"\n\n")
        all_link_data_new = asyncio.get_event_loop().run_until_complete(get_all_links(main_url))
        count_dict[content] = len(all_link_data_new)
        print(f"{content} = {len(all_link_data_new)}")

        count = 0    
        print("\n\n")

        for data in all_link_data_new:
            ####
            if count==125:
                break
            
            count += 1
            
            name = data['name']
            print(f"**** {count} out of {len(all_link_data_new)} --- {content} ~~~ elapsed: {elapsed_time} min ****")

            current_time = time.time()
            elapsed_time = int((current_time - start_time)//60)

            if name+"\n" in already_collected:
                print(f"{name} is already collected!\n\n")
                continue
            
            url_titlepage = data['url_titlepage']
            url_videopage = data['url_videopage']
            
            url_chunk = asyncio.get_event_loop().run_until_complete(get_url_of_vidchunk(url_videopage))
            if url_chunk == "":
                print(f"failed to get url_chunk of {name}\n")
            
            print("Name:", name)
            print("Titlepage:", url_titlepage)
            print("Videopage:", url_videopage)
            print("Chunk:", url_chunk)
            data['url_chunk'] = url_chunk
            data['content'] = "prime_" + content
            print("\n\n")
            with open("url_prime_" + content + ".csv", 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                if csvfile.tell() == 0: # if csv file is empty
                    writer.writeheader()  # Write the header row
                writer.writerow(data)  # Write the data rows
            
            already_file = open("already_collected.txt", 'a')
            already_file.write(name+"\n")
            
        #### 
        #if y ==2:
            #break
        #y += 1
            
            

    total_count = 0
    for content, count in count_dict.items():
        print(content, count)
        total_count += count


    print("TOTAL=", total_count)







